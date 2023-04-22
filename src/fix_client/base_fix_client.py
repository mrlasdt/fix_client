import quickfix as fix
import logging
from ..common.logger import setup_logger
__SOH__ = chr(1)
class BaseFixClient(fix.Application):
    """FIX Application"""
    execID = 0
    def __init__(self, logger_name:str, log_file_path:str):
        super().__init__()
        setup_logger(logger_name, log_file_path)
        self.logger = logging.getLogger(logger_name)

    def onCreate(self, sessionID):
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        self.ready=True
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        print("Session (%s) logout !" % sessionID.toString())
        self.ready=False
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info("(Admin) S >> %s" % msg)
        return
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info("(Admin) R << %s" % msg)
        return
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info("(App) S >> %s" % msg)
        return
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.logger.info("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

