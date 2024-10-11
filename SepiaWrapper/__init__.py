# -*- coding: utf-8 -*-
"""
# =============================================================================
#  Packages a simple wrapper for the Sepia2 API
# =============================================================================

Implemented at the moment:
    - change internal trigger frequency for SOM and SOMD
    - set delays for SOMD
    - configure burst array
    - change intensity for SLM
    
Not implemented:
    - Any settings for external triggering
    - Any laser modules other than SLM
    - combiner
    - Most hardware function (Firmware version, Temperatures ...)

@author: Johan Hummert
"""

# Higher level classes and functions
from .sepia2_class import sepia2
from .utilities import *

# submodules capsulating the DLL functions
from . import library
from . import firmware
from . import usb
from . import common
from . import scm
from . import som_somd
from . import slm
    
        
            
            
        
        
        
        