"""NDG Security Match type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "25/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.core import XacmlCoreBase
from ndg.xacml.core.attributevalue import AttributeValue
from ndg.xacml.core.attributedesignator import AttributeDesignator
from ndg.xacml.core.attributeselector import AttributeSelector
from ndg.xacml.core.functions import (FunctionMap, functionMap,
                                      UnsupportedStdFunctionError,
                                      UnsupportedFunctionError)
from ndg.xacml.core.context.exceptions import XacmlContextError


class MatchBase(XacmlCoreBase):
    """Base class for representation of SubjectMatch, ResourceMatch, 
    ActionMatch and EnvironmentMatch Target elements
    
    @cvar ELEMENT_LOCAL_NAME: XML Local Name of this element 
    @type ELEMENT_LOCAL_NAME: string
   
    @cvar MATCH_ID_ATTRIB_NAME: XML attribute name for match ID
    @type MATCH_ID_ATTRIB_NAME: string
   
    @cvar ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME: XML Local Name of attribute value
    child element 
    @type ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME: string

    @ivar __attributeValue: attribute value associated with this match
    @type __attributeValue: ndg.xacml.core.attributevalue.AttributeValue
    @ivar __attributeDesignator: attribute designator - only a designator or 
    selector may be set for a given instance not both
    @type __attributeDesignator: ndg.xacml.core.attributedesignator.AttributeDesignator
    @ivar __attributeSelector: attribute selector - only a designator or 
    selector may be set for a given instance not both
    @type __attributeSelector: ndg.xacml.core.attributeselector.AttributeSelector
    @ivar __matchId: match identifier
    @type __matchId: NoneType / basestring
    @ivar __function: function to be applied
    @type __function: ndg.xacml.core.functions.AbstractFunction derived type
    @ivar __functionMap: function mapping object to map URNs to function class
    implementations
    @type __functionMap: ndg.xacml.core.functions.FunctionMap
    @ivar __loadFunctionFromId: boolean determines whether or not to load
    function classes for given function URN in functionId set property method
    @type __loadFunctionFromId: bool
    """
    ELEMENT_LOCAL_NAME = None
    MATCH_ID_ATTRIB_NAME = 'MatchId'
    ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME = 'AttributeValue'

    __slots__ = (
        '__attributeValue', 
        '__attributeDesignator', 
        '__attributeSelector',
        '__matchId',
        '__function', 
        '__functionMap',
        '__loadFunctionFromId',
    )
    
    def __init__(self):
        """Initial attributes corresponding to the equivalent XACML schema type
        and also create a function map to map functions from MatchIds
        """
        self.__attributeValue = None
         
        # Either/or in schema
        self.__attributeDesignator = None
        self.__attributeSelector = None
        
        self.__matchId = None
        
        self.__function = None
        self.__functionMap = functionMap
        self.__loadFunctionFromId = True
        
    @property
    def attributeValue(self):
        """Match attribute value
        
        @return: attribute value
        @rtype: ndg.xacml.core.attributevalue.Attribute"""
        return self.__attributeValue
    
    @attributeValue.setter
    def attributeValue(self, value):
        """Set match attribute value.
        @param value: attribute value
        @type value: ndg.xacml.core.attributevalue.AttributeValue
        @raise TypeError: incorrect type set
        """
        if not isinstance(value, AttributeValue):
            raise TypeError('Expecting %r type for "matchId" '
                            'attribute; got %r' % 
                            (AttributeValue, type(value)))
            
        self.__attributeValue = value
        
    @property
    def attributeDesignator(self):
        """@return: attribute designator - only a designator or 
        selector may be set for a given instance not both
        @rtype: ndg.xacml.core.attributedesignator.AttributeDesignator
        """
        return self.__attributeDesignator
    
    @attributeDesignator.setter
    def attributeDesignator(self, value):
        """Set match attribute designator.  Match may have an 
        attributeDesignator or an attributeSelector setting a designator DELETES
        any attributeSelector previously set
        
        @param value: attribute selector - only a designator or 
        selector may be set for a given instance not both
        @type value: ndg.xacml.core.attributeselector.AttributeSelector  
        @raise TypeError: incorrect type for input value      
        """
        if not isinstance(value, AttributeDesignator):
            raise TypeError('Expecting %r type for "attributeDesignator" '
                            'attribute; got %r' % 
                            (AttributeDesignator, type(value)))
            
        self.__attributeDesignator = value
        self.__attributeSelector = None
 
    @property
    def attributeSelector(self):
        '''
        @return: attribute selector
        @rtype: ndg.xacml.core.attributeselector.AttributeSelector
        '''
        return self.__attributeSelector
    
    @attributeSelector.setter
    def attributeSelector(self, value):
        """Set match attribute selector.  Match may have an 
        attributeDesignator or an attributeSelector setting a selector DELETES
        any attributeDesignator previously set
        
        @param value: attribute selector
        @type value: ndg.xacml.core.attributeselector.AttributeSelector
        """
        if not isinstance(value, AttributeSelector):
            raise TypeError('Expecting %r type for "matchId" '
                            'attribute; got %r' % 
                            (AttributeSelector, type(value)))
            
        self.__attributeSelector = value
        self.__attributeDesignator = None
                       
    def _getMatchId(self):
        """Match identifier for match function
        @return: match identifier
        @rtype: NoneType / basestring
        """
        return self.__matchId

    def _setMatchId(self, value):
        """Match identifier for match function
        @param value: match identifier
        @type value: basestring
        @raise TypeError: if incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "matchId" '
                            'attribute; got %r' % type(value))
            
        self.__matchId = value
        
        # Also retrieve function for this match ID if a map has been set
        if self.__loadFunctionFromId:
            self.setFunctionFromMap(self.__functionMap)   

    matchId = property(_getMatchId, _setMatchId, None, 
                       "Match identifier for match function")
      
    @property
    def loadFunctionFromId(self):
        """Set to False to stop the functionId property set method automatically
        trying to load the corresponding function for the given functionId 

        @return: boolean determines whether or not to load
        function classes for given function URN in functionId set property 
        method
        @rtype: bool
        """
        return self.__loadFunctionFromId
    
    @loadFunctionFromId.setter
    def loadFunctionFromId(self, value):
        """
        @param value: boolean determines whether or not to load
        function classes for given function URN in functionId set property 
        method
        @type value: bool
        """
        if not isinstance(value, bool):
            raise TypeError('Expecting %r type for "loadFunctionFromId" '
                            'attribute; got %r' % (bool, type(value)))
            
        self.__loadFunctionFromId = value
        
    def setFunctionFromMap(self, functionMap):
        """Set the function from a function map - a dictionary of function ID to
        function mappings.  The function is looked up based on the "functionId"
        attribute.  This method is automatically called when the functionId set
        property method is invoked.  To switch off this behaviour set
        
        loadFunctionFromId = False
        
        @param functionMap: mapping of function URNs to function classes
        @type functionMap: dict like object
        @raise UnsupportedStdFunctionError: policy references a function type 
        which is in the XACML spec. but is not supported by this implementation
        @raise UnsupportedFunctionError: policy references a function type which
        is not supported by this implementation
        """
        if self.matchId is None:
            raise AttributeError('"functionId" attribute must be set in order '
                                 'to retrieve the required function')
            
        # Get function class for this <Apply> statement         
        functionClass = functionMap.get(self.matchId)
        if functionClass is NotImplemented:
            raise UnsupportedStdFunctionError('No match function class '
                                              'implemented for MatchId="%s"' % 
                                              self.matchId)
        elif functionClass is None:
            raise UnsupportedFunctionError('<Apply> function namespace %r is '
                                           'not recognised' % 
                                           self.matchId) 
            
        self.__function = functionClass()
    
    @property
    def functionMap(self):
        """functionMap object for PDP to retrieve functions from given XACML
        function URNs
        @return: function mapping object to map URNs to function 
        class implementations
        @rtype: ndg.xacml.core.functions.FunctionMap
        """
        return self.__functionMap
    
    @functionMap.setter
    def functionMap(self, value):
        '''functionMap object for PDP to retrieve functions from given XACML
        function URNs
        
        @param value: function mapping object to map URNs to function class
        implementations
        @type value: ndg.xacml.core.functions.FunctionMap
        @raise TypeError: raise if input value is incorrect type
        '''
        if not isinstance(value, FunctionMap):
            raise TypeError('Expecting %r derived type for "functionMap" '
                            'input; got %r instead' % (FunctionMap, 
                                                       type(value)))
        self.__functionMap = value
          
    @property  
    def function(self):
        """Function for this <Apply> instance
        @return: function to be applied
        @rtype: ndg.xacml.core.functions.AbstractFunction derived type
        """
        return self.__function
        
    def evaluate(self, context):
        """Evaluate the match object against the relevant element in the request
        context
        
        @param context: the request context
        @type context: ndg.xacml.core.context.request.Request
        @return: match status
        @rtype: bool
        """
        
        # Create a match function based on the presence or absence of an
        # AttributeDesignator or AttributeSelector
        if self.attributeDesignator is not None:
            requestAttributeValues = self.attributeDesignator.evaluate(context)
            
        elif self.attributeSelector is not None:
            # Nb. Evaluation is not currently supported.  This will require that
            # the request provide a reference to it's XML representation and an 
            # abstraction of the XML parser for executing XPath searches into 
            # that representation
            requestAttributeValues = self.attributeSelector.evaluate(context)
        else:
            raise XacmlContextError('No attribute designator or selector set '
                                    'for Target Match element %r with MatchId '
                                    '= %r and attributeValue = %r' %
                                    (self.__class__.ELEMENT_LOCAL_NAME,
                                     self.matchId,
                                     self.attributeValue))
            
        # Iterate through each attribute in the request in turn matching it
        # against the target using the generated _attributeMatch function.
        # The target match attribute must match any of the request attributes
        # for an overall True match status.
        #
        # Continue iterating through the whole list even if a True status
        # is found.  The other attributes need to be checked in case an
        # error occurs.  In this case the top-level PDP exception handling
        # block will catch it and set an overall decision of INDETERMINATE.
        attrMatchStatusValues = [False]*len(requestAttributeValues)
        matchFunction = self.function
        matchAttributeValue = self.attributeValue
        
        for i, requestAttributeValue in enumerate(requestAttributeValues):
            
            attrMatchStatusValues[i] = matchFunction.evaluate(
                                                         matchAttributeValue,
                                                         requestAttributeValue)
            if log.getEffectiveLevel() <= logging.DEBUG:
                if attrMatchStatusValues[i] == True:
                    log.debug('Target attribute value %r matches request '
                              'attribute value %r matches using match '
                              'function Id %r',
                              matchAttributeValue,
                              requestAttributeValue,
                              self.matchId)
                else:
                    log.debug('Target attribute value %r doesn\'t match '
                              'request attribute value %r with match function '
                              'Id %r',
                              matchAttributeValue,
                              requestAttributeValue,
                              self.matchId)
                    
            
        # Return true if a match was found.
        matchStatus = any(attrMatchStatusValues)
        
        return matchStatus
    
    
class SubjectMatch(MatchBase):
    "Subject Match Type"
    ELEMENT_LOCAL_NAME = 'SubjectMatch'
    ATTRIBUTE_DESIGNATOR_ELEMENT_LOCAL_NAME = 'SubjectAttributeDesignator'   
    
    
class ResourceMatch(MatchBase):
    "Resource Match"
    ELEMENT_LOCAL_NAME = 'ResourceMatch'
    ATTRIBUTE_DESIGNATOR_ELEMENT_LOCAL_NAME = 'ResourceAttributeDesignator'
    
    
class ActionMatch(MatchBase):
    "Action match"
    ELEMENT_LOCAL_NAME = 'ActionMatch'
    ATTRIBUTE_DESIGNATOR_ELEMENT_LOCAL_NAME = 'ActionAttributeDesignator'    
    
    
class EnvironmentMatch(MatchBase):
    "Environment Match"
    ELEMENT_LOCAL_NAME = 'EnvironmentMatch'
    ATTRIBUTE_DESIGNATOR_ELEMENT_LOCAL_NAME = 'EnvironmentAttributeDesignator'