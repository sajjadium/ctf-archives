#!/usr/bin/python3

import os
import sys
import subprocess
import string
import uuid
import hashlib
import random

###Boilerplate utils
def printError(errMsg):
    print(errMsg)
    exit()

def myInput(prompt):
    '''
    python input prompts to stderr by default, and there is no option to change this afaik
    this wrapper is just normal input with stdout prompt
    '''
    print(prompt,end='')
    return input()

def doPow(difficulty,adminSecret):
    challenge = ''.join(random.choices(string.ascii_letters,k=10))
    print(f"(int.from_bytes(hashlib.sha256(('{challenge}' + answer).encode()).digest(), byteorder='little') & ((1 << {difficulty}) - 1)) == 0")
    answer = myInput('answer > ')
    if answer==adminSecret or (int.from_bytes(hashlib.sha256((challenge+answer).encode()).digest(),byteorder='little')&((1<<difficulty)-1))==0:
        return True
    else:
        return False

###Instance management utils
def genInstanceId():
    return str(uuid.uuid4()).replace('-','')

def checkInstanceId(instanceId):
    if len(instanceId)!=32:
        return False
    instanceIdCSET = set(string.ascii_lowercase+string.digits)
    for c in instanceId:
        if c not in instanceIdCSET:
            return False
    return True

def instanceExists(instancePath,secret=None):
    if not os.path.exists(instancePath):
        return False
    if secret is not None:
        with open(os.path.join(instancePath,'secret'),'r') as f:
            secretF = f.read().strip()
        if secret!=secretF:
            return False
    return True

def instanceIsRunning(instanceId):
    if subprocess.getoutput('docker container ls -q -f "name=config_sentinel{instanceId}.*" 2>/dev/null')!='':
        return True
    return False

def populateInstanceConfig(instanceId,instancePath,instanceConfigPath,guestHomeDir):
    Dockerfile = f'''
from ubuntu:jammy

RUN useradd -m sentinel
USER sentinel
WORKDIR /home/sentinel/
ENTRYPOINT ["./sentinel"]
'''
    dockerCompose = f'''
version: '3'

volumes:
  storage{instanceId}:
    driver: local
    driver_opts:
      type: overlay
      o: lowerdir={guestHomeDir},upperdir={os.path.join(instancePath,'upper')},workdir={os.path.join(instancePath,'work')}
      device: overlay

services:
  sentinel{instanceId}:
    build: ./
    volumes:
      - storage{instanceId}:/home/sentinel/
    stdin_open : true
'''
    with open(os.path.join(instanceConfigPath,'Dockerfile'),'w') as f:
        f.write(Dockerfile)
    with open(os.path.join(instanceConfigPath,'docker-compose.yml'),'w') as f:
        f.write(dockerCompose)

def buildInstanceDocker(instanceId,instancePath):
    configPath = os.path.join(instancePath,'config')
    cwd = os.getcwd()
    os.chdir(configPath)
    os.system(f'docker-compose build sentinel{instanceId} 1>/dev/null 2>/dev/null')
    os.chdir(cwd)

def cleanupInstanceDocker(instanceId):
    os.system(f'docker rmi -f config_sentinel{instanceId} 1>/dev/null 2>/dev/null')
    os.system(f'docker volume rm config_storage{instanceId} 1>/dev/null 2>/dev/null')

def resetInstance(instanceId,instancePath,noCleanup=False):
    upperdirPath = os.path.join(instancePath,'upper')
    workdirPath = os.path.join(instancePath,'work')
    if noCleanup is False:
        cleanupInstanceDocker(instanceId)
        os.system(f'chmod -fR 777 {upperdirPath}')
        os.system(f'chmod -fR 777 {workdirPath}')
        os.system(f'rm -fr {upperdirPath}')
        os.system(f'rm -fr {workdirPath}')
        if os.path.exists(upperdirPath) or os.path.exists(workdirPath):
            printError(f'reset instance {instanceId} failed, please contact admin')
    os.system(f"mkdir -p {os.path.join(upperdirPath,'work')} && chmod 555 {upperdirPath} && chmod 777 {os.path.join(upperdirPath,'work')}")
    os.system(f'mkdir {workdirPath} && chmod 555 {workdirPath}')
    buildInstanceDocker(instanceId,instancePath)

