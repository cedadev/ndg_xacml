"""NDG Security Variable Definition type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "25/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core import XacmlPolicyBase


class VariableDefinition(XacmlPolicyBase):
    '''XACML Variable Definition Type - this class is a placeholder, it's not 
    currently implemented
    
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    '''
    ELEMENT_LOCAL_NAME = "VariableDefinition"

    __slots__ = ()
    
    def __init__(self):
        '''This class not needed yet'''
        raise NotImplementedError()
        