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

from ndg.xacml.core.attributevalue import AttributeValueClassFactory
from ndg.xacml.core.context.exceptions import MissingAttributeError
from ndg.xacml.core.context.request import Request
from ndg.xacml.core.expression import Expression
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.utils import TypedList


class AttributeSelector(Expression):
    '''XACML Attribute Selector type 
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string    
    @cvar REQUEST_CONTEXT_PATH_ATTRIB_NAME: request context XML attribute name
    @type REQUEST_CONTEXT_PATH_ATTRIB_NAME: string
    @cvar MUST_BE_PRESENT_ATTRIB_NAME: must be present XML attribute name
    @type MUST_BE_PRESENT_ATTRIB_NAME: string

    @ivar __attributeValueFactory: When evaluating matches, use an attribute 
    value class factory to create attribute values for match bag of the correct 
    DataType to respect type based rule functions
    @type __attributeValueFactory: ndg.xacml.core.attributevalue.AttributeValueClassFactory
    '''
    ELEMENT_LOCAL_NAME = 'AttributeSelector'
    MUST_BE_PRESENT_ATTRIB_NAME = 'MustBePresent'
    REQUEST_CONTEXT_PATH_ATTRIB_NAME = 'RequestContextPath'
    
    __slots__ = ('__mustBePresent',
                 '__requestContextPath',
                 '__attributeValueFactory'
                 )

    def __init__(self):
        '''XACML Attribute Selector type 
        '''
        super(AttributeSelector, self).__init__()
        self.__mustBePresent = None
        self.__requestContextPath = None

        # When evaluating matches, use an attribute value class factory to 
        # create attribute values for match bag of the correct DataType to 
        # respect type based rule functions
        self.__attributeValueFactory = AttributeValueClassFactory()
        
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

    @property
    def attributeValueFactory(self):
        """Get Attribute Value factory function
        
        @return: attribute value factory instance
        @rtype: ndg.xacml.core.attributevalue.AttributeValueClassFactory
        """
        return self.__attributeValueFactory 

    def evaluate(self, context):
        """Evaluates an XPath expression with the context node being the request
        using the XPath selector set in the context.
        @type context: ndg.xacml.core.context.request.Request
        @param context: request context
        @rtype: bag of dataType
        @return: bag of matched values
        """
        if not isinstance(context, Request):
            raise TypeError('Expecting %r type for context input; got %r' %
                            (Request, type(context)))
        
        log.debug("In AttributeSelector for path %r", self.requestContextPath)

        if not context.attributeSelector:
            raise ValueError('Attribute selector not set in Request object.')

        # Create the return value bag.
        dataType = self.dataType
        attributeValueClass = self.attributeValueFactory(dataType)
        if attributeValueClass is None:
            raise XMLParseError("No Attribute Value class available for "
                                "type %r" % dataType)
        attributeValueBag = TypedList(attributeValueClass)

        # Get the matched values and add to the bag as attributes of the
        # required type.
        values = context.attributeSelector.selectText(self.requestContextPath)
        for value in values:
            attributeValue = attributeValueClass()
            attributeValue.dataType = dataType
            attributeValue.value = value
            attributeValueBag.append(attributeValue)

        if len(attributeValueBag) == 0 and self.mustBePresent:
            raise MissingAttributeError('"MustBePresent" is set for '
                                        'AttrubuteSelector for path %r' %
                                        self.requestContextPath)

        return attributeValueBag
