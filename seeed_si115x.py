#!/usr/bin/python3
# -*- coding:utf-8 -*-
from grove.i2c import Bus
import logging
import time
import signal
import ctypes
#Registers,Parameters and commands

# commands

DEVICE_ADDRESS = 0x53
SI114X_QUERY = 0x80
SI114X_SET = 0xA0
SI114X_NOP = 0x0
SI114X_RESET    = 0x01
SI114X_BUSADDR    = 0x02
SI114X_PS_FORCE    = 0x05
SI114X_GET_CAL    = 0x12
SI114X_ALS_FORCE    = 0x06
SI114X_PSALS_FORCE    = 0x07
SI114X_PS_PAUSE    = 0x09
SI114X_ALS_PAUSE    = 0x0A
SI114X_PSALS_PAUSE    = 0xB
SI114X_PS_AUTO    = 0x0D
SI114X_ALS_AUTO   = 0x0E
SI114X_PSALS_AUTO = 0x0F

# IIC REGISTERS

############################

RESET_CMD_CTR = 0x00
RESET_SW = 0x01
FORCE = 0x11
PAUSE = 0x12
START = 0x13

PART_ID = 0x00
REV_ID = 0x01
MFR_ID = 0x02
INFO_0 = 0x03
INFO_1 = 0x04
HOSTIN_3 = 0x07
HOSTIN_2 = 0x08
HOSTIN_0 = 0x0A
COMMAND = 0x0B
IRQ_ENABLE = 0x0F
RESPONSE_0 = 0x11
RESPONSE_1 = 0x10

IRQ_STATUS = 0x12
HOSTOUT_0 = 0x13
HOSTOUT_1 = 0x14
HOSTOUT_2 = 0x15
HOSTOUT_3 = 0x16
HOSTOUT_4 = 0x17
HOSTOUT_5 = 0x18
HOSTOUT_6 = 0x19
HOSTOUT_7 = 0x1A
HOSTOUT_8 = 0x1B
HOSTOUT_9 = 0x1C
HOSTOUT_10 = 0x1D
HOSTOUT_11 = 0x1E
HOSTOUT_12 = 0x1F
HOSTOUT_13 = 0x20
HOSTOUT_14 = 0x21
HOSTOUT_15 = 0x22
HOSTOUT_16 = 0x23
HOSTOUT_17 = 0x24
HOSTOUT_18 = 0x25
HOSTOUT_19 = 0x26
HOSTOUT_20 = 0x27
HOSTOUT_21 = 0x28
HOSTOUT_22 = 0x29
HOSTOUT_23 = 0x2A
HOSTOUT_24 = 0x2B
HOSTOUT_25 = 0x2C

I2C_ADDR = 0x00
CHAN_LIST = 0x01
ADCCONFIG_0 = 0x02
ADCSENS_0 = 0x03
ADCPOST_0 = 0x04
MEASCONFIG_0 = 0x05

ADCCONFIG_1 = 0x06
ADCSENS_1 = 0x07
ADCPOST_1 = 0x08
MEASCONFIG_1 = 0x09
ADCCONFIG_2 = 0x0A
ADCSENS_2 = 0x0B
ADCPOST_2 = 0x0C
MEASCONFIG_2 = 0x0D
ADCCONFIG_3 = 0x0E
ADCSENS_3 = 0x0F
ADCPOST_3 = 0x10
MEASCONFIG_3 = 0x11
ADCCONFIG_4 = 0x12
ADCSENS_4 = 0x13
ADCPOST_4 = 0x14
MEASCONFIG_4 = 0x15
ADCCONFIG_5 = 0x16
ADCSENS_5 = 0x17
ADCPOST_5 = 0x18
MEASCONFIG_5 = 0x19

MEASRATE_H = 0x1A
MEASRATE_L = 0x1B
MEASCOUNT_0 = 0x1C
MEASCOUNT_1 = 0x1D
MEASCOUNT_2 = 0x1E

LED1_A = 0x1F
LED1_B = 0x20
LED2_A = 0x21
LED2_B = 0x22
LED3_A = 0x23
LED3_B = 0x24
THRESHOLD0_H = 0x25
THRESHOLD0_L = 0x26
THRESHOLD1_H = 0x27
THRESHOLD1_L = 0x28
THRESHOLD2_H = 0x29
THRESHOLD2_L = 0x2A
BURST = 0x2B

############################



