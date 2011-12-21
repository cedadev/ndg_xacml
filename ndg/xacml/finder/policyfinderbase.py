"""NDG Security finder base class

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "01/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"

from abc import ABCMeta, abstractmethod
import logging
log = logging.getLogger(__name__)

from ndg.xacml.parsers import XMLParseError

class PolicyFinderBase(object):
    """
    Base class for policy finders. The specific finder strategy is implemented
    in the findPolicy and findPolicySet methods.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.policyMap = {}
        self.policySetMap = {}

    @abstractmethod
    def findPolicy(self, policyIdReference, common):
        """
        Retrieves a policy for a specified policy ID.
        @param policyIdReference: policy ID reference
        @type policyIdReference: str
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: policy
        @rtype: None (subclasses should return ndg.xacml.core.policy.Policy)
        """
        return None

    @abstractmethod
    def findPolicySet(self, policySetIdReference, common):
        """
        Retrieves a policy set for a specified policy set ID.
        @param policySetIdReference: policy set ID reference
        @type policySetIdReference: str
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: policy set
        @type: None (subclasses should return ndg.xacml.core.policy.PolicySet)
        """
        return None

    def setReader(self, reader):
        """
        Sets the reader to be used when parsing referenced policies.
        @param reader: reader
        @type reader: ndg.xacml.parsers.AbstractReader derived type
        """
        self.reader = reader

    def addPolicyReference(self, policy):
        """
        @param policy: policy
        @type policy: ndg.xacml.core.policy.Policy
        @raise XMLParseError: if the policy's ID is a duplicate of one already
        found
        """
        if policy.policyId in self.policyMap:
            raise XMLParseError("Duplicate Policy ID %r found" % policy.policyId)
        self.policyMap[policy.policyId] = policy

    def addPolicySetReference(self, policySet):
        """
        @param policy: policy set
        @type policy: ndg.xacml.core.policy.PolicySet
        @raise XMLParseError: if the policy's ID is a duplicate of one already
        found
        """
        if policySet.policySetId in self.policySetMap:
            raise XMLParseError("Duplicate PolicySet ID %r found" % policySet.policySetId)
        self.policySetMap[policySet.policySetId] = policySet
