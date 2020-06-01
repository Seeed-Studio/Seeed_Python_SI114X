# Seeed_Python_SI114X

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

pip3 install seeed-python-mlx90640

```

To install system-wide (this may be required in some cases):

```

sudo pip3 install seeed-python-mlx90640

```

if you want to update the driver locally from PyPI. you can use:

```
pip3 install --upgrade seeed-python-mlx90640
```

## Usage Notes

First, Check the corresponding i2c number of the board:

```

(.env) pi@raspberrypi:~ $ ls /dev/i2c*
/dev/i2c-1

```

Check if the i2c device works properly， 0x33 is the MLX90640 i2c address.
```

pi@raspberrypi:~/Seeed_Python_SGP30 $ i2cdetect -y -r 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- 33 -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --

```

## initialize the sersor object:

Initialize the sersor object and config the sersor refresh rate.

```python
import seeed_mlx90640
mlx = seeed_mlx90640.grove_mxl90640()
mlx.refresh_rate = seeed_mlx90640.RefreshRate.REFRESH_8_HZ  # The fastest for raspberry 4 
# REFRESH_0_5_HZ = 0b000  # 0.5Hz
# REFRESH_1_HZ = 0b001  # 1Hz
# REFRESH_2_HZ = 0b010  # 2Hz
# REFRESH_4_HZ = 0b011  # 4Hz
# REFRESH_8_HZ = 0b100  # 8Hz
# REFRESH_16_HZ = 0b101  # 16Hz
# REFRESH_32_HZ = 0b110  # 32Hz
# REFRESH_64_HZ = 0b111  # 64Hz
```

## Reading from the Sensor

To read from the sensor:

```python
     try:
          frame = [0]*768
          mlx.getFrame(frame)
     except ValueError:
          continue
```

maybe you can add content that below to the config.txt to get the fastest rate recommended for compatibility

```bash
dtparam=i2c_arm=on,i2c_arm_baudrate=400000
```  

This will give you a framerate of - at most - 8FPS.

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