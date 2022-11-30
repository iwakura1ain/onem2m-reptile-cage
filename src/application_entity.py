import cse_interface as cse
import sensor_interface as sens
from log.log import *

import os, configparser


def startAE(config):
    """
    AE 생성, CSEInterface 생성 -> main AE loop
    ---
    config : config 
    """
    
    uuid = config["UUID"]["uuid"]
    applicationEntity = ApplicationEntity(uuid, config["AE"])
    cseInterface = cse.CSEInterface(uuid, config["CSE"])

    #add sensors to ae
    for name, sensorType in config["AE-SENSORS"]:
        applicationEntity.registerSensors(name, sensorType)

    #if container does not exist -> create containers 
    if applicationEntity.getContainers(cseInterface) is None:
        applicationEntity.createContainers(cseInterface)

    #main loop
    while(True):
        sensorValues = applicationEntity.getSensorValues()
        applicationEntity.sendSensorValues(cseInterface, sensorValues)      


class ApplicationEntity:
    """
    IOT 장치에서 센서값을 읽고 전달하는 역할
    ---
    startLogger : 로깅 기능 시작
    config : configParser 
    cseInterface : cse interface
    sensors : { "name": Sensor, ... } 이루어진 센서들
    """
    
    def __init__(self, uuid, config):
        self.uuid = uuid
        self.groupName = config["group_name"]
        self.aeName = config["ae_name"]
        self.cntName = self.uuid

        self.groupPath = f"{self.aeName}/{self.groupName}"
        self.cntPath = f"{self.aeName}/{self.groupName}/{self.cntName}"
        
        self.sensors = {}
    
            
    def registerSensors(self, name, sensorType, interface=None):
        """
        센서 추가
        ---
        name : 센서 이름
        sensorType : 센서 종류
        interface : 센서 wrapper 함수 
        """
        new = sens.Sensor(name, sensorType, interface)
        self.sensors.update({name: new})
        
        
    def getSensorValues(self, **kwargs):
        """
        센서값 읽는 함수 
        ---
        name : 센서 이름 
        """
        retval = {}
        for name, s in self.sensors.iteritems():
            retval[name] = s.readSensor(**kwargs)
        
        return retval

    def sendSensorValues(self, cseInterface, sensorValues):
        """
        센서값 cse로 보내는 함수 
        """
        for name, val in sensorValues.iteritems():
            cseInterface.createCIN(path=f"{self.cntPath}/{name}", con=val)
    
    def getContainers(self, cseInterface):
        """
        센서들 위한 컨테이너 존재하는지 확인 
        """        
        res = cseInterface.getCNT(self.cntPath)
        try:
            return res.json()["m2m:cnt"]

        except KeyError: #no container in server
            return None

        except: #no connection 
            return None #TODO: error recovery when no connection 

        
    def createContainers(self, cseInterface): #TODO: error recovery here
        """
        센서들 위한 컨테이너 생성 
        """
        cseInterface.createCNT(path=self.groupPath, rn=self.cntName) #create base cnt        
        for name, s in self.sensors: # create individual sensor cnt 
            cseInterface.createCNT(path=self.cntPath, rn=name)

            
    
    













