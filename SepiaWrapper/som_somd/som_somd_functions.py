# -*- coding: utf-8 -*-
"""
As you could already learn from the main manual chapters on the oscillator modules, these modules are a very
powerful means for the design of synchronized controlling signals. They incorporate the complex functionalities of
a base clock oscillator with pre-divider, a burst generator, a sequencer and a signal splitter for multiple
synchronous outputs in one entity. To date, PicoQuant offers oscillator modules mainly in two variants: the
SOM 828 and the SOM 828-D.

Functions that exist in both variants have an added type argument, that will decide between SOM and SOMD

Missing functions:
    
    int SEPIA2_SOM_GetTriggerRange(int iDevIdx, int iSlotId, out int piMilliVoltLow, out int piMilliVoltHigh);
    int SEPIA2_SOM_GetTriggerLevel(int iDevIdx, int iSlotId, out int piMilliVolt);
    int SEPIA2_SOM_SetTriggerLevel(int iDevIdx, int iSlotId, int iMilliVolt);
    
    int SEPIA2_SOMD_SynchronizeNow(int iDevIdx, int iSlotId);
    int SEPIA2_SOMD_DecodeModuleState(ushort wState, StringBuilder cStatusText);
    int SEPIA2_SOMD_GetStatusError(int iDevIdx, int iSlotId, out ushort pwState, out short piErrorCode);
    int SEPIA2_SOMD_GetTrigSyncFreq(int iDevIdx, int iSlotId, out byte pbFreqStable, out uint pulTrigSyncFreq);
    int SEPIA2_SOMD_GetFWVersion(int iDevIdx, int iSlotId, out uint pulFWVersion);
    
    int SEPIA2_SOMD_FWReadPage(int iDevIdx, int iSlotId, ushort iPageIdx, out byte pbFWPage);
    int SEPIA2_SOMD_FWWritePage(int iDevIdx, int iSlotId, ushort iPageIdx, out byte pbFWPage);
    int SEPIA2_SOMD_GetHWParams(int iDevIdx, int iSlotId, out ushort pwHWParTemp1, out ushort pwHWParTemp2, out ushort pwHWParTemp3, out ushort pwHWParVolt1, out ushort pwHWParVolt2, out ushort pwHWParVolt3, out ushort pwHWParVolt4, out ushort pwHWParAUX);    

@author: Johan Hummert
"""

import ctypes as ct

from ..Sepia2_Lib import Sepia2_Lib


def get_out_and_sync_enable(device_index, slot_id, module_type):
    '''
    This function gets the current values of the output control and sync signal composing.
    (For the following illustrations refer to the screen shot of the main dialogue in the main manual
    and to the chapter on sync signal composition with SOM 828 modules.)
    Each bit in the byte pointed at by out_enable stands for an output enable boolean. Thus
    if all bits are set except of the second and fifth, this byte reads 0xED, which means all but the
    second and fifth output channel are enabled.
    Each bit in the byte pointed at by sync_enable stands for an sync enable boolean. Thus
    if all bits are clear except of the first and third, this byte reads 0x05, which means only the first
    and third output channel is mirrored to the sync signal composition.
    The byte pointed at by <pbSyncInverse> stands for a boolean. It defines whether the sync
    mask length stands for the count of pulses first let through (bSyncInverse = true, 1) or for the
    count of pulses first blocked (bSyncInverse = false, 0)

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    out_enable : STR
        Bitstring showing which lasers are enabled.
    sync_enable : STR
        Bitstring showing for which lasers sync is enabled.
    sync_inverse : BOOL
        Bitstring showing if sync is inverted

    '''
    out_enable = ct.c_ubyte()
    sync_enable = ct.c_ubyte()
    sync_inverse = ct.c_ubyte()
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_GetOutNSyncEnable(device_index,
                                                        slot_id,
                                                        ct.byref(out_enable),
                                                        ct.byref(sync_enable),
                                                        ct.byref(sync_inverse)
                                                        )
    elif module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_GetOutNSyncEnable(device_index,
                                                        slot_id,
                                                        ct.byref(out_enable),
                                                        ct.byref(sync_enable),
                                                        ct.byref(sync_inverse)
                                                        )
    out_enable = '{:08b}'.format(out_enable.value)
    sync_enable = '{:08b}'.format(sync_enable.value)
    sync_inverse = bool(sync_inverse.value)
    return status, out_enable, sync_enable, sync_inverse


