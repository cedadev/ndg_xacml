"""NDG Security Policy Defaults type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "19/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core import XacmlCoreBase


class PolicyDefaults(XacmlCoreBase):
    """XACML PolicyDefaults type
    
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    @cvar XPATH_VERSION_ELEMENT_NAME: XML local name for XPath version element
    @type XPATH_VERSION_ELEMENT_NAME: string
   
    @ivar __xpathVersion: XPath version
    @type __xpathVersion: basestring / NoneType
    """
    ELEMENT_LOCAL_NAME = 'PolicyDefaults'
    XPATH_VERSION_ELEMENT_NAME = 'XPathVersion'
    
    __slots__ = ('__xpathVersion', )
    
    def __init__(self):
        """Initialise attributes"""
        super(PolicyDefaults, self).__init__()
        self.__xpathVersion = None
        
    def _get_xpathVersion(self):
        """@return: XPath version
        @rtype: basestring / NoneType
        """
        return self.__xpathVersion

    def _set_xpathVersion(self, value):
        """@param value: XPath version
        @type value: basestring / NoneType
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "xpathVersion" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__xpathVersion = value   

    xpathVersion = property(_get_xpathVersion, _set_xpathVersion, None, 
                            "PolicyDefaults type XPath version") 

          
