import threading
import socket

class ResponseThread(threading.Thread):
    def __init__(self, src, dest):
        super(ResponseThread, self).__init__()
        self.src = src
        self.dest = dest

    def run(self):
        while True:
            try:
                data = self.src.recv(4096)
                print "Response:", data
                if not data:
                    break
                self.dest.send(data)
            except:
                import traceback
                print traceback.format_exc()
                break
                
class RequestThread(threading.Thread):
    def __init__(self, src):
        super(RequestThread, self).__init__()
        self.src = src

    def run(self):
        headerParts = []
        dataParts = []
        while True:
            data = self.src.recv(4096)
            print "Request:", data
            if not data:
                break
            parts = data.split("\r\n\r\n")
            headerParts.append(parts[0])
            dataParts.append(data)
            if len(parts) > 1:
                break
        headers = "".join(headerParts)
        headers = headers.split("\r\n")
        protocol = headers[0].split()[0].lower().strip()
        if protocol not in ('get', 'post', 'connect'):
            print "Unknown protocol: %s" % protocol


        headerDict = {}
        for i in headers[1:]:
            parts = i.split(":")
            if len(parts) > 1:
                headerDict[parts[0].strip()] = ":".join(parts[1:])

        host = headerDict.get("Host", None)
        if not host:
            raise RuntimeError, "Host not found"
        print "Host:", host

        dest = socket.socket()
        if ":" in host:
            dest.connect((host.split(":")[0], int(host.split(":")[1])))
        else:
            dest.connect((host, 80))


        for i in dataParts:
            dest.send(i)

        r = ResponseThread(dest, src)
        r.start()

        while True:
            data = self.src.recv(4096)
            if not data:
                break
            dest.send(data)
        self.src.close()
        dest.close()
        r.join()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 60000))
    s.listen(5)
    while True:
        src, address = s.accept()
        r = RequestThread(src)
        r.start()
