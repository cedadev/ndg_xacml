"""NDG Security Condition type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "19/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.utils import TypedList
from ndg.xacml.core.expression import Expression
from ndg.xacml.core.functions import (FunctionMap, functionMap,
                                      UnsupportedStdFunctionError,
                                      UnsupportedFunctionError)


class Apply(Expression):
    """XACML Apply type
    
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    @cvar FUNCTION_ID_ATTRIB_NAME: function ID XML attribute name
    @type FUNCTION_ID_ATTRIB_NAME: string

    @ivar __functionId: URN corresponding to function to be applied
    @type __functionId: basestring/NoneType
    @ivar __function: function to be applied
    @type __function: ndg.xacml.core.functions.AbstractFunction derived type
    @ivar __functionMap: function mapping object to map URNs to function class
    implementations
    @type __functionMap: ndg.xacml.core.functions.FunctionMap
    @ivar __loadFunctionFromId: boolean determines whether or not to load
    function classes for given function URN in functionId set property method
    @type __loadFunctionFromId: bool
    @ivar __expressions: list of expressions contained in the Apply statement
    @type __expressions: ndg.xacml.utils.TypedList
    """
    ELEMENT_LOCAL_NAME = 'Apply'
    FUNCTION_ID_ATTRIB_NAME = 'FunctionId'
    
    __slots__ = (
        '__functionId', 
        '__function', 
        '__functionMap',
        '__loadFunctionFromId',
        '__expressions'
    )
    
    def __init__(self):
        """Initialise attributes"""
        super(Apply, self).__init__()
        self.__functionId = None
        self.__function = None
        self.__functionMap = functionMap
        self.__loadFunctionFromId = True
        self.__expressions = TypedList(Expression)
      
    @property
    def loadFunctionFromId(self):
        """Set to False to stop the functionId property set method automatically
        trying to load the corresponding function for the given functionId
        
        @return: flag setting
        @rtype: bool""" 
        return self.__loadFunctionFromId
    
    @loadFunctionFromId.setter
    def loadFunctionFromId(self, value):
        """Set to False to stop the functionId property set method automatically
        trying to load the corresponding function for the given functionId
        
        @param value: flag setting
        @type value: bool
        @raise TypeError: incorrect input type
        """ 
        if not isinstance(value, bool):
            raise TypeError('Expecting %r type for "loadFunctionFromId" '
                            'attribute; got %r' % (bool, type(value)))
            
        self.__loadFunctionFromId = value
        
    def _get_functionId(self):
        """Get function ID
        @return: function ID for this Apply statement
        @rtype: basestring/NoneType
        """
        return self.__functionId

    def _set_functionId(self, value):
        """Set function ID
        @param value: function URN
        @type value: basestring
        @raise TypeError: incorrect input type
        """ 
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "functionId" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__functionId = value
        
        # Also retrieve function for this function ID if a map has been set
        if self.__loadFunctionFromId:
            self.setFunctionFromMap(self.__functionMap)   

    functionId = property(_get_functionId, _set_functionId, None, 
                          "Apply type Function ID") 
        
    def setFunctionFromMap(self, functionMap):
        """Set the function from a function map - a dictionary of function ID to
        function mappings.  The function is looked up based on the "functionId"
        attribute.  This method is automatically called when the functionId set
        property method is invoked.  To switch off this behaviour set
        
        loadFunctionFromId = False
    
        @param functionMap: function mapping object to map URNs to function 
        class implementations
        @type functionMap: ndg.xacml.core.functions.FunctionMap
        
        @raise UnsupportedStdFunctionError: policy references a function type 
        which is in the XACML spec. but is not supported by this implementation
        @raise UnsupportedFunctionError: policy references a function type which
        is not supported by this implementation
        """
        if self.functionId is None:
            raise AttributeError('"functionId" attribute must be set in order '
                                 'to retrieve the required function')
            
        # Get function class for this <Apply> statement         
        functionClass = functionMap.get(self.functionId)
        if functionClass is NotImplemented:
            raise UnsupportedStdFunctionError('No match function class '
                                              'implemented for MatchId="%s"' % 
                                              self.functionId)
        elif functionClass is None:
            raise UnsupportedFunctionError('<Apply> function namespace %r is '
                                           'not recognised' % 
                                           self.functionId) 
            
        self.__function = functionClass()
    
    @property
    def functionMap(self):
        """functionMap object for PDP to retrieve functions from given XACML
        function URNs
        @return: function mapping object
        @rtype: ndg.xacml.core.functions.FunctionMap
        """
        return self.__functionMap
    
    @functionMap.setter
    def functionMap(self, value):
        '''functionMap object for PDP to retrieve functions from given XACML
        function URNs
        @param value: function mapping object to map URNs to function 
        class implementations
        @type value: ndg.xacml.core.functions.FunctionMap
        @raise TypeError: incorrect type for input value
        '''
        if not isinstance(value, FunctionMap):
            raise TypeError('Expecting %r derived type for "functionMap" '
                            'input; got %r instead' % (FunctionMap, 
                                                       type(value)))
        self.__functionMap = value
          
    @property  
    def function(self):
        """Get Function for this <Apply> instance
        @return: function to be applied
        @rtype: ndg.xacml.core.functions.AbstractFunction derived type
        """
        return self.__function
        
    @property
    def expressions(self):
        """List of expression sub-elements
        @return: list of expressions contained in the Apply statement
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__expressions 
    
    def evaluate(self, context):
        """Evaluate a given <Apply> statement in a rule condition
        
        @param context: the request context
        @type context: ndg.xacml.core.context.request.Request
        @return: attribute value(s) resulting from execution of this expression
        in a condition
        @rtype: AttributeValue/NoneType
        """ 
        
        # Marshal inputs
        funcInputs = [None]*len(self.expressions)

        for i, expression in enumerate(self.expressions):
            funcInputs[i] = expression.evaluate(context)
            
        # Execute function on the retrieved inputs
        result = self.function.evaluate(*tuple(funcInputs))
        
        # Pass the result back to the parent <Apply> element
        return result
