"""NDG XACML equal function module - contains classes to represent XACML 1.0
*-equal functions

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "26/03/10"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
from ndg.xacml.core.context.exceptions import XacmlContextTypeError
from ndg.xacml.core.functions import AbstractFunction, FunctionClassFactoryBase


class EqualBase(AbstractFunction):
    """Generic equal function for all types
    
    @cvar TYPE: attribute type for the given implementation.  Derived classes
    should set appropriately
    @type TYPE: NoneType
    """
    TYPE = None
    
    def evaluate(self, attribute1, attribute2):
        """Match input attribute values
        
        @param attribute1: first of two attributes to match
        @type attribute1: ndg.xacml.core.attributevalue.AttributeValue derived
        @param attribute2: second attribute
        @type attribute2: ndg.xacml.core.attributevalue.AttributeValue derived
        @return: True if attributes match, False otherwise
        @rtype: bool
        """
        if not isinstance(attribute1, self.__class__.TYPE):
            raise XacmlContextTypeError('Expecting %r derived type for '
                                        '"attribute1"; got %r' %
                                        (self.__class__.TYPE, 
                                         type(attribute1)))
            
        if not isinstance(attribute2, self.__class__.TYPE):
            raise XacmlContextTypeError('Expecting %r derived type for '
                                        '"attribute2"; got %r' %
                                        (self.__class__.TYPE, 
                                         type(attribute2)))
            
        return attribute1.value == attribute2.value
    

class FunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-equal XACML function classes
    
    @cvar FUNCTION_NAMES: equal function URNs
    @type FUNCTION_NAMES: tuple
    
    @cvar FUNCTION_NS_SUFFIX: generic suffix for equal function URNs
    @type FUNCTION_NS_SUFFIX: string
    
    @cvar FUNCTION_BASE_CLASS: base class for all equal function classes
    @type FUNCTION_BASE_CLASS: ndg.xacml.core.functions.v1.EqualBase
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
        'urn:oasis:names:tc:xacml:1.0:function:xpath-node-equal'
    )
    FUNCTION_NS_SUFFIX = '-equal'
    FUNCTION_BASE_CLASS = EqualBase
