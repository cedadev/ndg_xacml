#!/usr/bin/env python
"""NDG XACML Context unit test package 

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
from os import path

from ndg.xacml.core import Identifiers
from ndg.xacml.core.attribute import Attribute
from ndg.xacml.core.attributevalue import (AttributeValue, 
                                           AttributeValueClassFactory)

from ndg.xacml.core.context.environment import Environment
from ndg.xacml.core.context.request import Request
from ndg.xacml.core.context.subject import Subject
from ndg.xacml.core.context.resource import Resource
from ndg.xacml.core.context.action import Action
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.handler import CtxHandlerBase
from ndg.xacml.parsers.etree.factory import ReaderFactory

from ndg.xacml.test import XACML_NDGTEST1_FILEPATH
 
ROLE_ATTRIBUTE_ID = "urn:ndg:security:authz:1.0:attr"
SUBJECT_ID = 'https://my.name.somewhere.ac.uk'

attributeValueFactory = AttributeValueClassFactory()
AnyUriAttributeValue = attributeValueFactory(AttributeValue.ANY_TYPE_URI)
StringAttributeValue = attributeValueFactory(AttributeValue.STRING_TYPE_URI)


class TestContextHandler(CtxHandlerBase):
    """Test implementation of Context Handler which includes an implemented PIP
    interface"""
    
    def __init__(self):
        """Add an attribute to hold a reference to a policy information point"""
        
        super(TestContextHandler, self).__init__()
        
    def handlePEPRequest(self, myRequest):
        """Handle request from Policy Enforcement Point
        
        @param pepRequest: request from PEP, derived class determines its type
        e.g. SAML AuthzDecisionQuery
        @type myRequest: type
        @return: PEP response - derived class determines type
        @rtype: None
        """
        
        # Convert myRequest to XACML context request - var assignment here is 
        # representative of this process rather than actually doing anything.
        xacmlRequest = myRequest
        
        if self.pdp is None:
            raise TypeError('No "pdp" attribute set')
        
        # Add a reference to this context so that the PDP can invoke queries
        # back to the PIP
        xacmlRequest.ctxHandler = self 
               
        xacmlResponse = self.pdp.evaluate(xacmlRequest)
        
        # Convert XACML context response to domain specific request
        myResponse = xacmlResponse
        
        return myResponse
    
    def pipQuery(self, request, designator):
        '''PIP adds admin attribute value for given attribute ID and for any 
        subject'''
        if designator.attributeId == ROLE_ATTRIBUTE_ID:
            attrVal = StringAttributeValue(value='admin')
            return [attrVal]
        else:
            return None 
        
        
class XacmlContextBaseTestCase(unittest.TestCase):
    """Base class containing common methods for test initialisation"""
    
    @staticmethod
    def _createRequestCtx(resourceId, 
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
            subject = Subject()
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
        
        resource = Resource()
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
        
    @staticmethod
    def _createPDPfromNdgTest1Policy():
        """Create PDP from NDG test policy file"""
        pdp = PDP.fromPolicySource(XACML_NDGTEST1_FILEPATH, ReaderFactory)
        return pdp
