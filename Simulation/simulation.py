import sys
import os
import socket
import threading
import random
import time
from EnvInterface import IEnvironment


def start_simulation(environment):
    environment.run_simulation()


def main():
    environment = IEnvironment()
    simulation_thread = threading.Thread(target=start_simulation, args=[environment])
    simulation_thread.daemon = True
    simulation_thread.start()

    while True:
        time.sleep(1)
        print(environment.get_humidity())


if __name__ == "__main__":
    main()