#!/usr/bin/env python
"""NDG XACML functions unit tests 

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

from ndg.xacml.core.functions import FunctionMap, AbstractFunction
from ndg.xacml.core.functions.v2.regexp_match import RegexpMatchBase
from ndg.xacml.core.context.exceptions import XacmlContextTypeError


def custom_function_factory(function_ns):
    class CustomFunctionAbstractFunction(AbstractFunction):
        FUNCTION_NS = 'urn:ndg:xacml:test:integer-square'
        def evaluate(self, num):
            """square an integer
            
            @param num: number to square
            @type num: int
            @rtype: int
            @raise TypeError: incorrect type for input
            """
            if not isinstance(num, int):
                raise XacmlContextTypeError('%r function expecting "int" type; '
                                            'got %r' % 
                                            (self.__class__.FUNCTION_NS, 
                                             type(num)))
            
            return num * num
       
    if function_ns == CustomFunctionAbstractFunction.FUNCTION_NS:
        return CustomFunctionAbstractFunction 
    else:
        return None 
            
            
class FunctionTestCase(unittest.TestCase):
    """Test XACML functions implementation
    
    The log output gives an indication of the XACML functions which are not 
    implemented yet"""
    
    def test01LoadMap(self):   
        funcMap = FunctionMap()
        funcMap.loadAllCore()
        anyUriMatchNs = \
            'urn:oasis:names:tc:xacml:2.0:function:anyURI-regexp-match'
            
        self.assert_(issubclass(funcMap.get(anyUriMatchNs), RegexpMatchBase))

    def test01_add_custom_function(self):
        func_map = FunctionMap()
        func_map.loadAllCore()
        func_map.load_custom_function('urn:ndg:xacml:test:integer-square',
                                  custom_function_factory)
        
        self.assertIn('urn:ndg:xacml:test:integer-square', func_map, 
                      'custom function not added into map')
        
if __name__ == "__main__":
    unittest.main()