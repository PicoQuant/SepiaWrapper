# -*- coding: utf-8 -*-

"""
Provides the laser class for simpler control of SLM laser devices

@author: Johan Hummert
"""

from .library import decode_error
from .slm import get_intensity_fine_step, set_intensity_fine_step, get_pulse_parameters, set_pulse_parameters
from .slm import decode_head_type, decode_freq_trigger_mode

class SepiaLibError(Exception):
    pass

class SepiaWrapperError(Exception):
    pass

class laser:
    def check_error(self):
        '''
        Check for errors in calls to the Sepia2 API.
        
        Returns
        -------
        none
        
        '''
        if self.status != 0:
            # decode error message
            self.status, error = decode_error(self.status)
            if self.status == 0:
                raise SepiaLibError(error)
            else:
                self.status, error = decode_error(self.status)
                raise SepiaLibError(error)
        
    def __init__(self, device_index, slot_id, module_type):
        '''
        
        Initiate the class.
        
        Parameters
        ----------
        deviceidx : INT
            USB index for the laser driver (0...7)

        Returns
        -------
        none


        '''
        self.device_index = device_index
        self.status = 0
        self.slot_id = slot_id
        self.module_type = module_type
        return
    
    def set_intensity(self, intensity):
        '''
        Set intensity for the laser

        Parameters
        ----------
        intensity : FLOAT
            Intensity value in %

        Returns
        -------
        none

        '''
        if self.module_type == 'SLM':
            self.status = set_intensity_fine_step(self.device_index, self.slot_id, round(intensity*10))
            self.check_error()
        return
    
    def set_pulse_parameters(self, trigger, pulsed):
        '''
        Set pulse parameters for the laser pulse

        Parameters
        ----------
        trigger : INT
            Trigger mode (e.g. 7 for external falling to use the laser with oscillator)
        pulsed : BOOL
            True if pulsed, False for off / CW
            

        Returns
        -------
        none
        
        '''
        if self.module_type == 'SLM':
            self.status = set_pulse_parameters(self.device_index, self.slot_id, trigger, pulsed)
            self.check_error()
        return
        
    def get_current_status(self, verbose=True):
        '''
        Get the current settings of the laser device

        Parameters
        ----------
        verbose : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        status : INT
            0 if successful, otherwise errorcode.
        out : DICT
            Current laser parameters

        '''
        out = {'module_type': self.module_type,
               'slot_id': self.slot_id}
        if self.module_type == 'SLM':
            self.status, trigger, pulsed, head_type = get_pulse_parameters(self.device_index, self.slot_id)
            self.check_error()
            out['trigger'] = trigger
            out['pulsed'] = pulsed
            self.status, head_type = decode_head_type(head_type)
            out['head_type'] = head_type
            self.check_error()
            self.status, trigger_mode = decode_freq_trigger_mode(trigger)
            out['trigger_mode'] = trigger_mode
            self.check_error()
            self.status, intensity = get_intensity_fine_step(self.device_index, self.slot_id)
            out['intensity'] = intensity/10
            self.check_error()
        if verbose:
            for k in out.keys():
                print(k, out[k])
        return out
            
            
            
        
    
    
    
    
        
        
            
            
        
        
        
        
