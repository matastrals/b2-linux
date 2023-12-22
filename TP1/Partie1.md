# I. Init

_**Avant tout, je n'ai pas mis dans le rendu les commandes "cd". Tu vois en général dans quel dossier je suis donc je juge cela inutile.**_

🌞 **Ajouter votre utilisateur au groupe `docker`**

```
[matastral@docker ~]$ sudo groupadd docker
[sudo] password for matastral:
groupadd: group 'docker' already exists
[matastral@docker ~]$ sudo usermod -aG docker matastral
[matastral@docker ~]$ exit
logout
[matastral@docker ~]$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

🌞 **Lancer un conteneur NGINX**

```
[matastral@docker ~]$ docker run -d -p 9999:80 nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
af107e978371: Pull complete
336ba1f05c3e: Pull complete
8c37d2ff6efa: Pull complete
51d6357098de: Pull complete
782f1ecce57d: Pull complete
5e99d351b073: Pull complete
7b73345df136: Pull complete
Digest: sha256:bd30b8d47b230de52431cc71c5cce149b8d5d4c87c204902acf2504435d4b4c9
Status: Downloaded newer image for nginx:latest
49ce4c2f9c05b37ac12afe026741baeca9f138cd2d43ec8fc9a51e3cb26377bb
```

🌞 **Visitons**

```
[matastral@docker ~]$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS
           NAMES
49ce4c2f9c05   nginx     "/docker-entrypoint.…"   About a minute ago   Up About a minute   0.0.0.0:9999->80/tcp, :::9999->80/tcp   peaceful_sanderson
```

```
[matastral@docker ~]$ docker logs --tail 10 49ce4c2f9c05
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2023/12/21 14:28:03 [notice] 1#1: using the "epoll" event method
2023/12/21 14:28:03 [notice] 1#1: nginx/1.25.3
2023/12/21 14:28:03 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
2023/12/21 14:28:03 [notice] 1#1: OS: Linux 5.14.0-284.30.1.el9_2.x86_64
2023/12/21 14:28:03 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1073741816:1073741816
2023/12/21 14:28:03 [notice] 1#1: start worker processes
2023/12/21 14:28:03 [notice] 1#1: start worker process 28
```


```
[matastral@docker ~]$ docker inspect 49ce4c2f9c05
[
    {
        "Id": "49ce4c2f9c05b37ac12afe026741baeca9f138cd2d43ec8fc9a51e3cb26377bb",
        "Created": "2023-12-21T14:28:03.050217015Z",
        "Path": "/docker-entrypoint.sh",
        "Args": [
            "nginx",
            "-g",
            "daemon off;"
        ],
[...](bcp d'infos)[...]

                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                }
            }
        }
    }
]
```

```
[matastral@docker ~]$ sudo ss -lnpt | grep docker
[sudo] password for matastral:
LISTEN 0      4096         0.0.0.0:9999      0.0.0.0:*    users:(("docker-proxy",pid=7138,fd=4))
LISTEN 0      4096            [::]:9999         [::]:*    users:(("docker-proxy",pid=7143,fd=4))
```

```
[matastral@docker ~]$ sudo firewall-cmd --add-port=9999/tcp --permanent
success
[matastral@docker ~]$ sudo firewall-cmd --reload
success
```

```
[matastral@docker ~]$ curl http://10.1.2.2:9999 --head
HTTP/1.1 200 OK
Server: nginx/1.25.3
Date: Thu, 21 Dec 2023 14:48:15 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Tue, 24 Oct 2023 13:46:47 GMT
Connection: keep-alive
ETag: "6537cac7-267"
Accept-Ranges: bytes
```

🌞 **On va ajouter un site Web au conteneur NGINX**

```
[matastral@docker ~]$ mkdir nginx
[matastral@docker nginx]$ touch index.html
[matastral@docker nginx]$ nano index.html
[matastral@docker nginx]$ cat index.html
<h1>MEOOOW</h1>
[matastral@docker nginx]$ touch site_nul.conf
[matastral@docker nginx]$ nano site_nul.conf
[matastral@docker nginx]$ cat site_nul.conf
server {
    listen        8080;

    location / {
        root /var/www/html;
    }
}
```

```
[matastral@docker ~]$ docker run -d -p 9999:8080 -v /home/matastral/nginx/index.html:/var/www/html/index.html -v /home/matastral/nginx/site_nul.conf:/etc/nginx/conf.d/site_nul.conf nginx
597136fde00f2b0d4a9bbd48091a579d92de6b5dc9e7bdd83570e4e0126c4d03
```

🌞 **Visitons**

```
[matastral@docker nginx]$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS
             NAMES
830b72043b3e   nginx     "/docker-entrypoint.…"   5 seconds ago   Up 5 seconds   80/tcp, 0.0.0.0:9999->8080/tcp, :::9999->8080/tcp   intelligent_hopper
[matastral@docker nginx]$ curl http://10.1.2.2:9999
<h1>MEOOOW</h1>
```

🌞 **Lance un conteneur Python, avec un shell**

```
[matastral@docker ~]$ docker run -it python bash
Unable to find image 'python:latest' locally
latest: Pulling from library/python
bc0734b949dc: Pull complete
b5de22c0f5cd: Pull complete
917ee5330e73: Pull complete
b43bd898d5fb: Pull complete
7fad4bffde24: Pull complete
d685eb68699f: Pull complete
107007f161d0: Pull complete
02b85463d724: Pull complete
Digest: sha256:3733015cdd1bd7d9a0b9fe21a925b608de82131aa4f3d397e465a1fcb545d36f
Status: Downloaded newer image for python:latest
```

🌞 **Installe des libs Python**

```
root@e884189cb27f:/# pip install aiohttp
root@e884189cb27f:/# pip install aioconsole
```

```
root@e884189cb27f:/# python
Python 3.12.1 (main, Dec 19 2023, 20:14:15) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import aiohttp
```

[Go pour la partie 2 youhouuu](./Partie2.md)