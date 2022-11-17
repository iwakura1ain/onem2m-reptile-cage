import cse_interface as cse
import sensor_interface as sens
from log.log import *

import os, configparser

applicationEntity = None
cseInterface = None

def startAE(config):
    """
    AE 생성, CSEInterface 생성 -> main AE loop
    ---
    config : config 
    """
    
    global ApplicationEntity, cseInterface
    
    if ApplicationEntity is None and cseInterface is None:
        applicationEntity = ApplicationEntity(config["AE"])
        cseInterface = cse.CSEInterface(config["CSE"])

        while(True):
            #main AE loop 
            pass
    

class ApplicationEntity:
    """
    IOT 장치에서 센서값을 읽고 전달하는 역할
    ---
    startLogger : 로깅 기능 시작
    config : configParser 
    cseInterface : cse interface
    sensors : { "name": Sensor, ... } 이루어진 센서들
    """
    
    def __init__(self, config):
        #TODO: offload to main
        #startLogger(self.config["log_dir"], self.config["log_level"])

        self.config = config       
        self.sensors = {}
    

    def addSensor(self, name, sensorType, interface=None):
        """
        센서 추가
        ---
        name : 센서 이름
        sensorType : 센서 종류
        interface : 센서 wrapper 함수 
        """
        new = sens.Sensor(name, sensorType, interface)
        self.sensors.update({name: new})
        
        
    def readSensor(self, name, **kwargs):
        """
        센서값 읽는 함수 
        ---
        name : 센서 이름 
        """
        return self.sensors[name].readSensor(**kwargs)
        






