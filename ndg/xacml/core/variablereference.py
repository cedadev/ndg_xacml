"""NDG Security Variable Reference type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "29/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core import XacmlPolicyBase


class VariableReference(XacmlPolicyBase):
    '''XACML Variable Reference Type - this class is a placeholder, it's not 
    currently implemented
    
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    '''
    ELEMENT_LOCAL_NAME = "VariableReference"

    __slots__ = ()
    
    def __init__(self):
        '''This class not needed yet'''
        raise NotImplementedError()