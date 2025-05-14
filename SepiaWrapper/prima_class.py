# -*- coding: utf-8 -*-

"""
Provides the prima class for simpler control of prima laser devices.

@author: Tjorben Matthes
"""
from .library import decode_error
from .pri import (get_device_info, decode_operation_mode, get_operation_mode, set_operation_mode, decode_trigger_source,
                  get_trigger_source, set_trigger_source, get_trigger_level_limits, get_trigger_level,
                  set_trigger_level,
                  get_frequency_limits, get_frequency, set_frequency, get_gating_limits, get_gating_data,
                  set_gating_data,
                  get_gating_enabled, set_gating_enabled, get_gate_high_impedance, set_gate_high_impedance,
                  decode_wavelength,
                  get_wavelength_idx, set_wavelength_idx, get_intensity, set_intensity)


class SepiaLibError(Exception):
    pass


class SepiaWrapperError(Exception):
    pass


class Prima:
    def check_error(self):
        """
        Check for errors in calls to the Sepia2 API.

        Returns
        -------
        none

        """
        if self.status != 0:
            # decode error message
            self.status, error = decode_error(self.status)
            if self.status == 0:
                raise SepiaLibError(error)
            else:
                self.status, error = decode_error(self.status)
                raise SepiaLibError(error)

    def __init__(self, device_index, slot_id, module_type):
        """

        Initiate the class.

        Parameters
        ----------
        device_index : INT
            USB index for the laser driver (0...7)

        Returns
        -------
        none


        """

        if module_type != 'PRI':
            raise RuntimeWarning('This class is only for prima lasers.')
        self.device_index = device_index
        self.status = 0
        self.slot_id = slot_id
        self.module_type = module_type
        return

    def set_intensity(self, intensity):
        """
        Set intensity for the laser

        Parameters
        ----------
        intensity : FLOAT
            Intensity value in %

        Returns
        -------
        none

        """
        self.status = set_intensity(self.device_index, self.slot_id, round(intensity * 10))
        self.check_error()
        return

    def set_laser_parameters(self, operation_mode, trig_source = 0, op_freq=None):
        """

        Parameters
        ----------
        operation_mode : INT
            desired operation mode (0 off, 1 narrow pulse, 2 broad pulse, 3 cw)
        trig_source : INT, optional
            trigger source for pulsed operation, defaults to 0
        op_freq : INT, optional
            operation frequency for pulsed operation, defaults to None

        Returns
        -------

        """

        if operation_mode == 1 or operation_mode == 2:
            if op_freq is None:
                raise RuntimeError('For a pulsed operation mode a pulse frequency has to be specified.')
            self.status = set_operation_mode(self.device_index, self.slot_id, operation_mode)
            self.check_error()
            self.status = set_frequency(self.device_index, self.slot_id, op_freq)
            self.check_error()
            self.status = set_trigger_source(self.device_index, self.slot_id, trig_source)
            self.check_error()
        else:
            self.status = set_operation_mode(self.device_index, self.slot_id, operation_mode)
            self.check_error()
        return


    def change_operation_wavelength(self, wavelength_index):
        """
        The function takes the index value for the desired wavelength.
        Parameters
        ----------
        wavelength_index : INT
            index for desired wavelength (0, 1, 2)

        Returns
        -------

        """
        self.status = set_wavelength_idx(self.device_index, self.slot_id, wavelength_index)
        self.check_error()
        return

    def set_gating_parameters(self, gating_on_time, gating_off_time_factor, gating_enable):
        """

        Parameters
        ----------
        gating_on_time : INT
            gating on time in ns
        gating_off_time_factor : INT
            gating off time factor of the on timee
        gating_enable : BOOL
            enable or disable gating

        Returns
        -------

        """
        self.status = set_gating_data(self.device_index, self.slot_id, gating_on_time, gating_off_time_factor)
        self.check_error()
        self.status = set_gating_enabled(self.device_index, self.slot_id, gating_enable)
        self.check_error()
        return

    def get_current_status(self, verbose=True):
        """
        Get the current settings of the laser device

        Parameters
        ----------
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        out : DICT
            Current laser parameters

        """
        out = {'module_type': self.module_type,
               'slot_id': self.slot_id}

        # Get operation mode
        self.status, oper_mode_idx = get_operation_mode(self.device_index, self.slot_id)
        self.check_error()
        self.status, oper_mode = decode_operation_mode(self.device_index, self.slot_id, oper_mode_idx)
        self.check_error()
        out['Operation mode'] = oper_mode

        # Get trigger source
        self.status, trg_src_idx = get_trigger_source(self.device_index, self.slot_id)
        self.check_error()
        self.status, trg_src, freq_enable, t_lvl_enable = decode_trigger_source(self.device_index, self.slot_id,
                                                                                trg_src_idx)
        self.check_error()
        out['Trigger source'] = trg_src
        out['Frequency enabled'] = freq_enable
        out['Trigger level enabled'] = t_lvl_enable

        # Get trigger level
        self.status, trg_level = get_trigger_level(self.device_index, self.slot_id)
        self.check_error()
        out['Trigger level'] = trg_level

        # Get trigger level limits
        self.status, min_lvl, max_lvl, lvl_res = get_trigger_level_limits(self.device_index, self.slot_id)
        self.check_error()
        out['Trigger level min'] = min_lvl
        out['Trigger level max'] = max_lvl
        out['Trigger level resolution'] = lvl_res

        # Get frequency
        self.status, frequency = get_frequency(self.device_index, self.slot_id)
        self.check_error()
        out['Frequency'] = frequency

        # Get frequency limits
        self.status, min_freq, max_freq = get_frequency_limits(self.device_index, self.slot_id)
        self.check_error()
        out['Frequency min'] = min_freq
        out['Frequency max'] = max_freq

        # Get gating data
        self.status, on_time, off_time_factor = get_gating_data(self.device_index, self.slot_id)
        self.check_error()
        out['Gating on time'] = on_time
        out['Gating off time factor'] = off_time_factor

        # Get gating limits
        self.status, min_on_time, max_on_time, min_off_time_factor, max_off_time_factor = get_gating_limits(
            self.device_index, self.slot_id)
        self.check_error()
        out['Gating min on time'] = min_on_time
        out['Gating max on time'] = max_on_time
        out['Gating min off time factor'] = min_off_time_factor
        out['Gating max off time factor'] = max_off_time_factor

        # Get gating enabled
        self.status, gating_enabled = get_gating_enabled(self.device_index, self.slot_id)
        self.check_error()
        out['Gating enabled'] = gating_enabled

        # Get gate high impedance
        self.status, high_impedance = get_gate_high_impedance(self.device_index, self.slot_id)
        self.check_error()
        out['Gate high impedance'] = high_impedance

        # Get wavelength index
        self.status, wl_idx = get_wavelength_idx(self.device_index, self.slot_id)
        self.check_error()
        self.status, wavelength = decode_wavelength(self.device_index, self.slot_id, wl_idx)
        self.check_error()
        out['Current Wavelength'] = wavelength
        out['Current wavelength index'] = wl_idx

        # Get intensity
        self.status, intensity = get_intensity(self.device_index, self.slot_id, wl_idx)
        self.check_error()
        out['Intensity'] = intensity

        if verbose:
            for k in out.keys():
                print(f'{k}: {out[k]}')
        return out

    def device_information(self, verbose=True):
        """

        Parameters
        ----------
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        out : DICT
            Fundamental information on the laser.

        """
        out = {'module_type': self.module_type,
               'slot_id': self.slot_id}

        self.status, device_id, device_type, fw_version, wl_count = get_device_info(self.device_index, self.slot_id)
        out['Device ID'] = device_id
        out['Device Type'] = device_type
        out['Firmware Version'] = fw_version
        out['Number of wavelengths available'] = wl_count
        self.check_error()
        if verbose:
            for k in out.keys():
                print(f'{k}: {out[k]}')
        return out














