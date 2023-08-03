#!/usr/bin/python3
# -*- coding:utf-8 -*-
from grove.i2c import Bus
from enum import IntEnum
import logging
import time
import signal


class I2C_ADDR(IntEnum):
    SI114X = 0x60

class SI114X_REG(IntEnum):
    PART_ID = 0x00
    REV_ID = 0x01
    SEQ_ID = 0x02
    INT_CFG = 0x03
    IRQ_ENABLE = 0x04
    IRQ_MODE1 = 0x05
    IRQ_MODE2 = 0x06
    HW_KEY = 0x07
    MEAS_RATE0 = 0x08
    MEAS_RATE1 = 0x09
    PS_RATE = 0x0A
    PS_LED21 = 0x0F
    PS_LED3 = 0x10
    UCOEFF0 = 0x13
    UCOEFF1 = 0x14
    UCOEFF2 = 0x15
    UCOEFF3 = 0x16
    WR = 0x17
    COMMAND = 0x18
    RESPONSE = 0x20
    IRQ_STATUS = 0x21
    ALS_VIS_DATA0 = 0x22
    ALS_VIS_DATA1 = 0x23
    ALS_IR_DATA0 = 0x24
    ALS_IR_DATA1 = 0x25
    PS1_DATA0 = 0x26
    PS1_DATA1 = 0x27
    PS2_DATA0 = 0x28
    PS2_DATA1 = 0x29
    PS3_DATA0 = 0x2A
    PS3_DATA1 = 0x2B
    AUX_DATA0_UVINDEX0 = 0x2C
    AUX_DATA1_UVINDEX1 = 0x2D
    RD = 0x2E
    CHIP_STAT = 0x30


class SI114X_CMD(IntEnum):
    NOP = 0x00
    RESET = 0x01
    BUSADDR = 0x02
    PS_FORCE = 0x05
    ALS_FORCE = 0x06
    PSALS_FORCE = 0x07
    PS_PAUSE = 0x09
    ALS_PAUSE = 0x0A
    PSALS_PAUSE = 0x0B
    PS_AUTO = 0x0D
    ALS_AUTO = 0x0E
    PSALS_AUTO = 0x0F
    QUERY = 0x80
    SET = 0xA0


class SI114X_PARAM(IntEnum):
    I2CADDR = 0x00
    CHLIST = 0x01
    PSLED12_SELECT = 0x02
    PSLED3_SELECT = 0x03
    PS_ENCODING = 0x05
    ALS_ENCODING = 0x06
    PS1_ADCMUX = 0x07
    PS2_ADCMUX = 0x08
    PS3_ADCMUX = 0x09
    PS_ADC_COUNTER = 0x0A
    PS_ADC_GAIN = 0x0B
    PS_ADC_MISC = 0x0C
    ALS_IR_ADCMUX = 0x0E
    AUX_ADCMUX = 0x0F
    ALS_VIS_ADC_COUNTER = 0x10
    ALS_VIS_ADC_GAIN = 0x11
    ALS_VIS_ADC_MISC = 0x12
    LED_REC = 0x1C
    ALS_IR_ADC_COUNTER = 0x1D
    ALS_IR_ADC_GAIN = 0x1E
    ALS_IR_ADC_MISC = 0x1F


class SI114X_CHLIST(IntEnum):
    ENPS1 = 0x01
    ENPS2 = 0x02
    ENPS3 = 0x04
    ENALSVIS = 0x10
    ENALSIR = 0x20
    ENAUX = 0x40
    ENUV = 0x80

#USER SETTINGS DEFINE

class SI114X_ADCMUX(IntEnum):
    SMALL_IR = 0x00
    VISIABLE = 0x02
    LARGE_IR = 0x03
    NO = 0x06
    GND = 0x25
    TEMPERATURE = 0x65
    VDD = 0x75

class SI114X_LED_SEL(IntEnum):
    PS1_NONE = 0x00
    PS1_LED1 = 0x01
    PS1_LED2 = 0x02
    PS1_LED3 = 0x04
    PS2_NONE = 0x00
    PS2_LED1 = 0x10
    PS2_LED2 = 0x20
    PS2_LED3 = 0x40

