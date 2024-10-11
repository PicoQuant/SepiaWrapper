# -*- coding: utf-8 -*-
"""
Unlike most of the others, all functions of the LIB group also work “off-line”, without a PQ Laser Device running.
They are intended to provide informations on the running conditions of the library itself.

Missing functions:
    int SEPIA2_LIB_IsRunningOnWine(out byte pbIsRunningOnWine);
    

@author: Johan Hummert
"""

import ctypes as ct

from ..Sepia2_Lib import Sepia2_Lib

def decode_error(status):
    '''
    This function is supposed to return an error string (human–readable) associated with a given
    error code. If status is no member of the legal error codes list, the function returns an
    error code -9999 itself, which reads "LIB: unknown error code"
    
    Parameters
    ----------
    status : INT
        Errorcode returned by other Sepia2 functions.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    message : STR
        Human readable error message.

    '''
    errorbuffer = ct.create_string_buffer(128)
    # decode error message
    status = Sepia2_Lib.SEPIA2_LIB_DecodeError(status, ct.byref(errorbuffer))
    message = errorbuffer.value.decode('utf8')
    return status, message

def get_version():
    '''
    This function returns the current library version string. To be aware of version changing
    trouble, you should call this function and check the version string in your programs, too. The
    format of the version string is:
        
    <MajorVersion:1>.<MinorVersion:1>.<Target:2>.<Build>
    
    where <Target> identifies the word width of the CPU, the library was compiled for. A legal
    version string could read e.g. “1.1.32.393”, which stands for the software version 1.1, compiled
    for an x86 target architecture and coming as build 393, whilst “1.1.64.393” identifies the same
    software version, but compiled for a x64 target.
    Take care that at least the first three parts of the version string comply with the expected
    reference, thus check for compliance of the first 7 characters.    

    Returns
    -------
    status : INT
        0 if successfull, otherwise errorcode.
    version : STR
        Library version

    '''
    versionbuffer = ct.create_string_buffer(128)
    status = Sepia2_Lib.SEPIA2_LIB_GetVersion(ct.byref(versionbuffer))
    version = versionbuffer.value.decode('utf8')
    return status, version

def get_usb_version():
    '''
    This function returns the current library version string of the USB driver. This function is
    commonly used together with the previous function SEPIA2_LIB_GetVersion to generate a
    version string that contains both the current library and USB driver version.

    Returns
    -------
    status : INT
        0 if successfull, otherwise errorcode.
    usb_version : STR
        USB Version

    '''
    usbbuffer = ct.create_string_buffer(128)
    status = Sepia2_Lib.SEPIA2_LIB_GetVersion(ct.byref(usbbuffer))
    usb_version = usbbuffer.value.decode('utf8')
    return status, usb_version



        
            
            
        
        
        
        