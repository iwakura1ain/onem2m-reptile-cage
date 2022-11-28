import requests as req 
import json
import uuid

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

    def createCNT(self, rn, lbl=["none"], mbs = 16384):
        body = {
            "m2m:cnt":{
                "rn":rn,
                "lbl":lbl,
                "mbs":mbs
            }
        }
        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

    def getCNT(self, rn):
        """
        CNT 조회
        ---
        rn: 조회할 CNT 이름 
        """
        try:
            res = req.get(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass

    def modifyCNT(self, rn, **kwargs):
        """
        CNT 수정
        ---
        rn: 수정할 CNT 이름
        **kwargs: 바꾸고 싶은 값을 인자로 -> modifyCNT(rn, key="val", ...) 전달
        """
        body = {"m2m:cnt":kwargs}

        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

    def deleteCNT(self, rn):
        """
        CNT 삭제
        ---
        rn: 삭제할 CNT 이름 
        """
        try:
            res = req.delete(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass
            
            
    def createCIN(self, con):
        body = {
            "m2m:cin":{
                "con": con
            }
        }

        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

    def getCIN(self, rn):
        """
        CIN 조회
        ---
        rn: 조회할 CIN 이름 
        """
        try:
            res = req.get(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass

    def modifyCIN(self, rn, **kwargs):
        """
        CIN 수정
        ---
        rn: 수정할 cin 이름
        **kwargs: 바꾸고 싶은 값을 인자로 -> modifyCIN(rn, key="val", ...) 전달
        """
        body = {"m2m:ae": kwargs}
        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

    def deleteCIN(self, rn):
        """
        CIN 삭제
        ---
        rn: 삭제할 CIN 이름 
        """
        try:
            res = req.delete(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass

    def createACP(self):
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

        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

    def getACP(self, rn):
        """
        ACP 조회
        ---
        rn: 조회할 ACP 이름 
        """
        try:
            res = req.get(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass

    def modifyACP(self, rn, **kwargs):
        """
        ACP 수정
        ---
        rn: 수정할 acp 이름
        **kwargs: 바꾸고 싶은 값을 인자로 -> modifyACP(rn, key="val", ...) 전달
        """
        body = {"m2m:ae": kwargs}
        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

    def deleteACP(self, rn):
        """
        ACP 삭제
        ---
        rn: 삭제할 ACP 이름 
        """
        try:
            res = req.delete(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass

    def createSubscription(self, rn, net, nu, exc):
        body = {
            "m2m:sub": {
        	"rn": rn,
            "enc": {
        	    "net": net
        	},
        	"nu": nu,
        	"exc": exc,
            }
        }

        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

    def getSubscription(self, rn):
        """
        Subscription 조회
        ---
        rn: 조회할 Subscription 이름 
        """
        try:
            res = req.get(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass

    def modifySubscription(self, rn, **kwargs):
        """
        Subscription 수정
        ---
        rn: 수정할 Subscription 이름
        **kwargs: 바꾸고 싶은 값을 인자로 -> modifySubscription(rn, key="val", ...) 전달
        """
        body = {"m2m:ae": kwargs}
        try:
            res = req.post(url=self.url, headers=self.headers, json=body)
            print(res.text)
            
        except RequestException:
            pass

    def deleteSubscription(self, rn):
        """
        Subscription 삭제
        ---
        rn: 삭제할 Subscription 이름 
        """
        try:
            res = req.delete(url=f"{self.url}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass