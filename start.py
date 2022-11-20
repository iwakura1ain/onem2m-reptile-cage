#!/usr/bin/python3 
import src.application_entity as ae
import src.log.log as log

import configparser

def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    log.startLogger(config["LOG"])
    ae.startAE(config)

if __name__=="__main__":
    main()

#test for commit1
#test for commit2