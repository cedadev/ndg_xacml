"""NDG XACML AttributeDesignator type

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

from ndg.xacml.utils import TypedList
from ndg.xacml.core.expression import Expression
from ndg.xacml.core.attributevalue import (AttributeValue, 
                                           AttributeValueClassFactory)
from ndg.xacml.core.context.request import Request
from ndg.xacml.core.context.handler import CtxHandlerInterface
from ndg.xacml.core.context.exceptions import MissingAttributeError


class AttributeDesignator(Expression):
    '''Base class for XACML Attribute Designator types
    
    @cvar ATTRIBUTE_ID_ATTRIB_NAME: attribute ID XML attribute name
    @type ATTRIBUTE_ID_ATTRIB_NAME: string
    @cvar ISSUER_ATTRIB_NAME: issuer XML attribute name
    @type ISSUER_ATTRIB_NAME: string
    @cvar MUST_BE_PRESENT_ATTRIB_NAME: must be present XML attribute name
    @type MUST_BE_PRESENT_ATTRIB_NAME: string
    
    @ivar __attributeId: attribute ID for this designator
    @type __attributeId: basestring / NoneType
    @ivar __issuer: issuer if the designator
    @type __issuer: basestring / NoneType
    @ivar __mustBePresent: XML must be present flag
    @type __mustBePresent: bool
    @ivar __attributeValueFactory: When evaluating matches, use an attribute 
    value class factory to create attribute values for match bag of the correct 
    DataType to respect type based rule functions
    @type __attributeValueFactory: ndg.xacml.core.attributevalue.AttributeValueClassFactory
    '''
    ATTRIBUTE_ID_ATTRIB_NAME = 'AttributeId'
    ISSUER_ATTRIB_NAME = 'Issuer'
    MUST_BE_PRESENT_ATTRIB_NAME = 'MustBePresent'
    
    __slots__ = (
        '__attributeId', 
        '__issuer', 
        '__mustBePresent',
        '__attributeValueFactory'
    )
    
    def __init__(self):
        """Initialise attributes"""
        super(AttributeDesignator, self).__init__()
        self.__attributeId = None
        self.__issuer = None
        self.__mustBePresent = False
        
        # When evaluating matches, use an attribute value class factory to 
        # create attribute values for match bag of the correct DataType to 
        # respect type based rule functions
        self.__attributeValueFactory = AttributeValueClassFactory()

    @property
    def attributeId(self):
        """Get Attribute Id
        @return: attribute ID
        @rtype: basestring / NoneType
        """
        return self.__attributeId

    @attributeId.setter
    def attributeId(self, value):
        """Set Attribute Id
        @param value: attribute ID
        @type value: basestring 
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "attributeId" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__attributeId = value  
        
    @property
    def issuer(self):
        """Get Issuer
        @return: issuer
        @rtype: basestring / NoneType
        """
        return self.__issuer

    @issuer.setter
    def issuer(self, value):
        """Set Issuer
        @param value: issuer
        @type value: basestring
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "issuer" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__issuer = value   

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
                           
        
class SubjectAttributeDesignator(AttributeDesignator):
    """XACML Subject Attribute Designator type
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    """
    ELEMENT_LOCAL_NAME = 'SubjectAttributeDesignator'
    __slots__ = ()
    
    def evaluate(self, context):
        """Evaluate the result of the SubjectAttributeDesignator in a condition
        
        @param context: the request context
        @type context: ndg.xacml.core.context.request.Request
        @return: attribute value(s) resulting from execution of this expression
        in a condition
        @rtype: AttributeValue/NoneType  
        """ 
        if not isinstance(context, Request):
            raise TypeError('Expecting %r type for context input; got %r' %
                            (Request, type(context)))
        
        dataType = self.dataType
        attributeValueBag = TypedList(self.attributeValueFactory(dataType))
        attributeId = self.attributeId
        issuer = self.issuer
        
        log.debug("In SubjectAttributeDesignator for attribute %r", attributeId)
        
        if issuer is not None:
            _issuerMatch = lambda _issuer: issuer == _issuer
        else:
            _issuerMatch = lambda _issuer: True
        
        _attributeMatch = lambda attr: (attr.attributeId == attributeId and 
                                        attr.dataType == dataType and
                                        _issuerMatch(attr.issuer))
                                        
        for subject in context.subjects:  
            for attr in subject.attributes:
                if _attributeMatch(attr):
                    attributeValueBag.extend([i for i in attr.attributeValues
                                              if i.dataType == dataType])
                    
            if context.ctxHandler is not None:
                # Try querying the Policy Information Point via the Context 
                # Handler to see if values for the attribute specified in this 
                # designator can be retrieved externally. If retrieved, they're 
                # added to the bag.
                log.debug("Making query to PIP for additional subject "
                          "attributes to satify match")
                
                attributeValues = context.ctxHandler.pipQuery(context, self)
                if attributeValues is not None:
                    log.debug("PIP retrieved additional subject attributes: %r",
                              attributeValues)
                    
                    # Weed out any duplicates
                    if len(attributeValueBag) > 0:
                        filtAttributeValues = [attrVal 
                                           for attrVal in attributeValues 
                                           if attrVal not in attributeValueBag]
                    else:
                        filtAttributeValues = attributeValues
                        
                    attributeValueBag.extend(filtAttributeValues)
                    
        if len(attributeValueBag) == 0 and self.mustBePresent:
            raise MissingAttributeError('"MustBePresent" is set for %r but no '
                                        'match for attributeId=%r, dataType=%r '
                                        'and issuer=%r' % 
                                        (self.__class__.__name__,
                                         self.attributeId,
                                         self.dataType,
                                         self.issuer)) 
                        
        return attributeValueBag
        
        
class ResourceAttributeDesignator(AttributeDesignator):
    """XACML Resource Attribute Designator type
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    """
    ELEMENT_LOCAL_NAME = 'ResourceAttributeDesignator'
    __slots__ = ()
    
    def evaluate(self, context):
        """Evaluate the result of the ResourceAttributeDesignator in a condition
        
        @param context: the request context
        @type context: ndg.xacml.core.context.request.Request
        @return: attribute value(s) resulting from execution of this expression
        in a condition
        @rtype: AttributeValue/NoneType  
        """ 
        if not isinstance(context, Request):
            raise TypeError('Expecting %r type for context input; got %r' %
                            (Request, type(context)))
        
        dataType = self.dataType
        attributeValueBag = TypedList(self.attributeValueFactory(dataType))
        attributeId = self.attributeId
        issuer = self.issuer
        
        if issuer is not None:
            _issuerMatch = lambda _issuer: issuer == _issuer
        else:
            _issuerMatch = lambda _issuer: True
        
        _attributeMatch = lambda attr: (attr.attributeId == attributeId and 
                                        attr.dataType == dataType and
                                        _issuerMatch(attr.issuer))
                    
        for resource in context.resources:
            for attr in resource.attributes:
                if _attributeMatch(attr):
                    attributeValueBag.extend([i for i in attr.attributeValues
                                              if i.dataType == dataType])
                    
        if len(attributeValueBag) == 0 and self.mustBePresent:
            raise MissingAttributeError('"MustBePresent" is set for %r but no '
                                        'match for attributeId=%r, dataType=%r '
                                        'and issuer=%r' % 
                                        (self.__class__.__name__,
                                         self.attributeId,
                                         self.dataType,
                                         self.issuer)) 
                        
        return attributeValueBag
    
        
class ActionAttributeDesignator(AttributeDesignator):
    """XACML Action Attribute Designator type
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    """
    ELEMENT_LOCAL_NAME = 'ActionAttributeDesignator'
    __slots__ = ()
    
    def evaluate(self, context):
        """Evaluate the result of the ActionAttributeDesignator in a condition
        
        @param context: the request context
        @type context: ndg.xacml.core.context.request.Request
        @return: attribute value(s) resulting from execution of this expression
        in a condition
        @rtype: AttributeValue/NoneType  
        """ 
        if not isinstance(context, Request):
            raise TypeError('Expecting %r type for context input; got %r' %
                            (Request, type(context)))
        
        dataType = self.dataType
        attributeValueBag = TypedList(self.attributeValueFactory(dataType))
        attributeId = self.attributeId
        issuer = self.issuer
        action = context.action
        
        if issuer is not None:
            _issuerMatch = lambda _issuer: issuer == _issuer
        else:
            _issuerMatch = lambda _issuer: True
        
        _attributeMatch = lambda attr: (attr.attributeId == attributeId and 
                                        attr.dataType == dataType and
                                        _issuerMatch(attr.issuer))
                    
        for attr in action.attributes:
            if _attributeMatch(attr):
                attributeValueBag.extend([i for i in attr.attributeValues
                                          if i.dataType == dataType])
                    
        if len(attributeValueBag) == 0 and self.mustBePresent:
            raise MissingAttributeError('"MustBePresent" is set for %r but no '
                                        'match for attributeId=%r, dataType=%r '
                                        'and issuer=%r' % 
                                        (self.__class__.__name__,
                                         self.attributeId,
                                         self.dataType,
                                         self.issuer)) 
                        
        return attributeValueBag    
    
    
class EnvironmentAttributeDesignator(AttributeDesignator):
    """XACML Environment Attribute Designator type
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    """
    ELEMENT_LOCAL_NAME = 'EnvironmentAttributeDesignator'
    __slots__ = ()
    
    def evaluate(self, context):
        """Evaluate the result of the EnvironmentAttributeDesignator in a 
        condition
        
        @param context: the request context
        @type context: ndg.xacml.core.context.request.Request
        @return: attribute value(s) resulting from execution of this expression
        in a condition
        @rtype: AttributeValue/NoneType  
        """ 
        if not isinstance(context, Request):
            raise TypeError('Expecting %r type for context input; got %r' %
                            (Request, type(context)))
        
        dataType = self.dataType
        attributeValueBag = TypedList(self.attributeValueFactory(dataType))
        attributeId = self.attributeId
        issuer = self.issuer
        environment = context.environment
        
        if issuer is not None:
            _issuerMatch = lambda _issuer: issuer == _issuer
        else:
            _issuerMatch = lambda _issuer: True   
        
        _attributeMatch = lambda attr: (attr.attributeId == attributeId and 
                                        attr.dataType == dataType and
                                        _issuerMatch(attr.issuer))
                 
        for attr in environment.attributes:
            if _attributeMatch(attr):
                attributeValueBag.extend([i for i in attr.attributeValues
                                          if i.dataType == dataType])
                    
        if len(attributeValueBag) == 0 and self.mustBePresent:
            raise MissingAttributeError('"MustBePresent" is set for %r but no '
                                        'match for attributeId=%r, dataType=%r '
                                        'and issuer=%r' % 
                                        (self.__class__.__name__,
                                         self.attributeId,
                                         self.dataType,
                                         self.issuer)) 
                        
        return attributeValueBag