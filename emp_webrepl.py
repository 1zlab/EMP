import socket
import json
import uos
import gc
import network
import websocket
import websocket_helper
import _webrepl
from emp_utils import rainbow


class WebREPL():
    _instance = None

    @classmethod
    def send(cls,json_data):
        WebREPL().ws.write(json_data)



    def __new__(cls):
        if not cls._instance:
            cls._instance = super(WebREPL, cls).__new__(cls)
            cls._instance.ws = None
            cls._instance.listen_s = None
            cls._instance.client_s = None
            cls._instance.wr = None
        return cls._instance

    @classmethod
    def setup_conn(cls,port, accept_handler):
        WebREPL().listen_s = socket.socket()
        WebREPL().listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        ai = socket.getaddrinfo("0.0.0.0", port)
        addr = ai[0][4]

        WebREPL().listen_s.bind(addr)
        WebREPL().listen_s.listen(1)
        if accept_handler:
            WebREPL().listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
        for i in (network.AP_IF, network.STA_IF):
            iface = network.WLAN(i)
            if iface.active():
                print(rainbow("WebREPL daemon started on ws://%s:%d" % (iface.ifconfig()[0], port), color='green'))
        return WebREPL().listen_s

    @classmethod
    def accept_conn(cls,listen_sock):

        cl, remote_addr = listen_sock.accept()
        prev = uos.dupterm(None)
        uos.dupterm(prev)
        if prev:
            print("\nConcurrent WebREPL connection from", remote_addr, "rejected")
            cl.close()
            return
        print("\nWebREPL connection from:", remote_addr)
        WebREPL().client_s = cl
        websocket_helper.server_handshake(cl)
        WebREPL().ws = websocket.websocket(cl, True)

        WebREPL().wr = _webrepl._webrepl(WebREPL().ws)
        type(WebREPL().wr)
        cl.setblocking(False)
        # notify REPL on socket incoming data
        cl.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)
        uos.dupterm(WebREPL().wr)
        

    @classmethod
    def stop(cls):
        uos.dupterm(None)
        if WebREPL().client_s:
            WebREPL().client_s.close()
        if WebREPL().listen_s:
            WebREPL().listen_s.close()

    @classmethod
    def start(cls,port=8266, password=None):
        WebREPL().stop()
        if password is None:
            try:
                import webrepl_cfg
                _webrepl.password(webrepl_cfg.PASS)
                WebREPL().setup_conn(port, WebREPL().accept_conn)
                print("Started webrepl in normal mode")
            except:
                print("WebREPL is not configured, run 'import webrepl_setup'")
        else:
            _webrepl.password(password)
            WebREPL().setup_conn(port, WebREPL().accept_conn)
            print(rainbow("WebREPL started.", color='green'))

    @classmethod
    def start_foreground(cls,port=8266):
        WebREPL().stop()
        s = WebREPL().setup_conn(port, None)
        WebREPL().accept_conn(s)



def emp_sender(func):
    def wrapper(*args, **kwargs):     
        rsp = dict(func=func.__name__, data=func(*args, **kwargs))
        WebREPL.send(json.dumps(rsp) + '\n\r')
        gc.collect()
    return wrapper
