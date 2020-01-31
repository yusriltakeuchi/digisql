import os
import yaml
import sys
import datetime
from colorama import init
from colorama import Fore, Back, Style

init()

YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
RED = Fore.RED
GREEN = Fore.GREEN

def loadConfig(type):
    config = yaml.safe_load(open('config.yml'))
    if (type == "backup"):
        return config['CONFIG']['BACKUP']
    elif (type == "restore"):
        return config['CONFIG']['RESTORE']

'''
Mendeteksi argument
'''
def parsingArg():
    types = ""
    for x in range(0, len(sys.argv)):
        if sys.argv[x] == "--type":
            types = sys.argv[x+1]
    return types

def headers():
    print(" ")
    print("{0}      ------[ {1}DigiSQL {0}]------".format(YELLOW, BLUE))
    print("{0}    {1}DigiSQL - Auto Backup PostgreSQL ".format(YELLOW, BLUE))
    print("{0}    --------------------------------".format(YELLOW))
    print("{0}      Written by Yusril Rapsanjani  ".format(BLUE))
    print("{0}            Version v1.0  ".format(BLUE))
    print("{0}    --------------------------------".format(YELLOW))

def createFolder():
    folderName = "backup"
    if not os.path.exists(folderName):
        os.makedirs(folderName)

def createBackupPayload(config):
    timeNow = datetime.datetime.now()

    _filename = "backup/{0}-{1}".format(timeNow.strftime("%Y-%m-%d_%H-%M"), config['output'])
    _payload = "PGPASSWORD='{0}' pg_dump -h {1} -U {2} -p {3} {4} > {5}".format(config['password'], config['host'], config['username'], config['port'], config['database'], _filename)
    return _payload, _filename

def createRestorePayload(config):
    _payload = "PGPASSWORD='{0}' psql -U {1} -f {2} {3}".format(config['password'], config['username'], config['from_backup'], config['database'])
    return _payload

def backupDatabase():
    #Loading config
    print("{0}    [•] Reading config.".format(YELLOW))
    config = loadConfig("backup")

    #Create folder backup
    print("{0}    [•] Creating backup folder.".format(YELLOW))
    createFolder()

    #generate payload
    print("{0}    [•] Generating payload.".format(YELLOW))
    payload, filename = createBackupPayload(config)

    #backup database
    print("{0}    [•] Starting backup database.".format(YELLOW))
    try:
        os.popen(payload, 'r')
        print("{0}    [✓] Backup database success.".format(GREEN))
        print("{0}    [✓] File saved as name {1}{2}".format(GREEN, BLUE, filename))
    except:
        os.remove(filename)
        print("{0}    [x] Backup database failed.".format(RED))

def restoreDatabase():
    #Loading config
    print("{0}    [•] Reading config.".format(YELLOW))
    config = loadConfig("restore")

    #check file
    print("{0}    [•] Checking file.".format(YELLOW))
    if os.path.exists(config['from_backup']):
        #generate payload
        print("{0}    [•] Generating payload.".format(YELLOW))
        payload = createRestorePayload(config)

        #backup database
        print("{0}    [•] Starting restore database.".format(YELLOW))
        try:
            os.system(payload)
            print("{0}    [✓] Restore database success.".format(GREEN))
        except:
            os.remove(filename)
            print("{0}    [x] Restore database failed.".format(RED))
    else:
        print("{0}    [x] File not found.".format(RED))

def main():
    headers()

    # Get type
    types = parsingArg()
    if (types == ""):
        print("{0}            COMMAND HELP           ".format(YELLOW))
        print("{0}    --------------------------------".format(YELLOW))
        print("{0}    1. python3 digisql.py --type backup - To Backup database".format(YELLOW))
        print("{0}    2. python3 digisql.py --type restore - To Restore database".format(YELLOW))
        return
    
    if (types == "backup"):
        print("{0}            BACKUP DATABASE         ".format(YELLOW))
        print("{0}    --------------------------------".format(YELLOW))
        backupDatabase()
    elif (types == "restore"):
        print("{0}            RESTORE DATABASE        ".format(YELLOW))
        print("{0}    --------------------------------".format(YELLOW))
        restoreDatabase()

if __name__ == "__main__":
    main()