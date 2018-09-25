# This module should be imported from REPL, not run from command line.
import socket
import uos
import network
import websocket
import websocket_helper
import _webrepl


class WebREPL():
    listen_s = None
    client_s = None
    ws = None

    @classmethod
    def setup_conn(cls,port, accept_handler):
        cls.listen_s = socket.socket()
        cls.listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        ai = socket.getaddrinfo("0.0.0.0", port)
        addr = ai[0][4]

        cls.listen_s.bind(addr)
        cls.listen_s.listen(1)
        if accept_handler:
            cls.listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
        for i in (network.AP_IF, network.STA_IF):
            iface = network.WLAN(i)
            if iface.active():
                print("WebREPL daemon started on cls.ws://%s:%d" % (iface.ifconfig()[0], port))
        return cls.listen_s

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
        cls.client_s = cl
        websocket_helper.server_handshake(cl)
        cls.ws = websocket.websocket(cl, True)
        cls.ws = _webrepl._webrepl(cls.ws)
        cl.setblocking(False)
        # notify REPL on socket incoming data
        cl.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)
        uos.dupterm(cls.ws)
        

    @classmethod
    def stop(cls):
        uos.dupterm(None)
        if cls.client_s:
            cls.client_s.close()
        if cls.listen_s:
            cls.listen_s.close()

    @classmethod
    def start(cls,port=8266, password=None):
        cls.stop()
        if password is None:
            try:
                import webrepl_cfg
                _webrepl.password(webrepl_cfg.PASS)
                cls.setup_conn(port, cls.accept_conn)
                print("Started webrepl in normal mode")
            except:
                print("WebREPL is not configured, run 'import webrepl_setup'")
        else:
            _webrepl.password(password)
            cls.setup_conn(port, cls.accept_conn)
            print("Started webrepl in manual override mode")

    @classmethod
    def start_foreground(cls,port=8266):
        cls.stop()
        s = cls.setup_conn(port, None)
        cls.accept_conn(s)
