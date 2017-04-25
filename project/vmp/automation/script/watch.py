from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import socket
import sys
import difflib
import tempfile
import json


class TemuHandler(FileSystemEventHandler):

    def __init__(self, server_IP="127.0.0.1", server_port=10001, hash_value=""):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)
            self.hash_value = hash_value
            self.sock.connect((server_IP, server_port))
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(1)

    def on_created(self, event):
        if ".hooklog" in event.src_path:
            print("hooklog created: " + event.src_path)
            # self.sock.sendall(event.src_path)
            self.tmp = tempfile.TemporaryFile()

    def on_modified(self, event):
        if ".hooklog" in event.src_path:
            print("modified: " + event.src_path)
            # compare
            with open(event.src_path, "r") as temu_hooklog:
                diff = difflib.unified_diff(self.tmp.readlines(), temu_hooklog.readlines(), fromfile='file1',
                                            tofile='file2')
                lines = list(diff)[2:]
                added = [line[1:] for line in lines if line[0] == '+']
                process_id = event.src_path.split("_")[1].split(".")[0]
                if added:
                    data = ''.join(added)
                    data_size = 512
                    while data:
                        send_message = {'sample_hash': self.hash_value, "process_id": process_id, "data": data[0:data_size-1]}
                        self.sock.sendall(json.dumps(send_message))
                        time.sleep(0.5)
                        data = data[data_size:]

                    # update tmp
                    temu_hooklog.seek(0)
                    self.tmp.seek(0)
                    self.tmp.write(temu_hooklog.read())
                    self.tmp.seek(0)

    def on_moved(self, event):
        if ".hooklog" in event.src_path:
            self.sock.close()
            self.tmp.close()


path = "/home/root"
print sys.argv
event_handler = TemuHandler(sys.argv[2], int(sys.argv[3]), sys.argv[1])

observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
