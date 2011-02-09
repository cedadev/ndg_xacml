"""NDG XACML 2.0 regular expression matching function module

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "26/03/10"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
from ndg.xacml.core.functions import FunctionClassFactoryBase

# Use v1.0 schema base class for version 2.0 additional types
from ndg.xacml.core.functions.v1.regexp_match import RegexpMatchBase
    

class FunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-regexp-match XACML function classes
    
    @cvar FUNCTION_NAMES: regular expression match function URNs
    @type FUNCTION_NAMES: tuple
    
    @cvar FUNCTION_NS_SUFFIX: generic suffix for one and only function URNs
    @type FUNCTION_NS_SUFFIX: string
    
    @cvar FUNCTION_BASE_CLASS: base class for regular expression match function 
    classes 
    @type FUNCTION_BASE_CLASS: ndg.xacml.core.functions.v1.RegexMatchBase
    """
    FUNCTION_NS_SUFFIX = RegexpMatchBase.FUNCTION_NS_SUFFIX
    FUNCTION_BASE_CLASS = RegexpMatchBase
    FUNCTION_NAMES = (
        'urn:oasis:names:tc:xacml:2.0:function:anyURI-regexp-match',
        'urn:oasis:names:tc:xacml:2.0:function:ipAddress-regexp-match',
        'urn:oasis:names:tc:xacml:2.0:function:dnsName-regexp-match',
        'urn:oasis:names:tc:xacml:2.0:function:rfc822Name-regexp-match',
        'urn:oasis:names:tc:xacml:2.0:function:x500Name-regexp-match'
    )