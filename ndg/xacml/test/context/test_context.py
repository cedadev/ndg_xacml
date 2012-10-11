#!/usr/bin/env python
"""NDG XACML Context unit tests 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "26/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)

from ndg.xacml.core.context.pdpinterface import PDPInterface
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.handler import CtxHandlerInterface
from ndg.xacml.core.context.response import Response
from ndg.xacml.core.context.result import Result, Decision
from ndg.xacml.test.context import XacmlContextBaseTestCase, TestContextHandler  


class XacmlContextTestCase(XacmlContextBaseTestCase):
    """Test PDP, PAP, PIP and Context handler"""
    
    def test01CreateRequest(self):
        requestCtx = self._createRequestCtx("http://localhost")
        self.assert_(requestCtx)
        
    def test02CreateResponse(self):
        response = Response()
        result = Result()
        response.results.append(result)
        result.decision = Decision()
        result.decision.value = Decision.NOT_APPLICABLE
        
    def test03AbstractCtxHandler(self):
        self.assertRaises(TypeError, CtxHandlerInterface, 
                          "Context handler is an abstract base class")
        
    def test04CreateCtxHandler(self):
        ctxHandler = TestContextHandler()
        self.assert_(ctxHandler)
        
    def test05PDPInterface(self):
        self.assertRaises(TypeError, PDPInterface)
        
    def test06CreatePDP(self):
        pdp = PDP()
        self.assert_(pdp)
        
    def test07CreatePDPfromPolicy(self):
        pdp = self._createPDPfromNdgTest1Policy()
        self.assert_(pdp)
        
                                
if __name__ == "__main__":
    unittest.main()