"""NDG XACML Condition type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "15/04/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from abc import abstractmethod

from ndg.xacml.core.context.result import Decision


# Rule Combining algorithms from the XACML spec.
ALGORITHMS = (
'urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:deny-overrides',
'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:deny-overrides',
'urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:permit-overrides',
'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:permit-overrides',
'urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:first-applicable',
'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:first-applicable',
'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:only-one-applicable',
'urn:oasis:names:tc:xacml:1.1:rule-combining-algorithm:ordered-deny-overrides',
'urn:oasis:names:tc:xacml:1.1:policy-combining-algorithm:ordered-deny-overrides',
'urn:oasis:names:tc:xacml:1.1:rule-combining-algorithm:ordered-permit-overrides',
'urn:oasis:names:tc:xacml:1.1:policy-combining-algorithm:ordered-permit-overrides',
)


class RuleCombiningAlgInterface(object):
    """Interface class for XAML rule combining algorithms"""
    
    @abstractmethod
    def evaluate(self, rules, context):
        """Combine the input rule results to make an access control decision 
        based.  Derived classes must implement this method.  This implementation
        returns indeterminate result.
        
        @param rules: rules from the policy.  Decisions from these will be put
        together into a single decision by this algorithm
        @type rules: TypedList(<ndg.xacml.core.rule.Rule>)
        @param context: request context to apply to the rules
        @type context: ndg.xacml.core.request.Request
        @return: resulting overall access control decision
        @rtype: ndg.xacml.core.context.result.Decision
        """
        return Decision.INDETERMINATE


class DenyOverridesRuleCombiningAlg(RuleCombiningAlgInterface):
    """Deny overrides rule combining algorithm"""
    
    def evaluate(self, rules, context):
        """Combine the input rule results to make an access control decision.
        Implementation taken direct from XACML 2.0 spec. pseudo code - Section
        C.1 Deny Overrides
        
        @param rules: rules from the policy.  Decisions from these will be put
        together into a single decision by this algorithm
        @type rules: TypedList(<ndg.xacml.core.rule.Rule>)
        @param context: request context to apply to the rules
        @type context: ndg.xacml.core.request.Request
        @return: resulting overall access control decision
        @rtype: ndg.xacml.core.context.result.Decision
        """
        atLeastOneError = False
        potentialDeny = False
        atLeastOnePermit = False
        
        for rule in rules:
            decision = rule.evaluate(context)
            if decision == Decision.DENY:
                return Decision.DENY

            if decision == Decision.PERMIT:
                atLeastOnePermit = True
                continue
            
            if decision == Decision.NOT_APPLICABLE:
                continue
            
            if decision == Decision.INDETERMINATE:
                atLeastOneError = True
    
                if rule.effect.value == Decision.DENY:
                    potentialDeny = True
                    
                continue

        if potentialDeny:
            return Decision.INDETERMINATE

        elif atLeastOnePermit:
            return Decision.PERMIT
        
        elif atLeastOneError:
            return Decision.INDETERMINATE
        else:
            return Decision.NOT_APPLICABLE


class PermitOverridesRuleCombiningAlg(RuleCombiningAlgInterface):
    """Implementation of permit overrides XACML rule combining algorithm"""
    
    def evaluate(self, rules, context):
        """Combine the input rule results to make an access control decision.
        Implementation taken direct from XACML 2.0 spec. pseudo code - Section
        C.3
        
        @param rules: rules from the policy.  Decisions from these will be put
        together into a single decision by this algorithm
        @type rules: TypedList(<ndg.xacml.core.rule.Rule>)
        @param context: request context to apply to the rules
        @type context: ndg.xacml.core.request.Request
        @return: resulting overall access control decision
        @rtype: ndg.xacml.core.context.result.Decision
        """
        atLeastOneError = False
        potentialPermit = False
        atLeastOneDeny = False
        
        for rule in rules:
            decision = rule.evaluate(context)
            if decision == Decision.DENY:
                atLeastOneDeny = True
                continue
            
            if decision == Decision.PERMIT:
                log.debug("Rule %r permits, returning overall permit decision",
                          rule.id)
                return Decision.PERMIT
            
            if decision == Decision.NOT_APPLICABLE:
                continue
            
            if decision == Decision.INDETERMINATE:
                atLeastOneError = True
                
                if rule.effect.value == Decision.PERMIT_STR:
                    potentialPermit = True
                
                continue
        
        if potentialPermit:
            log.debug('Rule found with potential permit but it evaluates to '
                      'indeterminate, returning overall indeterminate decision')
            return Decision.INDETERMINATE
        
        if atLeastOneDeny:
            log.debug('At least one rule with a deny decision found, returning '
                      'overall deny decision')
            return Decision.DENY
        
        if atLeastOneError:
            log.debug('At least one rule with an error found, returning '
                      'overall indeterminate decision')
            return Decision.INDETERMINATE
        
        log.debug('No rules were applicable to the request, returning '
                  'overall not applicable decision')
        return Decision.NOT_APPLICABLE

    
class FirstApplicableRuleCombiningAlg(RuleCombiningAlgInterface):
    """Implementation of first applicable XACML rule combining algorithm"""
    
    def evaluate(self, rules, context):
        """Combine the input rule results to make an access control decision.
        Implementation taken direct from XACML 2.0 spec. pseudo code - Section
        C.5
        
        @param rules: rules from the policy.  Decisions from these will be put
        together into a single decision by this algorithm
        @type rules: TypedList(<ndg.xacml.core.rule.Rule>)
        @param context: request context to apply to the rules
        @type context: ndg.xacml.core.request.Request
        @return: resulting overall access control decision
        @rtype: ndg.xacml.core.context.result.Decision
        """
        for rule in rules:
            decision = rule.evaluate(context)
            if decision == Decision.DENY:
                log.debug("Rule %r denies, returning overall deny decision",
                          rule.id)
                return Decision.DENY

            if decision == Decision.PERMIT:
                log.debug("Rule %r permits, returning overall permit decision",
                          rule.id)
                return Decision.PERMIT

            if decision == Decision.NOT_APPLICABLE:
                continue

            if decision == Decision.INDETERMINATE:
                log.debug("Rule %r is indeterminate, returning overall "
                          "indeterminate decision", rule.id)
                return Decision.INDETERMINATE
        
        log.debug('No rules were applicable to the request, returning '
                  'overall not applicable decision')
        return Decision.NOT_APPLICABLE


class RuleCombiningAlgClassFactory(object):
    """Class Factory mapping Rule Combining Algorithm identifiers to their
    class implementations"""
    
    # All algorithms are not implemented by default(!)
    DEFAULT_MAP = {}.fromkeys(ALGORITHMS, NotImplemented)
    
    # Permit overrides is the only one currently implemented
    DEFAULT_MAP.update({
    'urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:deny-overrides':
        DenyOverridesRuleCombiningAlg,      
    'urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:permit-overrides':
        PermitOverridesRuleCombiningAlg,
    'urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:first-applicable':
        FirstApplicableRuleCombiningAlg
    })
    __slots__ = ('__map',)
    
    def __init__(self, map=DEFAULT_MAP):
        """Initialise mapping of identifiers to class implementations
        
        @param map: mapping of rule combining algorithms IDs to classes.  Set 
        this to override the default taken from the DEFAULT_MAP class variable
        """
        self.__map = map
    
    def __call__(self, identifier):
        """Return the class for a given Rule Combining Algorithm identifier
        @param identifier: XACML rule combining algorithm urn
        @type identifier: basestring
        @return: rule combining class corresponding to the given input
        identifier
        @rtype: RuleCombiningAlgInterface derived type or NoneType if no match 
        is found or NotImplementedType if the identifier corresponds to a valid 
        XACML rule combining algorithm but is not supported in this 
        implementation
        """
        return self.__map.get(identifier)
