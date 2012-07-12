#!/usr/bin/env python
"""NDG XACML PDP unit tests 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "28/10/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id: test_pdp.py 8078 2012-06-19 14:10:35Z pjkersha $"
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)

from ndg.xacml.core.policy import Policy
from ndg.xacml.core.target import Target
from ndg.xacml.core import Identifiers
from ndg.xacml.core.context.environment import Environment
from ndg.xacml.core.context.request import Request
from ndg.xacml.core.context.result import Decision
from ndg.xacml.core.context.action import Action
from ndg.xacml.core.context.resource import Resource as ResourceCtx
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.subject import Subject as CtxSubject
from ndg.xacml.core.resource import Resource, ResourceMatch
from ndg.xacml.core.subject import Subject, SubjectMatch
from ndg.xacml.core.attributedesignator import (SubjectAttributeDesignator,
                                                ResourceAttributeDesignator)
from ndg.xacml.core.attribute import Attribute
from ndg.xacml.core.attributevalue import (AttributeValueClassFactory,
                                           AttributeValue)
from ndg.xacml.core.rule import Rule, Effect

ROLE_ATTRIBUTE_ID = "urn:ndg:security:authz:1.0:attr"
SUBJECT_ID = 'https://my.name.somewhere.ac.uk'
attributeValueFactory = AttributeValueClassFactory()
AnyUriAttributeValue = attributeValueFactory(AttributeValue.ANY_TYPE_URI)
StringAttributeValue = attributeValueFactory(AttributeValue.STRING_TYPE_URI)
   
   
class XacmlDynamicPolicyTestCase(unittest.TestCase):
    """Test Dynamic creation of policy and rules from code API instead of
    XML policy file"""
    attributeValueClassFactory = AttributeValueClassFactory()
    
    
    def _create_policy(self):
        self.policy = Policy()
        self.policy.policyId = 'Dynamic Policy Test'
        self.policy.ruleCombiningAlgId = \
    'urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:permit-overrides'
        
        # Add top-level target - determines an overall match for this policy 
        self.policy.target = Target()
        
        # Match based on resource - add a resource match to the target
        resource = Resource()
        resource_match = ResourceMatch()
        resource_match.matchId = "urn:oasis:names:tc:xacml:2.0:function:anyURI-regexp-match"
        
        resource_match.attributeValue = self.__class__.attributeValueClassFactory(
                                    "http://www.w3.org/2001/XMLSchema#anyURI")()
        resource_match.attributeValue.value = '^http://localhost/.*'
        resource_match.attributeDesignator = ResourceAttributeDesignator()
        resource_match.attributeDesignator.attributeId = "urn:oasis:names:tc:xacml:1.0:resource:resource-id"
        resource_match.attributeDesignator.dataType = "http://www.w3.org/2001/XMLSchema#anyURI"
        resource.matches.append(resource_match)
        self.policy.target.resources.append(resource) 
        
        # Add rules
        denyall_rule = Rule()
        denyall_rule.id = 'Deny all rule'
        denyall_rule.effect = Effect.DENY
        
        self.policy.rules.append(denyall_rule)
        
        singlerole_rule = Rule()
        singlerole_rule.id = 'dataset1 rule'
        singlerole_rule.effect = Effect.PERMIT
        singlerole_rule.target = Target()
        
        resource_match1 = ResourceMatch()
        resource_match1.matchId = "urn:oasis:names:tc:xacml:2.0:function:anyURI-regexp-match"
        
        resource_match1.attributeValue = self.__class__.attributeValueClassFactory(
                                    "http://www.w3.org/2001/XMLSchema#anyURI")()
        resource_match1.attributeValue.value = '^http://localhost/dataset1/.*$'
        resource_match1.attributeDesignator = ResourceAttributeDesignator()
        resource_match1.attributeDesignator.attributeId = "urn:oasis:names:tc:xacml:1.0:resource:resource-id"
        resource_match1.attributeDesignator.dataType = "http://www.w3.org/2001/XMLSchema#anyURI"

        resource1 = Resource()
        resource1.matches.append(resource_match1)

        singlerole_rule.target.resources.append(resource1)
        
        subject_match1 = SubjectMatch()
        subject_match1.matchId = "urn:oasis:names:tc:xacml:1.0:function:string-equal"
        
        subject_match1.attributeValue = self.__class__.attributeValueClassFactory(
                                    "http://www.w3.org/2001/XMLSchema#string")()
        subject_match1.attributeValue.value = 'staff'
        subject_match1.attributeDesignator = SubjectAttributeDesignator()
        subject_match1.attributeDesignator.attributeId = ROLE_ATTRIBUTE_ID
        subject_match1.attributeDesignator.dataType = "http://www.w3.org/2001/XMLSchema#string"

        subject1 = Subject()
        subject1.matches.append(subject_match1)

        singlerole_rule.target.subjects.append(subject1)
        
        self.policy.rules.append(singlerole_rule)

    @staticmethod
    def _create_request_ctx(resourceId, 
                          includeSubject=True,
                          subjectId=SUBJECT_ID,
                          subjectRoles=None,
                          roleAttributeId=ROLE_ATTRIBUTE_ID,
                          action='read',
                          resourceContent=None):
        """Create an example XACML Request Context for tests"""
        if subjectRoles is None:
            subjectRoles = ('staff',)
            
        request = Request()
        
        if includeSubject:
            subject = CtxSubject()
            openidSubjectAttribute = Attribute()
            
            openidSubjectAttribute.attributeId = "urn:esg:openid"
            openidSubjectAttribute.dataType = AnyUriAttributeValue.IDENTIFIER
            
            openidSubjectAttribute.attributeValues.append(
                                                        AnyUriAttributeValue())
            openidSubjectAttribute.attributeValues[-1].value = subjectId
                                        
            
            subject.attributes.append(openidSubjectAttribute)
    
            for role in subjectRoles:
                roleAttribute = Attribute()
                
                roleAttribute.attributeId = roleAttributeId
                roleAttribute.dataType = StringAttributeValue.IDENTIFIER
                
                roleAttribute.attributeValues.append(StringAttributeValue())
                roleAttribute.attributeValues[-1].value = role 
            
                subject.attributes.append(roleAttribute)
                                      
            request.subjects.append(subject)
        
        resource = ResourceCtx()
        resourceAttribute = Attribute()
        resource.attributes.append(resourceAttribute)
        
        resourceAttribute.attributeId = Identifiers.Resource.RESOURCE_ID
                            
        resourceAttribute.dataType = AnyUriAttributeValue.IDENTIFIER
        resourceAttribute.attributeValues.append(AnyUriAttributeValue())
        resourceAttribute.attributeValues[-1].value = resourceId

        resource.resourceContent = resourceContent

        request.resources.append(resource)
        
        request.action = Action()
        actionAttribute = Attribute()
        request.action.attributes.append(actionAttribute)
        
        actionAttribute.attributeId = Identifiers.Action.ACTION_ID
        actionAttribute.dataType = StringAttributeValue.IDENTIFIER
        actionAttribute.attributeValues.append(StringAttributeValue())
        actionAttribute.attributeValues[-1].value = action

        request.environment = Environment()
        
        return request
    
    def _create_pdp(self):
        self._create_policy()
        self.pdp = PDP(policy=self.policy)
        
    def test01_create_policy(self):
        self._create_policy()
        
    def test02_create_pdp(self):
        self._create_pdp()
        
    def test03_test_rule(self):
        self._create_pdp()
        request = self._create_request_ctx('http://localhost/dataset1/my.nc', 
                                           subjectId='http://me.openid.ac.uk', 
                                           subjectRoles=('staff',))
        response = self.pdp.evaluate(request)
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision") 
    
        
if __name__ == "__main__":
    unittest.main()