# -*- coding: utf-8 -*-
"""
Provides the sepia2 class for simpler control of PDL 828 driver devices

@author: Johan Hummert
"""

from .library import decode_error
from .usb import open_device, is_open_device, close_device
from .firmware import get_module_map, get_module_info_by_map_index, free_module_map
from .common import get_module_type, decode_module_type, decode_module_type_abbreviated
from .scm import set_laser_softlocked, get_laser_locked

from .oscillator_class import oscillator
from .laser_class import laser


class sepia2:
    def check_error(self):
        '''
        Check for errors in calls to the Sepia2 API.
        
        Returns
        -------
        bool
        
        '''
        if self.status != 0:
            # decode error message
            self.status, self.error = decode_error(self.status)
            print(self.error)
            return True   
        else:
            return False
        
    def __init__(self, device_index, restart=False, verbose=False):
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
        None.

        '''
        self.device_index = device_index
        self.status = 0
        self.error = 'No Error'
        # initiate USB connection
        self.status, self.productmodel, self.serialnumber = open_device(self.device_index)
        # return if no device found
        if self.check_error():
            return
        # Number of connected modules
        self.status, self.module_count = get_module_map(self.device_index, restart=restart)
        if self.check_error():
            return
        # Modules
        self.modules = []
        self.lasers = []
        self.oscillator = None
        self.safety = None
        for I in range(self.module_count):
            # Get Module information
            self.status, slot_id, is_primary, is_backplane, has_uptime_counter = get_module_info_by_map_index(self.device_index, I)
            if self.check_error():
                return
            # get module type
            self.status, module_type = get_module_type(self.device_index, slot_id, is_primary)
            if self.check_error():
                return
            # decode to module name abbreviation
            self.status, module_type = decode_module_type_abbreviated(module_type)
            if self.check_error():
                return
            # write into modules
            module = {'slot_id': slot_id,
                      'is_primary': is_primary,
                      'is_backplane': is_backplane,
                      'has_uptime_counter': has_uptime_counter,
                      'module_type': module_type}
            self.modules.append(module)
            # set up modules if implemented
            if module_type == 'SOM' or module_type == 'SOMD':
                self.oscillator = oscillator(self.device_index, slot_id, module_type)
            elif module_type == 'SCM':
                self.safety = module
            elif module_type == 'SLM':
                self.lasers.append(laser(self.device_index, slot_id, module_type))
        if verbose:
            # Print some sort of welcome message
            print('Connected to {:s}, SNR {:s}'.format(self.productmodel, self.serialnumber))
            if oscillator is not None:
                print('{:s} oscillator module'.format(self.oscillator.module_type))
            for I in range(len(self.lasers)):
                print('Laser Module {:d}: {:s}'.format(I, self.lasers[I].module_type))
        # set up oscillator module
        return
            
    def __del__(self):
        '''
        class destructor. Will softlock the laser if USB connection is left open.
        It is advisable to close connection with close, which will not lock the laser.

        Returns
        -------
        None.

        '''
        self.status, is_open = is_open_device(self.device_index)
        if self.check_error():
            return
        if is_open:
            # soft lock laser
            set_laser_softlocked(self.device_index, self.safety['slot_id'], True)
            if self.check_error():
                return
            # clear module map
            self.status = free_module_map(self.device_index)
            if self.check_error():
                return        
            # close USB connection
            self.status = close_device(self.device_index)
            if self.check_error():
                return
        return
        
    def close(self):
        '''
        Close USB connection. Laser will be left running if it was running.

        Returns
        -------
        None.

        '''
        # clear module map
        self.status = free_module_map(self.device_index)
        if self.check_error():
            return        
        # close USB connection
        self.status = close_device(self.device_index)
        if self.check_error():
            return
        return
    
    def unlock(self):
        '''
        Unlock the softlock

        Returns
        -------
        None.

        '''
        self.status = set_laser_softlocked(self.device_index, self.safety['slot_id'], False)
        if self.check_error():
            return
        return
    
    def lock(self):
        '''
        Lock the softlock

        Returns
        -------
        None.

        '''
        self.status = set_laser_softlocked(self.device_index, self.safety['slot_id'], True)
        self.check_error()
        return
        
    
    def start_laser_simple(self, index, frequency, intensity, delay=None):
        '''
        Start a single laser (and turn all others off). Will reset burst values and set internal triggering.

        Parameters
        ----------
        index : INT
            Laser index (0...7). If there is no SLM device at this index, will return an error.
        frequency : FLOAT
            Repetition rate in MHz
        intensity : FLOAT
            Intensity in %
        delay : FLOAT, optional
            Coarse delay in ns. If None, delay will be left unchanged. The default is None.

        Returns
        -------
        delay_out : FLOAT
            Coarse delay set
        frequency_out : FLOAT
            Frequency set

        '''
        # Unlock
        self.unlock()
        if self.oscillator is not None:
            # Set trigger frequency
            self.status, frequency_out = self.oscillator.set_clock_internal(frequency)
            if self.check_error():
                return
            # Set burst values
            self.status = self.oscillator.set_burst_array([1,0,0,0,0,0,0,0])
            if self.check_error():
                return
            # Enable output
            self.status = self.oscillator.set_output(index, 0, False)
            if self.check_error():
                return
            # set delay
            if delay is not None:
                self.status, delay_out, _ = self.oscillator.set_delay(index, delay, 0)
                if self.check_error():
                    return
            # Set pulsed and external trigger
            self.status = self.lasers[index].set_pulse_parameters(7, True)
            if self.check_error():
                return
        # set intensity
        self.status = self.lasers[index].set_intensity(intensity)
        if self.check_error():
            return
        return delay_out, frequency_out
        
    def stop_lasers(self):
        '''
        Turn output off for all lasers.

        Returns
        -------
        None.

        '''
        if self.oscillator is not None:
            self.status = self.oscillator.set_output(None)
            self.check_error()
            return
            
            
            
    
    
        
        
            
            
        
        
        
        
