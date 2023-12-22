# II. Images

🌞 **Récupérez des images**

```
[matastral@docker ~]$ docker pull python:3.11
[matastral@docker ~]$ docker pull mysql:5.7
[matastral@docker ~]$ docker pull wordpress 
```

```
[matastral@docker ~]$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
mysql        5.7       5107333e08a8   9 days ago    501MB
python       latest    fc7a60e86bae   2 weeks ago   1.02GB
wordpress    latest    fd2f5a0c6fba   2 weeks ago   739MB
python       3.11      22140cbb3b0c   2 weeks ago   1.01GB
nginx        latest    d453dd892d93   8 weeks ago   187MB
```


🌞 **Lancez un conteneur à partir de l'image Python**

```
[matastral@docker ~]$ docker run -it 22140cbb3b0c bash
root@512f518e684e:/# python --version
Python 3.11.7
```

Pour construire une image il faut :

- créer un fichier `Dockerfile`
- exécuter une commande `docker build` pour produire une image à partir du `Dockerfile`

🌞 **Ecrire un Dockerfile pour une image qui héberge une application Python**

```
[matastral@docker ~]$ mkdir python_app_build
[matastral@docker python_app_build]$ nano app.py
[matastral@docker python_app_build]$ cat Dockerfile
FROM debian

RUN apt update -y && apt install -y python3

RUN apt install python3-emoji

COPY app.py /home/matastral/python_app_build/app.py

ENTRYPOINT ["python3", "/home/matastral/python_app_build/app.py"]
```

🌞 **Build l'image**

```
[matastral@docker python_app_build]$ docker build . -t python_app:version_de_ouf
[matastral@docker python_app_build]$ docker image ls | grep python
python_app   version_de_ouf   bb718a0d02e8   About a minute ago   190MB
```

🌞 **Lancer l'image**

```
[matastral@docker python_app_build]$ docker run python_app:version_de_ouf
Cet exemple d'application est vraiment naze 👎
```

[Et on continue pour la partie 3 youpiiiii (nan)](./Partie3.md)