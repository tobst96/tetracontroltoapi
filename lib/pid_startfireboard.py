import logging, chromalog, sys, subprocess, configparser, os

from pygelf import GelfUdpHandler

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

class sendStatusToFireboard:

    def __init__(self, issi, status, name):   
        self.issi = issi
        self.status = status
        self.name = name
        LOGGER.info("[" + str(os.getpid()) + "] " + "[Fireboard] Prüfe senden: " + self.name + " | " + self.status + " | " + self.issi)
        self.readConfig()
        self.searchToken()

    def readConfig(self):
        try:
            self.config = configparser.ConfigParser(interpolation=None)
            file = f"/var/StatusClient/config/config.ini"
            self.config.read(file, encoding='utf-8')
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))


    def searchToken(self):
            try:
                self.path_items = self.config.items("Fireboard")
                for key, token in self.path_items: 
                    if token != "Kann belibig erweitert werden. Token Nummer nur erhöhen":
                        self.token = token
                        self.loadFireboard()
            except Exception as ex:
                LOGGER.error(str(ex))
                LOGDAT.error(str(ex))

    def loadFireboard(self):
        try:
            subprocess.Popen(["python3", "/var/StatusClient/lib/pid_statusfireboard.py", self.status, self.issi, self.name, self.token], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as ex:
            LOGGER.error(str(ex))
            LOGDAT.error(str(ex))

sendStatusToFireboard(status = sys.argv[1], issi = sys.argv[2], name = sys.argv[3])