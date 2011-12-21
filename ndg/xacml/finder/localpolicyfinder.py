"""NDG XACML policy finder resolving within base policy document

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "02/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.finder.policyfinderbase import PolicyFinderBase
from ndg.xacml.parsers import XMLParseError

class LocalPolicyFinder(PolicyFinderBase):
    """
    Policy and Policy Set finder that only resolves references to already parsed
    Polices and Policy Sets.
    """
    def findPolicy(self, policyIdReference, common):
        """
        Retrieves a policy for a specified policy ID.
        @param policyIdReference: policy ID reference
        @type policyIdReference: str
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: policy
        @rtype: ndg.xacml.core.policy.Policy
        @raise XMLParseError: policy of specified ID not found
        """
        if policyIdReference not in self.policyMap:
            raise XMLParseError("Referenced Policy of ID %r not found" % policyIdReference)
        return self.policyMap.get(policyIdReference, None)

    def findPolicySet(self, policySetIdReference, common):
        """
        Retrieves a policy set for a specified policy set ID.
        @param policySetIdReference: policy set ID reference
        @type policySetIdReference: str
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: policy set
        @rtype: ndg.xacml.core.policy.PolicySet
        @raise XMLParseError: policy set of specified ID not found
        """
        if policySetIdReference not in self.policySetMap:
            raise XMLParseError("Referenced PolicySet of ID %r not found" % policySetIdReference)
        return self.policySetMap.get(policySetIdReference, None)
