import logging
import json
import tarfile
from datetime import datetime
import uuid
import sys
import paramiko
from restore_backup import restore


def main():

    if (len(sys.argv) > 1):
        if (sys.argv[1] == "backup"):
            logging.info('Start of the backup...')
            backup()
        elif (sys.argv[1] == "list"):
            list()
        elif (sys.argv[1] == "restore"):
            restore()
        elif (sys.argv[1] == "delete"):
            delete()
        elif (sys.argv[1] == "clean"):
            clean()



def backup():
    data_json = readJsonFile()
    backup_name, date_str = backupName()
    compress(backup_name, data_json['backup']['files']['path'])
    if data_json['backup']['directory']['ssh']['active']:
        ssh(data_json['backup']['directory']['ssh']['ip'], 
            data_json['backup']['directory']['ssh']['port'], 
            data_json['backup']['directory']['ssh']['username'],
            data_json['backup']['directory']['ssh']['password'],
            data_json['backup']['files']['path'],
            data_json['backup']['directory']['path'])
    addToState(backup_name[:8], date_str, data_json['backup']['directory']['path'])

def addToState(id:str, time:str, path:str):
    with open('state.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    data[id] = {}
    data[id]['time'] = time
    data[id]['path'] = path
    with open('state.json', 'w') as file:
        json.dump(data, file)



def readJsonFile() -> dict :
    with open('backup.json') as mon_fichier:
        data = json.load(mon_fichier)
        return data

def backupName() -> str : 
    today_date = datetime.now()
    format_personnalise = "%d/%m/%Y %H:%M:%S"
    today_formated_date = today_date.strftime(format_personnalise)
    date_str = today_formated_date.replace("/", "-").replace(" ", "_").replace(":", "")
    hash = str(uuid.uuid4())[:8]
    backup_name = hash + "_" + date_str
    return backup_name, date_str


def compress(backup_name:str, path:str):
    archive = tarfile.open(path + backup_name + ".tar", "w:gz")
    archive.add("./save", arcname="")


def ssh(ip:str, port:str, username:str, password:str, local_path:str, destination_path:str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip + ":" + port, username, password)
    sftp = ssh.open_sftp()
    sftp.put(local_path, destination_path)
    sftp.close()
    ssh.close()


if __name__ == "__main__":
    main()