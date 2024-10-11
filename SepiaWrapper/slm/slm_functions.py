# -*- coding: utf-8 -*-
"""
SLM 828 modules can interface the huge families of pulsed laser diode heads (LDH series)
and pulsed LED

@author: Johan Hummert
"""

import ctypes as ct

from ..Sepia2_Lib import Sepia2_Lib


def get_intensity_fine_step(device_index, slot_id):
    '''
    This function gets the current intensity value of a given SLM driver module: The intensity
    stands for the current per mille value of the laser head controlling voltage.

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
    intensity : INT
        per mille intensity

    '''
    intensity = ct.c_short()
    status = Sepia2_Lib.SEPIA2_SLM_GetIntensityFineStep(device_index, slot_id, ct.byref(intensity))
    intensity = intensity.value
    return status, intensity


def set_intensity_fine_step(device_index, slot_id, intensity):
    '''
    This function sets the current intensity value of a given SLM driver module: The intensity
    stands for the current per mille value of the laser head controlling voltage.
    

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : C_INT
        Module slot id.
    intensity : INT
        per mille intensity

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    intensity = ct.c_short(intensity)
    status = Sepia2_Lib.SEPIA2_SLM_SetIntensityFineStep(device_index, slot_id, intensity)
    return status

def get_pulse_parameters(device_index, slot_id):
    '''
    This function gets the current pulse parameter values of a given SLM driver module:
    The integer trigger_mode stands for an index into the list of int. frequencies / ext.
    trigger modi.
    The pulse mode stands for a boolean and may be read as follows:
    1 : “pulses enabled”; 0 : either “laser off” or “continuous wave”, depending on the capabilities
    of the used head.

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
    trigger_mode : C_INT
        to be decoded by decode_freq_trigger_mode
    pulse_mode : BOOL
        True if pulsed
    head_type : C_INT
        to be decoded by decode_head_type

    '''
    trigger_mode = ct.c_int()
    pulse_mode = ct.c_ubyte()
    head_type = ct.c_int()
    status = Sepia2_Lib.SEPIA2_SLM_GetPulseParameters(device_index, slot_id,
                                                      ct.byref(trigger_mode),
                                                      ct.byref(pulse_mode),
                                                      ct.byref(head_type))
    pulse_mode = bool(pulse_mode.value)
    trigger_mode = trigger_mode.value
    head_type = head_type.value
    return status, trigger_mode, pulse_mode, head_type


def set_pulse_parameters(device_index, slot_id, trigger_mode, pulse_mode):
    '''
    This function sets the current pulse parameter values of a given SLM driver module:
    The integer trigger_mode stands for an index into the list of int. frequencies / ext.
    trigger modi.
    The pulse mode stands for a boolean and may be read as follows:
    1 : “pulses enabled”; 0 : either “laser off” or “continuous wave”, depending on the capabilities
    of the used head.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    trigger_mode : INT
        to be decoded by decode_freq_trigger_mode
    pulse_mode : BOOL
        True if pulsed

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    trigger_mode = ct.c_int(trigger_mode)
    pulse_mode = ct.c_ubyte(pulse_mode)
    status = Sepia2_Lib.SEPIA2_SLM_SetPulseParameters(device_index, slot_id, trigger_mode, pulse_mode)
    return status

def decode_head_type(head_type):
    '''
    Returns the head type string at list position <iHeadType> for any SLM module. This function
    also works “off line”, since all SLM modules provide the same list of pulsed LED / laser head
    types.

    Parameters
    ----------
    head_type : C_INT
        Head type identifier

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    head_type_str : STR
        Head type description

    '''
    head_type_str = ct.create_string_buffer(32)
    status = Sepia2_Lib.SEPIA2_SLM_DecodeHeadType(head_type, ct.byref(head_type_str))
    head_type_str = head_type_str.value.decode('utf8')
    return status, head_type_str

def decode_freq_trigger_mode(trigger_mode):
    '''
    Returns the frequency resp. trigger mode string at list position <iFreq> for any SLM module.
    This function also works “off line”, since all SLM modules provide the same list of int.
    frequencies resp. ext. trigger modi

    Parameters
    ----------
    head_type : C_INT
        Trigger mode identifier

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    trigger_mode_str : STR
        Trigger mode description

    '''
    trigger_mode_str = ct.create_string_buffer(32)
    status = Sepia2_Lib.SEPIA2_SLM_DecodeFreqTrigMode(trigger_mode, ct.byref(trigger_mode_str))
    trigger_mode_str = trigger_mode_str.value.decode('utf8')
    return status, trigger_mode_str