class SI114X_ADC_GAIN(IntEnum):
    DIV1 = 0x00
    DIV2 = 0x01
    DIV4 = 0x02
    DIV8 = 0x03
    DIV16 = 0x04
    DIV32 = 0x05

class SI114X_LED_CURRENT(IntEnum):
    CUR5MA = 0x01
    CUR11MA = 0x02
    CUR22MA = 0x03
    CUR45MA = 0x04

#Recovery period the  ADC takes before making a PS measurement
class SI114X_ADC_COUNTER(IntEnum):
    ADCCLK1 = 0x00
    ADCCLK7 = 0x01
    ADCCLK15 = 0x02
    ADCCLK31 = 0x03
    ADCCLK63 = 0x04
    ADCCLK127 = 0x05
    ADCCLK255 = 0x06
    ADCCLK511 = 0x07

class SI114X_ADC_MISC(IntEnum):
    LOWRANGE = 0x00
    HIGHRANGE = 0x20
    ADC_NORMALPROXIMITY = 0x00
    ADC_RAWADC = 0x04

#IRQ ENABLE
class SI114X_IRQEN(IntEnum):
    ALS = 0x01
    PS1 = 0x04
    PS2 = 0x08
    PS3 = 0x10


class grove_si114x(object):
    def __init__(self,address = I2C_ADDR.SI114X):
        self.bus = Bus()
        self.addr = address
        self._logger = logging.getLogger('grove_si114x')
        assert self.Begin() , "Please check if the I2C device insert in I2C of Base Hat"
    def __del__(self):
        self._WriteByte(SI114X_REG.COMMAND, SI114X_CMD.RESET)
        time.sleep(0.1)
        self.bus.close()
    def __exit__(self):
        self.bus.close()
    #Init the si114x and begin to collect data
    def Begin(self):
        if self._ReadByte(SI114X_REG.PART_ID) != 0X45:
            return False
        self.Reset()
        #INIT
        self.DeInit()
        return True
    #reset the si114x
    #inclue IRQ reg, command regs...
    def Reset(self):
        self._WriteByte(SI114X_REG.MEAS_RATE0, 0)
        self._WriteByte(SI114X_REG.MEAS_RATE1, 0)
        self._WriteByte(SI114X_REG.IRQ_ENABLE, 0)
        self._WriteByte(SI114X_REG.IRQ_MODE1, 0)
        self._WriteByte(SI114X_REG.IRQ_MODE2, 0)
        self._WriteByte(SI114X_REG.INT_CFG, 0)
        self._WriteByte(SI114X_REG.IRQ_STATUS, 0xFF)
        self._WriteByte(SI114X_REG.COMMAND, SI114X_CMD.RESET)
        time.sleep(0.1)
        self._WriteByte(SI114X_REG.HW_KEY, 0x17)
        time.sleep(0.1)  

    #default init  
    def DeInit(self):
        #ENABLE UV reading
        #these reg must be set to the fixed value
        self._WriteByte(SI114X_REG.UCOEFF0, 0x29)
        self._WriteByte(SI114X_REG.UCOEFF1, 0x89)
        self._WriteByte(SI114X_REG.UCOEFF2, 0x02)
        self._WriteByte(SI114X_REG.UCOEFF3, 0x00)
        self.WriteParamData(SI114X_PARAM.CHLIST, SI114X_CHLIST.ENUV | SI114X_CHLIST.ENALSIR | SI114X_CHLIST.ENALSVIS |
                    SI114X_CHLIST.ENPS1)
        #set LED1 CURRENT(22.4mA)(It is a normal value for many LED)
        self.WriteParamData(SI114X_PARAM.PS1_ADCMUX, SI114X_ADCMUX.LARGE_IR)
        self._WriteByte(SI114X_REG.PS_LED21, SI114X_LED_CURRENT.CUR22MA)
        self.WriteParamData(SI114X_PARAM.PSLED12_SELECT, SI114X_LED_SEL.PS1_LED1)
        #PS ADC SETTING
        self.WriteParamData(SI114X_PARAM.PS_ADC_GAIN, SI114X_ADC_GAIN.DIV1)
        self.WriteParamData(SI114X_PARAM.PS_ADC_COUNTER, SI114X_ADC_COUNTER.ADCCLK511)
        self.WriteParamData(SI114X_PARAM.PS_ADC_MISC, SI114X_ADC_MISC.HIGHRANGE | SI114X_ADC_MISC.ADC_RAWADC)
        #VIS ADC SETTING
        self.WriteParamData(SI114X_PARAM.ALS_VIS_ADC_GAIN, SI114X_ADC_GAIN.DIV1)
        self.WriteParamData(SI114X_PARAM.ALS_VIS_ADC_COUNTER, SI114X_ADC_COUNTER.ADCCLK511)
        self.WriteParamData(SI114X_PARAM.ALS_VIS_ADC_MISC, SI114X_ADC_MISC.HIGHRANGE)
        #IR ADC SETTING
        self.WriteParamData(SI114X_PARAM.ALS_IR_ADC_GAIN, SI114X_ADC_GAIN.DIV1)
        self.WriteParamData(SI114X_PARAM.ALS_IR_ADC_COUNTER, SI114X_ADC_COUNTER.ADCCLK511)
        self.WriteParamData(SI114X_PARAM.ALS_IR_ADC_MISC, SI114X_ADC_MISC.HIGHRANGE)
        #interrupt enable
        self._WriteByte(SI114X_REG.INT_CFG, 1)
        self._WriteByte(SI114X_REG.IRQ_ENABLE, SI114X_IRQEN.ALS)
        #AUTO RUN
        self._WriteByte(SI114X_REG.MEAS_RATE0, 0xFF)
        self._WriteByte(SI114X_REG.COMMAND, SI114X_CMD.PSALS_AUTO)

    #read param data
    def ReadParamData(self,Reg):
        self._WriteByte(SI114X_REG.COMMAND, Reg | SI114X_CMD.QUERY)
        return self._ReadByte(SI114X_CMD.RD)

    #writ param data
    def WriteParamData(self,Reg,Value):
        #write Value into PARAMWR reg first
        self._WriteByte(SI114X_REG.WR, Value)
        self._WriteByte(SI114X_REG.COMMAND, Reg | SI114X_CMD.SET)
        #SI114X writes value out to PARAM_RD,read and confirm its right
        return self._ReadByte(SI114X_REG.RD)

    #Read Visible Value
    @property
    def ReadVisible(self):
        return self._ReadHalfWord(SI114X_REG.ALS_VIS_DATA0)

    #Read IR Value    
    @property
    def ReadIR(self):
        return self._ReadHalfWord(SI114X_REG.ALS_IR_DATA0)

    #Read UV Value
    #this function is a int value ,but the real value must be div 100
    @property
    def ReadUV(self):
        return self._ReadHalfWord(SI114X_REG.AUX_DATA0_UVINDEX0)
    
    #Read Proximity Value
    def ReadProximity(self,PSn):
         return self._ReadHalfWord(PSn)

    # read 8 bit data from Reg
    def _ReadByte(self,Reg):
        try:
            read_data = self.bus.read_byte_data(self.addr,Reg)
        except OSError:
            raise  OSError("Please check if the I2C device insert in I2C of Base Hat")
        return read_data

    # Write 8 bit data to Reg
    def _WriteByte(self,Reg,Value):
        try:
            self.bus.write_byte_data(self.addr,Reg,Value)
        except OSError:
            raise OSError("Please check if the I2C device insert in I2C of Base Hat")

    # read 16 bit data from Reg
    def _ReadHalfWord(self,Reg):
        try:
            block = self.bus.read_i2c_block_data(self.addr,Reg, 2)
        except OSError:
            raise OSError("Please check if the I2C device insert in I2C of Base Hat")
        read_data = (block[0] & 0xff) | (block[1] << 8)
        return read_data   
def handler(signalnum, handler):
    print("Please use Ctrl C to quit")
def main():
    signal.signal(signal.SIGTSTP, handler) # Ctrl-z
    signal.signal(signal.SIGQUIT, handler) # Ctrl-\
    SI1145 = grove_si114x()
    print("Please use Ctrl C to quit")
    while True:
        print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible , SI1145.ReadUV/100 , SI1145.ReadIR),end=" ")
        print('\r', end='')
        time.sleep(0.5)

if __name__ == "__main__":
    main()     
    