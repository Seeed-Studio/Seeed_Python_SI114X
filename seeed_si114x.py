#!/usr/bin/python3
# -*- coding:utf-8 -*-
from grove.i2c import Bus
import logging
import time
import signal
#Registers,Parameters and commands

# commands

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

SI114X_PART_ID  = 0x00
SI114X_REV_ID  = 0x01
SI114X_SEQ_ID  = 0x02
SI114X_INT_CFG  = 0x03
SI114X_IRQ_ENABLE  = 0x04
SI114X_IRQ_MODE1 = 0x05
SI114X_IRQ_MODE2 = 0x06
SI114X_HW_KEY  = 0x07
SI114X_MEAS_RATE0 = 0x08
SI114X_MEAS_RATE1  = 0x09
SI114X_PS_RATE  = 0x0A
SI114X_PS_LED21  = 0x0F
SI114X_PS_LED3  = 0x10
SI114X_UCOEFF0  = 0x13
SI114X_UCOEFF1  = 0x14
SI114X_UCOEFF2  = 0x15
SI114X_UCOEFF3  = 0x16
SI114X_WR  = 0x17
SI114X_COMMAND  = 0x18
SI114X_RESPONSE  = 0x20
SI114X_IRQ_STATUS  = 0x21
SI114X_ALS_VIS_DATA0 = 0x22
SI114X_ALS_VIS_DATA1 = 0x23
SI114X_ALS_IR_DATA0 = 0x24
SI114X_ALS_IR_DATA1 = 0x25
SI114X_PS1_DATA0 = 0x26
SI114X_PS1_DATA1 = 0x27
SI114X_PS2_DATA0 = 0x28
SI114X_PS2_DATA1 = 0x29
SI114X_PS3_DATA0 = 0x2A
SI114X_PS3_DATA1 = 0x2B
SI114X_AUX_DATA0_UVINDEX0 = 0x2C
SI114X_AUX_DATA1_UVINDEX1 = 0x2D
SI114X_RD = 0x2E
SI114X_CHIP_STAT = 0x30

#Parameters

SI114X_I2C_ADDR = 0x00

SI114X_CHLIST   = 0x01
SI114X_CHLIST_ENUV = 0x80
SI114X_CHLIST_ENAUX = 0x40
SI114X_CHLIST_ENALSIR = 0x20
SI114X_CHLIST_ENALSVIS = 0x10
SI114X_CHLIST_ENPS1 = 0x01
SI114X_CHLIST_ENPS2 = 0x02
SI114X_CHLIST_ENPS3 = 0x04

SI114X_PSLED12_SELECT   = 0x02
SI114X_PSLED3_SELECT   = 0x03

SI114X_PS_ENCODE   = 0x05
SI114X_ALS_ENCODE  = 0x06

SI114X_PS1_ADCMUX   = 0x07
SI114X_PS2_ADCMUX   = 0x08
SI114X_PS3_ADCMUX   = 0x09

SI114X_PS_ADC_COUNTER   = 0x0A
SI114X_PS_ADC_GAIN = 0x0B
SI114X_PS_ADC_MISC = 0x0C

SI114X_ALS_IR_ADC_MUX   = 0x0E
SI114X_AUX_ADC_MUX   = 0x0F

SI114X_ALS_VIS_ADC_COUNTER   = 0x10
SI114X_ALS_VIS_ADC_GAIN = 0x11
SI114X_ALS_VIS_ADC_MISC = 0x12

SI114X_LED_REC = 0x1C

SI114X_ALS_IR_ADC_COUNTER   = 0x1D
SI114X_ALS_IR_ADC_GAIN = 0x1E
SI114X_ALS_IR_ADC_MISC = 0x1F

#USER SETTINGS DEFINE

#ADCMUX

SI114X_ADCMUX_SMALL_IR  = 0x00
SI114X_ADCMUX_VISIABLE = 0x02
SI114X_ADCMUX_LARGE_IR  = 0x03
SI114X_ADCMUX_NO  = 0x06
SI114X_ADCMUX_GND  = 0x25
SI114X_ADCMUX_TEMPERATURE  = 0x65
SI114X_ADCMUX_VDD  = 0x75

#LED SEL

