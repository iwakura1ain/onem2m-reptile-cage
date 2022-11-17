import requests, json

class CSEInterface:
    """
    CSE와 interface하는 클래스
    ---
    config : configparser instance
    ---
    cse_* : cse 정보
    """
    
    def __init__(self, config):
        self.config = config
        
        # self.cse_ip = self.config["cse_ip"]
        # self.cse_port = self.config["cse_port"]
        # self.cse_release = self.config["cse_release"]

        
    def getHeaders(self):
        return {
	    "X-M2M-Origin": "S"+name,
	    "X-M2M-RI": "req"+requestNr,
	    "Content-Type": "application/vnd.onem2m-res+json;ty=2"
	}
    
        

    @logInfo("creating AE")
    def createAE(self):
        headers = self.getHeaders()
        body = { 
	    "m2m:ae":{
		"rn":name,			
		"api":"app.company.com",
		"rr":false
	    }
	}


    def createCNT(self):
        headers = self.getHeaders()
        body = {
	    "m2m:cnt":{
		"rn":"DATA",
		"mni":10000
	    }
	}
        
        
    def createCIN(self):
        headers = self.getHeaders()
        body = {
	    "m2m:cin":{
	        "con": con
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
		"rn": "sub",
		"nu": ["http://"+config.app.ip+":"+config.app.port+"/"+"S"+name+"?ct=json"],
		"nct": 2,
		"enc": {
		    "net": [3]
		}
	    }
	}
    
        




