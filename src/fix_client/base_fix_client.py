import quickfix as fix
import logging
from ..common.logger import setup_logger


class BaseFixClient(fix.Application):
    __SOH__ = chr(1)
    execID = 0

    def __init__(self, settings: dict):
        super().__init__()
        self._settings = settings
        setup_logger(**settings["logger"])
        self.logger = logging.getLogger(settings["logger"]["name"])
        self._ready = False
        self.create_timestamp = 0
        self.refresh_time = settings["refresh_time"]
        self._data_receive: list[dict] = []
        self._last_sent_order = -1
        self.print_verbose = settings["print_verbose"]

    @property
    def ready(self):
        return self._ready

    def onCreate(self, sessionID):
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        self._ready = True
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        print("Session (%s) logout !" % sessionID.toString())
        self._ready = False
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(BaseFixClient.__SOH__, "|")
        self.logger.info("(Admin) S >> %s" % msg)
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(BaseFixClient.__SOH__, "|")
        self.logger.info("(Admin) R << %s" % msg)
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(BaseFixClient.__SOH__, "|")
        self.logger.info("(App) S >> %s" % msg)
        return

    def fromApp(self, message, sessionID):
        msg = message.toString().replace(BaseFixClient.__SOH__, "|")
        self.logger.info("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)