def launchInstance(instanceId,instanceConfigPath):
    os.chdir(instanceConfigPath)
    print(os.getcwd())
    os.system(f'docker-compose run --rm sentinel{instanceId}')

def createInstance(instanceRootDir,guestHomeDir):
    secret = hashlib.sha256(myInput('secret > ').strip().encode()).hexdigest()
    instanceId = genInstanceId()
    instancePath = os.path.join(instanceRootDir,instanceId)
    while instanceExists(instancePath):
        instanceId = getInstanceId()
        instancePath = os.path.join(instanceRootDir,instanceId)
    os.mkdir(instancePath)
    with open(os.path.join(instancePath,'secret'),'w') as f:
        f.write(secret)
    instanceConfigPath = os.path.join(instancePath,'config')
    os.mkdir(instanceConfigPath)
    populateInstanceConfig(instanceId,instancePath,instanceConfigPath,guestHomeDir)
    print(f'instanceId : {instanceId} (keep this for future reference)')
    sys.stdout.flush()
    resetInstance(instanceId,instancePath,noCleanup=True)
    launchInstance(instanceId,instanceConfigPath)

def resumeInstance(instanceRootDir,reset=False):
    instanceId = myInput('instanceId > ').strip()
    secret = hashlib.sha256(myInput('secret > ').strip().encode()).hexdigest()
    if checkInstanceId(instanceId) is False:
        printError(f'illegal instanceId : {instanceId}')
    instancePath = os.path.join(instanceRootDir,instanceId)
    if not instanceExists(instancePath,secret):
        printError(f'instance {instanceId}:{secret} does not exist')
    if instanceIsRunning(instanceId):
        printError(f'cannot reset/resume {instanceId} while it is running')
    if reset:
        resetInstance(instanceId,instancePath)
    instanceConfigPath = os.path.join(instancePath,'config')
    launchInstance(instanceId,instanceConfigPath)

def removeInstance(instanceRootDir):
    instanceId = myInput('instanceId > ').strip()
    secret = hashlib.sha256(myInput('secret > ').strip().encode()).hexdigest()
    if checkInstanceId(instanceId) is False:
        printError(f'illegal instanceId : {instanceId}')
    instancePath = os.path.join(instanceRootDir,instanceId)
    if not instanceExists(instancePath,secret):
        printError(f'instance {instanceId}:{secret} does not exist')
    if instanceIsRunning(instanceId):
        printError(f'cannot delete {instanceId} while it is running')
    cleanupInstanceDocker(instanceId)
    os.system(f'chmod -fR 777 {instancePath}')
    os.system(f'rm -fr {instancePath}')

###Service
def menu():
    print('========================================')
    print('                Sentinel                ')
    print('   Flag Secure Computing as a Service   ')
    print('========================================')
    print('  1. Create new instance                ')
    print('  2. Resume previous instance           ')
    print('  3. Reset and resume previous instance ')
    print('  4. Remove instance                    ')
    print('  5. Leave                              ')
    print('========================================')
    return int(myInput('Choice > ').strip())

if __name__=='__main__':
    if len(sys.argv)!=5:
        printError('usage : python3 instanceManager.py [instanceRootDir] [guestHomeDir] [powDifficulty] [adminSecret]')
    instanceRootDir = sys.argv[1]
    guestHomeDir = sys.argv[2]
    powDifficulty = int(sys.argv[3])
    adminSecret = sys.argv[4]
    match menu():
        case 1:
            if doPow(powDifficulty,adminSecret) is False:
                printError('invalid pow')
            createInstance(instanceRootDir,guestHomeDir)
        case 2:
            resumeInstance(instanceRootDir,reset=False)
        case 3:
            resumeInstance(instanceRootDir,reset=True)
        case 4:
            removeInstance(instanceRootDir)
        case 5:
            print('goodbye')
        case _:
            print('unrecognized option')
