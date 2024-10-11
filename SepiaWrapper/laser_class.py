# -*- coding: utf-8 -*-

"""
Provides the laser class for simpler control of SLM laser devices

@author: Johan Hummert
"""

from .library import decode_error
from .slm import get_intensity_fine_step, set_intensity_fine_step, get_pulse_parameters, set_pulse_parameters
from .slm import decode_head_type, decode_freq_trigger_mode

class laser:
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
        
        Initiate the class. Connects to the laser driver with the USB index
        deviceidx. Gets the module map and soft-locks the laser. Laser
        will be unlocked by unlock_lasers and start_lasers_simple.
        
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
        self.error = 'No Error'
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
        status : INT
            0 if successful, otherwise errorcode

        '''
        if self.module_type == 'SLM':
            self.status = set_intensity_fine_step(self.device_index, self.slot_id, round(intensity*10))
        return self.status
    
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
        status : INT
            0 if successful, otherwise errorcode.

        '''
        if self.module_type == 'SLM':
            self.status = set_pulse_parameters(self.device_index, self.slot_id, trigger, pulsed)
        return self.status
        
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
            if self.check_error():
                return self.status, None
            out['trigger'] = trigger
            out['pulsed'] = pulsed
            self.status, head_type = decode_head_type(head_type)
            out['head_type'] = head_type
            if self.check_error():
                return self.status, None
            self.status, trigger_mode = decode_freq_trigger_mode(trigger)
            out['trigger_mode'] = trigger_mode
            if self.check_error():
                return self.status, None
            self.status, intensity = get_intensity_fine_step(self.device_index, self.slot_id)
            out['intensity'] = intensity/10
            if self.check_error():
                return self.status, None
        if verbose:
            for k in out.keys():
                print(k, out[k])
        return self.status, out
            
            
            
        
    
    
    
    
        
        
            
            
        
        
        
        
