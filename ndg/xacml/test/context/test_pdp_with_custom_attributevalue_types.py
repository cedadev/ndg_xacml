#!/usr/bin/env python
"""NDG unit tests for PDP working with a policy and request context containing
custom AttributeValue data types

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "28/10/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)

from ndg.xacml.core import Identifiers
from ndg.xacml.core.attribute import Attribute
from ndg.xacml.core.attributevalue import AttributeValueClassFactory
from ndg.xacml.core.functions import functionMap
from ndg.xacml.core.context.request import Request
from ndg.xacml.core.context.subject import Subject
from ndg.xacml.core.context.resource import Resource
from ndg.xacml.core.context.action import Action

from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.parsers.etree.attributevaluereader import (
                                                DataTypeReaderClassFactory)
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import (XACML_ESGFTEST1_FILEPATH,  
                            GroupRoleAttributeValue, 
                            ETreeGroupRoleDataTypeReader,
                            GroupRoleBag,
                            GroupRoleAtLeastOneMemberOf)
from ndg.xacml.test.context import (AnyUriAttributeValue, StringAttributeValue,
                                    SUBJECT_ID)

    
class XacmlEvalPdpWithCustomAttrTypes(unittest.TestCase):
    """Evaluate a policy which contains custom XACML Attribute Value Data types
    """
    AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID = \
        'http://localhost/at-least-one-of-subject-role-restricted'       
    SUBJECT_DOES_NOT_HAVE_ANY_OF_SPECIFIED_ROLES_ID = \
        'http://localhost/subject-does-not-have-any-of-specified-roles'
        
    @staticmethod
    def _createRequestCtx(resourceId, 
                          includeSubject=True,
                          subjectGroupRoles=None,
                          groupRoleAttributeId='urn:esg:attr',
                          action='read'):
        """Create an example XACML Request Context for tests"""
        if subjectGroupRoles is None:
            subjectGroupRoles = [('ACME', 'default')]
            
        request = Request()
        
        if includeSubject:
            subject = Subject()
            openidSubjectAttribute = Attribute()
            
            openidSubjectAttribute.attributeId = "urn:esg:openid"
            openidSubjectAttribute.dataType = AnyUriAttributeValue.IDENTIFIER
            
            openidSubjectAttribute.attributeValues.append(
                                                        AnyUriAttributeValue())
            openidSubjectAttribute.attributeValues[-1].value = SUBJECT_ID
                                        
            
            subject.attributes.append(openidSubjectAttribute)
    
            for group, role in subjectGroupRoles:
                groupRoleAttribute = Attribute()
                
                groupRoleAttribute.attributeId = groupRoleAttributeId
                groupRoleAttribute.dataType = 'urn:grouprole'
                
                groupRoleAttribute.attributeValues.append(
                                                    GroupRoleAttributeValue())
                groupRoleAttribute.attributeValues[-1].group = group 
                groupRoleAttribute.attributeValues[-1].role = role 
            
                subject.attributes.append(groupRoleAttribute)
                                      
            request.subjects.append(subject)
        
        resource = Resource()
        resourceAttribute = Attribute()
        resource.attributes.append(resourceAttribute)
        
        resourceAttribute.attributeId = Identifiers.Resource.RESOURCE_ID
                            
        resourceAttribute.dataType = AnyUriAttributeValue.IDENTIFIER
        resourceAttribute.attributeValues.append(AnyUriAttributeValue())
        resourceAttribute.attributeValues[-1].value = resourceId

        request.resources.append(resource)
        
        request.action = Action()
        actionAttribute = Attribute()
        request.action.attributes.append(actionAttribute)
        
        actionAttribute.attributeId = Identifiers.Action.ACTION_ID
        actionAttribute.dataType = StringAttributeValue.IDENTIFIER
        actionAttribute.attributeValues.append(StringAttributeValue())
        actionAttribute.attributeValues[-1].value = action
        
        return request
        
    def setUp(self):
        """Use ESG sample policy"""
        # Add new type
        AttributeValueClassFactory.addClass('urn:grouprole', 
                                            GroupRoleAttributeValue)
        
        # Add new parser for this type
        DataTypeReaderClassFactory.addReader('urn:grouprole', 
                                ETreeGroupRoleDataTypeReader)
        
        # Add extra matching and bag functions
        functionMap['urn:grouprole-bag'] = GroupRoleBag
        functionMap['urn:grouprole-at-least-one-member-of'
                    ] = GroupRoleAtLeastOneMemberOf
        
        # Example policy with custom attribute value type used with ESGF 
        self.pdp = PDP.fromPolicySource(XACML_ESGFTEST1_FILEPATH, ReaderFactory)
                    
    def test01AtLeastOneSubjectRoleResource(self):
        # Test at least one member function
        request = self._createRequestCtx(
                    self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID,
                    action='write')
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")    
                    
    def test02SubjectDoesNotHaveAnyOfSpecifiedRolesForResource(self):
        # Test at least one member function
        request = self._createRequestCtx(
        self.__class__.SUBJECT_DOES_NOT_HAVE_ANY_OF_SPECIFIED_ROLES_ID,
        action='write')
        
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")    
           
            
if __name__ == "__main__":
    unittest.main()