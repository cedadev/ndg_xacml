"""NDG XACML one and only functions module

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "01/04/10"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
from ndg.xacml.core.functions import (AbstractFunction, 
                                      FunctionClassFactoryInterface)
from ndg.xacml.core.context.exceptions import XacmlContextTypeError


class And(AbstractFunction):
    """Base class for XACML <type>-and functions
    
    @cvar FUNCTION_NS: namespace for this function
    @type FUNCTION_NS: string
    @cvar ATTRIBUTE_TYPE: type for arguments
    @type ATTRIBUTE_TYPE: str
    """
    FUNCTION_NS = AbstractFunction.V1_0_FUNCTION_NS + 'and'
    ATTRIBUTE_TYPE = bool
    
    def evaluate(self, *args):
        """perform AND function on the variable length argument list of elements

        access_control-xacml-2.0-core-spec-os, Fe 2005 - A.3.5 Logical functions
        access_control-xacml-2.0-core-spec-os, Fe 2005 - 4.2.4.2 ( Rule 2 a[346] ... a[361] )
        @param *args: variable number of elements to be AND'ed
        @type bool: ndg.xacml.utils.TypedList

        @return: result of AND operation on the inputs
        @rtype: bool
        """
        if len(args)==0:
            return True
        else:
            for n, arg in enumerate(args):
                if type(arg) != self.__class__.ATTRIBUTE_TYPE:
                    raise XacmlContextTypeError(
                                'Expecting %r type for attribute %d; got %r' %
                                (self.__class__.ATTRIBUTE_TYPE, n + 1,
                                 type(arg)))
            for arg in args:
                if not arg:
                    return False
        return True


class FunctionClassFactory(FunctionClassFactoryInterface):
    """Class Factory for and XACML function class
    
    @cvar FUNCTION_NS: URN for and function
    @type FUNCTION_NS: string
    """
    FUNCTION_NS = 'urn:oasis:names:tc:xacml:1.0:function:and'
    
    def __call__(self, identifier):
        '''Create class for the And XACML function identifier
        
        @param identifier: XACML and function identifier
        @type identifier: basestring
        @return: and function class or None if identifier doesn't match
        @rtype: ndg.xacml.core.functions.v1.and.And / NoneType
        '''
        if identifier == And.FUNCTION_NS:
            return And
        else:
            return None
