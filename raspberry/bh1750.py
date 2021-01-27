import smbus
import time

DEVICE = 0x23

ONE_TIME_HIGH_RES_MODE_1 = 0x20

bus = smbus.SMBus(1)

def convertToNumber(data):
    result=(data[1] + (256 * data[0])) / 1.2
    return (result)

def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

def main():

    while True:
        lightLevel=readLight()
        print("Light Level : " + format(lightLevel,'.2f') + " lx")
        time.sleep(0.5)

if __name__=="__main__":
     main()
