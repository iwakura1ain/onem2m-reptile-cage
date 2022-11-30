#!/usr/bin/python3 

import src.application_entity as ae
import src.log.log as log

import configparser, uuid

def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if config["UUID"]["uuid"] == "":
        with open("config.ini", "w") as configfile:
            config["UUID"]["uuid"] = str(uuid.uuid4())
            config.write(configfile)
            
    log.startLogger(config)
    ae.startAE(config)

if __name__=="__main__":
    main()

