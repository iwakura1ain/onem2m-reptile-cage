import src.cse_interface as cse
import src.sensor_interface as sens
from src.log.log import *

from time import sleep
import uuid as UUID
import json 


def startAE(config, groupname): #TODO: error messages 
    """
    AE 생성, CSEInterface 생성 -> main AE loop
    ---
    config : config 
    """

    #create uuid 
    try:
        if config["AE"]["uuid"] != "":
            with open("config.ini", "w+") as configfile:
                uuid = str(UUID.uuid4())
                config.set("AE", "uuid", uuid)
                config.set("AE", "group_name", groupname)
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
        t = applicationEntity.checkAE(cseInterface)
        print(t)
        print("\nAE verified")
        
        t = applicationEntity.checkGroup(cseInterface)
        print(t)
        print("\ngroup verified")

    except ConnectionError:
        logError("error no connection")
        quit()

        
    #main loop
    for i in range(3):
        sensorValues = applicationEntity.getSensorValues()       
        applicationEntity.sendSensorValues(cseInterface, sensorValues)
        applicationEntity.checkControl(cseInterface)

        sleep(1)

    return


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
        self.control = {}

        
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
        self.sensors[name] = new
        

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
            logInfo(f"read {name}")
        
        return retval

    
    def sendSensorValues(self, cseInterface, sensorValues):
        """
        센서값 cse로 보내는 함수 
        """

        for name, val in (sensorValues | self.control).items():
            res = cseInterface.createCIN(path=f"/{self.aeName}/{name}", con=val)
            print(f"\n\n{name} read value\n", res)
            if res is None:
                logError(f"error while sending  {name}")
            else:
                logInfo(f"sent {name}")

                
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
            

    
    def checkGroup(self, cseInterface): #TODO: error recovery
        """
        group 내에 존재하는지 확인 존재 확인 
        """

        res = cseInterface.getGRP(rn=self.groupName)
        addList = []
        if "m2m:grp" in res.keys(): # group exists
            if "mid" in res["m2m:grp"].keys():
                addList = res["m2m:grp"]["mid"]
                
            else:
                addList = []

            print(f"old group: {addList}")

            res2 = cseInterface.delGRP(rn=self.groupName)
                
                
            addList.append(f"Mobius/{self.aeName}")
            print(f"new group: {addList}")
            #res = cseInterface.modifyGRP(rn=self.groupName, mid=addList)
            res = cseInterface.createGRP(rn=self.groupName, mid=addList)
            
            print("\n\n group add request: \n", addList, "\n group add returned: \n", res, "\n\n")

        else:
            res = cseInterface.createGRP(rn=self.groupName, mid=[f"Mobius/{self.aeName}"])
            if "mid" not in res["m2m:grp"].keys():
                res = [f"Mobius/{self.aeName}"]
                res = cseInterface.modifyGRP(rn=self.groupName, mid=res)
                res2 = cseInterface.delGRP(rn=self.groupName)
                res3 = cseInterface.createGRP(rn=self.groupName, mid=res)
                

        print(res) 
        return res
                
                            
            
    @logCall("checking control messages from dashboard")
    def checkControl(self, cseInterface):
        for name, s in self.sensors.items():
            try:
                res = cseInterface.getCIN(rn="/la", path=f"/{self.aeName}/{name}/control")
                res = res["m2m:cin"]["con"]

                if self.control[name] != res:
                    logInfo(f"received control from dashboard {name} : {res: <10}")
                    self.control[name] = res
                
            except KeyError:
                pass


        
    













