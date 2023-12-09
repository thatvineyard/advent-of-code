import os
import subprocess
import sys
import time
from watchdog.observers import (
    Observer,
)
from watchdog.events import (
    FileSystemEventHandler,
    EVENT_TYPE_MODIFIED,
    FileModifiedEvent,
)
import multiprocessing
from libraries import cli, file_manager

watch_date = cli.get_date()


def on_change():
    subprocess.run(
        "py test.py",
    )


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.previous_trigger = time.time()
        self.current_thread: multiprocessing.Process | None = None

    def on_modified(
        self,
        event,
    ):
        if not event.is_directory and event.event_type == EVENT_TYPE_MODIFIED:
            if time.time() - self.previous_trigger > 1:
                self.previous_trigger = time.time()
                print(f"File {event.src_path} has been modified!")
                subprocess.run(
                    f"py {event.src_path}",
                )
                # if self.current_thread:
                #     self.current_thread.terminate()
                # self.current_thread = multiprocessing.Process(target=on_change, args=())
                # print("Created thread")
                # self.current_thread.start()
                # print("Joining thread")
                # self.current_thread.join()


def monitor_file_changes(
    directory,
):
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(
        event_handler,
        path=directory,
        recursive=True,
    )
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


monitor_file_changes(file_manager.get_date_dir(watch_date))
