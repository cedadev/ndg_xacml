'''
Created on 31 Aug 2011

@author: rwilkinson
'''
import logging
import os.path
import time
import unittest

from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import THIS_DIR
from ndg.xacml.test.context import XacmlContextBaseTestCase


logging.basicConfig(level=logging.ERROR)

class Test(XacmlContextBaseTestCase):
    """Tests for FAAM policy set with nested policies for efficiency.
    """
    RESOURCE_B555_ID = 'http://localhost/download/badc/faam/data/2010/b555-sep-15/core_raw/b555_raw_data.dat'
    XACML_FAAM_FILENAME = 'policy_faam_policyset.xml'
    XACML_FILEPATH = os.path.join(THIS_DIR, 'faam_policyset', XACML_FAAM_FILENAME)

    def setUp(self):
        print "Setting up"
        self.pdp = PDP.fromPolicySource(self.__class__.XACML_FILEPATH, ReaderFactory)
        print "Setup complete"


    def test01(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_B555_ID,
                            subjectRoles=('faam_admin',))
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
                            self.__class__.RESOURCE_B555_ID,
                            subjectRoles=('group1',))
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
                            self.__class__.RESOURCE_B555_ID,
                            subjectRoles=('faam_admin',))
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
