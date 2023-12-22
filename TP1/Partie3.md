# III. Docker compose

🌞 **Créez un fichier `docker-compose.yml`**

```
[matastral@docker ~]$ mkdir compose_test
[matastral@docker compose_test]$ cat docker-compose.yml
version: "3"

services:
  conteneur_nul:
    image: debian
    entrypoint: sleep 9999
  conteneur_flopesque:
    image: debian
    entrypoint: sleep 9999
```

🌞 **Lancez les deux conteneurs** avec `docker compose`

```
[matastral@docker compose_test]$ docker compose up -d
[+] Running 3/3
 ✔ Network compose_test_default                  Created                                                                                               0.3s
 ✔ Container compose_test-conteneur_flopesque-1  Started                                                                                               0.0s
 ✔ Container compose_test-conteneur_nul-1        Started
```

🌞 **Vérifier que les deux conteneurs tournent**

```
[matastral@docker compose_test]$ docker compose top
compose_test-conteneur_flopesque-1
UID    PID     PPID    C    STIME   TTY   TIME       CMD
root   16730   16709   0    15:28   ?     00:00:00   sleep 9999

compose_test-conteneur_nul-1
UID    PID     PPID    C    STIME   TTY   TIME       CMD
root   16768   16741   0    15:28   ?     00:00:00   sleep 9999
```

🌞 **Pop un shell dans le conteneur `conteneur_nul`**

```
[matastral@docker compose_test]$ docker exec -it compose_test-conteneur_nul-1 bash
root@6d8d49ea4e4b:/# apt-get update && apt-get install -y iputils-ping
root@6d8d49ea4e4b:/# ping conteneur_flopesque
PING conteneur_flopesque (172.18.0.2) 56(84) bytes of data.
64 bytes from compose_test-conteneur_flopesque-1.compose_test_default (172.18.0.2): icmp_seq=1 ttl=64 time=0.080 ms
64 bytes from compose_test-conteneur_flopesque-1.compose_test_default (172.18.0.2): icmp_seq=2 ttl=64 time=0.079 ms
```