def set_out_and_sync_enable(device_index, slot_id, module_type, out_enable, sync_enable, sync_inverse):
    '''
    This function sets the new values for the output control and sync signal composing.
    (For the following illustrations refer to the screen shot of the main dialogue in the main manual
    and to the chapter on sync signal composition with SOM 828 modules.)

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.
    out_enable : STR
        Bitstring showing which lasers to enable.
    sync_enable : STR
        Bitstring showing which syncs to enable.
    sync_inverse : BOOL
        Bitstring showing if sync is inverted

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    out_enable = ct.c_ubyte(int(out_enable, 2))
    sync_enable = ct.c_ubyte(int(sync_enable, 2))
    sync_inverse = ct.c_ubyte(sync_inverse)
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_SetOutNSyncEnable(device_index,
                                                        slot_id,
                                                        out_enable,
                                                        sync_enable,
                                                        sync_inverse
                                                        )
    elif module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_SetOutNSyncEnable(device_index,
                                                        slot_id,
                                                        out_enable,
                                                        sync_enable,
                                                        sync_inverse
                                                        )
    return status


def get_freq_trigger_mode(device_index, slot_id, module_type):
    '''
    This function inquires the current setting for the reference source in a given SOM. In the
    integer output it returns an index into the list of possible sources.    

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    frequency_trigger_mode : INT
        frequency trigger mode, to be decoded by decode_freq_trigger_mode

    '''
    freq_trigger_mode = ct.c_int()
    sync_now = ct.c_ubyte(0)
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_GetFreqTrigMode(device_index,
                                                      slot_id,
                                                      ct.byref(freq_trigger_mode)
                                                      )
    elif module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_GetFreqTrigMode(device_index,
                                                      slot_id,
                                                      ct.byref(freq_trigger_mode),
                                                      ct.byref(sync_now)
                                                      )
    freq_trigger_mode = freq_trigger_mode.value
    sync_now = bool(sync_now.value)
    return status, freq_trigger_mode, sync_now


def set_freq_trigger_mode(device_index, slot_id, module_type, freq_trigger_mode, sync_now=False):
    '''
    This function sets the new reference source for a given SOM. It is passed over as a new value
    for the index into the list of possible sources.    

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.
    frequency_trigger_mode : INT
        frequency trigger mode, meaning to be decoded by decode_freq_trigger_mode

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    freq_trigger_mode = ct.c_int(freq_trigger_mode)
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_SetFreqTrigMode(device_index,
                                                      slot_id,
                                                      freq_trigger_mode
                                                      )
    elif module_type == 'SOMD':
        sync_now = ct.c_ubyte(sync_now)
        status = Sepia2_Lib.SEPIA2_SOMD_SetFreqTrigMode(device_index,
                                                        slot_id,
                                                        freq_trigger_mode,
                                                        sync_now
                                                        )
    return status

def decode_freq_trigger_mode(device_index, slot_id, module_type, freq_trigger_mode):
    '''
    Returns the frequency resp. trigger mode string at list position <iFreqTrigMode> for a given
    SOM module. This function only works “on line”, with a PQ Laser Device running, because
    each SOM may carry its individual list of reference sources. Only the list positions 0 and 1 are
    identical for all SOM modules: They always carry the external trigger option on respectively
    raising and falling edges. To get the whole table, loop over the list position index starting with 0
    until the function terminates with an error.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.
    frequency_trigger_mode : INT
        frequency trigger mode, as returned by get_freq_trigger_mode

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    trigger_mode : STR
        readable description of the trigger mode

    '''
    trigger_mode = ct.create_string_buffer(32)
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_DecodeFreqTrigMode(device_index,
                                                          slot_id,
                                                          freq_trigger_mode,
                                                          ct.byref(trigger_mode)
                                                          )
    elif module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_DecodeFreqTrigMode(device_index,
                                                           slot_id,
                                                           freq_trigger_mode,
                                                           ct.byref(trigger_mode)
                                                           )
    trigger_mode = trigger_mode.value.decode('utf8')
    return status, trigger_mode


def get_burst_values(device_index, slot_id, module_type):
    '''
    This function returns the current settings of the determining values for the timing of the
    pre scaler. Refer to the main manual chapter on SOM 828 modules to learn about these
    values.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    divider : INT
        divider value
    presync : INT
        current pre sync value
    mask_sync : INT
        current mask sync value

    '''
    presync = ct.c_ubyte()
    mask_sync = ct.c_ubyte()
    if module_type == 'SOM':
        divider = ct.c_ubyte()
        status = Sepia2_Lib.SEPIA2_SOM_GetBurstValues(device_index, slot_id,
                                                      ct.byref(divider),
                                                      ct.byref(presync),
                                                      ct.byref(mask_sync))
    if module_type == 'SOMD':
        divider = ct.c_short()
        status = Sepia2_Lib.SEPIA2_SOMD_GetBurstValues(device_index, slot_id,
                                                       ct.byref(divider),
                                                       ct.byref(presync),
                                                       ct.byref(mask_sync))
    divider = int(divider.value)
    presync = int(presync.value)
    mask_sync = int(mask_sync.value)
    return status, divider, presync, mask_sync

