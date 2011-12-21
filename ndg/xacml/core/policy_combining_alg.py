"""NDG XACML Policy Combining Algorithm definitions

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "01/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from abc import abstractmethod

from ndg.xacml.core.context.result import Decision


# Policy combining algorithms from the XACML spec.
ALGORITHMS = (
'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:deny-overrides',
'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:permit-overrides',
'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:first-applicable',
'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:only-one-applicable',
'urn:oasis:names:tc:xacml:1.1:policy-combining-algorithm:ordered-deny-overrides',
'urn:oasis:names:tc:xacml:1.1:policy-combining-algorithm:ordered-permit-overrides',
)


class PolicyCombiningAlgInterface(object):
    """Interface class for XAML policy combining algorithms"""

    @abstractmethod
    def evaluate(self, policies, context):
        """Combine the results from evaluating policies or policy sets to make
        an access control decision.  Derived classes must implement this
        method.  This implementation returns indeterminate result.

        @param policies: policies and/or policy sets.  Decisions from these
        will be put together into a single decision by this algorithm.
        @type policies: TypedList(<ndg.xacml.core.policybase.PolicyBase>)
        @param context: request context to apply to the rules
        @type context: ndg.xacml.core.request.Request
        @return: resulting overall access control decision
        @rtype: ndg.xacml.core.context.result.Decision
        """
        return Decision.INDETERMINATE


class DenyOverridesPolicyCombiningAlg(PolicyCombiningAlgInterface):
    """Deny overrides policy combining algorithm"""

    def evaluate(self, policies, context):
        """Combine the input policy results to make an access control decision.
        Implementation taken directly from XACML 2.0 spec. pseudo code -
        Section C.1 Deny Overrides

        @param policies: policies and/or policy sets.  Decisions from these
        will be put together into a single decision by this algorithm.
        @type policies: TypedList(<ndg.xacml.core.policybase.PolicyBase>)
        @param context: request context to apply to the rules
        @type context: ndg.xacml.core.request.Request
        @return: resulting overall access control decision
        @rtype: ndg.xacml.core.context.result.Decision
        """
        atLeastOnePermit = False

        for policy in policies:
            decision = policy.evaluate(context)
            if decision == Decision.DENY:
                return Decision.DENY

            if decision == Decision.PERMIT:
                atLeastOnePermit = True
                continue

            if decision == Decision.NOT_APPLICABLE:
                continue

            if decision == Decision.INDETERMINATE:
                return Decision.DENY

        if atLeastOnePermit:
            return Decision.PERMIT

        return Decision.NOT_APPLICABLE

class PermitOverridesPolicyCombiningAlg(PolicyCombiningAlgInterface):
    """Implementation of permit overrides XACML policy combining algorithm"""

    def evaluate(self, policies, context):
        """Combine the input policy results to make an access control decision.
        Implementation taken directly from XACML 2.0 spec. pseudo code -
        Section C.3 Permit Overrides

        @param policies: policies and/or policy sets.  Decisions from these
        will be put together into a single decision by this algorithm.
        @type policies: TypedList(<ndg.xacml.core.policybase.PolicyBase>)
        @param context: request context to apply to the rules
        @type context: ndg.xacml.core.request.Request
        @return: resulting overall access control decision
        @rtype: ndg.xacml.core.context.result.Decision
        """
        atLeastOneError = False
        atLeastOneDeny = False

        for policy in policies:
            decision = policy.evaluate(context)
            if decision == Decision.DENY:
                atLeastOneDeny = True
                continue

            if decision == Decision.PERMIT:
                log.debug("Policy %r permits, returning overall permit"
                          " decision", policy.ident)
                return Decision.PERMIT

            if decision == Decision.NOT_APPLICABLE:
                continue

            if decision == Decision.INDETERMINATE:
                atLeastOneError = True
                continue

        if atLeastOneDeny:
            log.debug('At least one policy with a deny decision found, '
                      'returning overall deny decision')
            return Decision.DENY

        if atLeastOneError:
            log.debug('At least one policy with an error found, returning '
                      'overall indeterminate decision')
            return Decision.INDETERMINATE

        log.debug('No policies were applicable to the request, returning '
                  'overall not applicable decision')
        return Decision.NOT_APPLICABLE


class FirstApplicablePolicyCombiningAlg(PolicyCombiningAlgInterface):
    """Implementation of first applicable XACML policy combining algorithm"""

    def evaluate(self, policies, context):
        """Combine the results from evaluating policies or policy sets to make
        an access control decision.  Implementation taken directly from XACML
        2.0 spec. pseudo code - Section C.5 First Applicable

        @param policies: policies and/or policy sets.  Decisions from these
        will be put together into a single decision by this algorithm.
        @type policies: TypedList(<ndg.xacml.core.policybase.PolicyBase>)
        @param context: request context to apply to the rules
        @type context: ndg.xacml.core.request.Request
        @return: resulting overall access control decision
        @rtype: ndg.xacml.core.context.result.Decision
        """
        for policy in policies:
            decision = policy.evaluate(context)
            if decision == Decision.DENY:
                log.debug("Policy %r denies, returning overall deny decision",
                          policy.ident)
                return Decision.DENY

            if decision == Decision.PERMIT:
                log.debug("Policy %r permits, returning overall permit "
                          "decision",
                          policy.ident)
                return Decision.PERMIT

            if decision == Decision.NOT_APPLICABLE:
                continue

            if decision == Decision.INDETERMINATE:
                log.debug("Policy %r is indeterminate, returning overall "
                          "indeterminate decision", policy.ident)
                return Decision.INDETERMINATE

        log.debug('No policies were applicable to the request, returning '
                  'overall not applicable decision')
        return Decision.NOT_APPLICABLE


class PolicyCombiningAlgClassFactory(object):
    """Class Factory mapping Policy Combining Algorithm identifiers to their
    class implementations"""

    # All algorithms are not implemented by default(!)
    DEFAULT_MAP = {}.fromkeys(ALGORITHMS, NotImplemented)

    # Permit overrides is the only one currently implemented
    DEFAULT_MAP.update({
    'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:deny-overrides':
        DenyOverridesPolicyCombiningAlg,
    'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:permit-overrides':
        PermitOverridesPolicyCombiningAlg,
    'urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:first-applicable':
        FirstApplicablePolicyCombiningAlg
    })
    __slots__ = ('__map',)

    def __init__(self, map=DEFAULT_MAP):
        """Initialise mapping of identifiers to class implementations

        @param map: mapping of policy combining algorithms IDs to classes.  Set
        this to override the default taken from the DEFAULT_MAP class variable
        """
        self.__map = map

    def __call__(self, identifier):
        """Return the class for a given Policy Combining Algorithm identifier
        @param identifier: XACML policy combining algorithm urn
        @type identifier: basestring
        @return: policy combining class corresponding to the given input
        identifier
        @rtype: PolicyCombiningAlgInterface derived type or NoneType if no match
        is found or NotImplementedType if the identifier corresponds to a valid
        XACML policy combining algorithm but is not supported in this
        implementation
        """
        return self.__map.get(identifier)
