from random import randint
from string import ascii_letters
import time
from picamera2 import Picamera2, Preview
from PIL import Image

class SensorInterface:
    global Image
    
    picam2 = Picamera2()
    picam2.start_preview(Preview.NULL)
    preview_config = picam2.create_preview_configuration(main={"size": (640,350)})
    capture_config = picam2.create_still_configuration(main={"size": (640, 350)})
    picam2.configure(preview_config)
    new = picam2

    @staticmethod
    def CameraSensor():
        try:
            SensorInterface.picam2.start()
            time.sleep(3)
            image = SensorInterface.picam2.switch_mode_and_capture_image(SensorInterface.capture_config)
            img_resize = image.resize((180,120))
            return img_resize
        except:
           file = Image.open("test.jpg")
           img_resize = file.resize((180,120))
           return img_resize

   
    read_functions = {}
    @classmethod
    def addSensorInterface(cls, sensorType, interface=None):

        cls.Camera = ("Camera","CameraSensor","CameraSensor")

        
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

class Sensor(SensorInterface):

    def __init__(self, name, sensorType, interface=None):
        self.name = name
        self.sensorType = sensorType
        type(self).addSensorInterface(sensorType, interface)

        self.Camera = ("Camera","CameraSensor","CameraSensor")
      
    
    def readSensor(self, **kwargs):

        return type(self).read_functions[self.sensorType](**kwargs)
        

def main():

    temp = Sensor("Camera","CameraSensor","CameraSensor")
    print(temp.readSensor())

if __name__ == "__main__":
    main()
