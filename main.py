import docker
import flask
import json
import time
import numpy as np
import pandas as pd
import os
import shutil
import zipfile
import tarfile
from flask_cors import CORS
from flask import request
from Processor import DataProcessor
from WebStatus import Status
from DockerProcessor import DockerApplication
from Utils import uncompress_file
import pymysql
from Config import *

conn=pymysql.connect(host=host,port=port,user=username,password=password,database=database)
cursor=conn.cursor()
col_name=["id","container_id","container_name","command","create_time","status","log","user_id","image_id"]
app=flask.Flask("__name__")
CORS(app)

@app.route("/nuistp/fill",methods=["POST"])
def file_fill():
    res=dict()
    info=request.json
    fill_type=info["fillType"] #“mean”|“max”|“min”|“zero”
    file_pth=info["filePth"]
    data_processor = DataProcessor(file_pth)
    if fill_type in ["mean","max","min","zero"] and data_processor.has_none:
        df=data_processor.fill(fill_type)
        df.to_csv(file_pth)
        res["status"]=Status.OK.value
    else:
        res["status"]=Status.INTERNALERROR.value
    return res

@app.route("/nuistp/fileInfo",methods=["POST"])
def test():
    begin=time.time()
    res=dict()
    info=request.json
    file_path=info["filePth"]
    data_processor=DataProcessor(file_path)
    res["basic"] =[{'name':'特征数量','content':str(data_processor.feature_nums)},
                   {'name':'类别数量','content':str(data_processor.label_nums)},
                   {'name':'是否有空','content':'含有' if data_processor.has_none else '不包含'},
                   {'name':'填充方式','content':'暂无填充'}]
    if not data_processor.has_none:
        res["avg"]=data_processor.f_mean.tolist()
        res["std"]=data_processor.f_std.tolist()
        res["min"]=data_processor.f_min.tolist()
        res["max"]=data_processor.f_max.tolist()
        res["featureNums"]=data_processor.feature_nums
        res["status"]=Status.OK.value
    else:
        res["status"]=Status.FILEHASNONE.value
    end=time.time()
    print((end-begin)*1000)
    return res

@app.route("/nuistp/train",methods=["POST"])
def dockerService():
    res=dict()
    args=request.json
    # 默认算法(系统需cp数据集至共享目录/自定义算法解压压缩包(tar|zip|gz|7z)即可)
    if args["type"]==0:
        # 将训练集拷贝至共享目录
        shutil.copy(args["trainSetSavePth"],args["newTrainSetSavePth"])
    else:
        uncompress_file(args["algorithmSavePth"],"/home/code")
    params = {
        "command": args["command"],
        "volumes": ["/home/code:/home/code"],
        "working_dir": "/home/code",
        "detach": True,
        "remove": False,
    }
    myDockerApp = DockerApplication(image_name=args["mirror"])
    myDockerApp.run_container(params)
    res["containerId"] = myDockerApp.container.short_id
    return res

@app.route("/nuistp/getFileHead",methods=["POST"])
def getFileHead():
    res=dict()
    args=request.json
    df=pd.read_csv(args["save_pth"])
    res["status"]=Status.OK.value
    res["col"]=df.columns.tolist()
    res["types"]=df.iloc[:,-1].unique().tolist()
    return res

@app.route("/nuistp/getOneFeatureDistribution",methods=["POST"])
def getOneFeatureDistribution():
    args=request.json
    res=dict()
    df=pd.read_csv(args["save_pth"])
    label=df.columns[-1]
    group=df.groupby(label)
    type_distribution=group.get_group(args["type_selected"])[args["feature_selected"]].tolist()
    res["feature_distribution"]={
        args["type_selected"]:{
            "data":[[index,item] for (index,item) in enumerate(type_distribution)]
        },
    }
    return res

@app.route("/nuistp/getOccupytion",methods=["POST"])
def getOccupytion():
    args=request.json
    res=dict()
    df=pd.read_csv(args["save_pth"])
    labels=df.columns[-1]
    group=df.groupby(labels)
    group_dict=group.groups
    occuption=[]
    for key in group_dict.keys():
        occuption.append({"name":key,"value":len(group_dict[key])})
    res["occuption"]=occuption
    return res

@app.route("/nuistp/pca",methods=["POST"])
def pca():
    args=request.json
    res=dict()
    processor=DataProcessor(args["save_pth"])
    if processor.has_none:
        res["status"]=Status.INTERNALERROR.value
    else:
        pca_data,_=processor.pca(3)
        res["pcaData"]=pca_data.tolist()
        res["status"] = Status.OK.value
    return res

@app.route("/nuistp/getContainerStatus",methods=["POST"])
def getContainerStatus():
    res=dict()
    client=docker.DockerClient(docker_conn)
    sql="select * from container"
    cursor = conn.cursor()
    cursor.execute(sql)
    result_set=cursor.fetchall()
    container_list=[]
    for rs in result_set:
        rs=list(rs)
        rs_dict=dict()
        # 获取容器状态
        status=client.containers.get(rs[1]).status
        if status!=rs[1]:
            rs[5]=status
            update_sql=f"update container set status={status} where container_id={rs[0]}"
            cursor.execute(update_sql)
        for index, item in enumerate(rs):
            rs_dict[col_name[index]] = item
        container_list.append(rs_dict)
    res["container_status"]=container_list
    res["status"]=Status.OK.value
    return res

# 构建docker镜像
@app.route("/nuistp/buildImage",methods=["POST"])
def buildImage():
    res=dict()
    form=request.form
    file=request.files.get("file")
    tag=f"{form.get('imageName')}:{form.get('imageTag')}"
    file.save(dockerfile_save_pth)
    client = docker.DockerClient(docker_conn)
    image,_=client.images.build(path="/home/wsy", tag=tag)
    print(image.short_id[7:])
    res["status"]=Status.OK.value
    return res
    # file=request.files.get("file")
    # args=request

    # client=docker.DockerClient(docker_conn)
    # client.images.build(path="",tag="")




# @app.route("/nuist/dataShow",methods=["POST"])
# def dataShow():
#     args=request.json
#     res=dict()
#     show_type=args["show_type"]
#
#     if show_type in ["classScatter","sampleOccupytion","pca"]:
#         data_processor=DataProcessor(args["save_pth"])
#         if data_processor.has_none:
#             res["status"]=Status.INTERNALERROR.value
#         else:
#             match show_type:
#                 case "classScatter":
#                     break
#
#
#     else:
#         res["status"]=Status.INTERNALERROR.value
#
#     return res



if __name__=='__main__':
    app.run(host="0.0.0.0",port=8080,debug=False)




