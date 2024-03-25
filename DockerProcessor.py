import time
import docker

docker_url = "http://123.60.19.158:2375"
default_image = "python:3.8"

class DockerApplication:
    def __init__(self, url=docker_url, image_name=default_image, image_path=None):
        self.client = docker.DockerClient(base_url=url)
        self.image_name = image_name
        if image_path is not None:
            try:
                with open(image_path, 'rb') as f:
                    img_obj = self.client.images.load(f)[0]
                self.image = self.client.images.get(img_obj.short_id)
                self.image.tag(self.image_name)
            except Exception as e:
                print(e)
        else:
            self.image = self.client.images.get(self.image_name)

    def run_container(self, params):
        """
        command: 容器启动代码
        volumes: 挂载路径
        working_dir: 工作路径
        detach: 是否带日志输出
        """
        self.container = self.client.containers.run(self.image, **params)
        print(self.container.status)

    def get_container_status(self):
        self.container.reload()
        return self.container.status

    def close(self):
        with open("./log.txt", "w") as f:
            f.write(self.container.logs().decode("utf-8"))
        self.container.remove()
        self.client.close()

#
# if __name__ == "__main__":
#     params = {
#         "command": "python3 main.py",
#         "volumes": ["/home/code:/home/code"],
#         "working_dir": "/home/code",
#         "detach": True,
#         "remove": False,
#     }
#     myDockerApp = DockerApplication()
#     myDockerApp.run_container(params)
#     while True:
#         status = myDockerApp.get_container_status()
#         if status == "exited":
#             myDockerApp.close()
#             break
#         time.sleep(1)





