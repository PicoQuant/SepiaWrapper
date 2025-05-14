# -*- coding: utf-8 -*-
"""
This module implements the functionality of the prima laser devices.

@author: Tjorben Matthes
"""

import ctypes as ct

from ..Sepia2_Lib import Sepia2_Lib

def get_device_info(device_index, slot_id, device_id = None, device_type = None, fw_version = None):
    """
    This function acquires information from the specified Prima device and returns the firmware version and number of
    wavelengths (i.e. laser diodes) present in the queried Prima device.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    device_id : STR, optional
        Device id. The default is None.
    device_type : STR, optional
        Device type. The default is None.
    fw_version : STR, optional
        Firmware version. The default is None.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    device_id: STR
        Device id.
    device_type: STR
        Device type.
    fw_version: STR
        Firmware version.
    wl_count: INT
        Wavelength Count.

    """
    if device_id is None:
        device_id = ct.create_string_buffer(128)
    else:
        device_id = ct.create_string_buffer(device_id, 128)
    if device_type is None:
        device_type = ct.create_string_buffer(128)
    else:
        device_type = ct.create_string_buffer(device_type, 128)
    if fw_version is None:
        fw_version = ct.create_string_buffer(128)
    else:
        fw_version = ct.create_string_buffer(fw_version, 128)
    wl_count = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetDeviceInfo(device_index, slot_id, ct.byref(device_id), ct.byref(device_type),
                                                 ct.byref(fw_version), ct.byref(wl_count))
    device_id = device_id.value.decode('utf8')
    device_type = device_type.value.decode('utf8')
    fw_version = fw_version.value.decode('utf8')
    wl_count = wl_count.value

    return status, device_id, device_type, fw_version, wl_count

def decode_operation_mode(device_index, slot_id, oper_mode_idx):
    """
    Decodes the operation mode index to a human-readable string.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    oper_mode_idx : INT
        Operation mode index.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    oper_mode : STR
        Operation mode string.
    """
    oper_mode = ct.create_string_buffer(64)
    status = Sepia2_Lib.SEPIA2_PRI_DecodeOperationMode(device_index, slot_id, oper_mode_idx, ct.byref(oper_mode))
    oper_mode = oper_mode.value.decode('utf8')
    return status, oper_mode


def get_operation_mode(device_index, slot_id):
    """
    Gets the current operation mode index.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    oper_mode_idx : INT
        Operation mode index.
    """
    oper_mode_idx = ct.c_int()
    status = Sepia2_Lib.SEPIA2_PRI_GetOperationMode(device_index, slot_id, ct.byref(oper_mode_idx))
    return status, oper_mode_idx.value


def set_operation_mode(device_index, slot_id, oper_mode_idx):
    """
    Sets the operation mode.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    oper_mode_idx : INT
        Desired operation mode index.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    status = Sepia2_Lib.SEPIA2_PRI_SetOperationMode(device_index, slot_id, oper_mode_idx)
    return status


def decode_trigger_source(device_index, slot_id, trg_src_idx):
    """
    Decodes the trigger source index to a human-readable string.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    trg_src_idx : INT
        Trigger source index.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    trg_src : STR
        Trigger source string.
    freq_enable : BOOL
        Frequency enabled in GUI.
    t_lvl_enable : BOOL
        Trigger level enabled in GUI.
    """
    trg_src = ct.create_string_buffer(64)
    freq_enable = ct.c_ubyte()
    t_lvl_enable = ct.c_ubyte()

    status = Sepia2_Lib.SEPIA2_PRI_DecodeTriggerSource(device_index, slot_id, trg_src_idx, ct.byref(trg_src),
                                                       ct.byref(freq_enable), ct.byref(t_lvl_enable))

    trg_src = trg_src.value.decode('utf8')

    return status, trg_src, bool(freq_enable.value), bool(t_lvl_enable.value)


def get_trigger_source(device_index, slot_id):
    """
    Gets the current trigger source index.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    trg_src_idx : INT
        Trigger source index.
    """

    trg_src_idx = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetTriggerSource(device_index, slot_id, ct.byref(trg_src_idx))

    return status, trg_src_idx.value


def set_trigger_source(device_index, slot_id, trg_src_idx):
    """
    Sets the trigger source.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    trg_src_idx : INT
        Desired trigger source index.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    status = Sepia2_Lib.SEPIA2_PRI_SetTriggerSource(device_index, slot_id, trg_src_idx)
    return status


