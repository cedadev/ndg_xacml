"""NDG XACML PDP tests with policy references resolved by URL

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "02/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"

import logging
import os.path
import time
import unittest

from ndg.xacml.finder.urlpolicyfinder import UrlPolicyFinder
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import THIS_DIR
from ndg.xacml.test.context import XacmlContextBaseTestCase


logging.basicConfig(level=logging.ERROR)

class Test(XacmlContextBaseTestCase):

    RESOURCE_DL1_ID = 'http://localhost/download/set1/action-and-single-subject-role-restricted-1'
    RESOURCE_DL2_ID = 'http://localhost/download/set3/action-and-single-subject-role-restricted-2'
    RESOURCE_VIEW1_ID = 'http://localhost/view/set1/action-and-single-subject-role-restricted-1'
    RESOURCE_VIEW2_ID = 'http://localhost/view/set2/action-and-single-subject-role-restricted-2'
    XACML_POLICY_SET_FILENAME = 'policy_set_url_references.xml'
    XACML_POLICY_SET_FILEPATH = os.path.join(THIS_DIR, XACML_POLICY_SET_FILENAME)

    def setUp(self):
        print "Setting up"
        self.pdp = PDP.fromPolicySource(self.__class__.XACML_POLICY_SET_FILEPATH, ReaderFactory,
                                        UrlPolicyFinder(THIS_DIR))
        print "Setup complete"


    def test01(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_DL1_ID,
                            subjectRoles=('staff',))
        print "Starting request"
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print("Response received after %fs" % (time.time() - start_time))
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test02(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_DL2_ID,
                            subjectRoles=('staff',))
        print "Starting request"
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print("Response received after %fs" % (time.time() - start_time))
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test03(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_VIEW1_ID,
                            subjectRoles=('admin',))
        print "Starting request"
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print("Response received after %fs" % (time.time() - start_time))
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test04(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_VIEW2_ID,
                            subjectRoles=('staff',))
        print "Starting request"
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print("Response received after %fs" % (time.time() - start_time))
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")


if __name__ == "__main__":
    unittest.main()
