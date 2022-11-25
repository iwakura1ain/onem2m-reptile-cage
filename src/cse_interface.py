import json, uuid
import requests as req
from requests.exceptions import RequestException

class CSEInterface:
    """
    CSE와 interface하는 클래스
    ---
    uuid: ae uuid 
    
    cse_ip: cse ip
    cse_port: cse port
    cse_cb: cse container base

    url: cse url
    headers: request headers
    """
    
    def __init__(self, config):
        self.uuid = str(uuid.uuid4())
        
        self.cse_ip = config["cse_ip"]
        self.cse_port = config["cse_port"]
        self.cse_cb = config["cse_cb"]

        self.url = f"http://{self.cse_ip}:{self.cse_port}/{self.cse_cb}"
        self.headers = {
            "Accept": "application/json",
            "X-M2M-RI": "req" + self.uuid,
            "X-M2M-Origin": "S" + self.uuid,
            "Content-Type": "application/vnd.onem2m-res+json;ty=2"
        }
        

    def getAE(self, rn):
        """
        AE 조회
        ---
        rn: 조회할 AE 이름 
        """
        try:
            res = req.get(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass
        
       
    def createAE(self, rn, lbl=["none"], rr="true", api="cage.create.ae", poa=["127.0.0.1"]):
        """
        AE 생성
        ---
        rn: 생성할 AE 이름
        ...
        """
        body = {
            "m2m:ae": {
                "rn": rn,
                "api": api,
                "rr": rr,
                "lbl": lbl,
                "poa": poa
            }
        }

        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

        
    def modifyAE(self, rn, **kwargs):
        """
        AE 수정
        ---
        rn: 수정할 ae 이름
        **kwargs: 바꾸고 싶은 값을 인자로 -> modifyAE(rn, key="val", ...) 전달
        """
        body = {"m2m:ae": kwargs}
        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass
        
        
    def deleteAE(self, rn):
        """
        AE 삭제
        ---
        rn: 삭제할 AE 이름 
        """
        try:
            res = req.delete(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass
     
        

    @logInfo("creating AE")
    def createAE(self):
        headers = self.getHeaders()
        body = { 
            "m2m:ae":{
                "rn":"justin",			
                "api":"0.2.481.2.0001.001.000111",
                "rr":True,
                "poa":["http://203.254.173.104:9727"]
            }
        }


    def createCNT(self):
        headers = self.getHeaders()
        body = {
            "m2m:cnt":{
                "rn":"ss",
                "lbl":["ss"],
                "mbs":16384
            }
        }
            
            
    def createCIN(self):
        headers = self.getHeaders()
        body = {
            "m2m:cin":{
                "con": "123"
            }
        }
            
            
    def createACP(self):
        headers = self.getHeaders()
        body = {
            "m2m:acp" : {
                "rn" : "acp_ryeubi",
                "pv" : {
                    "acr" : [{
                        "acco" : [],
                        "acor" : [
                            "justin"
                            ],
                        "acop" : "59"
                    }, 
                    {
                        "acor" : [
                            "ryeubi"
                            ],
                        "acop" : "63"
                    }]
                },
                "pvs" : {
                    "acr" : [{
                        "acco" : [],
                        "acor" : [
                            "justin1"
                            ],
                        "acop" : "59"
                    }, 
                    {
                        "acor" : [
                            "ryeubi"
                            ],
                        "acop" : "63"
                    }]
                }
            }
        }

        
    def createSubscription(self):
        headers = self.getHeaders()
        body = {
            "m2m:sub": {
        	"rn": "sub1",
            "enc": {
        	    "net": [3]
        	},
        	"nu": ["//keti.re.kr/Mobius/Mobius/justin"],
        	"exc": 10,
            }
        }





