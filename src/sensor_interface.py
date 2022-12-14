import time
#import board, adafruit_dht, picamera
from PIL import Image
from io import BytesIO
import base64

from random import randint
from string import ascii_letters


class SensorInterface:
    """
    센서와 interface하는 클래스
    
    - 각 센서값 읽어오는 wrapper 함수를 static으로 정의
    - addSensorInterface 통해 read_functions에 함수를 등록
    - readSensor를 사용해 센서 읽음     
    ---    
    """
    read_functions = {}
    picam2 = None
    
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
        return str(randint(-10000, 10000))
    
    @staticmethod
    def randomStr(**kwargs):
        return ascii_letters[randint(0, 10):randint(10, 20)]      
    
    # @staticmethod
    # def tempSensor(**kwargs):
    #     try: 
    #         return adafruit_dht.DHT11(board.D18).temperature
    #     except:
    #         return 0

    # @staticmethod
    # def humiditySensor(**kwargs):
    #     try:
    #         return adafruit_dht.DHT11(board.D18).humidity
    #     except:
    #         return 0
    
    @staticmethod
    def cameraSensor():
        # try:
        #     if picam2 is None:
        #         picam2 = Picamera2()
        #         picam2.start()
        
        #     image =  picam2.capture_image(main={"size": (1024, 768)})

        #     buff = BytesIO()
        #     image.save(buff, format="JPEG")
        #     return base64.b64encode(buff.getvalue())
            
        
        image = Image.open("test.jpeg")

        buff = BytesIO()
        image.save(buff, format="JPEG")
        return str(base64.b64encode(buff.getvalue()), "utf-8")

            

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






