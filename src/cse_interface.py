import requests as req
from requests.exceptions import RequestException
import json

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
    
    def __init__(self, uuid, config):
        self.uuid = uuid
        
        self.cse_ip = config["cse_ip"]
        self.cse_port = config["cse_port"]
        self.cse_cb = config["cse_cb"]

        self.baseurl = f"http://{self.cse_ip}:{self.cse_port}/{self.cse_cb}"
        self.headers = {
            "Accept": "application/json",
            "X-M2M-RI": "req" + self.uuid,
            "X-M2M-Origin": "S" + self.uuid,
            "Content-Type": "application/vnd.onem2m-res+json;ty=2"
        }

        self.adminHeaders = {
            "Accept": "application/json",
            "X-M2M-RI": "dks",
            "X-M2M-Origin": "dks",
            "Content-Type": "application/vnd.onem2m-res+json;ty=2"
        }
                

    def getAE(self, rn, path="/"):
        """
        AE 조회
        ---
        rn: 조회할 AE 이름 
        """
        try:
            res = req.get(url=f"{self.baseurl}{path}{rn}", headers=self.headers)
            return res.json()
            
        except RequestException:
            return None
        
       
    def createAE(self, rn, path="", lbl=["none"], rr="true", api="cage.create.ae", poa=["127.0.0.1"]):
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
            res = req.post(url=f"{self.baseurl}{path}", headers=self.headers, json=body)
            return res.json()
            
        except RequestException:
            return None 

        
    def modifyAE(self, rn, **kwargs):
        """
        AE 수정
        ---
        rn: 수정할 ae 이름
        **kwargs: 바꾸고 싶은 값을 인자로 -> modifyAE(rn, key="val", ...) 전달
        """
        body = {"m2m:ae": kwargs}
        try:
            res = req.post(url=self.baseurl, headers=self.headers, json=body)
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
            res = req.delete(url=f"{self.baseurl}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass
     

    def createCNT(self, rn, path="", lbl=["none"], mbs=16384):
        body = {
            "m2m:cnt": {
                "rn": rn,
                "lbl": lbl,
                "mbs": mbs
            }
        }
        try:
            res = req.post(url=f"{self.baseurl}{path}", headers=self.headers, json=body)
            return res.json()
            
        except RequestException:
            return None


    def getCNT(self, rn, path="/"):
        """
        CNT 조회
        ---
        rn: 조회할 CNT 이름 
        """
        try:
            res = req.get(url=f"{self.baseurl}{path}{rn}", headers=self.headers)
            return res.json()
            
        except RequestException:
            return None

    def modifyCNT(self, rn, **kwargs):
        """
        CNT 수정
        ---
        rn: 수정할 CNT 이름
        **kwargs: 바꾸고 싶은 값을 인자로 -> modifyCNT(rn, key="val", ...) 전달
        """
        body = {"m2m:cnt":kwargs}

        try:
            res = req.post(url=self.baseurl, headers=self.headers, json=json.dumps(body))
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
            res = req.delete(url=f"{self.baseurl}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass
            
            
    def createCIN(self, con, path=""):
        body = {
            "m2m:cin":{
                "con": con
            }
        }

        try:
            res = req.post(url=f"{self.baseurl}{path}", headers=self.headers, json=json.dumps(body))
            return res.json()
            
        except RequestException:
            return None

    def getCIN(self, rn, path="/"):
        """
        CIN 조회
        ---
        rn: 조회할 CIN 이름 
        """
        try:
            res = req.get(url=f"{self.baseurl}{path}{rn}", headers=self.headers)
            return res.json()
            
        except RequestException:
            return None

    def modifyCIN(self, rn, url, **kwargs):
        """
        CIN 수정
        ---
        rn: 수정할 cin 이름
        **kwargs: 바꾸고 싶은 값을 인자로 -> modifyCIN(rn, key="val", ...) 전달
        """
        body = {"m2m:ae": kwargs}
        try:
            res = req.post(url=self.baseurl, headers=self.headers, json=json.dumps(body))
            print(res.text)
            
        except RequestException:
            pass

    def deleteCIN(self, rn, url):
        """
        CIN 삭제
        ---
        rn: 삭제할 CIN 이름 
        """
        try:
            res = req.delete(url=f"{self.baseurl}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass


    def createGRP(self, rn, mid=[]):
        body = {
	    "m2m:grp": {
		"rn": rn,
		"mnm": 5,
		"mid": mid
	    }
        }

        try:
            res = req.post(url=f"{self.baseurl}", headers=self.headers, json=json.dumps(body))
            return res.json()
            
        except RequestException:
            return None

    def getGRP(self, rn):
        try:
            res = req.get(url=f"{self.baseurl}/{rn}", headers=self.headers)
            return res.json()
            
        except RequestException:
            return None

    def modifyGRP(self, rn, path="/", mid=[]):
        body = {
            "m2m:grp": {
                "mid": mid
            }
        }
        
        try:
            res = req.put(url=f"{self.baseurl}{path}{rn}", headers=self.adminHeaders, json=body)
            return res.json()
            
        except RequestException:
            return None
        

    def createACP(self, rn, acor1, acor2, acop1, acop2):
        body = {
            "m2m:acp" : {
                "rn" : rn,
                "pv" : {
                    "acr" : [{
                        "acco" : [],
                        "acor" : acor1,
                        "acop" : acop1
                    }, 
                    {
                        "acor" : acor2,
                        "acop" : acop2
                    }]
                },
                "pvs" : {
                    "acr" : [{
                        "acco" : [],
                        "acor" : acor1,
                        "acop" : acop1
                    }, 
                    {
                        "acor" : acor2,
                        "acop" : acop2
                    }]
                }
            }
        }

        try:
            res = req.post(url=self.baseurl, headers=self.headers, json=json.dumps(body))
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
            res = req.get(url=f"{self.baseurl}/{rn}", headers=self.headers)
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
            res = req.post(url=self.baseurl, headers=self.headers, json=json.dumps(body))
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
            res = req.delete(url=f"{self.baseurl}/{rn}", headers=self.headers)
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
            res = req.post(url=self.baseurl, headers=self.headers, json=json.dumps(body))
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
            res = req.get(url=f"{self.baseurl}/{rn}", headers=self.headers)
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
            res = req.post(url=self.baseurl, headers=self.headers, json=json.dumps(body))
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
            res = req.delete(url=f"{self.baseurl}/{rn}", headers=self.headers)
            print(res.text)
            
        except RequestException:
            pass


    