def get_trigger_level_limits(device_index, slot_id):
    """
    Gets the trigger level limits and resolution.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    min_lvl : INT
        Minimum trigger level [mV].
    max_lvl : INT
        Maximum trigger level [mV].
    lvl_res : INT
        Trigger level resolution [mV].
    """
    min_lvl = ct.c_int()
    max_lvl = ct.c_int()
    lvl_res = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetTriggerLevelLimits(device_index, slot_id, ct.byref(min_lvl), ct.byref(max_lvl),
                                                         ct.byref(lvl_res))

    return status, min_lvl.value, max_lvl.value, lvl_res.value


def get_trigger_level(device_index, slot_id):
    """
    Gets the current trigger level.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    trg_level : INT
        Current trigger level [mV].
    """
    trg_level = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetTriggerLevel(device_index, slot_id, ct.byref(trg_level))

    return status, trg_level.value


def set_trigger_level(device_index, slot_id, trg_level):
    """
    Sets the trigger level.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    trg_level : INT
        Desired trigger level [mV].

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    status = Sepia2_Lib.SEPIA2_PRI_SetTriggerLevel(device_index, slot_id, trg_level)
    return status


def get_frequency_limits(device_index, slot_id):
    """
    Gets the frequency limits.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    min_freq : INT
        Minimum frequency [Hz].
    max_freq : INT
        Maximum frequency [Hz].
    """
    min_freq = ct.c_int()
    max_freq = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetFrequencyLimits(device_index, slot_id, ct.byref(min_freq), ct.byref(max_freq))

    return status, min_freq.value, max_freq.value


def get_frequency(device_index, slot_id):
    """
    Gets the current frequency.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    frequency : INT
        Current frequency [Hz].
    """
    frequency = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetFrequency(device_index, slot_id, ct.byref(frequency))

    return status, frequency.value


def set_frequency(device_index, slot_id, frequency):
    """
    Sets the frequency.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    frequency : INT
        Desired frequency [Hz].

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    status = Sepia2_Lib.SEPIA2_PRI_SetFrequency(device_index, slot_id, frequency)
    return status

def get_gating_limits(device_index, slot_id):
    """
    Gets the gating limits.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    min_on_time : INT
        Minimum on time [ns].
    max_on_time : INT
        Maximum on time [ns].
    min_off_time_factor : INT
        Minimum off time factor.
    max_off_time_factor : INT
        Maximum off time factor.
    """
    min_on_time = ct.c_int()
    max_on_time = ct.c_int()
    min_off_time_factor = ct.c_int()
    max_off_time_factor = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetGatingLimits(device_index, slot_id, ct.byref(min_on_time), ct.byref(max_on_time), ct.byref(min_off_time_factor), ct.byref(max_off_time_factor))

    return status, min_on_time.value, max_on_time.value, min_off_time_factor.value, max_off_time_factor.value

def get_gating_data(device_index, slot_id):
    """
    Gets the current gating data.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    on_time : INT
        Current on time [ns].
    off_time_factor : INT
        Current off time factor.
    """
    on_time = ct.c_int()
    off_time_factor = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetGatingData(device_index, slot_id, ct.byref(on_time), ct.byref(off_time_factor))

    return status, on_time.value, off_time_factor.value

