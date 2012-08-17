'''
Created on 18 Oct 2011

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


logging.basicConfig(level=logging.DEBUG)

class TestPdpEoPolicySet(XacmlContextBaseTestCase):
    """Tests with Earth Observation data policy set
    """
    RESOURCE_1_ID = 'http://localhost/mtci/'
    RESOURCE_2_ID = 'http://localhost/mtci/myfile'
    RESOURCE_3_ID = 'http://localhost/'
    XACML_FILENAME = 'eo_policyset.xml'
    XACML_FILEPATH = os.path.join(THIS_DIR, 'eo_policyset', XACML_FILENAME)

    def setUp(self):
        print "Setting up"
        self.pdp = PDP.fromPolicySource(self.__class__.XACML_FILEPATH, ReaderFactory)
        print "Setup complete"


    def test01_dir_access(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_1_ID,
                            subjectRoles=())
        print "Starting request"
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print("Response received after %fs" % (time.time() - start_time))
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test02_file_access_with_role_set(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_2_ID,
                            roleAttributeId='urn:ceda:security:authz:1.0:attr',
                            subjectRoles=('mtci',))
        print "Starting request"
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print("Response received after %fs" % (time.time() - start_time))
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test03_file_access_with_no_roles_set(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_2_ID,
                            subjectRoles=())
        print "Starting request"
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print("Response received after %fs" % (time.time() - start_time))
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")



if __name__ == "__main__":
    unittest.main()
