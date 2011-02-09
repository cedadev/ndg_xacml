"""NDG XACML URI equal matching function module

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "30/03/10"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
from ndg.xacml.core.functions import AbstractFunction, FunctionClassFactoryBase
from ndg.xacml.core.context.exceptions import XacmlContextTypeError
from ndg.xacml.utils import TypedList as Bag


class AtLeastOneMemberOfBase(AbstractFunction):
    """Base class implementation for at least one member of XACML function -
    check at least one item in one set is contained in the second set
    
    urn:oasis:names:tc:xacml:1.0:function:<type>-at-least-one-member-of
    
    @cvar TYPE: attribute type for the given implementation.  Derived classes
    should set appropriately
    @type TYPE: NoneType
    """
    TYPE = None
    
    def evaluate(self, set1, set2):
        """Check input is contained in the bag
        
        @param set1: check to see if at least one item in this set is contained 
        in the second set
        @type set1: TypedList(self.__class__.TYPE)
        @param set2: bag of self.__class__.TYPE values
        @type set2: TypedList(self.__class__.TYPE)
        @return: True if str is in bag, False otherwise
        @rtype: bool
        """
        if not isinstance(set1, Bag):
            raise XacmlContextTypeError('Expecting %r derived type for "set1"; '
                                        'got %r' % (Bag, type(set1)))
            
        if set1.elementType != self.__class__.TYPE:
            raise XacmlContextTypeError('Expecting %r type elements for '
                                        '"set1"; got %r' %
                                        (self.__class__.TYPE, set1.elementType))
            
        if not isinstance(set2, Bag):
            raise XacmlContextTypeError('Expecting %r derived type for "set2"; '
                                        'got %r' % (Bag, type(set2)))
            
        if set2.elementType != self.__class__.TYPE:
            raise XacmlContextTypeError('Expecting %r type elements for '
                                        '"set2"; got %r' %
                                        (self.__class__.TYPE, set2.elementType))
            
        _set1 = set([attr.value for attr in set1])
        _set2 = set([attr.value for attr in set2])
        
        return len(list(_set1 & _set2)) > 0
    

class FunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-at-least-one-member-of XACML function classes
    
    @cvar FUNCTION_NAMES: list of at least one member of function URNs
    @type FUNCTION_NAMES: tuple
    
    @cvar FUNCTION_NS_SUFFIX: generic suffix for at least one member of function
    URNs
    @type FUNCTION_NS_SUFFIX: string
    
    @cvar FUNCTION_BASE_CLASS: base class for all at least one member of 
    function classes
    @type FUNCTION_BASE_CLASS: ndg.xacml.core.functions.v1.AtLeastOneMemberOfBase
    """
    FUNCTION_NAMES = (
'urn:oasis:names:tc:xacml:1.0:function:string-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:boolean-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:integer-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:double-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:time-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:date-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:dateTime-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:anyURI-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:hexBinary-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:base64Binary-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:x500Name-at-least-one-member-of',
'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-at-least-one-member-of',
    )
    FUNCTION_NS_SUFFIX = '-at-least-one-member-of'
    FUNCTION_BASE_CLASS = AtLeastOneMemberOfBase
