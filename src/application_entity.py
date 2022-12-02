import src.cse_interface as cse
import src.sensor_interface as sens
from src.log.log import *

from time import sleep
import uuid as UUID
import json 


def startAE(config): #TODO: error messages 
    """
    AE 생성, CSEInterface 생성 -> main AE loop
    ---
    config : config 
    """

    #create uuid 
    try:
        if config["AE"]["uuid"] == "":
            with open("config.ini", "w") as configfile:
                uuid = str(UUID.uuid4())
                config["AE"]["uuid"] = uuid
                config.write(configfile)
                
                logInfo(f"new UUID: {uuid}")
                
    except:
        logError("error while creating uuid")
        quit()
        
        
    #config file parsing, creating ae classes
    try:
        uuid = config["AE"]["uuid"]
        applicationEntity = ApplicationEntity(uuid, config["AE"])
        cseInterface = cse.CSEInterface(uuid, config["CSE"])
        
        #add sensors to ae
        for name, sensorType in config.items("AE-SENSORS"):
            logInfo(f"Sensor {name} : {sensorType} registered")
            applicationEntity.registerSensors(name, sensorType)
            
    except KeyError:
        logError("error while parsing config file")
        quit()
        
        
    #check if data structures exist on server -> if not create them 
    try:
        _ = applicationEntity.checkAE(cseInterface)
        logInfo("AE verified")
        
        _ = applicationEntity.checkGroup(cseInterface)
        logInfo("group verified")

    except ConnectionError:
        logError("error no connection")
        quit()

        
    #main loop
    while(True):
        sensorValues = applicationEntity.getSensorValues()
        logInfo(f"sensor read: \n{sensorValues}")
        
        applicationEntity.sendSensorValues(cseInterface, sensorValues)
        sleep(int(applicationEntity.interval))


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
        self.interval = config["send_interval"]

        self.aeName = uuid
        self.groupName = config["group_name"]
        
        self.sensors = {}
    
    @logCall("registering sensors")
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
        

    @logCall("reading sensor values")
    def getSensorValues(self, **kwargs):
        """
        센서값 읽는 함수 
        ---
        name : 센서 이름 
        """
        retval = {}
        for name, s in self.sensors.items():
            retval[name] = s.readSensor(**kwargs)
        
        return retval

    @logCall("sending sensor values")
    def sendSensorValues(self, cseInterface, sensorValues):
        """
        센서값 cse로 보내는 함수 
        """

        for name, val in sensorValues.items():
            res = cseInterface.createCIN(path=f"{self.aeName}/{name}", con=val)
            if res is None:
                logError(f"error while sending  {name} : {val}")
            else:
                logInfo(f"sent {name} : {val}")

    @logCall("checking AE on server")
    def checkAE(self, cseInterface):
        """
        cse에 ae와 cnt 존재 확인 
        """

        while True:
            try:
                res = cseInterface.getAE(rn=self.aeName) 
                return res["m2m:ae"]

            except KeyError: #no data
                cseInterface.createAE(rn=self.aeName) #create ae 
                for name, sensor in self.sensors.items(): #create sensor containers
                    cseInterface.createCNT(rn=name, path=f"/{self.aeName}")
                    
            except: #no connection 
                raise ConnectionError #TODO: error recovery when no connection
            

    @logCall("checking group on server")
    def checkGroup(self, cseInterface):
        """
        group 내에 존재하는지 확인 존재 확인 
        """
        while True:
            try:
                # group 조회 
                res = cseInterface.getGRP(rn=self.groupName)
                res = res["m2m:grp"]["mid"]

                # group에 ae 추가하기 
                aePath = f"Mobius/{self.aeName}"  #TODO: static baseurl
                if aePath not in res: 
                    res.append(aePath) # mid = res
                    res = cseInterface.modifyGRP(rn=self.groupName, mid=res)
                    res = res["m2m:grp"]["mid"]
                
                return res

            # no group
            except KeyError:
                cseInterface.createGRP(rn=self.groupName) #create group 

            # no connection
            except:
                raise ConnectionError #TODO: error recovery when no connection



            
    
    













