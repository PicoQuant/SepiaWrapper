# -*- coding: utf-8 -*-
"""
The functions of this group directly access low level structures from the firmware of the PQ Laser Device to
initialize the dynamic data layer of the library. Right after opening a PQ Laser Device, any program utilizing this
API has to perform a call to the GetModuleMap function, before it can access any module of the laser device.

Missing functions:
    int SEPIA2_FWR_DecodeErrPhaseName(int iErrPhase, StringBuilder cErrorPhase);
    
    int SEPIA2_FWR_GetLastError(int iDevIdx, out int piErrCode, out int piPhase, out int piLocation, out int piSlot, StringBuilder cCondition);
    
    int SEPIA2_FWR_GetUptimeInfoByMapIdx(int iDevIdx, int iMapIdx, out uint pulMainPowerUp, out uint pulActivePowerUp, out uint pulScaledPowerUp);
    int SEPIA2_FWR_CreateSupportRequestText(int iDevIdx, StringBuilder cPreamble, StringBuilder cCallingSW, int iOptions, int iBufferLen, StringBuilder cBuffer);

@author: Johan Hummert
"""

import ctypes as ct

from ..Sepia2_Lib import Sepia2_Lib

def get_module_map(device_index, restart=False):
    '''
    The map is a firmware and library internal data structure, which is essential to the work with
    PQ Laser Devices. It will be created by the firmware during start up. The library needs to have
    a copy of an actual map before you may access any module. You don't need to prepare
    memory, the function autonomously manages the memory acquirements for this task.
    Since the firmware doesn't actualise the map once it is running, you might wish to restart the
    firmware to assure up to date mapping. You could switch the power off and on again to reach
    the same goal, but you also could more simply call this function with iPerformRestart set to 1.
    The PQ Laser Device will perform the whole booting cycle with the tiny difference of not
    needing to load the firmware again.

    Parameters
    ----------
    device_index : INT
        USB channel
    restart : BOOL, optional
        If True perform soft reboot before creating module map. The default is False.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    num_modules : INT
        Number of modules in the device.

    '''
    restart = ct.c_int(restart)
    modulecount = ct.c_int()
    status = Sepia2_Lib.SEPIA2_FWR_GetModuleMap(device_index, restart, ct.byref(modulecount))
    num_modules = modulecount.value
    return status, num_modules


def get_module_info_by_map_index(device_index, map_index):
    '''
    Once the map is created and populated by the function GetModuleMap, you can scan it
    module by module, using this function. It returns the slot number, which is needed for all
    module-related functions later on, and three additional boolean information, namely if the
    module in question is a primary (e. g. laser driver) or a secondary module (e. g. laser head), if
    it identifies a backplane and furthermore, if the module supports uptime counters.

    Parameters
    ----------
    device_index : INT
        USB channel
    map_index : INT
        Module index.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    slot_id : INT
        slot id
    is_primary : BOOL
        True if it is a primary module
    is_backplane : BOOL
        true if there is a backplane
    has_uptime_counter : BOOL
        true if module has an uptime counter

    '''
    slot_id = ct.c_int()
    is_primary = ct.c_byte()
    is_backplane = ct.c_byte()
    has_uptime_counter = ct.c_byte()
    status = Sepia2_Lib.SEPIA2_FWR_GetModuleInfoByMapIdx(device_index,
                                                       map_index,
                                                       ct.byref(slot_id),
                                                       ct.byref(is_primary),
                                                       ct.byref(is_backplane),
                                                       ct.byref(has_uptime_counter))
    slot_id = slot_id.value
    is_primary = bool(is_primary.value)
    is_backplane = bool(is_backplane.value)
    has_uptime_counter = bool(has_uptime_counter.value)
    return status, slot_id, is_primary, is_backplane, has_uptime_counter 

def free_module_map(device_index):
    '''
    Since the library had to allocate memory for the map during the GetModuleMap function, this
    function is to restitute the memory just before your program terminates. You don't need to call
    this function between two calls of GetModuleMap for the same device index but you should
    call it for each device you ever inquired a map during the runtime of your program.

    Parameters
    ----------
    device_index : INT
        USB channel

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    status = Sepia2_Lib.SEPIA2_FWR_FreeModuleMap(device_index)
    return status

def get_version(device_index):
    '''
    This function, in opposite to other GetVersion functions only works “on line”, with the need for
    a PQ Laser Device running. It returns the actual firmware version string. To be aware of
    version changing trouble, you should call this function and check the version in your programs,
    too.

    Parameters
    ----------
    device_index : INT
        USB channel

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    fw_version : STR
        Firmware version

    '''
    fw_version = ct.create_string_buffer(8)
    status = Sepia2_Lib.SEPIA2_FWR_GetVersion(device_index, ct.byref(fw_version))
    fw_version = fw_version.value.decode('utf8')
    return status, fw_version

def get_working_mode(device_index):
    '''
    Get the current working mode.
    0: Default mode - Commands & full protective data are written immediately
    1: Volatile mode - Commands sent immediately, protective data retarded

    Parameters
    ----------
    device_index : INT
        USB channel

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    working_mode : INT
        current working mode

    '''
    working_mode = ct.c_int()
    status = Sepia2_Lib.SEPIA2_FWR_GetWorkingMode(device_index, ct.byref(working_mode))
    working_mode = working_mode.value
    return status, working_mode

def set_working_mode(device_index, working_mode):
    '''
    Set the working mode.
    0: Default mode - Commands & full protective data are written immediately
    1: Volatile mode - Commands sent immediately, protective data retarded

    Parameters
    ----------
    device_index : INT
        USB channel
    working_mode : INT
        working mode, must be 0 or 1

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    working_mode = ct.c_int(working_mode)
    status = Sepia2_Lib.SEPIA2_FWR_SetWorkingMode(device_index, working_mode)
    return status

def roll_back_to_permanent_values(device_index):
    '''
    This function re–sends commands to discard all changes made since the working mode was
    switched. The working mode changes to “stay permanent”.

    Parameters
    ----------
    device_index : INT
        USB channel

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    status = Sepia2_Lib.SEPIA2_FWR_RollBackToPermanentValues(device_index)
    return status

def store_as_permanent_values(device_index):
    '''
    This function calculates the protective data for all modules changed and sends them to the
    device. The working mode stays “volatile”.

    Parameters
    ----------
    device_index : INT
        USB channel

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    status = Sepia2_Lib.SEPIA2_FWR_StoreAsPermanentValues(device_index)
    return status
    

