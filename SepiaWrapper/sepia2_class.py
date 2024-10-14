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

class SepiaLibError(Exception):
    pass

class SepiaWrapperError(Exception):
    pass

class sepia2:
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
        
    def __init__(self, device_index, restart=False, verbose=False):
        '''
        
        Initiate the class. Connects to the laser driver with the USB index
        deviceidx. Gets the module map and creates submodules.
        
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
        # initiate USB connection
        self.status, self.productmodel, self.serialnumber = open_device(self.device_index)
        # return if no device found
        self.check_error()
        # Number of connected modules
        self.status, self.module_count = get_module_map(self.device_index, restart=restart)
        self.check_error()
        # Modules
        self.modules = []
        self.lasers = []
        self.oscillator = None
        self.safety = None
        for I in range(self.module_count):
            # Get Module information
            self.status, slot_id, is_primary, is_backplane, has_uptime_counter = get_module_info_by_map_index(self.device_index, I)
            self.check_error()
            # get module type
            self.status, module_type = get_module_type(self.device_index, slot_id, is_primary)
            self.check_error()
            # decode to module name abbreviation
            self.status, module_type = decode_module_type_abbreviated(module_type)
            self.check_error()
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
        self.check_error()
        if is_open:
            # soft lock laser
            set_laser_softlocked(self.device_index, self.safety['slot_id'], True)
            self.check_error()
            # clear module map
            self.status = free_module_map(self.device_index)
            self.check_error()
            # close USB connection
            self.status = close_device(self.device_index)
            self.check_error()
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
        self.check_error()      
        # close USB connection
        self.status = close_device(self.device_index)
        self.check_error()
        return
    
    def unlock(self):
        '''
        Unlock the softlock

        Returns
        -------
        None.

        '''
        self.status = set_laser_softlocked(self.device_index, self.safety['slot_id'], False)
        self.check_error()
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
            frequency_out = self.oscillator.set_clock_internal(frequency)
            # Set burst values
            self.oscillator.set_burst_array([1,0,0,0,0,0,0,0])
            # Enable output
            self.oscillator.set_output(index, 0, False)
            # set delay
            if delay is not None:
                delay_out, _ = self.oscillator.set_delay(index, delay, 0)
            # Set pulsed and external trigger
            self.lasers[index].set_pulse_parameters(7, True)
        # set intensity
        self.lasers[index].set_intensity(intensity)
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
            
            
            
    
    
        
        
            
            
        
        
        
        
