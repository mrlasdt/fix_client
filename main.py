import yaml
import time
from src.command import commands


class MainApplication(*commands):
    def __init__(self, settings_path: str):
        with open(settings_path) as f:
            # use safe_load instead load
            self._settings = yaml.safe_load(f)
            self._start_time = time.time()
            self._max_run_time = self._settings['max_run_time']


if __name__ == "__main__":
    app = MainApplication(settings_path="config/settings.yml")
    app.warmup()

    try:
        app.start()
    except Exception as e:
        print("[ERROR] %s" % e)
        app.stop()
    finally:
        app.stop()
