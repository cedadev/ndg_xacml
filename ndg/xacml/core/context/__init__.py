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
    ELEMENT_LOCAL_NAME = None
    __slots__ = ()
    
    def __init__(self):
        """ELEMENT_LOCAL_NAME check makes this class virtual - derived classes
        must override this method and set ELEMENT_LOCAL_NAME to the appropriate
        string
        """
        if self.__class__.ELEMENT_LOCAL_NAME is None:
            raise NotImplementedError('Set "ELEMENT_LOCAL_NAME" in a derived '
                                      'type')
    
   
class RequestChildBase(XacmlContextBase):
    """Base class for XACML Context Subject, Resource, Action and Environment
    types
    
    @ivar __attributes: XACML Context subject attributes
    @type __attributes: ndg.xacml.utils.TypedList
    """
    __slots__ = ('__attributes', )
    
    def __init__(self):
        """Initialise attribute list"""
        self.__attributes = TypedList(Attribute)
        
    @property
    def attributes(self):
        """
        @return: XACML Context subject attributes
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__attributes
    