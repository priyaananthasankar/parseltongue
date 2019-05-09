import docker
import requests
client = docker.from_env()
buildargs = {"CODE_PATH" : "./",
             "BASE_IMAGE": "prananth/test:dev"}
print("Building base image...")
base_img,build_iter= client.images.build(path='../',tag='prananth/test:dev')

print("Building target image...")
final_img,build_iter=client.images.build(path='../',tag='prananth/final_image:dev',dockerfile='Dockerfile.test',buildargs=buildargs)
ports = {'80':8080}
print("Starting target container...")
pyfunc_container = client.containers.run(final_img.tags[0],detach=True,ports=ports)
print("Running container: " , pyfunc_container.short_id)

#r = requests.get('http://localhost:8080/api/HttpTrigger')
#if r.status_code == 200:
 #   print(r.json())
