import sys
class StopCommand:
    def stop(self):
        self._initiator.stop()
        sys.exit()