class grove_si115x(object):
    def __init__(self,address = 0x53):
        self.bus = Bus()
        self.addr = address
        self._logger = logging.getLogger('grove_si115x')
        assert self.Begin() , "Please check if the I2C device insert in I2C of Base Hat"
    def __exit__(self):
        self.bus.close()
    #Init the si1151 and begin to collect data
    def Begin(self):
        if self._ReadByte(PART_ID) != 0X51:
            return False
        self.send_command(START)
        self.param_set(CHAN_LIST, 0B000010)
        self.param_set(MEASRATE_H, 0)
        self.param_set(MEASRATE_L, 1)
        self.param_set(MEASCOUNT_0, 5)
        self.param_set(MEASCOUNT_1, 10)
        self.param_set(MEASCOUNT_2, 10)
        self.param_set(THRESHOLD0_L, 200)
        self.param_set(THRESHOLD0_H, 0)
        try:
            self.bus.write_byte_data(self.addr,IRQ_ENABLE,0B000010)
        except OSError:
            raise OSError("Please check if the I2C device insert in I2C of Base Hat")

        conf_1 = [0B00000000,0B00000010,0B00000001,0B11000001]

        self.param_set(ADCCONFIG_0 + 1, conf_1[0])
        self.param_set(ADCSENS_0 + 1, conf_1[1])
        self.param_set(ADCPOST_0 + 1, conf_1[2])
        self.param_set(MEASCONFIG_0 + 1, conf_1[3])

        self.param_set(ADCCONFIG_0 + 3, conf_1[0])
        self.param_set(ADCSENS_0 + 3, conf_1[1])
        self.param_set(ADCPOST_0 + 3, conf_1[2])
        self.param_set(MEASCONFIG_0 + 3, conf_1[3])

        return True
    #reset the si1151
    #inclue IRQ reg, command regs...

##############################################################
    def send_command(self,code):
        while True:
            cmmnd_ctr = self.read_register(RESPONSE_0,1)
            self.write_data(COMMAND, code)
            self.read_register(RESPONSE_0,1)
            r = self.read_register(RESPONSE_0,1)
            if(r > cmmnd_ctr):
                break

    def write_data(self,Reg,Value):
        try:
            self.bus.write_byte_data(self.addr,Reg,Value)    
        except OSError:
            raise OSError("Please check if the I2C device insert in I2C of Base Hat")

    def read_register(self,Reg,Value):
        try:
            read_data = self.bus.read_i2c_block_data(self.addr,Reg,Value)
        except OSError:
            raise  OSError("Please check if the I2C device insert in I2C of Base Hat")
        return read_data

    def param_set(self,loc,val):
        register_P2 = loc | (0B10 << 6)
        while True:
            cmmnd_ctr = self.read_register(RESPONSE_0,1)
            self.write_data(HOSTIN_0, val)
            self.write_data(COMMAND, register_P2)
            r = self.read_register(RESPONSE_0,1)
            if(r > cmmnd_ctr):
                break

    def ReadHalfWord(self):
        self.send_command(FORCE)
        data0 = self.read_register(HOSTOUT_0,1)
        data1 = self.read_register(HOSTOUT_1,1)
        data3 =  (194 - data0[0]) * 256 + abs((230 - data1[0]))
        return abs(data3)

    def ReadHalfWord_UV(self):
        self.send_command(FORCE)
        data0 = self.read_register(HOSTOUT_0,1)
        data1 = self.read_register(HOSTOUT_1,1)
        data3 =  (194 - data0[0]) * 256 + abs((230 - data1[0]))
        return abs((194 - data0[0])/10)

    def ReadHalfWord_VISIBLE(self):
        self.send_command(FORCE)
        data0 = self.read_register(HOSTOUT_0,1)
        data1 = self.read_register(HOSTOUT_1,1)
        data3 =  (194 - data0[0]) * 256 + abs((230 - data1[0]))
        return abs(data3/3)




##############################################################

    # read 8 bit data from Reg
    def _ReadByte(self,Reg):
        try:
            read_data = self.bus.read_byte_data(self.addr,Reg)
        except OSError:
            raise  OSError("Please check if the I2C device insert in I2C of Base Hat")
        return read_data


def handler(signalnum, handler):
    print("Please use Ctrl C to quit")
def main():
    signal.signal(signal.SIGTSTP, handler) # Ctrl-z
    signal.signal(signal.SIGQUIT, handler) # Ctrl-\
    SI1151 = grove_si115x()
    print("Please use Ctrl C to quit")
    while True:
        print('Visible %03d  UV %.2f  IR %03d' % (SI1151.ReadHalfWord_VISIBLE(), SI1151.ReadHalfWord_UV(), SI1151.ReadHalfWord()),end=" ")
        print('\r', end='')
        time.sleep(0.5)

if __name__ == "__main__":
    main()     
    