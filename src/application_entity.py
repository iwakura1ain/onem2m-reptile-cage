import cse_interface as cse
import sensor_interface as sens
from log.log import *


def startAE(config): #TODO: error messages 
    """
    AE 생성, CSEInterface 생성 -> main AE loop
    ---
    config : config 
    """

    #config file parsing, creating ae classes
    try:
        uuid = config["AE"]["uuid"]
        applicationEntity = ApplicationEntity(uuid, config["AE"])
        cseInterface = cse.CSEInterface(uuid, config["CSE"])

        #add sensors to ae
        for name, sensorType in config["AE-SENSORS"]:
            applicationEntity.registerSensors(name, sensorType)
        
    except KeyError:
        #config file error 
        quit()
    
    #check if data structures exist on server -> if not create them 
    try:
        _ = applicationEntity.checkAE(cseInterface)
        _ = applicationEntity.checkGroup(cseInterface)

    except ConnectionError:
        #no connection 
        quit()
      
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
        self.aeName = uuid
        self.groupName = config["group_name"]
        
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
            cseInterface.createCIN(path=f"{self.aeName}/{name}", con=val)


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
                for name, sensor in self.sensors.iteritems(): #create sensor containers
                    cseInterface.createCNT(rn=name, path=f"/{self.aeName}")
                    
            except: #no connection 
                raise ConnectionError #TODO: error recovery when no connection

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
                    mid = res.append(aePath)
                    res = cseInterface.modifyGRP(rn=self.groupName, mid=mid)
                    res = ["m2m:grp"]["mid"]
                
                return res

            # no group
            except KeyError:
                cseInterface.createGRP(rn=self.groupName) #create group 

            # no connection
            except:
                raise ConnectionError #TODO: error recovery when no connection



            
    
    













