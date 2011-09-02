'''
Created on 26 Aug 2011

@author: rwilkinson
'''
import logging
import unittest

from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import XACML_FIRSTAPPLICABLE_FILEPATH
from ndg.xacml.test.context import XacmlContextBaseTestCase


logging.basicConfig(level=logging.DEBUG)

class Test(XacmlContextBaseTestCase):

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

    LEVEL1_ID = \
        'http://localhost/hierarchy/dir1'
    LEVEL2_ID = \
        'http://localhost/hierarchy/dir1/dir2'
    LEVEL3_ID = \
        'http://localhost/hierarchy/dir1/dir2/dir3'

    LEVEL1_NOINHERIT_ID = \
        'http://localhost/hierarchynoinherit/dir1'
    LEVEL2_NOINHERIT_ID = \
        'http://localhost/hierarchynoinherit/dir1/dir2'
    LEVEL3_NOINHERIT_ID = \
        'http://localhost/hierarchynoinherit/dir1/dir2/dir3'

    def setUp(self):
        self.pdp = PDP.fromPolicySource(XACML_FIRSTAPPLICABLE_FILEPATH, ReaderFactory)


    # Tests in which only one rule applies - these should give the same
    # results as with the permit-overrides rule combining algorithm.
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


    # Tests for resources in a hierarchy where more than one rule may apply,
    # but one is selected by the first applicable rule combining algorithm.
    # There are no deny rules for resources within the hierarchy so
    # permissions are inherited cumulatively down the hierarchy.
    def test10HierachyLevel1Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL1_ID,
                            subjectRoles=('postdoc',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test11HierachyLevel1Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL1_ID,
                            subjectRoles=('admin',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test12HierachyLevel2Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL2_ID,
                            subjectRoles=('admin',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test13HierachyLevel2Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL2_ID,
                            subjectRoles=('staff',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test14HierachyLevel3Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL3_ID,
                            subjectRoles=('staff',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test15HierachyLevel3Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL3_ID,
                            subjectRoles=('postdoc',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test16HierachyLevel3Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL3_ID,
                            subjectRoles=('admin',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  


    # Tests for resources in hierarchy where more than one rule may apply,
    # but one is selected by the first applicable rule combining algorithm.
    # Following the permit rules at each level in the hierarchy, there is
    # a deny rule for all subjects so that permissions are not inherited
    # down the hierarchy.
    def test20HierachyLevel1Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL1_NOINHERIT_ID,
                            subjectRoles=('postdoc',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test21HierachyLevel1Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL1_NOINHERIT_ID,
                            subjectRoles=('admin',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test22HierachyLevel2Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL2_NOINHERIT_ID,
                            subjectRoles=('admin',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test23HierachyLevel2Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL2_NOINHERIT_ID,
                            subjectRoles=('staff',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test24HierachyLevel3Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL3_NOINHERIT_ID,
                            subjectRoles=('staff',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test25HierachyLevel3Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL3_NOINHERIT_ID,
                            subjectRoles=('postdoc',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test26HierachyLevel3Resource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.LEVEL3_NOINHERIT_ID,
                            subjectRoles=('admin',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  


if __name__ == "__main__":
    unittest.main()
