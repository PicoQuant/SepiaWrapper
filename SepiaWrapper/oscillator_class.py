# -*- coding: utf-8 -*-
"""
Provides the oscillator class for simpler control of SLM laser devices

@author: Johan Hummert
"""

from .library import decode_error
from .som_somd import get_out_and_sync_enable, set_out_and_sync_enable
from .som_somd import set_freq_trigger_mode, get_freq_trigger_mode, decode_freq_trigger_mode
from .som_somd import get_burst_values, set_burst_values 
from .som_somd import get_delay_units, get_seq_output_infos, set_seq_output_infos
from .som_somd import get_burst_length_array, set_burst_length_array
from .som_somd import get_sequencer_control, set_sequencer_control, decode_sequencer_auxin_control

class oscillator:
    def check_error(self):
        '''
        Check for errors in calls to the Sepia2 API.
        
        Returns
        -------
        bool
        
        '''
        if self.status != 0:
            return True   
        else:
            return False
        
    def __init__(self, device_index, slot_id, module_type):
        '''        
        Parameters
        ----------
        deviceidx : INT
            USB index for the laser driver (0...7)

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode

        '''
        self.device_index = device_index
        self.status = 0
        self.error = 'No Error'
        self.slot_id = slot_id
        self.module_type = module_type
        self.status = self.set_sequencer(False, 0)
        return self.status
    
    def set_output(self, output, sync=None, sync_invert=None):
        '''
        Enable output for lasers based on a tuple, for instance (1, 5) will enable the second and 6th laser.
        sync and sync invert can also be set.
        
        Parameters
        ----------
        output : INT or TUPLE
            Which lasers to turn on 
        str_sync : INT or TUPLE, optional
            For which lasers to enable sync. If None the sync pattern will be left unchanged. default is None.
        sync_inverse : BOOL, optional
            whether to invert the sync. if None will be left unchanged. The default is None.

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode

        '''
        self.status, _, sync_before, invert_before = get_out_and_sync_enable(self.device_index,
                                                                             self.slot_id,
                                                                             self.module_type)
        if self.check_error():
            return self.status
        # Generate output bitstring
        output_array = [0]*8
        if type(output) is int:
            output_array[output] = 1
        elif type(output) is list or type(output) is tuple:
            for I in output:
                output_array[I] = 1
        elif output is None:
            pass
        output_bitstring = ''.join(map(str, output_array[::-1]))
        if sync is None:
            sync_bitstring = sync_before
        else:
            # Generate sync bitstring
            sync_array = [0]*8
            if type(sync) is int:
                sync_array[sync] = 1
            else:
                for I in sync:
                    sync_array[I] = 1
            sync_bitstring = ''.join(map(str, sync_array[::-1])) 
        if sync_invert is None:
            sync_invert = invert_before
        self.status = set_out_and_sync_enable(self.device_index, self.slot_id, self.module_type,
                                              output_bitstring, sync_bitstring, sync_invert)
        if self.check_error():
            return self.status
        return self.status
    
    def set_clock_internal(self, target_frequency):
        '''
        Set main clock frequency as 80MHz/divider. Only works for internal triggering
        and only for SOM and SOMD oscillators
        
        Parameters
        ----------
        target_frequency : FLOAT
            Main clock frequency to set in MHz.

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode
        actual_frequency : FLOAT
            Main clock frequency that is set after function call

        '''
        divider = round(80/target_frequency)
        if self.module_type == 'SOMD':
            # divider 16bit
            divider = min(divider, 65536)
        elif self.module_type == 'SOM':
            divider = min(divider, 255)
        actual_frequency = 80/divider
        # Set to internal Trigger 80MHz
        self.status = set_freq_trigger_mode(self.device_index, self.slot_id, self.module_type, 2)
        if self.check_error():
            return self.status, None
        # set divider
        self.status = set_burst_values(self.device_index, self.slot_id, self.module_type,
                                       divider, 0, 0)
        return self.status, actual_frequency
        
    def set_sequencer(self, aux_out, aux_in):
        '''
        Set the sequencer oux controls

        Parameters
        ----------
        aux_out : BOOL
            Wether to turn on aux_out
        aux_in : INT
            0: free running, 1: on aux high, 2: on aux low, 3: disabled

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode

        '''
        self.status = set_sequencer_control(self.device_index, self.slot_id, self.module_type, aux_out, aux_in)
        return self.status
    
    def set_delay(self, laser, delay_coarse, delay_fine):
        '''
        Set the delay for one laser. Sets both coarse and fine delay. The lasers are
        identified by numbers 0...7. This will disable burst combination for this laser.
        
        Parameters
        ----------
        laser : INT
            Position of the laser module (1...8).
        delay_coarse : FLOAT
            Target coarse delay to set for this laser in ns
        delay_fine : INT
            Target fine delay to set for this laser in steps

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode
        delay_coarse : FLOAT
            Coarse delay set for this laser after function call
        delay_fine : INT
            Fine delay set for this laser after function call

        '''
        self.status, coarse_step, fine_delay_max = get_delay_units(self.device_index, 
                                                                   self.slot_id)
        if self.check_error():
            return self.status, None, None
        coarse_step = 1e9 * coarse_step
        target_coarse = coarse_step * (delay_coarse // coarse_step)
        if delay_fine > fine_delay_max:
            delay_fine = fine_delay_max
        self.status = set_seq_output_infos(self.device_index, self.slot_id, laser,
                                           True, '00000001', False,
                                           target_coarse, delay_fine)
        if self.check_error():
            return self.status, None, None
        self.status, _, _, _, _, delay_coarse, delay_fine = get_seq_output_infos(self.device_index, self.slot_id, laser)
        if self.check_error():
            return self.status, None, None
        return self.status, delay_coarse, delay_fine
        
    def set_burst_array(self, burst_values):
        '''
        Set the burst array (i.e. burst values for all channels)
        
        Parameters
        ----------
        burst_values : LIST
            Burst values for all channels. Needs to contain 8 values.

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode

        '''
        self.status = set_burst_length_array(self.device_index, self.slot_id, self.module_type,
                                             burst_values)
        self.check_error()
        return self.status
    
    def set_combiner(self, laser, combination, masked):
        '''
        Set the combiner for one channel

        Parameters
        ----------
        laser : INT
            Which channel to set.
        combination : INT or LIST
            Which channels to combine. If INT only one channel is activated
        masked : INT
            Whether to use combiner mask

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode

        '''
        # get delays to leave them unchanged
        self.status, _, _, _, _, delay_coarse, delay_fine = get_seq_output_infos(self.device_index, self.slot_id, laser)
        if self.check_error():
            return self.status
        # Generate combination bitstring
        comb_array = [0]*8
        if type(combination) is int:
            comb_array[combination] = 1
        elif type(combination) is list or type(combination) is tuple:
            for I in combination:
                comb_array[I] = 1
        comb_bitstring = ''.join(map(str, comb_array[::-1]))
        # set sequencer info
        self.status = set_seq_output_infos(self.device_index, self.slot_id, laser, False, comb_bitstring, masked, delay_coarse, delay_fine)
        return self.status
        
    
    def get_current_status(self, verbose=True):
        '''
        Get the current oscillator parameters for all channels.

        Parameters
        ----------
        verbose : TYPE, optional
            If True will print the current settings. The default is True.

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode.
        out : DICT
            Current oscillator parameters

        '''
        out = {'module_type': self.module_type,
               'slot_id': self.slot_id}
        self.status, trigger_mode, sync_now = get_freq_trigger_mode(self.device_index, self.slot_id, self.module_type)
        if self.check_error():
            return self.status, None
        self.status, trigger_mode_str = decode_freq_trigger_mode(self.device_index, self.slot_id, self.module_type, trigger_mode)
        if self.check_error():
            return self.status, None
        # Trigger Mode
        out['trigger_mode'] = trigger_mode_str
        self.status, divider, presync, mask_sync = get_burst_values(self.device_index, self.slot_id, self.module_type)
        if self.check_error():
            return self.status, None
        out['divider'] = divider
        if trigger_mode == 2:
            out['clock frequency'] = 80/divider
        out['presync'] = presync
        out['mask_sync'] = mask_sync
        # Burst Array
        self.status, burst_array = get_burst_length_array(self.device_index, self.slot_id, self.module_type)
        if self.check_error():
            return self.status, None
        out['burst_array'] = burst_array
        # Out and Sync
        self.status, output, sync, sync_invert = get_out_and_sync_enable(self.device_index, self.slot_id, self.module_type)
        if self.check_error():
            return self.status, None
        out['output_enabled'] = [I for I in range(len(output)) if int(output[::-1][I])]
        out['sync_enabled'] = [I for I in range(len(sync)) if int(sync[::-1][I])]
        out['sync_mask_inverted'] = sync_invert
        # Sequencer Control
        self.status, auxin, auxout = get_sequencer_control(self.device_index, self.slot_id, self.module_type)
        if self.check_error():
            return self.status, None
        self.status, auxin_str = decode_sequencer_auxin_control(auxin, self.module_type)
        if self.check_error():
            return self.status, None
        out['sequencer'] = auxin_str
        out['sequencer_AuxOut'] = auxout
        # Sequencer Info
        if self.module_type == 'SOMD':
            for chan in range(8):
                self.status, delayed, force_undelayed, out_combi, masked_combi, delay_coarse, delay_fine = get_seq_output_infos(self.device_index, self.slot_id, chan)
                if self.check_error():
                    return self.status, None
                if delayed and not force_undelayed:
                    out['Channel_'+str(chan)] = 'delayed {:.2f} ns and {:d} a.u.'.format(delay_coarse, delay_fine)
                else:
                    comb = [I for I in range(len(out_combi)) if int(out_combi[::-1][I])]
                    out['Channel_'+str(chan)] = 'undelayed, combining {:s}, Masked: {:s}'.format(str(comb), str(masked_combi))
        if verbose:
            for k in out.keys():
                print(k, out[k])
        return self.status, out 
            
        
        
        
        
        
        
        
        
        
        
        
    
    
        
        
            
            
        
        
        
        
