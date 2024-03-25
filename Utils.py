import tarfile
import zipfile
import os


def uncompress_file(file_path,new_path):
    file_type=os.path.splitext(file_path)[-1]
    if file_type=='.zip':
       f=zipfile.ZipFile(file_path,"r")
       f.extractall(path=new_path)
    else:
        f=tarfile.TarFile(file_path,"r")
        f.extractall(path=new_path)

