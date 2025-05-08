# -*- coding: utf-8 -*-
"""
This module implements the safety features of the PQ Laser Device, as there are the thermal and voltage
monitoring, the interlock (hard locking) and soft locking capabilities.

Missing functions:
    int SEPIA2_SCM_GetPowerAndLaserLEDS(int iDevIdx, int iSlotId, out byte pbPowerLED, out byte pbLaserActiveLED);

@author: Johan Hummert
    additions by Tjorben Matthes
"""

import ctypes as ct

from ..Sepia2_Lib import Sepia2_Lib


def get_laser_locked(device_index, slot_id):
    '''
    Returns the state of the laser power line. If the line is down either by hardlock (key), power
    failure or softlock (firmware, GUI or custom program) it returns locked (i. e. true or 1),
    otherwise unlocked (i. e. false or 0).

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : C_INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    locked : BOOL
        True if laser is locked or failed.

    '''
    locked = ct.c_ubyte()
    status = Sepia2_Lib.SEPIA2_SCM_GetLaserLocked(device_index, slot_id, ct.byref(locked))
    locked = bool(locked.value)
    return status, locked

def get_laser_softlocked(device_index, slot_id):
    '''
    Returns the contents of the soft lock register.
    Note, that this information will not stand for the real state of the laser power line. A hard lock
    overrides a soft unlock.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : C_INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    locked : BOOL
        True if laser is locked or failed.

    '''
    locked = ct.c_ubyte()
    status = Sepia2_Lib.SEPIA2_SCM_GetLaserSoftLock(device_index, slot_id, ct.byref(locked))
    locked = bool(locked.value)
    return status, locked

def set_laser_softlocked(device_index, slot_id, locked):
    '''
    Sets the contents of the soft lock register.
    Note, that this information will not stand for the real state of the laser power line. A hard lock
    overrides a soft unlock.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : C_INT
        Module slot id.
    locked : BOOL
        True locks the laser, False unlocks the laser 

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    locked : BOOL
        True if laser is locked or failed.

    '''
    locked = ct.c_ubyte(locked)
    status = Sepia2_Lib.SEPIA2_SCM_SetLaserSoftLock(device_index, slot_id, locked)
    return status

def get_power_and_laser_leds(device_index, slot_id):
    """

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : C_INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    power_led : BOOL
        True if active
    laser_active_led : Bool
        True if active

    """
    power_led = ct.c_ubyte()
    laser_active_led = ct.c_ubyte()
    status = Sepia2_Lib.SEPIA2_SCM_GetPowerAndLaserLEDS(device_index, slot_id, ct.byref(power_led),
                                                        ct.byref(laser_active_led))
    power_led = bool(power_led.value)
    laser_active_led = bool(laser_active_led.value)
    return status, power_led, laser_active_led


    
    

    



