<!-- PROJECT SHIELDS -->
<!--
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![GPLv3 License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/lucastliu/sciencebot">
    <img src="images/bot34.jpg" alt="Logo" width="426" height="328">
  </a>

  <h3 align="center">sciencebot</h3>

  <p align="center">
    A modular & economical research vehicle platform
    <br />
    <a href="https://github.com/lucastliu/sciencebot/wiki">Wiki</a>
    ·
    <a href="https://github.com/lucastliu/sciencebot/blob/master/README.md">Software</a>
    ·
    <a href="https://github.com/lucastliu/sciencebot/issues">Request Feature</a>
  </p>
</p>



# Hardware

Guide for the physical vehicle construction, as well as sensor information
See seperate [Main README](https://github.com/lucastliu/sciencebot/blob/master/README.md) for overview and software documentation.
<!-- TABLE OF CONTENTS -->
## Table of Contents
- [Table of Contents](#table-of-contents)
- [Hardware Technologies](#hardware-technologies)
- [Images](#images)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
    + [Raspberry Pi](#raspberry-pi)
    + [Wheels](#wheels)
    + [Arduino Motor Microcontroller](#arduino-motor-microcontroller)
    + [BNO055 IMU](#bno055-imu)
    + [DWM1001](#dwm1001)
    + [OpenMV Cam H7 (Optional)](#openmv-cam-h7--optional-)
- [Testing & Troubleshooting](#testing---troubleshooting)


## Hardware Technologies
* [Raspberry Pi 3B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
* [Arudino Uno](https://store.arduino.cc/usa/arduino-uno-rev3)
* [Arduino Motor Shield](https://store.arduino.cc/usa/arduino-motor-shield-rev3)
* [Adafruit BNO055 Absolute Orientation Sensor](https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor)
* [DWM1001C Module](https://www.decawave.com/product/dwm1001-module/) x4
* [DC Gearbox Motor - "TT Motor"](https://www.adafruit.com/product/3777) x4
* [Open MV Cam H7](https://openmv.io/products/openmv-cam-h7) x2
* [12V DC - 5V DC Voltage Step Down Regulator](https://www.amazon.com/Car-Voltage-Converter-Regulator-Smartphone/dp/B07RYT4KKK)
* [18650 Batteries](https://www.batteryjunction.com/18650.html) x3
* [18650 Battery Housing](https://www.amazon.com/Aokin-Battery-Storage-Parallel-Batteries/dp/B07Q13T3RH)
* [Portable USB Charger](https://www.amazon.com/dp/B00X5SP0HC/) x4
* [USB Cable Type A/B](https://store.arduino.cc/usa/usb-2-0-cable-type-a-b)
* [USB to USB Micro Cable](https://www.amazon.com/AmazonBasics-Male-Micro-Cable-Black/dp/B0711PVX6Z) x8
* 3D Printed Chassis, Wheels, Components
* Assorted wires, M3 screws / nuts, zipties, command strips, etc

## Images
![bot][bot34]
![botside][bot_side_1]
![botside2][bot_side_2]
![botbottom][bot_bottom]

<!-- GETTING STARTED -->
## Getting Started



### Prerequisites

Gather parts. Acquire appropriate screwdriver. Multimeter also useful for debugging.

### Installation

#### Base Chassis, Mounts & Wheels

The basic frame, as well as modular mount pieces and the wheels of the sciencebot are 3D printed. Many components have 3mm holes arranged in grid fashion, which are great for making components adaptable and modular. Connections can be made with M3 screws, zipties, or with other parts. A variety of parts are provided under the [3D_parts folder](https://github.com/lucastliu/sciencebot/tree/master/3D_parts), but also feel free to make your own!

In addition, here are some links to OnShape files for the 3D parts:

[Base](https://cad.onshape.com/documents/a6b3f805fb03e809b82d1add/w/56e20282fa9ed432ed0b3781/e/dcdab560d54729ee209a3d05)

[Additional Mounts](https://cad.onshape.com/documents/7904cea1c97a22124acc52eb/w/d508e8c8701c0da82f3e15ee/e/760d4528fb9caa9cfacff0b7)

[Additional Generics](https://cad.onshape.com/documents/96bc3dd7c7456dd4e1d48dcb/w/7a2bb739f9d9a8153bb0c78c/e/8193ef8f2d9a02fdaa290d24)


#### Raspberry Pi

The Raspberry Pi is the central brain of the vehicle. All other components will be hooked up to the Pi.

![pi_pins][pi_pins]

The preferred method of powering the Pi is to simply connect a micro-usb cable to a USB power bank. This will allow for a significantly longer operating time, as the Pi consumes much more power than the Arduino. While developing / installing, one can also use wall power.

Alternatively, one can power the Pi through the 18650s by wiring the 12V battery source to the 12V input of the voltage converter, then connecting the 5V output of the converter to the micro-usb power port on the Pi. With this setup, the battery will drain quickly, as it must power both the Pi and Arduino.

![converter][converter]



#### Wheels

Attach wheel to motor shaft. Place thread ziptie through motor and chassis base. Hand dexterity required here. "Pre-bending" the ziptie before threading can make this easier. 
![botbottomfit][bot_fitting]
![botbottom1][bot_bottom_1]
Thread power and ground wires from motor through chassis. Repeat for all wheels.
![botbottom2][bot_bottom_2]


#### Arduino Motor Microcontroller

Our Arduino Uno will serve as the motor microcontroller. Attatch the motor shield to the Arduino, and wire the motors to the shield.

![ard1][ard1]

using the USB A/B Cable, connect the Arduino to the Raspberry Pi.

![ard2][ard2]


Test the motors by running `motor_test.py` (located under motors folder) on the Pi. Note the direction of spin for each wheel. Adjust the code in the Arduino `SerialMotor.ino` file, or the `SerialMotor.py` file to correct. Note that these files exist in the standalone motors folder, but also under dev_ws/src/nav/nav/motors for the ROS2 implementation. Changes need to be made in the dev_ws subdirectory to take effect for the ROS implementation. Same goes for the standalone.


#### BNO055 IMU
![imu][imu]
1. Connect the Power, Ground, SCL, and SDA pins to the correct pinouts on the Pi. [Sensor Pinouts](https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/pinouts)

2. Enable I2C on your Pi **(Pi > Preferences > Raspberry Pi Configuration > Interfaces)**

3. Run the [IMU example script](https://github.com/lucastliu/sciencebot/blob/master/imu/example.py) to confirm data is flowing properly to the Pi.


Note: IMU data is much better when properly calibrated, though heading data is still usable even without calibration. Calibration is achieved automatically by moving the vehicle/sensor in [predefined motion sequences](https://www.mathworks.com/help/supportpkg/arduino/ref/bno055imusensor.html) (see the "More About" section). 

Calibration status can be accessed in the same way as other sensor fields in the example script. The two relevant metrics are `sensor.calibration_status` (3 being the best) and `self.sensor.calibrated` (A boolean value for whether all calibration is complete).

User beware: The IMU will initially set whichever heading it is pointed to as "heading zero," but will automatically adjust itself to true due east as zero as it calibrates. Clockwise rotation corresponds to larger angles, which are given in degrees. Wrap-around to zero at 360 degrees (though occasionally the IMU will give readings up to 370). Make sure to convert to your appropriate co-ordinate system.

#### DWM1001

![dwm][dwm]

Follow the [Quick Deployment Guide](https://www.decawave.com/wp-content/uploads/2019/03/DWM1001_Gateway_Quick_Deployment_Guide.pdf)


The guide is very extensive, so here are some important highlights:

1. Make sure each DWM has up to date firmware, as described on page 9 of the guide.

2. Our main interest is to USB hookup each DWM to a computer, and use TeraTerm to program each DWM in UART mode. Instructions for this start on page 11 of the Quick Deployment Guide. You will need at minimum a DWM configured for tag mode (the one on the vehicle), an initator DWM, and at least 2 anchor DWMs. You must program the x,y,z (arbitrary origin) of the initiator and anchors, then place the modules in your physical space accordingly.

![dwms][dwms]

It tends to be easiest to set one DWM position at the origin, and place the other tags relative to the origin DWM.


3. After initial setup, we communicate from the Pi using [this API]( https://www.decawave.com/sites/default/files/dwm1001-api-guide.pdf). In particular, we use the `lec` mode (see API page 63) to get positioning data.
    

#### OpenMV Cam H7 (Optional)

![camh7][camh7]

Cameras are attached to 3D printed mounts. Wire micro-usb cable to Pi's USB ports (USB provides channel for Data and power).

Camera lens can be swapped out for different FOV and other properties. Standard M2 Lens mount.

## Testing & Troubleshooting

The various components port addresses need to be correctly determined and set during initialization. On the Pi, open a terminal and run
```sh
dmesg | grep -i usb
```
to see devices and respective ports. For instance, the Arduino may come up under port name `/dev/ttyACM1`. When the SerialMotor object is constructed, make sure to give it the correct port. This applies for any device connected to the Pi through USB.

During ROS operation, poorly formed code / nodes may cause ungraceful shutdown, and cause the vehicle to behave undesirably. Power cycling both the Pi and the Arduino will give you a fresh start. 

If the motors seem to continually spin (likely from the last motor command before communication failure), after power cycling, modify the `motor_test.py` script to set both motors to zero, and run the script to stop the motors.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[bot34]: images/bot34.jpg
[bot_front]: images/botfront.jpg
[bot_side_1]: images/botside1.jpg
[bot_side_2]: images/botside2.jpg
[bot_bottom]: images/bottom.png
[bot_bottom_1]: images/bottom_1.png
[bot_bottom_2]: images/bottom_2.png
[bot_fitting]: images/bottom_fitting.png
[pi_pins]: images/Pi-GPIO-Pinout-Diagram.png
[dwm]: images/dwm.png
[dwms]: images/dwms.png
[camh7]: images/camh7.png
[imu]: images/imu.png
[license-shield]: https://img.shields.io/badge/License-GPLv3-blue.svg
[license-url]: https://github.com/lucastliu/sciencebot/LICENSE.txt
[product-screenshot]: images/screenshot.png