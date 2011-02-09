"""NDG XACML Condition type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "25/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core import XacmlCoreBase
from ndg.xacml.core.expression import Expression


class Condition(XacmlCoreBase):
    """XACML 2.0 Rule Condition Note the difference to XACML 1.0: the Condition 
    element is its own type and not an Apply type.  It expects a single 
    Expression derived type child element

    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string

    @cvar APPLY_ELEMENT_LOCAL_NAME: XML local name for the apply element
    @type APPLY_ELEMENT_LOCAL_NAME: string

    @ivar __expression: expression in this condition
    @type __expression: ndg.xacml.core.expression.Expression
    """
    ELEMENT_LOCAL_NAME = 'Condition'
    APPLY_ELEMENT_LOCAL_NAME = 'Apply'
    
    __slots__ = ('__expression', )
    
    def __init__(self):
        super(Condition, self).__init__()
        self.__expression = None
        
    @property
    def expression(self):
        """Get expression
        
        @return: expression for this condition
        @rtype: ndg.xacml.core.expression.Expression / NoneType
        """
        return self.__expression
        
    @expression.setter
    def expression(self, value):
        """Set expression
        
        @param value: expression for this condition
        @type value: ndg.xacml.core.expression.Expression
        @raise TypeError: incorrect input type set
        """
        if not isinstance(value, Expression):
            raise TypeError('Expecting Expression or Expression derived type '
                            'for "expression" attribute; got %r' %
                            type(value))
        self.__expression = value
    
    def evaluate(self, context):
        """Evaluate this rule condition
        @param context: the request context
        @type context: ndg.xacml.core.request.Request
        @return: True/False status for whether the rule condition matched or
        not
        @rtype: bool
        """
        result = self.expression.evaluate(context)
        
        return result