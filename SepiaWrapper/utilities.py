# -*- coding: utf-8 -*-

from .library import decode_error, get_version, get_usb_version
from .usb import open_get_serial_number_and_close

def list_devices(verbose=True):
    '''
    List available devices

    Parameters
    ----------
    verbose : BOOL, optional
        If True, print list of devices. The default is True.

    Returns
    -------
    devices : DICT
        Dictionary containing some info on connected devices.

    '''
    devices = {'index': [],
               'product_model': [],
               'serial_number': []
               }
    for I in range(8):
        status, model, snr  = open_get_serial_number_and_close(I)
        if status == 0:
            devices['index'].append(I)
            devices['product_model'].append(model)
            devices['serial_number'].append(snr)
            print('Device {:d}: {:s}, serial number {:s}'.format(I, model, snr))
    return devices
    
            