SI114X_PSLED12_SELECT_PS1_NONE = 0x00
SI114X_PSLED12_SELECT_PS1_LED1 = 0x01
SI114X_PSLED12_SELECT_PS1_LED2 = 0x02
SI114X_PSLED12_SELECT_PS1_LED3 = 0x04
SI114X_PSLED12_SELECT_PS2_NONE = 0x00
SI114X_PSLED12_SELECT_PS2_LED1 = 0x10
SI114X_PSLED12_SELECT_PS2_LED2 = 0x20
SI114X_PSLED12_SELECT_PS2_LED3 = 0x40
SI114X_PSLED3_SELECT_PS2_NONE = 0x00
SI114X_PSLED3_SELECT_PS2_LED1 = 0x10
SI114X_PSLED3_SELECT_PS2_LED2 = 0x20
SI114X_PSLED3_SELECT_PS2_LED3 = 0x40

#ADC GAIN DIV

SI114X_ADC_GAIN_DIV1 = 0x00
SI114X_ADC_GAIN_DIV2 = 0x01
SI114X_ADC_GAIN_DIV4 = 0x02
SI114X_ADC_GAIN_DIV8 = 0x03
SI114X_ADC_GAIN_DIV16 = 0x04
SI114X_ADC_GAIN_DIV32 = 0x05

#LED CURRENT

SI114X_LED_CURRENT_5MA = 0x01
SI114X_LED_CURRENT_11MA = 0x02
SI114X_LED_CURRENT_22MA = 0x03
SI114X_LED_CURRENT_45MA = 0x04

#Recovery period the  ADC takes before making a PS measurement

SI114X_ADC_COUNTER_1ADCCLK = 0x00
SI114X_ADC_COUNTER_7ADCCLK = 0x01
SI114X_ADC_COUNTER_15ADCCLK = 0x02
SI114X_ADC_COUNTER_31ADCCLK = 0x03
SI114X_ADC_COUNTER_63ADCCLK = 0x04
SI114X_ADC_COUNTER_127ADCCLK = 0x05
SI114X_ADC_COUNTER_255ADCCLK = 0x06
SI114X_ADC_COUNTER_511ADCCLK = 0x07

#ADC MISC

SI114X_ADC_MISC_LOWRANGE = 0x00
SI114X_ADC_MISC_HIGHRANGE = 0x20
SI114X_ADC_MISC_ADC_NORMALPROXIMITY = 0x00
SI114X_ADC_MISC_ADC_RAWADC = 0x04

#INT OE

SI114X_INT_CFG_INTOE = 0x01

#IRQ ENABLE

SI114X_IRQEN_ALS = 0x01
SI114X_IRQEN_PS1 = 0x04
SI114X_IRQEN_PS2 = 0x08
SI114X_IRQEN_PS3 = 0x10

SI114X_ADDR = 0x60

class grove_si114x(object):
    def __init__(self,address = SI114X_ADDR):
        self.bus = Bus()
        self.addr = address
        self._logger = logging.getLogger('grove_si114x')
        assert self.Begin() , "Please check if the I2C device insert in I2C of Base Hat"
    def __del__(self):
        self.bus.close()
    def __exit__(self):
        self.bus.close()
    #Init the si114x and begin to collect data
    def Begin(self):
        self._WriteByte(SI114X_COMMAND, SI114X_RESET)
        time.sleep(0.1)
        if self._ReadByte(SI114X_PART_ID) != 0X45:
            return False
        self.Reset()
        #INIT
        self.DeInit()
        return True

    #reset the si114x
    #inclue IRQ reg, command regs...
    def Reset(self):
        self._WriteByte(SI114X_MEAS_RATE0, 0)
        self._WriteByte(SI114X_MEAS_RATE1, 0)
        self._WriteByte(SI114X_IRQ_ENABLE, 0)
        self._WriteByte(SI114X_IRQ_MODE1, 0)
        self._WriteByte(SI114X_IRQ_MODE2, 0)
        self._WriteByte(SI114X_INT_CFG, 0)
        self._WriteByte(SI114X_IRQ_STATUS, 0xFF)
        self._WriteByte(SI114X_COMMAND, SI114X_RESET)
        time.sleep(0.1)
        self._WriteByte(SI114X_HW_KEY, 0x17)
        time.sleep(0.1)  

    #default init  
    def DeInit(self):
        #ENABLE UV reading
        #these reg must be set to the fixed value
        self._WriteByte(SI114X_UCOEFF0, 0x29)
        self._WriteByte(SI114X_UCOEFF1, 0x89)
        self._WriteByte(SI114X_UCOEFF2, 0x02)
        self._WriteByte(SI114X_UCOEFF3, 0x00)
        self.WriteParamData(SI114X_CHLIST, SI114X_CHLIST_ENUV | SI114X_CHLIST_ENALSIR | SI114X_CHLIST_ENALSVIS |
                    SI114X_CHLIST_ENPS1)
        #
        #set LED1 CURRENT(22.4mA)(It is a normal value for many LED)
        #
        self.WriteParamData(SI114X_PS1_ADCMUX, SI114X_ADCMUX_LARGE_IR)
        self._WriteByte(SI114X_PS_LED21, SI114X_LED_CURRENT_22MA)
        self.WriteParamData(SI114X_PSLED12_SELECT, SI114X_PSLED12_SELECT_PS1_LED1) #
        #
        #PS ADC SETTING
        #
        self.WriteParamData(SI114X_PS_ADC_GAIN, SI114X_ADC_GAIN_DIV1)
        self.WriteParamData(SI114X_PS_ADC_COUNTER, SI114X_ADC_COUNTER_511ADCCLK)
        self.WriteParamData(SI114X_PS_ADC_MISC, SI114X_ADC_MISC_HIGHRANGE | SI114X_ADC_MISC_ADC_RAWADC)
        #
        #VIS ADC SETTING
        #
        self.WriteParamData(SI114X_ALS_VIS_ADC_GAIN, SI114X_ADC_GAIN_DIV1)
        self.WriteParamData(SI114X_ALS_VIS_ADC_COUNTER, SI114X_ADC_COUNTER_511ADCCLK)
        self.WriteParamData(SI114X_ALS_VIS_ADC_MISC, SI114X_ADC_MISC_HIGHRANGE)
        #
        #IR ADC SETTING
        #
        self.WriteParamData(SI114X_ALS_IR_ADC_GAIN, SI114X_ADC_GAIN_DIV1)
        self.WriteParamData(SI114X_ALS_IR_ADC_COUNTER, SI114X_ADC_COUNTER_511ADCCLK)
        self.WriteParamData(SI114X_ALS_IR_ADC_MISC, SI114X_ADC_MISC_HIGHRANGE)
        #
        #interrupt enable
        #
        self._WriteByte(SI114X_INT_CFG, SI114X_INT_CFG_INTOE)
        self._WriteByte(SI114X_IRQ_ENABLE, SI114X_IRQEN_ALS)
        #
        #AUTO RUN
        #
        self._WriteByte(SI114X_MEAS_RATE0, 0xFF)
        self._WriteByte(SI114X_COMMAND, SI114X_PSALS_AUTO)

    #read param data
    def ReadParamData(self,Reg):
        self._WriteByte(SI114X_COMMAND,Reg|SI114X_QUERY)
        return self._ReadByte(SI114X_RD)

    #writ param data
    def WriteParamData(self,Reg,Value):
        #write Value into PARAMWR reg first
        self._WriteByte(SI114X_WR, Value)
        self._WriteByte(SI114X_COMMAND, Reg | SI114X_SET)
        #SI114X writes value out to PARAM_RD,read and confirm its right
        return self._ReadByte(SI114X_RD)

    #Read Visible Value
    @property
    def ReadVisible(self):
        return self._ReadHalfWord(SI114X_ALS_VIS_DATA0)

    #Read IR Value    
    @property
    def ReadIR(self):
        return self._ReadHalfWord(SI114X_ALS_IR_DATA0)

    #Read UV Value
    #this function is a int value ,but the real value must be div 100
    @property
    def ReadUV(self):
        return self._ReadHalfWord(SI114X_AUX_DATA0_UVINDEX0)
    
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

def main():
    SI1145 = grove_si114x()
    print("Please use Ctrl C to quit")
    while True:
        print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible , SI1145.ReadUV/100 , SI1145.ReadIR),end=" ")
        print('\r', end='')
        time.sleep(0.5)

if __name__ == "__main__":
    main()     
    