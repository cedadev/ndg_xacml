"""NDG XACML Policy Decision Point type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "25/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.core.context.pdpinterface import PDPInterface
from ndg.xacml.core.policybase import PolicyBase
from ndg.xacml.finder.defaultfinder import getDefaultPolicyFinder


class PDP(PDPInterface):
    """A XACML Policy Decision Point implementation.  It supports the use of a 
    single policy but not policy sets
    
    @ivar __policy: policy object for PDP to use to apply access control
    decisions
    @type policy: ndg.xacml.core.policy.Policy / None
    """
    __slots__ = ('__policy',)
    
    def __init__(self, policy=None):
        """
        @param policy: policy object for PDP to use to apply access control
        decisions, may be omitted.
        @type policy: ndg.xacml.core.policy.Policy / None
        """
        self.__policy = None
        if policy is not None:
            self.policy = policy
        
    @classmethod
    def fromPolicySource(cls, source, readerFactory, finder=None):
        """Create a new PDP instance with a given policy
        @param source: source for policy
        @type source: type (dependent on the reader set, it could be for example
        a file path string, file object, XML element instance)
        @param readerFactory: reader factory returns the reader to use to read 
        this policy
        @type readerFactory: ndg.xacml.parsers.AbstractReader derived type
        @param finder: policy finder
        @type finder: ndg.xacml.finder.PolicyFinderBase subclass
        """           
        pdp = cls()
        if not finder:
            # Set a default policy finder.
            finder = getDefaultPolicyFinder(source)
        pdp.setPolicyFromSource(source, readerFactory, finder)
        return pdp
    
    def setPolicyFromSource(self, source, readerFactory, finder):
        """initialise PDP with the given policy
        @param source: source for policy
        @type source: type (dependent on the reader set, it could be for example
        a file path string, file object, XML element instance)
        @param readerFactory: reader factory returns the reader to use to read 
        this policy
        @type readerFactory: ndg.xacml.parsers.AbstractReader derived type
        @param finder: policy finder
        @type finder: ndg.xacml.finder.PolicyFinderBase subclass
        """           
        self.policy = PolicyBase.fromSource(source, readerFactory, finder)
        
    @property
    def policy(self):
        """Get policy
        @return: policy object for PDP to use to apply access control decisions
        @rtype: ndg.xacml.core.policy.Policy
        """
        return self.__policy
    
    @policy.setter
    def policy(self, value):
        '''Set policy
        @param value: policy object for PDP to use to apply access control 
        decisions
        @type value: ndg.xacml.core.policy.Policy
        '''
        if not isinstance(value, PolicyBase):
            raise TypeError('Expecting %r derived type for "policy" input; got '
                            '%r instead' % (PolicyBase, type(value)))
        self.__policy = value
                                        
    def evaluate(self, request):
        """Make an access control decision for the given request based on the
        single policy provided
        
        @param request: XACML request context
        @type request: ndg.xacml.core.context.request.Request
        @return: XACML response instance
        @rtype: ndg.xacml.core.context.response.Response
        """
        response = self.policy.evaluateResponse(request)
        
        return response



