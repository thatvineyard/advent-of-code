import multiprocessing
import time
from watchdog.observers import (
    Observer,
)
from watchdog.events import (
    FileSystemEventHandler,
    EVENT_TYPE_MODIFIED,
)



class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback, cooldown_seconds = 1):
        super().__init__()
        
        self._callback = callback
        self._cooldown_seconds = cooldown_seconds
        self.previous_trigger = time.time()
        self.current_thread: multiprocessing.Process | None = None

    def trigger(self):
        self._callback()

    def on_modified(self, event):
        if not event.is_directory and event.event_type == EVENT_TYPE_MODIFIED:
            if self.cooldown_expired():
                self.previous_trigger = time.time()
                print(f"File {event.src_path} has been modified!")
                self.trigger()

    def cooldown_expired(self):
        return time.time() > self.previous_trigger + self._cooldown_seconds

    # if self.current_thread:
    #     self.current_thread.terminate()
    # self.current_thread = multiprocessing.Process(target=on_change, args=())
    # print("Created thread")
    # self.current_thread.start()
    # print("Joining thread")
    # self.current_thread.join()

class Watcher:

    def __init__(self, watch_dir: str, on_change):
        self._watch_dir = watch_dir
        self._event_handler = FileChangeHandler(on_change)

    def start(self):
        print(f"👀 Starting to monitor files in {self._watch_dir}")
        Watcher.monitor_file_changes(self._watch_dir, self._event_handler)

    def monitor_file_changes(
        directory, event_handler: FileChangeHandler
    ):
        observer = Observer()
        observer.schedule(
            event_handler,
            path=directory,
            recursive=True,
        )
        observer.start()

        # manually trigger first
        event_handler.trigger()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

