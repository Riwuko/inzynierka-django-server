import urllib.request as req
import sys
import os
from html.parser import HTMLParser
import socketserver
import http.server
import socket
import threading
import random
import time
from EnvInterface import IEnvironment

connections = []


def handler(c, a, container, max_iter):
    global connections
    while True:
        data = c.recv(1024)
        print(data)
        if not data:
            connections.remove(c)
            c.close()
            break


def start_simulation(environment):
    environment.run_simulation()


def main():

    # Initialise data
    random.seed()
    port = 10201
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen(1)

    environment = IEnvironment()
    simulation_thread = threading.Thread(target=start_simulation, args=[environment])
    simulation_thread.daemon = True
    simulation_thread.start()

    while True:
        time.sleep(1)
        print(environment.get_humidity())

    while True:
        c, a = sock.accept()
        c_thread = threading.Thread(target=handler, args=(c, a, container, max_iter))
        c_thread.daemon = True
        c_thread.start()
        connections.append(c)
        print(connections)


if __name__ == "__main__":
    main()