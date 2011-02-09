"""NDG XACML one and only functions module

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "01/04/10"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
#from datetime import datetime, timedelta

from ndg.xacml.core.functions import AbstractFunction, FunctionClassFactoryBase
from ndg.xacml.utils import TypedList as Bag
from ndg.xacml.core.context.exceptions import XacmlContextError


class OneAndOnlyBase(AbstractFunction):
    """Base class for XACML <type>-one-and-only functions
    
    @cvar TYPE: attribute type for the given implementation.  Derived classes
    should set appropriately
    @type TYPE: NoneType
    """
    TYPE = None
    
    def evaluate(self, bag):
        """Check a bag has one element only and return it
        
        @param bag: bag containing one element
        @type bag: ndg.xacml.utils.TypedList
        @return: single item from bag
        @rtype: dependent on bag type set in derived type
        """
        if not isinstance(bag, Bag):
            raise XacmlContextError('Expecting %r derived type for "bag"; '
                                    'got %r' % (Bag, type(bag)))
            
        if bag.elementType != self.__class__.TYPE:
            raise XacmlContextError('Expecting %r type elements for "bag"; '
                                    'got %r' %
                                    (self.__class__.TYPE, bag.elementType))
                        
        nBagElems = len(bag)
        if nBagElems != 1:
            raise XacmlContextError('Expecting single element for %r bag; got '
                                    '%r' % (self.__class__.TYPE, nBagElems))
            
        return bag[0]
    

class FunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-one-and-only XACML function classes
    
    @cvar FUNCTION_NAMES: one and only function URNs
    @type FUNCTION_NAMES: tuple
    
    @cvar FUNCTION_NS_SUFFIX: generic suffix for one and only function URNs
    @type FUNCTION_NS_SUFFIX: string
    
    @cvar FUNCTION_BASE_CLASS: base class for all one and only function classes 
    @type FUNCTION_BASE_CLASS: ndg.xacml.core.functions.v1.OneAndOnlyBase
    """
    FUNCTION_NAMES = (
        'urn:oasis:names:tc:xacml:1.0:function:string-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:boolean-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:integer-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:double-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:time-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:date-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:dateTime-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:anyURI-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:hexBinary-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:base64Binary-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:dayTimeDuration-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:yearMonthDuration-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:x500Name-one-and-only',
        'urn:oasis:names:tc:xacml:1.0:function:rfc822Name-one-and-only'
    )
    FUNCTION_NS_SUFFIX = '-one-and-only'
    FUNCTION_BASE_CLASS = OneAndOnlyBase
    