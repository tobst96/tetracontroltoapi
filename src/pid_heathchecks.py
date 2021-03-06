from error import erroradd
import subprocess, sys
from safe import tosafe
import requests
from notifymydevice import NotifyMyDevice
from createconfig import createConfigFile
from logfunc import init_logging, loggingdatei
from tetracontrolstatus import TetraControlStatus
import logging, socket
from FeuerSoftVehicle import FeuerSoftVehicle
import schedule, time, configparser, ctypes
from pygelf import GelfUdpHandler
import logging, chromalog, subprocess
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
LOGGER.addHandler(GelfUdpHandler(host='https://seq.tobiobst.de', port=12201))

fhd = logging.FileHandler("/var/StatusClient/StatusAPI/logging.log", encoding = "UTF-8")
fhd.setLevel(logging.DEBUG)
LOGDAT = logging.getLogger('>>>logdata<<<')
LOGDAT.addHandler(fhd)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
fhd.setFormatter(formatter)  
LOGDAT.addHandler(fhd)  

try:        
    config = configparser.ConfigParser(interpolation=None)
    file = f"/var/StatusClient/config/config.ini"
    config.read(file, encoding='utf-8')
    uuidhc = config.get("Monitoring","URL")
    if uuidhc == "" or uuidhc == None:
        LOGGER.debug("Kein Monitoring eingerichtet. https://healthchecks.io")
    else:
        LOGGER.debug("Monitoring ..")
        url = uuidhc
        response = requests.get(url)
        if response.status_code == 200:
            LOGGER.info("Monitoring erfolgreich")
        else:
            LOGGER.error("Monitoring fehlgeschlagen")


except requests.RequestException as e:
    # Log ping failure here...
    LOGGER.error("Ping failed: %s" % e)  

