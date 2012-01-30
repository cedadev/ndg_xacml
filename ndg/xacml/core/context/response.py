"""NDG XACML module for Response type 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "23/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.utils import TypedList
from ndg.xacml.core.context import XacmlContextBase
from ndg.xacml.core.context.result import Result


class Response(XacmlContextBase):
    """XACML Response type
    @cvar ELEMENT_LOCAL_NAME: XML local element name for the response
    @type ELEMENT_LOCAL_NAME: string

    @ivar __results: resource content
    @type __results: ndg.xacml.utils.TypedList
    """
    ELEMENT_LOCAL_NAME = 'Response'
    
    __slots__ = ('__results', )
    
    def __init__(self):
        """"Initialise results list"""
        super(Response, self).__init__()
        self.__results = TypedList(Result)
        
    @property
    def results(self):
        """Get Response results list
        
        @return: results list
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__results

    def __getstate__(self):
        '''Enable pickling
        
        @return: object's attribute dictionary
        @rtype: dict
        '''
        _dict = super(Response, self).__getstate__()
        for attrName in Response.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_Response" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict
