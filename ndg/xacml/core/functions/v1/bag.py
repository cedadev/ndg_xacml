"""NDG XACML string bag function module

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "31/03/10"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
from ndg.xacml.utils import TypedList as Bag
from ndg.xacml.core.functions import AbstractFunction, FunctionClassFactoryBase


class BagBase(AbstractFunction):
    """Abstract bag function for all types of bag function
    
    urn:oasis:names:tc:xacml:1.0:function:<type>-bag
    
    @cvar TYPE: attribute type for the given implementation.  Derived classes
    should set appropriately
    @type TYPE: NoneType
    
    @cvar FUNCTION_SUFFIX: suffix for all bag function class names
    @type FUNCTION_SUFFIX: string
    
    @cvar FUNCTION_NS_SUFFIX: generic suffix for at least one member of function
    URNs
    @type FUNCTION_NS_SUFFIX: string
    """
    TYPE = None
    FUNCTION_SUFFIX = 'Bag'
    FUNCTION_NS_SUFFIX = '-bag'
    
    def evaluate(self, *args):
        """return inputs into a bag
        
        @param args: inputs to add to bag
        @type args: tuple
        @return: True if strings match, False otherwise
        @rtype: bool
        """
        bag = Bag(self.__class__.TYPE)
        for i in args:
            if not isinstance(i, self.__class__.TYPE):
                raise TypeError('Expecting %r derived type for bag element; '
                                'got %r' % (self.__class__.TYPE, type(i)))
            bag.append(i)
         
        return bag


class FunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-bag XACML function classes
    
    @cvar FUNCTION_NAMES: bag function URNs
    @type FUNCTION_NAMES: tuple
    
    @cvar FUNCTION_NS_SUFFIX: generic suffix for bag function URNs
    @type FUNCTION_NS_SUFFIX: string
    
    @cvar FUNCTION_BASE_CLASS: base class for all bag function classes
    @type FUNCTION_BASE_CLASS: ndg.xacml.core.functions.v1.BagBase
    """
    FUNCTION_NAMES = (
        'urn:oasis:names:tc:xacml:1.0:function:string-bag',
        'urn:oasis:names:tc:xacml:1.0:function:boolean-bag',
        'urn:oasis:names:tc:xacml:1.0:function:integer-bag',
        'urn:oasis:names:tc:xacml:1.0:function:double-bag',
        'urn:oasis:names:tc:xacml:1.0:function:time-bag',
        'urn:oasis:names:tc:xacml:1.0:function:date-bag',
        'urn:oasis:names:tc:xacml:1.0:function:dateTime-bag',
        'urn:oasis:names:tc:xacml:1.0:function:anyURI-bag',
        'urn:oasis:names:tc:xacml:1.0:function:hexBinary-bag',
        'urn:oasis:names:tc:xacml:1.0:function:base64Binary-bag',
        'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-bag',
        'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-bag',
        'urn:oasis:names:tc:xacml:1.0:function:x500Name-bag',
        'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-bag',
    )
    FUNCTION_NS_SUFFIX = '-bag'
    FUNCTION_BASE_CLASS = BagBase 
