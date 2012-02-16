"""NDG XACML1.0 Regular expression matching function module

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "26/03/10"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import re

from ndg.xacml.core.attributevalue import AttributeValueClassFactory
from ndg.xacml.core.functions import (AbstractFunction, 
                                      FunctionClassFactoryInterface)


class RegexpMatchBase(AbstractFunction):
    """XACML 2.0 Regular Expression matching base class function
    
    @cvar TYPE: attribute type for the given implementation.  Derived classes
    should set appropriately
    @type TYPE: NoneType
    
    @cvar FUNCTION_SUFFIX: suffix for all regular expression type function class
    names
    @type FUNCTION_SUFFIX: string
    
    @cvar FUNCTION_NS_SUFFIX: generic suffix for regular expression type 
    function URNs
    @type FUNCTION_NS_SUFFIX: string
    
    @cvar CLASS_NAME_SUFFIX: suffix for all regular expression class names
    @type CLASS_NAME_SUFFIX: string
    
    @cvar compiled_regexes: cache of compiled regular expressions
    @type compiled_regexes: dict of string mappings to re.RegexObject
    """
    FUNCTION_NS = None
    FUNCTION_NS_SUFFIX = '-regexp-match'
    CLASS_NAME_SUFFIX = 'RegexpMatch'
    TYPE = None

    compiled_regexes = {}
    
    def evaluate(self, pat, input):
        """Match URI against regular expression pattern
        
        @param pat: regular expression
        @type pat: basestring
        @param input: URI to match
        @type input: type
        @return: True if URI matches pattern, False otherwise
        @rtype: bool
        """
        if not isinstance(pat, self.__class__.TYPE):
            raise TypeError('Expecting %r derived type for "pat"; got %r' %
                            (self.__class__.TYPE, type(pat)))
            
        if not isinstance(input, self.__class__.TYPE):
            raise TypeError('Expecting %r derived type for "input"; got %r' %
                            (self.__class__.TYPE, type(input)))
            
        compiled_regex = self.compiled_regexes.get(pat.value, None)
        if compiled_regex is None:
            compiled_regex = re.compile(pat.value)
            self.compiled_regexes[pat.value] = compiled_regex
        return bool(compiled_regex.match(input.value))
    

attributeValueClassFactory = AttributeValueClassFactory()


class StringRegexMatch(RegexpMatchBase):
    """String regular expression match function class representation
    
    @cvar FUNCTION_NS: String regular expression match function URN
    @type FUNCTION_NS: string
    
    @cvar TYPE: string attribute value type
    @type TYPE: dynamically generated string type derived from 
    ndg.xacml.core.attributevalue.AttributeValue
    """
    FUNCTION_NS = 'urn:oasis:names:tc:xacml:1.0:function:string-regexp-match'
    TYPE = attributeValueClassFactory('http://www.w3.org/2001/XMLSchema#string')
    
    
class FunctionClassFactory(FunctionClassFactoryInterface):
    """Class Factory for string-regexp-match XACML function class.  Go to
    ndg.xacml.core.functions.v2.regexp_match module for additional functions 
    for other types.
    """
    def __call__(self, identifier):
        '''Create class for the Round XACML function identifier
        
        @param identifier: XACML string regular expression function identifier
        @type identifier: basestring
        @return: at least one member of class corresponding to the given input
        identifier, if no match is found returns None
        @rtype: ndg.xacml.core.functions.v1.regexp_match.StringRegexMatch / None
        '''
        if identifier == StringRegexMatch.FUNCTION_NS:
            return StringRegexMatch
        else:
            return None