def set_burst_values(device_index, slot_id, module_type, divider, presync, mask_sync):
    '''
    This function sets the new determining values for the timing of the pre scaler. Refer to the
    main manual chapter on SOM 828 modules to learn about these values.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.
    divider : INT
        desired divider value
    presync : INT
        desired pre sync value
    mask_sync : INT
        desired mask sync value

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    presync = ct.c_ubyte(presync)
    mask_sync = ct.c_ubyte(mask_sync)
    if module_type == 'SOM':
        divider = ct.c_ubyte(divider)
        status = Sepia2_Lib.SEPIA2_SOM_SetBurstValues(device_index, slot_id,
                                                      divider,
                                                      presync,
                                                      mask_sync)
    if module_type == 'SOMD':
        divider = ct.c_short(divider)
        status = Sepia2_Lib.SEPIA2_SOMD_SetBurstValues(device_index, slot_id,
                                                       divider,
                                                       presync,
                                                       mask_sync)
    return status

def get_burst_length_array(device_index, slot_id, module_type):
    '''
    This function gets the current values for the respective burst length of the eight output
    channels.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : C_INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    burst_lengths : LIST
        List of burst length values

    '''
    b1 = ct.c_long()
    b2 = ct.c_long()
    b3 = ct.c_long()
    b4 = ct.c_long()
    b5 = ct.c_long()
    b6 = ct.c_long()
    b7 = ct.c_long()
    b8 = ct.c_long()
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_GetBurstLengthArray(device_index, slot_id,
                                                            ct.byref(b1),
                                                            ct.byref(b2),
                                                            ct.byref(b3),
                                                            ct.byref(b4),
                                                            ct.byref(b5),
                                                            ct.byref(b6),
                                                            ct.byref(b7),
                                                            ct.byref(b8))
    if module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_GetBurstLengthArray(device_index, slot_id,
                                                            ct.byref(b1),
                                                            ct.byref(b2),
                                                            ct.byref(b3),
                                                            ct.byref(b4),
                                                            ct.byref(b5),
                                                            ct.byref(b6),
                                                            ct.byref(b7),
                                                            ct.byref(b8))
    burst_lengths = [b1.value, b2.value, b3.value, b4.value, b5.value, b6.value, b7.value, b8.value]
    return status, burst_lengths


def set_burst_length_array(device_index, slot_id, module_type, burst_lengths):
    '''
    This function gets the current values for the respective burst length of the eight output
    channels.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    module_type : STR
        Module type. Either 'SOM' or 'SOMD'.
    burst_lengths : LIST
        List of burst length values

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.

    '''
    burst_lengths = [ct.c_long(bl) for bl in burst_lengths]
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_SetBurstLengthArray(device_index, slot_id,
                                                           *burst_lengths)
    if module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_SetBurstLengthArray(device_index, slot_id,
                                                            *burst_lengths)
    return status
    
def decode_sequencer_auxin_control(auxin_control, module_type):
    str_auxin_control = ct.create_string_buffer(32)
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_DecodeAUXINSequencerCtrl(auxin_control, ct.byref(str_auxin_control))
    elif module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_DecodeAUXINSequencerCtrl(auxin_control, ct.byref(str_auxin_control))
    str_auxin_control = str_auxin_control.value.decode('utf8')
    return status, str_auxin_control
    
def get_sequencer_control(device_index, slot_id, module_type):
    aux_out = ct.c_ubyte()
    aux_in = ct.c_ubyte()
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_GetAUXIOSequencerCtrl(device_index, slot_id, ct.byref(aux_out), ct.byref(aux_in))
    elif module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_GetAUXIOSequencerCtrl(device_index, slot_id, ct.byref(aux_out), ct.byref(aux_in))
    aux_in = aux_in.value
    aux_out = bool(aux_out.value)
    return status, aux_in, aux_out
    
def set_sequencer_control(device_index, slot_id, module_type, aux_out, aux_in):
    aux_out = ct.c_ubyte(aux_out)
    aux_in = ct.c_ubyte(aux_in)
    if module_type == 'SOM':
        status = Sepia2_Lib.SEPIA2_SOM_SetAUXIOSequencerCtrl(device_index, slot_id, aux_out, aux_in)
    elif module_type == 'SOMD':
        status = Sepia2_Lib.SEPIA2_SOMD_SetAUXIOSequencerCtrl(device_index, slot_id, aux_out, aux_in)
    return status
    
def get_seq_output_infos(device_index, slot_id, seq_output_index):
    '''
    This function returns all information necessary to describe the state of the sequencer output
    identified by seq_output_index. Note, that it returns apparently redundant information: If e.g.
    delayed is True, the information on output combinations seems sort of useless, since
    burst combinations aren't allowed on delayed signals. On the other hand, there is no virtue in
    reading delay data, if delayed is false or force_undelayed is true.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : INT
        Module slot id.
    seq_output_index : INT
        sequencer output index (1 ... 8)

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    delayed : BOOL
        True if this laser is delayed
    force_undelayed : BOOL
        True if this laser is undelayed
    out_combi : STR
        bitstring (length 8) showing burst setting
    masked_combi : BOOL
        masked_combi (see Manual)
    delay_coarse : FLOAT
        coarse delay
    delay_fine : INT
        fine delay [a.u.].

    '''
    seq_output_index = ct.c_ubyte(seq_output_index)
    delayed = ct.c_ubyte()
    force_undelayed = ct.c_ubyte()
    out_combi = ct.c_ubyte()
    masked_combi = ct.c_ubyte()
    delay_coarse = ct.c_double()
    delay_fine = ct.c_ubyte()
    status = Sepia2_Lib.SEPIA2_SOMD_GetSeqOutputInfos(device_index, slot_id, seq_output_index,
                                                      ct.byref(delayed),
                                                      ct.byref(force_undelayed),
                                                      ct.byref(out_combi),
                                                      ct.byref(masked_combi),
                                                      ct.byref(delay_coarse),
                                                      ct.byref(delay_fine),
                                                      )
    delayed = bool(delayed.value)
    force_undelayed = bool(force_undelayed.value)
    out_combi = '{:08b}'.format(out_combi.value)
    masked_combi = bool(masked_combi.value)
    delay_coarse = delay_coarse.value
    delay_fine = delay_fine.value
    return status, delayed, force_undelayed, out_combi, masked_combi, delay_coarse, delay_fine

def set_seq_output_infos(device_index, slot_id, seq_output_index, delayed,
                         out_combi, masked_combi, delay_coarse, delay_fine):
    '''
    This function sets all information necessary to describe the state of the sequencer output
    identified by seq_output_index. Note, that it transmits apparently redundant information: If e.g.
    delayed is true, the information on output combinations seems sort of useless, since burst
    combinations aren't allowed on delayed signals. On the other hand, there is no virtue in setting
    delay data, if delayed is false.

    Parameters
    ----------
    device_index : INT
        device index.
    slot_id : C_INT
        Module slot id.
    seq_output_index : INT
        sequencer output index (1 ... 8)

    Returns
    -------
    status : INT
        0 if successful, otherwise errorcode.
    delayed : BOOL
        True if this laser is delayed
    force_undelayed : BOOL
        True if this laser is undelayed
    out_combi : STR
        bitstring (length 8) showing burst values
    masked_combi : BOOL
        masked_combi (see Manual)
    delay_coarse : FLOAT
        coarse delay
    delay_fine : INT
        fine delay [a.u.]. Call get_delay_units to get legal values

    '''
    delayed = ct.c_ubyte(delayed)
    out_combi = ct.c_ubyte(int(out_combi, 2))
    masked_combi = ct.c_ubyte(masked_combi)
    delay_coarse = ct.c_double(delay_coarse)
    delay_fine = ct.c_ubyte(delay_fine)
    status = Sepia2_Lib.SEPIA2_SOMD_SetSeqOutputInfos(device_index, slot_id, seq_output_index,
                                                      delayed,
                                                      out_combi,
                                                      masked_combi,
                                                      delay_coarse,
                                                      delay_fine,
                                                      )
    return status

def get_delay_units(device_index, slot_id):
    '''
    This function should always be called, after the base oscillator values (source, divider,
    synchronized frequency, etc.) had changed. It returns the coarse delay stepwidth in seconds
    and the currently possible amount of fine steps to apply. The coarse delay stepwidth is mainly
    varying with the main clock, depending on the trigger source (base oscillator or external signal)
    and the pre-division factor. Usually the stepwidth will be about 650 to 950 psec; the value is
    given in seconds. Since this value is varying on all changes to the main clock, the amount of
    steps to meet a desired delay length has to be recalculated then. The same goes for the
    amount of fine steps. A fine step has a module depending, individually varying steplength of
    typically 15 to 35 psec.

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
    coarse_delay_step : FLOAT
        coarse delay step in s
    fine_delay : INT
        Allowed maximum value for fine delay

    '''
    coarse_delay_step = ct.c_double()
    fine_delay = ct.c_ubyte()
    status = Sepia2_Lib.SEPIA2_SOMD_GetDelayUnits(device_index, slot_id, ct.byref(coarse_delay_step), ct.byref(fine_delay))
    coarse_delay_step = coarse_delay_step.value
    fine_delay = fine_delay.value
    return status, coarse_delay_step, fine_delay



