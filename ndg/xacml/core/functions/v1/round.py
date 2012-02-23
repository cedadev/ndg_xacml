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


class Round(AbstractFunction):
    """Base class for XACML <type>-round functions
    
    @cvar FUNCTION_NS: namespace for this function
    @type FUNCTION_NS: string
    """
    FUNCTION_NS = AbstractFunction.V1_0_FUNCTION_NS + 'round'
    
    def evaluate(self, num):
        """Execute mathematical round up of the input number
        
        @param num: number to round up
        @type num: int / long / float
        @rtype: float
        @raise TypeError: incorrect type for input
        """
        try:
            return round(num)
        except TypeError, e:
            raise XacmlContextTypeError('Round function: %s' % e)

    
class FunctionClassFactory(FunctionClassFactoryInterface):
    """Class Factory for round XACML function class
    """
    def __call__(self, identifier):
        '''Create class for the Round XACML function identifier
        
        @param identifier: XACML round function identifier
        @type identifier: basestring
        @return: round function class or None if identifier doesn't match
        @rtype: ndg.xacml.core.functions.v1.round.Round / NoneType
        '''
        if identifier == Round.FUNCTION_NS:
            return Round
        else:
            return None
