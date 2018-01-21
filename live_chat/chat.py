#!usr/bin/python3

import socket
import time
import re

import irc_cfg as cfg

s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

connected = False
run = True

while run:
    response = s.recv(2048).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        #print('Pong')
    else:
        username = re.search(r"\w+", response).group(0)
        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

        message = CHAT_MSG.sub("", response).rstrip('\n')

        if 'End of /NAMES list' in message:
            connected = True
            print('Listening to ', cfg.CHAN)

        if connected == True:
            if 'End of /NAMES list' in message:
                pass
            else:
                print(username.title() + ':', message)

        #so we don't send messages too fast
        time.sleep(1 / cfg.RATE)
