"""NDG XACML policy finder interpreting ID references as URLs

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "02/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import os

from ndg.xacml.core.policybase import PolicyBase
from ndg.xacml.finder.policyfinderbase import PolicyFinderBase
from ndg.xacml.parsers import XMLParseError
import ndg.xacml.utils.urlfetcher as urlfetcher

class UrlPolicyFinder(PolicyFinderBase):
    '''
    Concrete subclass of PolicyFinderBase that interprets ID references as URLs.
    '''

    # File scheme prefix
    _FILE_SCHEME = 'file://'
    # Other recognised scheme prefixes
    _NON_FILE_SCHEMES = ['ftp://', 'http://', 'https://']
    # Scheme to use if reference has no scheme prefix
    _DEFAULT_SCHEME = _FILE_SCHEME
    # String following scheme in URL
    _SCHEME_SEPARATOR = '://'
    # Path start implying relative path.
    _RELATIVE_PATH_PREFIX = '.' + os.path.sep

    def __init__(self, basePath):
        '''
        @param basePath: base path for resolving relative references
        @type basePath str
        '''
        super(UrlPolicyFinder, self).__init__()
        self.basePath = basePath

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
        policy = self.policyMap.get(policyIdReference, None)
        if policy is None:
            policy = self._findPolicyFromReference(policyIdReference, common)
        # Look up the policy by ID - this means that it will only be found if
        # the ID declared in the document matches the required ID.
        policy = self.policyMap.get(policyIdReference, None)
        if policy is None:
            raise XMLParseError("Referenced Policy of ID %r not found" %
                                policyIdReference)
        return policy

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
        policySet = self.policySetMap.get(policySetIdReference, None)
        if policySet is None:
            policySet = self._findPolicyFromReference(policySetIdReference,
                                                      common)
        # Look up the policy set by ID - this means that it will only be found
        # if the ID declared in the document matches the required ID.
        policySet = self.policySetMap.get(policySetIdReference, None)
        if policySet is None:
            raise XMLParseError("Referenced PolicySet of ID %r not found" %
                                policySetIdReference)
        return policySet

    def _findPolicyFromReference(self, reference, common):
        """
        Retrieves a policy or policy set for a specified ID that has not been
        read already by interpreting the reference as a URL.
        @param reference: ID reference
        @type reference: str
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: policy set
        @rtype: ndg.xacml.core.policy.PolicySet
        @raise XMLParseError: policy set of specified ID not found
        """
        url = self._makeUrlFromReference(reference)
        policyDoc = urlfetcher.fetch_stream_from_url(url)
        policy = PolicyBase.fromNestedSource(policyDoc, common)
        return policy

    def _makeUrlFromReference(self, reference):
        """
        Makes a URL from the reference. If it already begins with a known scheme
        prefix, the reference is not modified, otherwise it is made into a file
        URL (relative to the base path if it does not start with a path
        separator).
        file://dir/file and file://./dir/file are treated as relative paths.
        file:///dir/file is treated as an absolute path.
        @param reference: ID reference
        @type reference: str
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: URL
        @rtype: str
        """
        # See if reference looks like a URL for a known scheme.
        if reference.startswith(self._FILE_SCHEME):
            path = reference[len(self._FILE_SCHEME):]
            if path.startswith(self._RELATIVE_PATH_PREFIX):
                # Relative path - convert to absolute.
                path = path[len(self._RELATIVE_PATH_PREFIX):]
                url = self._FILE_SCHEME + os.path.join(self.basePath, path)
            elif not path.startswith(os.path.sep):
                # Relative path - convert to absolute.
                url = self._FILE_SCHEME + os.path.join(self.basePath, path)
            else:
                url = reference
        elif [True for scheme in self._NON_FILE_SCHEMES
            if reference.startswith(scheme)]:
            url = reference
        else:
            # No scheme so use default scheme.
            if reference.startswith(os.path.sep):
                url = self._DEFAULT_SCHEME + reference
            else:
                url = (self._DEFAULT_SCHEME +
                       os.path.join(self.basePath, reference))
        return url
