# -*- coding: utf-8 -*-
"""
The functions of the USB group handle the PQ Laser Device as an USB device. Besides opening and closing,
they provide information on the device and help to identify the desired instance if there is more than one
PQ Laser Device connected to the PC

Missing functions:
    # int SEPIA2_USB_GetStrDescrByIdx(int iDevIdx, int iDescrIdx, StringBuilder cDescriptor);
    

@author: Johan Hummert
"""

import ctypes as ct

from ..Sepia2_Lib import Sepia2_Lib

def open_device(device_index, productmodel=None, serialnumber=None):
    '''
    On success, this function grants exclusive access to the PQ Laser Device on USB channel
    <device_index>. It returns the product model and serial number of the device, even if the device is
    blocked or busy (error code -9004 or -9005; refer to appendix 4.2). If called with non-empty
    string arguments, the respective string works as condition. If you pass a product model string,
    e.g., “Sepia II” or “Solea”, all devices other than the specified model are ignored. The analogue
    goes, if you pass a serial number; Specifying both will work out as a logical AND
    performed on the respective conditions. Thus an error code is returned, if none of the
    connected devices match the condition.

    Parameters
    ----------
    device_index : INT
        USB channel
    productmodel : STR, optional
        Product Model of Device. The default is None.
    serialnumber : STR, optional
        Serial number of Device. The default is None.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    productmodel : STR
        Product Model of Device
    serialnumber : STR
        Serial number of Device
    '''
    if productmodel is None:
        productmodel = ct.create_string_buffer(128)
    else:
        ct.create_string_buffer(productmodel, 128)
    if serialnumber is None:
        serialnumber = ct.create_string_buffer(128)
    else:
        ct.create_string_buffer(serialnumber, 128)
    # initiate USB connection
    status = Sepia2_Lib.SEPIA2_USB_OpenDevice(device_index, ct.byref(productmodel), ct.byref(serialnumber))
    # return if no device found
    productmodel = productmodel.value.decode('utf8')
    serialnumber = serialnumber.value.decode('utf8')
    return status, productmodel, serialnumber


def open_get_serial_number_and_close(device_index, productmodel=None, serialnumber=None):
    '''
    When called with empty string parameters given, this function is used to iteratively get a
    complete list of all currently present PQ Laser Devices. It returns the product model and serial
    number of the device, even if the device is blocked or busy (error code -9004 or -9005; refer to
    appendix 4.2). The function opens the PQ Laser Device on USB channel <iDevIdx> non-
    exclusively, reads the product model and serial number and immediately closes the device
    again. Don't forget to clear the returned parameter strings if called in a loop. When called with
    non-empty string parameters, with respect to the conditions, the function behaves as specified
    for the OpenDevice function.

    Parameters
    ----------
    device_index : INT
        USB channel
    productmodel : STR, optional
        Product Model of Device. The default is None.
    serialnumber : STR, optional
        Serial number of Device. The default is None.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    productmodel : STR
        Product Model of Device
    serialnumber : STR
        Serial number of Device
    '''
    if productmodel is None:
        productmodel = ct.create_string_buffer(128)
    else:
        ct.create_string_buffer(productmodel, 128)
    if serialnumber is None:
        serialnumber = ct.create_string_buffer(128)
    else:
        ct.create_string_buffer(serialnumber, 128)
    # initiate USB connection
    status = Sepia2_Lib.SEPIA2_USB_OpenDevice(device_index, ct.byref(productmodel), ct.byref(serialnumber))
    # return if no device found
    productmodel = productmodel.value.decode('utf8')
    serialnumber = serialnumber.value.decode('utf8')
    return status, productmodel, serialnumber

def get_str_descriptor(device_index):
    '''
    Returns the concatenated string descriptors of the USB device. For a PQ Laser Device, you
    could find e.g., the product model string, the firmware build number, as well as the serial
    number there, which is relevant when requesting support by PicoQuant. Otherwise, this
    function is solely informative.

    Parameters
    ----------
    device_index : INT
        USB channel

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    description : STR
        device description.

    '''
    descriptor = ct.create_string_buffer(256)
    status = Sepia2_Lib.SEPIA2_USB_GetStrDescriptor(device_index, ct.byref(descriptor))
    description = descriptor.value.decode('utf8')
    return status, description

def is_open_device(device_index):
    '''
    Calling this function query whether the USB device with index device_index has been opened or
    not. The function returns the value true is the specified device is open.

    Parameters
    ----------
    device_index : INT
        USB channel

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    description : BOOL
        True if device is open.

    '''
    is_open = ct.c_ubyte()
    status = Sepia2_Lib.SEPIA2_USB_IsOpenDevice(device_index,
                                              ct.byref(is_open))
    return status, bool(is_open.value)

def close_device(device_index):
    '''
    Terminates the exclusive access to the PQ Laser Device identified by device_index

    Parameters
    ----------
    device_index : INT
        USB channel

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    status = Sepia2_Lib.SEPIA2_USB_CloseDevice(device_index)
    return status  
            
        
        
        
        