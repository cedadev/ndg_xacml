"""XACML CombinerParameter type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"

class CombinerParameter(object):
    '''XACML Combiner parameter class - currently not implemented
    
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    '''
    ELEMENT_LOCAL_NAME = "CombinerParameter"
    __slots__ = ()

    def __init__(self):
        '''@raise NotImplementedError: this class is a stub only
        '''
        raise NotImplementedError('Not currently implemented')