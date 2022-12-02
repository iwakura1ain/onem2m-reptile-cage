from random import randint
from string import ascii_letters
import time, board, adafruit_dht
from picamera2 import Picamera2, Preview
from PIL import Image

class SensorInterface:
    """
    센서와 interface하는 클래스
    
    - 각 센서값 읽어오는 wrapper 함수를 static으로 정의
    - addSensorInterface 통해 read_functions에 함수를 등록
    - readSensor를 사용해 센서 읽음     
    ---    
    """
    
    picam2 = Picamera2()
    picam2.start_preview(Preview.NULL)
    preview_config = picam2.create_preview_configuration(main={"size": (1024, 768)})
    capture_config = picam2.create_still_configuration(main={"size": (1024, 768)})
    picam2.configure(preview_config)


    @staticmethod
    def CameraSensor():
        try:
            SensorInterface.picam2.start()
            time.sleep(3)
            image = SensorInterface.picam2.switch_mode_and_capture_image(SensorInterface.capture_config)
            return image
        except:
           global Image
           file = Image.open("test.jpg")
           return file

    read_functions = {}
    
    @classmethod
    def addSensorInterface(cls, sensorType, interface=None):
        """
        read_functions에 센서 읽어오는 wrapper 함수를 등록
        ---
        sensorType : sensor type 
        interface : sensor read 하는 wrapper 함수 이름
        """
        if interface is None:
            cls.read_functions.update({sensorType: getattr(cls, sensorType)})
        else:
            cls.read_functions.update({sensorType: getattr(cls, interface)})

    @staticmethod
    def randomVal(**kwargs):
        return randint(-10000, 10000)
    
    @staticmethod
    def randomStr(**kwargs):
        return ascii_letters[randint(0, 10):randint(10, 20)]      
    
     @staticmethod
    def TempSensor():
       return adafruit_dht.DHT11(board.D18).temperature

    @staticmethod
    def HumiditySensor():
       return adafruit_dht.DHT11(board.D18).humidity
    
    @staticmethod
    def CameraSensor():
        return picamera.PiCamera.capture('Cage.jpeg')


class Sensor(SensorInterface):
    """
    각 센서 위한 클래스
    ---
    name : 개별 센서의 이름
    sensorType : 센서의 type
    interface : 센서 인터페이스 wrapper 함수 이름 
    """
    def __init__(self, name, sensorType, interface=None):
        self.name = name
        self.sensorType = sensorType
        type(self).addSensorInterface(sensorType, interface)
    
    def readSensor(self, **kwargs):
        """
        센서값 읽어오는 함수 
        """
        return type(self).read_functions[self.sensorType](**kwargs)






