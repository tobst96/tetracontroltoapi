import sys, requests, os
from pygelf import GelfUdpHandler
import chromalog
import logging


from datetime import datetime 
start_time = datetime.now() 

LOGGER = logging.getLogger('>>>main<<<')
chromalog.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
fh = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s - %(filename)s')
LOGGER.setLevel(logging.DEBUG)
file = ("/var/StatusClient/StatusAPI/logging.log")
fh = logging.FileHandler(file, encoding = "UTF-8")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(funcName)s')
fh.setFormatter(formatter)  
LOGGER.addHandler(fh)
LOGGER.addHandler(GelfUdpHandler(host='seq.tobiobst.de', port=12201, debug=True))

fhd = logging.FileHandler("/var/StatusClient/StatusAPI/logging.log", encoding = "UTF-8")
fhd.setLevel(logging.DEBUG)
LOGDAT = logging.getLogger('>>>logdata<<<')
LOGDAT.addHandler(fhd)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
fhd.setFormatter(formatter)  
LOGDAT.addHandler(fhd)  


def DiveraStatusCode(r):
    try:
        if str(r.status_code) == "403":
            LOGGER.error("[" + str(os.getpid()) + "] " + "Falscher Token!")
            LOGDAT.error("[" + str(os.getpid()) + "] " + "Falscher Token!")
    except Exception as ex:
        LOGGER.error(str(ex))
        LOGDAT.error(str(ex))

status = str(sys.argv[1])
url = str(sys.argv[2])
name = str(sys.argv[3])
token = str(sys.argv[4])
tokendb = token
try:

    try:
        r = requests.post(url, timeout = 60) 
        DiveraStatusCode(r)
        time_elapsed = datetime.now() - start_time 
        msg = (str(name) + " | Info: " + str(r.status_code) + " | Status: " + status + ' | Dauer: {}'.format(time_elapsed))
        LOGGER.debug("[" + str(os.getpid()) + "] " + "[Divera] " + token[0:10] + " " + msg)  
        LOGDAT.debug("[" + str(os.getpid()) + "] " + "[Divera] " + token[0:10] + " " + msg)

        jsondata = {
            "url" : url,
            "name" : name,
            "status" : status,
            "token" : token[0:10]
        }

        file = open("/var/StatusClient/StatusAPI/Divera.json", "a")
        file.write("\n" + str(jsondata))
        file.close()
            

        
    except Exception as ex:
        LOGGER.critical("[" + str(os.getpid()) + "] pid_StatusDivera" + "send divera " + str(ex)) 
        LOGDAT.critical("[" + str(os.getpid()) + "] pid_StatusDivera" + "send divera " + str(ex))
    

except Exception as ex:
    LOGGER.error("[" + str(os.getpid()) + "] pid_StatusDivera" + str(ex))
    LOGDAT.error("[" + str(os.getpid()) + "] pid_StatusDivera" + str(ex))