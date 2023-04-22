import time 
class Clock:
    
    def __init__(self, tick_size: float = 1.0, start_time: float = 0.0, end_time: float = 0.0):
        self._tick_size = tick_size
        self._tick_size = tick_size
        self._start_time = start_time
        self._end_time = end_time
        self._current_tick = start_time
        self._child_iterators = []

    def run(self):
        while True:
            now = time.time()

            # Sleep until the next tick
            next_tick_time = ((now // self._tick_size) + 1) * self._tick_size
            time.sleep(next_tick_time - now)
            self._current_tick = next_tick_time

            # Run through all the child iterators.
            for ci in self._child_iterators:
                child_iterator = ci
                # try:
                child_iterator.tick(self._current_tick)
                # except Exception as e:
                # print("[ERROR]: ","Unexpected error running clock tick.", e)

    def add_iterator(self, iterator):
        self._child_iterators.append(iterator)