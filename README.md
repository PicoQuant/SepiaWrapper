!(logo.png)
# SepiaWrapper
## Python control for PicoQuant Sepia PDL 828 laser drivers

**Author:** Johan Hummert
**Organization:** PicoQuant GmbH, Berlin, Germany
**Version:** 2024.0.1

Python Package to control Sepia2 laser devices.

## Dependencies

- **Python 3:**
	Tested with python 3.11
	
## Installation

To use the package you need to first install the [PDL 828 software and DLL](https://www.picoquant.com/products/category/picosecond-pulsed-driver/pdl-828-sepia-ii-computer-controlled-multichannel-picosecond-diode-laser-driver), including the python programming examples. Then you can clone / download the git repository and place the directory PythonWrapper/PythonWrapper in your $PYTHONPATH.

## Getting started

To list the Sepia devices available call:
```python
import SepiaWrapper
SepiaWrapper.list_devices()
```
You can then connect to the laser device on device_index 0 with
```python
sepia2 = SepiaWrapper.sepia2(0)
```
which will create an instance of the sepia2 class. To start a single laser on a device with a SOMD oscillator and a SLM laser device (e.g. and LDH type laser head) you can use this instance with
```python
laser_index = 0
repetition rate = 20 # in MHz
intensity = 80.3 # in %
delay = 8.2 # in ns
sepia2.start_laser_simple(laser_index, repetition_rate, intensity, delay=delay)
```
In the example python notebook you can see how to set more complex parameters of the SOMD oscillator, such as burst values or sequencer combinations.

Note that if the sepia2 instance is left to the garbage collector, this will soft-lock the laser for safety. If you want to end your python program and leave the laser on, call:
```python
sepia2.close()
```

### What is included

- **SOM and SOMD oscillators**
	With SOM and SOMD oscillators most functions for internal triggering of the oscillator are included. You can set burst values, use the combiner, delay lasers for SOMD oscillators
- **Sepia laser modules (SLM)**
	Setting of pulse parameters and intensity

### What is not included

- **External Triggering of Oscillators**
- **SML functions**
- **SWM functions**
- **VCL functions**
- **Solea functions**
- **VisUV/IR functions**
- **Prima functions**
- **Linux Support**
	Most of this might work under wine, but none of it was tested under wine
- **Most hardware diagnostics, such as voltages and temperatures**

## Examples

A more detailed example is available as a jupyter notebook explaining how to connect to a sepia2 device and control some parameters. You will need to install [jupyter](https://jupyter.org/) to run the example.

## Disclaimer

**Use the SepiaWrapper at your own risk. We are not responsible for any damages or losses resulting from the use of this software.**



