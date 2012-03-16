"""NDG XACML concatenate functions module

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "06/02/12"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
from ndg.xacml.core.attributevalue import AttributeValueClassFactory
from ndg.xacml.core.functions import (AbstractFunction,
                                      FunctionClassFactoryBase)
from ndg.xacml.core.context.exceptions import (XacmlContextError,
                                               XacmlContextTypeError)

attributeValueClassFactory = AttributeValueClassFactory()

class ConcatenateBase(AbstractFunction):
    """Base class for XACML <type>-concatenate functions

    @cvar FUNCTION_NS: namespace for this function
    @type FUNCTION_NS: string
    @cvar TYPE_REST: type for all but first argument
    @type TYPE_REST: type
    """
    FUNCTION_NS = None
    TYPE_REST = attributeValueClassFactory(
                                    'http://www.w3.org/2001/XMLSchema#string')

    def evaluate(self, *args):
        """Perform CONCATENATE function on the variable length argument list of
        elements

        access_control-xacml-2.0-core-spec-os, Feb 2005 - A.3.9 String functions
        @param *args: variable number of arguments to be concatenated
        @type *args: ndg.xacml.utils.TypedList

        @return: result of concatenating the inputs
        @rtype: type of first argument
        """
        # This implementation works because both concatenate functions append
        # string values to a first argument, which may not be a string but is of
        # the same type as the return value. (The native type of the first
        # argument and return value must be basestring.)
        if len(args) < 2:
            # Must have at least two arguments.
            raise XacmlContextError(
                            "Argument list should have length two or greater")
        else:
            # Check types.
            if not isinstance(args[0], self.__class__.TYPE):
                raise XacmlContextTypeError('Expecting %r derived type for '
                                            'argument 1; got %r' %
                                            (self.__class__.TYPE,
                                             type(args[0])))
            for n, arg in enumerate(args[1:]):
                if not isinstance(arg, self.__class__.TYPE_REST):
                    raise XacmlContextTypeError('Expecting %r derived type for '
                                                'argument %d; got %r' %
                                                (self.__class__.TYPE_REST,
                                                 n + 1,
                                                 type(arg)))

            result = ''.join([a.value for a in args])
        returnValue = self.__class__.TYPE(result)
        return returnValue


class FunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-concatenate XACML 2.0 function classes

    @cvar FUNCTION_NAMES: concatenate function URNs
    @type FUNCTION_NAMES: tuple

    @cvar FUNCTION_NS_SUFFIX: generic suffix for concatenate function URNs
    @type FUNCTION_NS_SUFFIX: string

    @cvar FUNCTION_BASE_CLASS: base class for all concatenate classes
    @type FUNCTION_BASE_CLASS: type
    """
    FUNCTION_NAMES = (
        'urn:oasis:names:tc:xacml:2.0:function:string-concatenate',
        'urn:oasis:names:tc:xacml:2.0:function:url-string-concatenate'
    )
    FUNCTION_NS_SUFFIX = '-concatenate'
    FUNCTION_BASE_CLASS = ConcatenateBase
