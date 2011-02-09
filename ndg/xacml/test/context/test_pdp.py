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
__revision__ = "$Id$"
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)

from ndg.xacml.core.context.result import Decision
from ndg.xacml.test.context import XacmlContextBaseTestCase, TestContextHandler

    
class XacmlEvalPdpWithPermitOverridesPolicyTestCase(XacmlContextBaseTestCase):
    """Test PDP with permit overrides rule combining algorithm"""
    
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
    
    # This could be any applicable resource value, provided there's no rule to
    # override and enable access
    PRIVATE_RESOURCE_ID = 'http://localhost/private-resource'
    
    PUBLIC_RESOURCE_ID = 'http://localhost/resource-only-restricted'
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
        
    SINGLE_SUBJECT_ROLE_RESTRICTED_ID = \
        'http://localhost/single-subject-role-restricted'
    ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID = \
        'http://localhost/action-and-single-subject-role-restricted'
    AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID = \
        'http://localhost/at-least-one-of-subject-role-restricted'
        
    def setUp(self):
        self.pdp = self._createPDPfromNdgTest1Policy()
        
    def test01NotApplicable(self):
        # Set a resource Id that doesn't match the main target
        request = self._createRequestCtx(
                                    self.__class__.NOT_APPLICABLE_RESOURCE_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.NOT_APPLICABLE, 
                        "Expecting not applicable decision")
        
    def test02PublicallyAccessibleResource(self):
        # Test a resource which has no subject restrictions
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID,
                                         includeSubject=False)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")
        
    def test03PrivateResource(self):
        request = self._createRequestCtx(
                                    self.__class__.PRIVATE_RESOURCE_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")

    def test04SingleSubjectRoleRestrictedResource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.SINGLE_SUBJECT_ROLE_RESTRICTED_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test05SingleSubjectRoleRestrictedResourceDeniesAccess(self):
        # Subject doesn't have the required role for access
        request = self._createRequestCtx(
                            self.__class__.SINGLE_SUBJECT_ROLE_RESTRICTED_ID,
                            subjectRoles=('student',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test06ActionAndSingleSubjectRoleRestrictedResource(self):
        # Test restriction based on action type as well as subject role
        request = self._createRequestCtx(
                    self.__class__.ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")

    def test07ActionAndSingleSubjectRoleRestrictedResourceDeniesAccess(self):
        # Test subject requests invalid action type
        request = self._createRequestCtx(
                    self.__class__.ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID,
                    action='write')
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test08AtLeastOneSubjectRoleResource(self):
        # Test at least one member function
        request = self._createRequestCtx(
                    self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID,
                    action='write')
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")             

    def test09AtLeastOneSubjectRoleResourceDeniesAccess(self):
        # Test at least one member function where subject doesn't have one of
        # the required roles
        request = self._createRequestCtx(
                    self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID,
                    subjectRoles=('student',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")             
    
    def test10PipAddsRequiredAttributeValToEnableAccess(self):
        # The PDP is part of a context handler with a PIP which adds subject
        # attributes under prescribed conditions on the evaluation of 
        # subject attribute designators.  In this case the addition of the PIP
        # adds an attribute value to one of the subject's attributes which means
        # they're granted access where otherwise access would be denied
        ctxHandler = TestContextHandler()
        ctxHandler.pdp = self.pdp
        
        request = self._createRequestCtx(
                    self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID,
                    subjectRoles=('student',))
        
        response = ctxHandler.handlePEPRequest(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting PERMIT decision")            
        
        
if __name__ == "__main__":
    unittest.main()