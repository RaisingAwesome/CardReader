# Web Server
# 2021 - Sean J. Miller
#!/usr/bin/python3

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import os.path

def GetPage(the_file):
    PAGE=""
    with open('/home/pi/CardReader/' + the_file) as f:
        PAGE = f.read()
        f.close
    return PAGE

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index')
            self.end_headers()
        elif self.path == '/index':
            PAGE=GetPage('index.html').replace('<DYNAMIC/>','<strong>This is content dynamically inserted in the static index.html file.</strong>')
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=UTF-8')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/download':
            PAGE=GetPage('download.html').replace('<DYNAMIC/>','')
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=UTF-8')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                #logging.warning(
                #    'Removed streaming client %s: %s',
                #    self.client_address, str(e))
                pass

        elif self.path == '/still.jpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                self.wfile.write(b'--FRAME\r\n')
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', len(frame))
                self.end_headers()
                self.wfile.write(frame)
                self.wfile.write(b'\r\n')
            except Exception as e:
                pass

        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

#with picamera.PiCamera(resolution='2592x1944', framerate=15) as camera:
#    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
#    camera.rotation = 180
#    camera.start_recording(output, format='mjpeg')
try:
        address = ('', 80) #Port 80 requires running python3 with sudo
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
finally:
#        camera.stop_recording()
        quit()

