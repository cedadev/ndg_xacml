"""NDG XACML AttributeSelector type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.core.expression import Expression


class AttributeSelector(Expression):
    '''XACML Attribute Selector type 
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string    
    @cvar REQUEST_CONTEXT_PATH_ATTRIB_NAME: request context XML attribute name
    @type REQUEST_CONTEXT_PATH_ATTRIB_NAME: string
    @cvar MUST_BE_PRESENT_ATTRIB_NAME: must be present XML attribute name
    @type MUST_BE_PRESENT_ATTRIB_NAME: string

    '''
    ELEMENT_LOCAL_NAME = 'AttributeSelector'
    MUST_BE_PRESENT_ATTRIB_NAME = 'MustBePresent'
    REQUEST_CONTEXT_PATH_ATTRIB_NAME = 'RequestContextPath'
    
    __slots__ = ('__mustBePresent', '__requestContextPath')

    def __init__(self):
        '''XACML Attribute Selector type 
        '''
        super(AttributeSelector, self).__init__()
        self.__mustBePresent = None
        self.__requestContextPath = None
        
    @property
    def requestContextPath(self):
        """Get request context path
        @return: request context path
        @rtype: basestring
        """
        return self.__requestContextPath

    @requestContextPath.setter
    def requestContextPath(self, value):
        """Set request context path
        @param value: request context path
        @type value: basestring
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "requestContextPath" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__requestContextPath = value   

    @property
    def mustBePresent(self):
        """Get Must Be Present flag
        @return: must be present flag
        @rtype: bool
        """
        return self.__mustBePresent

    @mustBePresent.setter
    def mustBePresent(self, value):
        """Set Must Be Present flag
        @param value: must be present flag
        @type value: bool
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, bool):
            raise TypeError('Expecting %r type for "mustBePresent" '
                            'attribute; got %r' % (bool, type(value)))
            
        self.__mustBePresent = value 

    def evaluate(self, context):
        """Placeholder to override abstract method and enable this class to be
        instantiated.  However, AttributeSelectors are not fully implemented so
        this method raises a not implemented error.
        """
        raise NotImplementedError('PDP evaluation for AttributeSelectors is '
                                  'not currently implemented')