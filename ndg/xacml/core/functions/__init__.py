"""NDG XACML package for functions

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "26/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
import traceback
import logging
log = logging.getLogger(__name__)

from ndg.xacml.core.attributevalue import (AttributeValue, 
                                           AttributeValueClassFactory)
from ndg.xacml.utils import VettedDict, _isIterable
from ndg.xacml.utils.factory import callModuleObject


# Mapping for function name prefixes that are not real types, but play a similar
# role
SPECIAL_TYPE_MAP = {
    'url-string': 'AnyURI',
    'xpath-node': 'String'}

class AbstractFunction(object):
    """Abstract Base class for all XACML matching functions
    @cvar FUNCTION_NS: namespace for the given function
    @type FUNCTION_NS: NoneType (must be string in derived type)
    
    @cvar V1_0_FUNCTION_NS: XACML 1.0 function namespace prefix
    @type V1_0_FUNCTION_NS: string
    
    @cvar V2_0_FUNCTION_NS: XACML 2.0 function namespace prefix
    @type V2_0_FUNCTION_NS: string
    """
    __metaclass__ = ABCMeta
    
    FUNCTION_NS = None
    V1_0_FUNCTION_NS = "urn:oasis:names:tc:xacml:1.0:function:"
    V2_0_FUNCTION_NS = "urn:oasis:names:tc:xacml:2.0:function:"
    
    def __init__(self):
        """
        @raise TypeError: if FUNCTION_NS not set correctly
        """
        if self.__class__.FUNCTION_NS is None:
            raise TypeError('"FUNCTION_NS" class variable must be defined in '
                            'derived classes')
            
    @abstractmethod
    def evaluate(self, *inputs):
        """Evaluate the function from the given input arguments and context
        
        @param inputs: input arguments need to evaluate the function
        @type inputs: tuple
        @return: derived type should return True for match, False otherwise
        @rtype: bool (derived type), NoneType for THIS implementation
        """
    
        
class XacmlFunctionNames(object):
    """XACML standard match function names
    
    @cvar FUNCTION_NAMES: list of all the XACML function URNs
    @type FUNCTION_NAMES: tuple    
    """
    FUNCTION_NAMES = (
'urn:oasis:names:tc:xacml:1.0:function:string-equal',
'urn:oasis:names:tc:xacml:1.0:function:boolean-equal',
'urn:oasis:names:tc:xacml:1.0:function:integer-equal',
'urn:oasis:names:tc:xacml:1.0:function:double-equal',
'urn:oasis:names:tc:xacml:1.0:function:date-equal',
'urn:oasis:names:tc:xacml:1.0:function:time-equal',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-equal',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-equal',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-equal',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-equal',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-equal',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-equal',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-equal',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-equal',
'urn:oasis:names:tc:xacml:1.0:function:integer-add',
'urn:oasis:names:tc:xacml:1.0:function:double-add',
'urn:oasis:names:tc:xacml:1.0:function:integer-subtract',
'urn:oasis:names:tc:xacml:1.0:function:double-subtract',
'urn:oasis:names:tc:xacml:1.0:function:integer-multiply',
'urn:oasis:names:tc:xacml:1.0:function:double-multiply',
'urn:oasis:names:tc:xacml:1.0:function:integer-divide',
'urn:oasis:names:tc:xacml:1.0:function:double-divide',
'urn:oasis:names:tc:xacml:1.0:function:integer-mod',
'urn:oasis:names:tc:xacml:1.0:function:integer-abs',
'urn:oasis:names:tc:xacml:1.0:function:double-abs',
'urn:oasis:names:tc:xacml:1.0:function:round',
'urn:oasis:names:tc:xacml:1.0:function:floor',
'urn:oasis:names:tc:xacml:1.0:function:string-normalize-space',
'urn:oasis:names:tc:xacml:1.0:function:string-normalize-to-lower-case',
'urn:oasis:names:tc:xacml:1.0:function:double-to-integer',
'urn:oasis:names:tc:xacml:1.0:function:integer-to-double',
'urn:oasis:names:tc:xacml:1.0:function:or',
'urn:oasis:names:tc:xacml:1.0:function:and',
'urn:oasis:names:tc:xacml:1.0:function:n-of',
'urn:oasis:names:tc:xacml:1.0:function:not',
'urn:oasis:names:tc:xacml:1.0:function:integer-greater-than',
'urn:oasis:names:tc:xacml:1.0:function:integer-greater-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:integer-less-than',
'urn:oasis:names:tc:xacml:1.0:function:integer-less-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:double-greater-than',
'urn:oasis:names:tc:xacml:1.0:function:double-greater-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:double-less-than',
'urn:oasis:names:tc:xacml:1.0:function:double-less-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-add-dayTimeDuration',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-add-yearMonthDuration',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-subtract-dayTimeDuration',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-subtract-yearMonthDuration', 
'urn:oasis:names:tc:xacml:1.0:function:date-add-yearMonthDuration',
'urn:oasis:names:tc:xacml:1.0:function:date-subtract-yearMonthDuration',
'urn:oasis:names:tc:xacml:1.0:function:string-greater-than',
'urn:oasis:names:tc:xacml:1.0:function:string-greater-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:string-less-than',
'urn:oasis:names:tc:xacml:1.0:function:string-less-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:time-greater-than',
'urn:oasis:names:tc:xacml:1.0:function:time-greater-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:time-less-than',
'urn:oasis:names:tc:xacml:1.0:function:time-less-than-or-equal',
'urn:oasis:names:tc:xacml:2.0:function:time-in-range',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-greater-than',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-greater-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-less-than',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-less-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:date-greater-than',
'urn:oasis:names:tc:xacml:1.0:function:date-greater-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:date-less-than',
'urn:oasis:names:tc:xacml:1.0:function:date-less-than-or-equal',
'urn:oasis:names:tc:xacml:1.0:function:string-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:string-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:string-is-in',
'urn:oasis:names:tc:xacml:1.0:function:string-bag',
'urn:oasis:names:tc:xacml:1.0:function:boolean-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:boolean-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:boolean-is-in',
'urn:oasis:names:tc:xacml:1.0:function:boolean-bag',
'urn:oasis:names:tc:xacml:1.0:function:integer-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:integer-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:integer-is-in',
'urn:oasis:names:tc:xacml:1.0:function:integer-bag',
'urn:oasis:names:tc:xacml:1.0:function:double-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:double-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:double-is-in',
'urn:oasis:names:tc:xacml:1.0:function:double-bag',
'urn:oasis:names:tc:xacml:1.0:function:time-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:time-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:time-is-in',
'urn:oasis:names:tc:xacml:1.0:function:time-bag',
'urn:oasis:names:tc:xacml:1.0:function:date-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:date-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:date-is-in',
'urn:oasis:names:tc:xacml:1.0:function:date-bag',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-is-in',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-bag',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-is-in',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-bag',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-is-in',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-bag',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-is-in',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-bag',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-is-in',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-bag',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-is-in',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-bag',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-is-in',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-bag',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-one-and-only',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-bag-size',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-is-in',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-bag',
'urn:oasis:names:tc:xacml:2.0:function:string-concatenate',
'urn:oasis:names:tc:xacml:2.0:function:uri-string-concatenate',
'urn:oasis:names:tc:xacml:1.0:function:any-of',
'urn:oasis:names:tc:xacml:1.0:function:all-of',
'urn:oasis:names:tc:xacml:1.0:function:any-of-any',
'urn:oasis:names:tc:xacml:1.0:function:all-of-any',
'urn:oasis:names:tc:xacml:1.0:function:any-of-all',
'urn:oasis:names:tc:xacml:1.0:function:all-of-all',
'urn:oasis:names:tc:xacml:1.0:function:map',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-match',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-match',
'urn:oasis:names:tc:xacml:1.0:function:string-regexp-match',
'urn:oasis:names:tc:xacml:2.0:function:anyURI-regexp-match',
'urn:oasis:names:tc:xacml:2.0:function:ipAddress-regexp-match',
'urn:oasis:names:tc:xacml:2.0:function:dnsName-regexp-match',
'urn:oasis:names:tc:xacml:2.0:function:rfc822Name-regexp-match',
'urn:oasis:names:tc:xacml:2.0:function:x500Name-regexp-match',
'urn:oasis:names:tc:xacml:1.0:function:xpath-node-count',
'urn:oasis:names:tc:xacml:1.0:function:xpath-node-equal',
'urn:oasis:names:tc:xacml:1.0:function:xpath-node-match',
'urn:oasis:names:tc:xacml:1.0:function:string-intersection',
'urn:oasis:names:tc:xacml:1.0:function:string-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:string-union',
'urn:oasis:names:tc:xacml:1.0:function:string-subset',
'urn:oasis:names:tc:xacml:1.0:function:string-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:boolean-intersection',
'urn:oasis:names:tc:xacml:1.0:function:boolean-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:boolean-union',
'urn:oasis:names:tc:xacml:1.0:function:boolean-subset',
'urn:oasis:names:tc:xacml:1.0:function:boolean-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:integer-intersection',
'urn:oasis:names:tc:xacml:1.0:function:integer-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:integer-union',
'urn:oasis:names:tc:xacml:1.0:function:integer-subset',
'urn:oasis:names:tc:xacml:1.0:function:integer-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:double-intersection',
'urn:oasis:names:tc:xacml:1.0:function:double-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:double-union',
'urn:oasis:names:tc:xacml:1.0:function:double-subset',
'urn:oasis:names:tc:xacml:1.0:function:double-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:time-intersection',
'urn:oasis:names:tc:xacml:1.0:function:time-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:time-union',
'urn:oasis:names:tc:xacml:1.0:function:time-subset',
'urn:oasis:names:tc:xacml:1.0:function:time-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:date-intersection',
'urn:oasis:names:tc:xacml:1.0:function:date-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:date-union',
'urn:oasis:names:tc:xacml:1.0:function:date-subset',
'urn:oasis:names:tc:xacml:1.0:function:date-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-intersection',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-union',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-subset',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-intersection',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-union',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-subset',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-intersection',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-union',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-subset',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-intersection',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-union',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-subset',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-intersection',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-union',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-subset',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-intersection',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-union',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-subset',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-intersection',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-union',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-subset',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-set-equals',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-intersection',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-union',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-subset',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-set-equals',
    )

from ndg.xacml import XacmlError


class UnsupportedFunctionError(XacmlError):
    """Encountered a function type that is not recognised as part of the XACML
    specification and is not supported in this implementation"""

 
class UnsupportedStdFunctionError(UnsupportedFunctionError): 
    """Encountered a function type that is not supported even though it is
    part of the XACML specification"""
    
    
def unsupportedFunctionErrorFactory(identifier, msg=None):
    """Factory function to return an unsupported function exception based on
    the function identifier passed in
    
    @param identifier: XACML function namespace to check
    @type identifier: basestring
    
    @return: unsupported function exception instance
    @rtype: UnsupportedFunctionError or UnsupportedStdFunctionError depending
    on the identifier passed
    """
    if identifier in XacmlFunctionNames.FUNCTION_NAMES:
        if msg is None:
            msg = "%s: %s" % (UnsupportedStdFunctionError.__doc__, identifier)
            
        raise UnsupportedStdFunctionError(msg)
    else:
        if msg is None:
            msg = "%s: %s" % (UnsupportedFunctionError.__doc__, identifier)
            
        raise UnsupportedFunctionError(msg)
    

class OverwritingStdFunctionError(XacmlError):
    """Attempting to overwrite a standard function namespace with a custom one
    (probably from load_custom_function method)"""
    
    
class FunctionClassFactoryInterface(object):
    """Interface class for function module class factory class
    """
    __meta__ = ABCMeta
    
    @abstractmethod
    def __call__(self, identifier):
        '''Create class for the given XACML function identifier
        
        @param identifier: XACML function identifier
        @type identifier: basestring
        @return: at least one member of class corresponding to the given input
        identifier
        @rtype: AbstractFunction derived type or NoneType if no match is found
        '''
        return None
    

class FunctionClassFactoryBase(FunctionClassFactoryInterface):
    """Base implementation for XACML Function Class Factory.  There should be
    one derived type for each function family implemented in sub-modules of 
    ndg.xacml.core.functions 
    
    e.g.
    
    for urn:oasis:names:tc:xacml:1.0:function:<type>-at-least-one-member-of a 
    class factory should exist,
    
    ndg.xacml.core.functions.v1.at_least_one_member_of.FunctionClassFactory
    
    which will be capable of returning a type derived from AbstractFunction:
    
    <type>AtLeastOneMemberOf    
    
    e.g. StringAtLeastOneMemberOf, BooleanAtLeastOneMemberOf.
    
    This class is for convenience only some function factories are better 
    derived directly from FunctionClassFactoryInterface
    
    Derived classes MUST define these class variables:
    
    @cvar FUNCTION_NAMES: list of function identifiers that this factory can
    produce classes for e.g.:
    
    ('urn:oasis:names:tc:xacml:1.0:function:string-at-least-one-member-of', ...)
    
    @type FUNCTION_NAMES: NoneType (but list in derived class)
   
    @cvar FUNCTION_NS_SUFFIX: urn suffix for the family of function to define
    e.g. -at-least-one-member-of is the suffix for the URN:
    
    urn:oasis:names:tc:xacml:1.0:function:string-at-least-one-member-of
    @type FUNCTION_NS_SUFFIX: NoneType (but basestring in derived class)
    
    @cvar FUNCTION_BASE_CLASS: base class for this family of functions e.g for
    urn:oasis:names:tc:xacml:1.0:function:string-at-least-one-member-of,
    ndg.xacml.core.functions.v1.at_least_one_member_of.AtLeastOneMemberOfBase
    @type FUNCTION_BASE_CLASS: NoneType (but AbstractFunction derived type in 
    derived function factory class)
    """
    
    FUNCTION_NS_SUFFIX = None
    FUNCTION_NAMES = None
    FUNCTION_BASE_CLASS = None
    
    URN_SEP = ':'
    FUNCTION_NAME_SEP = '-'
    __slots__ = ('__map', 'attributeValueClassFactory', 'functionSuffix')
    
    def __init__(self):
        '''This class is in fact abstract - derived types must define the 
        FUNCTION_NS_SUFFIX and FUNCTION_BASE_CLASS class variables
        '''
        if None in (self.__class__.FUNCTION_NS_SUFFIX, 
                    self.__class__.FUNCTION_BASE_CLASS):
            raise TypeError('"FUNCTION_NS_SUFFIX" and "FUNCTION_BASE_CLASS" '
                            'must be defined in a derived implementation of '
                            'FunctionClassFactoryBase.  See '
                            'FunctionClassFactoryBase.__doc__ contents')
        
        if not _isIterable(self.__class__.FUNCTION_NAMES):
            raise TypeError('"FUNCTION_NAMES" class variable must be an '
                            'iterable of string type function identifiers; got '
                            '%r' % self.__class__.FUNCTION_NAMES)

        self.__map = {}   
        
        # Enables creation of matching attribute types to relevant to the 
        # function classes    
        self.attributeValueClassFactory = AttributeValueClassFactory()
            
        
        functionSuffixParts = self.__class__.FUNCTION_NS_SUFFIX.split(
                                            self.__class__.FUNCTION_NAME_SEP)
        self.functionSuffix = ''.join([n[0].upper() + n[1:] 
                                  for n in functionSuffixParts if n])
        
    def initAllFunctionClasses(self):
        """Create classes for all functions for a data type e.g. a derived class
        could implement a factory for <type>-at-least-one-member-of functions:
        string-at-least-one-member-of, boolean-at-least-one-member-of, etc. 
        
        Function classes are placed in a look-up table __map for the __call__()
        method to access
        
        In practice, there shouldn't be a need to load all the functions in
        one go.  The __call__ method loads functions and caches them as needed.
        """        
        for identifier in self.__class__.FUNCTION_NAMES:
            self.loadFunction(identifier)        

    def loadFunction(self, identifier):
        """Create a class for the given function namespace and cache it in the 
        function class look-up table for future requests.  Note that this call
        overwrites any existing entry in the cache whereas __call__ will try
        to use an entry in the cache if it already exists
        
        @param identifier: XACML function namespace
        @type identifier: basestring
        """

        # str.capitalize doesn't do what's required: need to capitalize the 
        # first letter of the word BUT retain camel case for the rest of it
        _capitalize = lambda s: s[0].upper() + s[1:]
        
        # Extract the function name and the type portion of the function
        # name in order to make an implementation of a class to handle it
        functionName = identifier.split(self.__class__.URN_SEP)[-1]
        typePart = functionName.split(self.__class__.FUNCTION_NS_SUFFIX)[0]
        
        # Attempt to infer from the function name the associated type
        typeName = _capitalize(typePart)
        
        # Remove any hyphens converting to camel case
        if '-' in typeName:
            typeName = ''.join([_capitalize(i) for i in typeName.split('-')])
            
        typeURI = AttributeValue.TYPE_URI_MAP.get(typeName)
        if typeURI is None:
            # Ugly hack to allow for functions that start with a prefix that
            # isn't a real type.
            if typePart in SPECIAL_TYPE_MAP:
                typeURI = AttributeValue.TYPE_URI_MAP[
                                                    SPECIAL_TYPE_MAP[typePart]]
            else:
                raise TypeError('No AttributeValue.TYPE_URI_MAP entry for '
                                '%r type' % typePart) 
            
        _type = self.attributeValueClassFactory(typeURI)
        if _type is None:
            raise TypeError('No AttributeValue.TYPE_MAP entry for %r type' %
                            typeName)
          
        className = typeName + self.functionSuffix
        classVars = {
            'TYPE': _type,
            'FUNCTION_NS': identifier
        }
        
        functionClass = type(className, 
                             (self.__class__.FUNCTION_BASE_CLASS, ), 
                             classVars)
        
        self.__map[identifier] = functionClass
            
    def __call__(self, identifier):
        """Return the class for the given XACML type function identifier
        
        @param identifier: XACML *-at-least-one-member-of type function
        identifier
        @type identifier: basestring
        @return: at least one member of class corresponding to the given input
        identifier
        @rtype: AtLeastOneMemberOfBase derived type or None if no match is 
        found
        """
        # Check the cache first
        functionClass = self.__map.get(identifier)
        if functionClass is None:
            # No class set in the cache - try loading the new class and updating
            # the cache.
            self.loadFunction(identifier)
            
        # This should result in a safe retrieval from the cache because of the
        # above check - None return would result otherwise.
        return self.__map.get(identifier)
        
    
class FunctionMapError(Exception):
    """Generic Error exception class for FunctionMap"""
    
    
class FunctionMapConfigError(FunctionMapError):
    """Configuration related exception for FunctionMap"""
        
        
class FunctionMap(VettedDict):
    """Map function IDs to their class implementations in the various function
    sub-modules.  It provide a layer over the various 
    FunctionClassFactoryInterface implementations so that a function class can 
    be obtained directly from a given XACML function URN.  
    
    @cvar FUNCTION_PKG_PREFIX: python package path for functions package
    @type FUNCTION_PKG_PREFIX: string
    
    @cvar V1_0_PKG_PREFIX: python package path for XACML 1.0 functions package
    @type V1_0_PKG_PREFIX: string
    
    @cvar V2_0_PKG_PREFIX: python package path for XACML 2.0 functions package
    @type V2_0_PKG_PREFIX: string
    
    @cvar SUPPORTED_NSS: mapping of function URN prefix to Python package
    @type SUPPORTED_NSS: dict
    
    @cvar FUNCTION_CLASS_FACTORY_CLASSNAME: standard name for class factory
    which should be present in each generic function module.  This factory is 
    invoked to create the function class for any given function URN related to
    that module
    @type FUNCTION_CLASS_FACTORY_CLASSNAME: string
    """
    FUNCTION_PKG_PREFIX = 'ndg.xacml.core.functions.'
    
    V1_0_PKG_PREFIX = FUNCTION_PKG_PREFIX + 'v1.'
    V2_0_PKG_PREFIX = FUNCTION_PKG_PREFIX + 'v2.'
    
    SUPPORTED_NSS = {
        AbstractFunction.V1_0_FUNCTION_NS: V1_0_PKG_PREFIX,
        AbstractFunction.V2_0_FUNCTION_NS: V2_0_PKG_PREFIX
    }
    
    # Each function module is expected to have a class factory for obtaining
    # a class for the given function identifier associated with that module
    FUNCTION_CLASS_FACTORY_CLASSNAME = 'FunctionClassFactory'
    
    def __init__(self):
        """Force type for dictionary key value pairs: function values must be
        of AbstractFunction derived type and ID keys string type
        """        
        # Filters are defined as staticmethods but reference via self here to 
        # enable derived class to override them as standard methods without
        # needing to redefine this __init__ method            
        VettedDict.__init__(self, self.keyFilter, self.valueFilter)
        
        # This classes maintains a list of XACML function URN -> Function class
        # mappings.  This additional dict enables caching of class factories 
        # used to obtain the function classes.  There is one class factory per
        # function module e.g. ndg.xacml.core.functions.v1.equal contains a 
        # class factory which creates the various 
        # urn:oasis:names:tc:xacml:1.0:function:<type>-equal function classes
        self.__classFactoryMap = {}
        self.__custom_class_factory_map = {}
        
    @staticmethod
    def keyFilter(key):
        """Enforce string type keys
        
        @param key: function URN
        @type key: basestring
        @return: True for valid key type
        @rtype: bool
        @raise TypeError: invalid key type
        """
        if not isinstance(key, basestring):
            raise TypeError('Expecting %r type for key; got %r' % 
                            (basestring, type(key))) 
            
        return True 
    
    @staticmethod
    def valueFilter(value):
        """Enforce AbstractFunction derived types for match functions
        
        @param value: function URN
        @type value: ndg.xacml.core.functions.AbstractFunction / NotImplemented
        @return: True for valid function type
        @rtype: bool
        @raise TypeError: invlaid key type
        """
        if value is NotImplemented:
            return True
        
        elif not issubclass(value, AbstractFunction):
            raise TypeError('Expecting %r derived type for value; got %r' % 
                            (AbstractFunction, value)) 
            
        return True 
           
    def loadAllCore(self):
        """Load all core XACML functions"""
        
        for functionNs in XacmlFunctionNames.FUNCTION_NAMES:
            self.loadFunction(functionNs)
            
    def loadFunction(self, functionNs):
        """Get package to retrieve function class for the given XACML function
        namespace
        
        @param functionNs: XACML function namespace
        @type functionNs: basestring
        """
        # Try map for custom function class
        if functionNs in self:
            return self[functionNs]
        
        # else try the class factory - there is one factory per family of 
        # functions e.g. bag functions, at least one member of functions etc.
        functionFactory = self.__classFactoryMap.get(functionNs)
        if functionFactory is not None:
            # Get function class from previously cached factory
            self[functionNs] = functionFactory(functionNs)
            return
            
        # No Factory has been cached for this function yet
        cls = FunctionMap
        classPath = None
        
        for namespacePrefix, pkgNamePrefix in cls.SUPPORTED_NSS.items():
            if functionNs.startswith(namespacePrefix):
                # Namespace is recognised - translate into a path to a 
                # function class in the right functions package
                functionName = functionNs.split(namespacePrefix)[-1]
                functionNameParts = functionName.split('-')
                
                if len(functionNameParts) == 1:
                    moduleName = functionNameParts[0]
                else:
                    prefix = None
                    # Ugly hack to allow for functions that start with a prefix
                    # that isn't a real type.
                    for pfx in SPECIAL_TYPE_MAP.iterkeys():
                        pfxsep = pfx + '-'
                        if functionName.startswith(pfxsep):
                            prefix = pfxsep
                            break
                    if prefix:
                        suffix = functionName[len(prefix):]
                        moduleName = '_'.join(suffix.split('-')).lower()
                    else:
                        moduleName = '_'.join(functionNameParts[1:]).lower()

                classPath = pkgNamePrefix + moduleName + '.' + \
                            cls.FUNCTION_CLASS_FACTORY_CLASSNAME
                break

        if classPath is None:
            raise FunctionMapConfigError('Namespace for function not '
                                         'recognised: %r' % functionNs) 
                       
        # Try instantiating the function class and loading it into the map
        try:
            functionFactory = callModuleObject(classPath)
                      
        except (ImportError, AttributeError), e:
            log.error("Error importing function factory class %r for function "
                      "identifier %r: %s", classPath, functionNs, str(e))
            
            # No implementation exists - default to Abstract function
            self[functionNs] = NotImplemented
        else:
            function = functionFactory(functionNs)
            if function is None:
                raise unsupportedFunctionErrorFactory(functionNs)
                
            self[functionNs] = function
            self.__classFactoryMap[functionNs] = functionFactory
    
    def load_custom_function(self, 
                             function_ns, 
                             function_factory=None,
                             function_factory_path=None):
        """Add a user defined function to the list of functions supported"""
        
        if function_ns in XacmlFunctionNames.FUNCTION_NAMES:
            raise OverwritingStdFunctionError("Attempting to overwrite the "
                                              "standard function namespace %r"
                                              "with a new custom function" %
                                              function_ns)
        if function_factory is None:
            if not isinstance(function_factory_path, basestring):
                raise TypeError('Expecting "function_factory_path" keyword '
                                'set to string function factory path; got %r' %
                                function_factory_path)
            try:
                function_factory = callModuleObject(function_factory_path)
                          
            except (ImportError, AttributeError), e:
                log.error("Error importing function factory class %r for custom "
                          "function identifier %r: %s", function_factory_path, 
                          function_ns, str(e))
                raise
        
        function = function_factory(function_ns)
        if function is None:
            raise unsupportedFunctionErrorFactory(function_ns)
        
        self[function_ns] = function
        self.__custom_class_factory_map[function_ns] = function_factory
         
    def __getitem__(self, key):
        """Override base class implementation to load and cache function classes
        if they don't otherwise exist
        
        @param key: function URN
        @type key: basestring
        @return: function class
        @rtype: ndg.xacml.core.functions.AbstractFunction / NotImplemented
        """
        functionClass = VettedDict.get(self, key)
        if functionClass is None:
            self.loadFunction(key)
            
        return VettedDict.__getitem__(self, key)
        
    def get(self, key, *arg):
        """Likewise to __getitem__, enable loading and caching of function 
        classes if they don't otherwise exist
        
        @param key: XACML function URN
        @type key: basestring
        @param arg: set a single additional argument if required which is 
        used as the default value should the key not be found in the map
        @type arg: tuple
        @return: function class
        @rtype: ndg.xacml.core.functions.AbstractFunction / NotImplemented
        """
        functionClass = VettedDict.get(self, key, *arg)
        if functionClass is None:
            self.loadFunction(key)
            return VettedDict.get(self, key, *arg)    
        else:
            return functionClass

# Function map singleton used by match and apply classes - add new keys to
# this dictionary to enable support for custom functions
functionMap = FunctionMap()
