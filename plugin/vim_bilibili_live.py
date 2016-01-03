# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, division, absolute_import, print_function)

try:
    import vim
except ImportError:
    vim = object()

import socket
import sys
import struct
import json
import time

from threading import Thread, RLock

SERVER = 'livecmt.bilibili.com'


def info(*args):
    pass
    # now = datetime.datetime.now()
    # print datetime.datetime.strftime(now, '[%H:%M:%S]'), u' '.join(map(unicode, args))


class State(object):
    chat_id   = None
    connected = False
    reactor   = None
    username  = u'-'
    current   = u'-'
    online    = 0


class Heartbeat(Thread):
    daemon = True
    args = ()

    def run(self):
        sock, lock = self.args
        while True:
            with lock:
                try:
                    sock.sendall(struct.pack('>HH', 258, 4))
                except socket.error:
                    break

            time.sleep(30)


class Reactor(Thread):
    daemon = True
    socket = None

    def run(self):
        try:
            self.do_run()
        except socket.error:
            try:
                self.socket and self.socket.close()
            except:
                pass

            if State.reactor is self:
                print("vim-bilibili-live: Something's wrong, please reconnect!", file=sys.stderr)
        finally:
            if State.reactor is self:
                State.connected = False
                State.reactor = None

    def shutdown(self):
        self.socket and self.socket.close()
        State.reactor = None

    def do_run(self):
        assert State.chat_id
        State.connected = False
        State.reactor = self

        State.current = u'正在连接弹幕服务器...'
        lock = RLock()
        sock = socket.socket()
        self.socket = sock
        sock.connect((SERVER, 88))

        State.current = u'-'

        with lock:
            handshake = struct.pack('>HHII',
                257,  # Magic
                12,  # Length or something
                State.chat_id,
                1,  # Should be your user id, not supporting sending for now
            )

            sock.sendall(handshake)

        State.connected = True
        hb = Heartbeat(name='Heartbeat')
        hb.args = sock, lock
        hb.start()

        def recvall(n):
            # Helper function to recv n bytes or return None if EOF is hit
            data = []
            l = 0
            while l < n:
                packet = sock.recv(n - l)
                if not packet:
                    return b''.join(data)

                data.append(packet)
                l += len(packet)

            return b''.join(data)

        readshort = lambda: struct.unpack('>H', recvall(2))[0]
        readint = lambda: struct.unpack('>I', recvall(4))[0]
        read = recvall

        operations = {}

        def operation(code):
            def decorate(f):
                operations[code] = f
                return f

            return decorate

        @operation(1)
        def online():
            State.online = str(readint())

        @operation(2)
        @operation(4)
        def player_command():
            l = readshort() - 4
            data = read(l)
            assert len(data) == l

            pkt = json.loads(data)
            if pkt['cmd'] == 'DANMU_MSG':
                State.username, State.current = pkt['info'][2][1], pkt['info'][1]
            else:
                info('player_command', data)

        @operation(5)
        def player_broadcast():
            l = readshort() - 4
            data = read(l)
            info('player_broadcast', data)

        @operation(6)
        def new_scroll_message():
            l = readshort() - 4
            data = read(l)
            info('new_scroll_message', data)

        @operation(8)
        def call_player_action():
            op = readshort()
            info('call_player_action', op)

        while True:
            op = readshort()
            operations[op]()


def s(*texts):
    return [{'contents': unicode(s), 'highlight_groups': ['information:unimportant']} for s in texts]


def bilibili_live(pl):
    if not State.reactor:
        return None

    if not State.connected:
        if State.current:
            return s(State.current)
        else:
            return '???'

    return s(State.online, State.username, State.current)


def disconnect():
    if State.reactor:
        State.reactor.shutdown()


def connect(chat_id):
    try:
        State.chat_id = int(chat_id)
    except ValueError:
        print(u'Invalid chat_id', file=sys.stderr)
        return

    disconnect()

    Reactor(name='Reactor').start()

__all__ = [
    'bilibili_live',
    'disconnect',
    'connect',
]
