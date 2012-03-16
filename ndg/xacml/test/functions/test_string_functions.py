"""NDG XACML tests for string functions

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "14/03/12"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'

import logging
from os import path
import unittest

from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test.context import XacmlContextBaseTestCase

logging.basicConfig(level=logging.DEBUG)

THIS_DIR = path.dirname(__file__)
XACML_CONCATENATE_TEST_FILEPATH = path.join(THIS_DIR, "policy_concatenate.xml")

class Test(XacmlContextBaseTestCase):

    RESOURCE1_ID = 'http://localhost/resource1'
    RESOURCE2_ID = 'http://localhost/resource2'
    RESOURCE3_ID = 'http://localhost/resource3'
    RESOURCE4_ID = 'http://localhost/resource4'
    RESOURCE5_ID = 'http://localhost/resource5'
    RESOURCE6_ID = 'http://localhost/resource6'
    RESOURCE7_ID = 'http://localhost/resource7'
    RESOURCE8_ID = 'http://localhost/resource8'


    def test01_01StringConcatenate2Values(self):
        """Test concatenation of 2 string values resulting in permit decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CONCATENATE_TEST_FILEPATH,
                                        ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE1_ID,
                                         subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test01_02StringConcatenate2Values(self):
        """Test concatenation of 2 string values resulting in deny decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CONCATENATE_TEST_FILEPATH,
                                        ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE2_ID,
                                         subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test01_03StringConcatenate4Values(self):
        """Test concatenation of 4 string values resulting in permit decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CONCATENATE_TEST_FILEPATH,
                                        ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE3_ID,
                                         subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test01_04StringConcatenate4Values(self):
        """Test concatenation of 4 string values resulting in deny decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CONCATENATE_TEST_FILEPATH,
                                        ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE4_ID,
                                         subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")


    def test02_01UrlStringConcatenate2Values(self):
        """Test concatenation of URI and 1 string value resulting in permit
        decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CONCATENATE_TEST_FILEPATH,
                                        ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE5_ID,
                                         subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test02_02UrlStringConcatenate2Values(self):
        """Test concatenation of URI and 1 string value resulting in deny
        decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CONCATENATE_TEST_FILEPATH,
                                        ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE6_ID,
                                         subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test02_03UrlStringConcatenate3Values(self):
        """Test concatenation of URI and 2 string values resulting in permit
        decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CONCATENATE_TEST_FILEPATH,
                                        ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE7_ID,
                                         subjectId='testuser1',
                                         subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test02_04UrlStringConcatenate3Values(self):
        """Test concatenation of URI and 2 string values resulting in deny
        decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CONCATENATE_TEST_FILEPATH,
                                        ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE8_ID,
                                         subjectId='testuser1',
                                         subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

if __name__ == "__main__":
    unittest.main()
