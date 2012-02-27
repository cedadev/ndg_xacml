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


logging.basicConfig(level=logging.ERROR)

class Test(XacmlContextBaseTestCase):
    """Tests with CMIP5 policy set using nested policies and policy sets for
    efficiency.
    """
    RESOURCE_1_ID = 'http://localhost/thredds/dodsC/cmip5.output1.MOHC.HadGEM2-ES.rcp60.day.land.day.r1i1p1.mrsos.20111007.aggregation.dods'
    RESOURCE_2_ID = 'http://localhost/thredds/dodsC/cmip5.output1.MOHC.HadGEM2-ES.rcp60.day.land.day.r1i1p1.mrsos.20110915.aggregation.dods'
    RESOURCE_3_ID = 'http://localhost/thredds/dodsC/cmip5.output1.MOHC.HadGEM2-ES.rcp60.3hr.land.3hr.r1i1p1.mrsos.20111007.aggregation.dods'
    XACML_FILENAME = 'cmip5-policyset.xml'
    XACML_FILEPATH = os.path.join(THIS_DIR, 'cmip5_policyset', XACML_FILENAME)

    def setUp(self):
        print "Setting up"
        self.pdp = PDP.fromPolicySource(self.__class__.XACML_FILEPATH, ReaderFactory)
        print "Setup complete"


    def test01(self):
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_1_ID,
                            subjectRoles=('cmip5_research',))
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
                            self.__class__.RESOURCE_2_ID,
                            subjectRoles=('cmip5_research',))
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
                            self.__class__.RESOURCE_3_ID,
                            subjectRoles=('cmip5_research',))
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