def set_gating_data(device_index, slot_id, on_time, off_time_factor):
    """
    Sets the gating data.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    on_time : INT
        Desired on time [ns].
    off_time_factor : INT
        Desired off time factor.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    status = Sepia2_Lib.SEPIA2_PRI_SetGatingData(device_index, slot_id, on_time, off_time_factor)
    return status

def get_gating_enabled(device_index, slot_id):
    """
    Gets the current gating enable state.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    gating_enabled : BOOL
        Current gating enable state.
    """
    gating_enabled = ct.c_ubyte()

    status = Sepia2_Lib.SEPIA2_PRI_GetGatingEnabled(device_index, slot_id, ct.byref(gating_enabled))

    return status, bool(gating_enabled.value)

def set_gating_enabled(device_index, slot_id, gating_enabled):
    """
    Sets the gating enable state.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    gating_enabled : BOOL
        Desired gating enable state.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    gating_enabled = ct.c_ubyte(gating_enabled)

    status = Sepia2_Lib.SEPIA2_PRI_SetGatingEnabled(device_index, slot_id, gating_enabled)
    return status

def get_gate_high_impedance(device_index, slot_id):
    """
    Gets the current high impedance state of the gate.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    high_impedance : BOOL
        Current high impedance state of the gate.
    """
    high_impedance = ct.c_ubyte()

    status = Sepia2_Lib.SEPIA2_PRI_GetGateHighImpedance(device_index, slot_id, ct.byref(high_impedance))

    return status, bool(high_impedance.value)

def set_gate_high_impedance(device_index, slot_id, high_impedance):
    """
    Sets the high impedance state of the gate.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    high_impedance : BOOL
        Desired high impedance state of the gate.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    high_impedance = ct.c_ubyte(high_impedance)

    status = Sepia2_Lib.SEPIA2_PRI_SetGateHighImpedance(device_index, slot_id, high_impedance)
    return status

def decode_wavelength(device_index, slot_id, wl_idx):
    """
    Decodes the wavelength index to a human-readable value in nm.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    wl_idx : INT
        Wavelength index.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    wavelength : INT
        Wavelength value in nm.
    """
    wavelength = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_DecodeWavelength(device_index, slot_id, wl_idx, ct.byref(wavelength))

    return status, wavelength.value

def get_wavelength_idx(device_index, slot_id):
    """
    Gets the current wavelength index.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    wl_idx : INT
        Current wavelength index.
    """
    wl_idx = ct.c_int()

    status = Sepia2_Lib.SEPIA2_PRI_GetWavelengthIdx(device_index, slot_id, ct.byref(wl_idx))

    return status, wl_idx.value

def set_wavelength_idx(device_index, slot_id, wl_idx):
    """
    Sets the wavelength index.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    wl_idx : INT
        Desired wavelength index.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    status = Sepia2_Lib.SEPIA2_PRI_SetWavelengthIdx(device_index, slot_id, wl_idx)
    return status

def get_intensity(device_index, slot_id, wl_idx):
    """
    Gets the current intensity setting for a specific wavelength index in per mille of the pump current.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    wl_idx : INT
        Wavelength index.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    intensity : WORD
        Current intensity setting in per mille of the pump current.
    """
    intensity = ct.c_ushort()

    status = Sepia2_Lib.SEPIA2_PRI_GetIntensity(device_index, slot_id, wl_idx, ct.byref(intensity))

    return status, intensity.value

def set_intensity(device_index, slot_id, wl_idx, intensity):
    """
    Sets the intensity for a specific wavelength index in per mille of the pump current.

    Parameters
    ----------
    device_index : INT
        Device index.
    slot_id : INT
        Module slot id.
    wl_idx : INT
        Wavelength index.
    intensity : WORD
        Desired intensity setting in per mille of the pump current.

    Returns
    -------
    status : INT
        0 if successful, otherwise error code.
    """
    intensity = ct.c_ushort(intensity)

    status = Sepia2_Lib.SEPIA2_PRI_SetIntensity(device_index, slot_id, wl_idx, intensity)
    return status