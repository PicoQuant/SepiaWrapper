# -*- coding: utf-8 -*-
"""
The functions of the COM group are strictly generic and will work on any module you might find plugged to a
PQ Laser Device. Except for the functions on presets and updates, they are mainly informative.
To obtain the same information for the backplane, which is strictly speaking not a module at all, you can input "-1"
as the slot number, where appropriate. This appplies especially to the common function GetSerialNumber, by
which you could get the serial number of the whole Sepia II device.

Missing functions:
    int SEPIA2_COM_GetSerialNumber(int iDevIdx, int iSlotId, int iGetPrimary, StringBuilder cSerialNumber);
    int SEPIA2_COM_GetSupplementaryInfos(int iDevIdx, int iSlotId, int iGetPrimary, StringBuilder cLabel, StringBuilder cReleaseDate, StringBuilder cRevision, StringBuilder cHdrMemo);
    int SEPIA2_COM_GetPresetInfo(int iDevIdx, int iSlotId, int iGetPrimary, int iPresetNr, out byte pbIsSet, StringBuilder cPresetMemo);
    int SEPIA2_COM_RecallPreset(int iDevIdx, int iSlotId, int iGetPrimary, int iPresetNr);
    int SEPIA2_COM_SaveAsPreset(int iDevIdx, int iSlotId, int iSetPrimary, int iPresetNr, StringBuilder cPresetMemo);
    int SEPIA2_COM_IsWritableModule(int iDevIdx, int iSlotId, int iGetPrimary, out byte pbIsWritable);
    int SEPIA2_COM_UpdateModuleData(int iDevIdx, int iSlotId, int iSetPrimary, StringBuilder pcDCLFileName);

@author: Johan Hummert
"""

import ctypes as ct

from ..Sepia2_Lib import Sepia2_Lib

def get_module_type(device_index, slot_id, is_primary):
    '''
    Returns the module type code for a primary or secondary module respectively, located in a
    given slot.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    is_primary : BOOL
        True if this is primary module.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    c_module_type : INT
        Module type code

    '''
    module_type = ct.c_int()
    status = Sepia2_Lib.SEPIA2_COM_GetModuleType(device_index, slot_id, ct.c_int(is_primary), ct.byref(module_type))
    module_type = module_type.value
    return status, module_type


def decode_module_type(module_type):
    '''
    This function works “off line”, without a PQ Laser Device running. It decodes the module type
    code returned by the common function GetModuleType and returns the appropriate module
    type string (ASCII–readable).

    Parameters
    ----------
    module_type : INT
        as returned by get_module_type

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    module_type : STR
        module type (long)

    '''
    module_type_buffer = ct.create_string_buffer(64)
    status = Sepia2_Lib.SEPIA2_COM_DecodeModuleType(module_type, ct.byref(module_type_buffer))
    module_type = module_type_buffer.value.decode('utf8')
    return status, module_type

def decode_module_type_abbreviated(module_type):
    '''
    This function works “off line”, without a PQ Laser Device running, too. It decodes the module
    type code returned by the common function GetModuleType and returns the appropriate
    module type abbreviation string (ASCII–readable).

    Parameters
    ----------
    c_module_type : C_INT
        as returned by get_module_type

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    module_type : STR
        module type (short)

    '''
    module_type_buffer = ct.create_string_buffer(8)
    status = Sepia2_Lib.SEPIA2_COM_DecodeModuleTypeAbbr(module_type, ct.byref(module_type_buffer))
    module_type = module_type_buffer.value.decode('utf8')
    return status, module_type

def has_secondary_module(device_index, slot_id):
    '''
    Returns if the module in the named slot has attached a secondary one (laser head).
    
    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    has_secondary : BOOL
        True if this module has a secondary module.

    '''
    has_secondary = ct.c_int()
    status = Sepia2_Lib.SEPIA2_COM_HasSecondaryModule(device_index, slot_id, ct.byref(has_secondary))
    has_secondary = bool(has_secondary.value)
    return status, has_secondary
    
    

    



