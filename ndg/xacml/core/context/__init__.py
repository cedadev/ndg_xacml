"""NDG XACML context package defines classes for types in the access control
context schema

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "24/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.utils import TypedList
from ndg.xacml.core import XacmlCoreBase
from ndg.xacml.core.attribute import Attribute


class XacmlContextBase(XacmlCoreBase):
    """Base class for XACML Request and Response types
    
    @cvar ELEMENT_LOCAL_NAME: XML local element name, derived classes should
    set
    @type ELEMENT_LOCAL_NAME: None"""
    XACML_2_0_CONTEXT_NS = XacmlCoreBase.XACML_2_0_NS_PREFIX + ':context:schema:os'
    XACML_2_0_CONTEXT_NS_PREFIX = 'xacml-context'

    ELEMENT_LOCAL_NAME = None
    __slots__ = ()
    
    def __init__(self):
        """ELEMENT_LOCAL_NAME check makes this class virtual - derived classes
        must override this method and set ELEMENT_LOCAL_NAME to the appropriate
        string
        """
        super(XacmlContextBase, self).__init__()
        if self.__class__.ELEMENT_LOCAL_NAME is None:
            raise NotImplementedError('Set "ELEMENT_LOCAL_NAME" in a derived '
                                      'type')

    def __getstate__(self):
        '''Enable pickling
        
        @return: object's attribute dictionary
        @rtype: dict
        '''
        _dict = super(XacmlContextBase, self).__getstate__()
        for attrName in XacmlContextBase.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_XacmlContextBase" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict

    def __setstate__(self, attrDict):
        '''Explicit implementation needed with __slots__'''
        for attr, val in attrDict.items():
            setattr(self, attr, val)

class RequestChildBase(XacmlContextBase):
    """Base class for XACML Context Subject, Resource, Action and Environment
    types
    
    @ivar __attributes: XACML Context subject attributes
    @type __attributes: ndg.xacml.utils.TypedList
    """
    __slots__ = ('__attributes', )
    
    def __init__(self):
        """Initialise attribute list"""
        super(RequestChildBase, self).__init__()
        self.__attributes = TypedList(Attribute)
        
    @property
    def attributes(self):
        """
        @return: XACML Context subject attributes
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__attributes

    def __getstate__(self):
        '''Enable pickling
        
        @return: object's attribute dictionary
        @rtype: dict
        '''
        _dict = super(RequestChildBase, self).__getstate__()
        for attrName in RequestChildBase.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_RequestChildBase" + attrName
            _dict[attrName] = getattr(self, attrName)
        return _dict
