# Seeed_Python_SI114X

![](https://camo.githubusercontent.com/0b16b004205798245778945edb73f36c7e5d7adf/68747470733a2f2f73746174696373332e736565656473747564696f2e636f6d2f696d616765732f70726f647563742f313031303230303839253230312e6a7067)

Grove - Sunlight Sensor (si114x) is a multi-channel digital light sensor, which has the ability to detect UV-light, visible light and infrared light.

This device is based on SI1145, a new sensor from SiLabs. The Si1145 is a low-power, reflectance-based, infrared proximity, UV index and ambient light sensor with I2C digital interface and programmable-event interrupt output. This device offers excellent performance under a wide dynamic range and a variety of light sources including direct sunlight.

# Dependencies

This driver depends on:
- [***grove.py***](https://github.com/Seeed-Studio/grove.py)

This is easy to install with the following command.

```python
pip3 install Seeed-grove.py
```
 
## Installing from PyPI

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally from PyPI. To install for current user:

```

pip3 install seeed-python-si114x

```

To install system-wide (this may be required in some cases):

```

sudo pip3 install seeed-python-si114x

```

if you want to update the driver locally from PyPI. you can use:

```
pip3 install --upgrade seeed-python-si114x
```

## Usage Notes

First, Check the corresponding i2c number of the board:

```

(.env) pi@raspberrypi:~ $ ls /dev/i2c*
/dev/i2c-1

```

Check if the i2c device works properly， 0x60 is the SI114x i2c address.
```

pi@raspberrypi:~/Seeed_Python_SI114X $ i2cdetect -y -r 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- 04 -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- UU -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: 60 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --   

```

## Usage

```python
import seeed_si114x
import time
import signal
def handler(signalnum, handler):
    print("Please use Ctrl C to quit")
def main():
    SI1145 = seeed_si114x.grove_si114x()
    print("Please use Ctrl C to quit")
    signal.signal(signal.SIGTSTP, handler) # Ctrl-z
    signal.signal(signal.SIGQUIT, handler) # Ctrl-\
    while True:
        print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible , SI1145.ReadUV/100 , SI1145.ReadIR),end=" ")
        print('\r', end='')
        time.sleep(0.5)
if __name__  == '__main__':
    main()
```

## API Reference

- uint16_t ReadVisible(void): return visible light of Ambient.

```python
    print("Visible %03d" % SI1145.ReadVisible)
```

- uint16_t ReadUV(void): return Ultraviolet (UV) Index.

```python
    print("UV %.2f" % SI1145.ReadUV / 100)
```

- uint16_t ReadIR(void): return infrared light of Ambient.

```python
    print("IR %03d" % SI1145.ReadIR)
```
----

This software is written by seeed studio<br>
and is licensed under [The MIT License](http://opensource.org/licenses/mit-license.php). Check License.txt for more information.<br>

Contributing to this software is warmly welcomed. You can do this basically by<br>
[forking](https://help.github.com/articles/fork-a-repo), committing modifications and then [pulling requests](https://help.github.com/articles/using-pull-requests) (follow the links above<br>
for operating guide). Adding change log and your contact into file header is encouraged.<br>
Thanks for your contribution.

Seeed Studio is an open hardware facilitation company based in Shenzhen, China. <br>
Benefiting from local manufacture power and convenient global logistic system, <br>
we integrate resources to serve new era of innovation. Seeed also works with <br>
global distributors and partners to push open hardware movement.<br>


[![Analytics](https://ga-beacon.appspot.com/UA-46589105-3/Grove_LED_Bar)](https://github.com/igrigorik/ga-beacon)
