#!/usr/bin/env python

"""NDG XACML

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'

# Bootstrap setuptools if necessary.
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

_longDescription = """\
XACML 2.0 implementation for CEDA (the Centre for Environmental Data Archival) 
STFC, Rutherford Appleton Laboratory.  This is follow on work from the NERC 
(Natural Environment Research Council) DataGrid 3 Project.

XACML (eXtensible Access Control Mark-up Language), is an XML based language for
expressing access control policies.

See: http://www.oasis-open.org/committees/xacml/

Release 0.5.1
-------------
 * Added MANIFEST.in to fix missing policy files in test area
 * fixed epydoc mark-up

Release 0.5.0
-------------
Major enhancements including additional language features and support for lxml:

 * Optional support for lxml as alternative to ElementTree - gives better Xpath support
 * Added concatenate functions and custom functions for URL encoding and MD5 hash custom functions.
 * Added support for language features:
   - for SAML 2.0 profile of XACML v2.0 (http://docs.oasis-open.org/xacml/2.0/access_control-xacml-2.0-saml-profile-spec-os.pdf)
   - AttributeSelectors
   - PolicySets. 
   - first-applicable rule combining algorithm
   - Incorporated NOT and modified AND functions (from Prashant Kediyal). 
 * Support for adding custom functions with ndg.xacml.core.functions.FunctionMap.load_custom_function
 * Fix for ticket:1130 and related bug
  - In ndg.xacml.core.target.Target._matchChild, all SubjectMatches within a 
  Subject must evaluate to true for an overall match for the Subject (and 
  similarly for Resource, Action and Environment).
  - In ndg.xacml.core.match.MatchBase, matching of the attribute value for a 
  SubjectMatch with any of the values for the selected attribute of the Subject 
  should result in an overall match (and similarly for Resource, Action and 
  Environment).

Release 0.4.0
-------------
Added support for custom DataTypes and functions. e.g.

        # Add attribute value type
        AttributeValueClassFactory.addClass('<my new type uri', 
                                            MyAttributeValueClass)
        
        # ...and new parser for this type
        DataTypeReaderClassFactory.addReader('<my new type uri', 
                                             ETreeMyDataTypeReaderClass)
        
        # Add new function
        functionMap['<my function type uri'] = MyNewFunctionClass

Release 0.3
-----------
Includes important fixes for equals functions, and improvement to at least one
member functions.  Unit tests improved with wider coverage of different rule
definitions and example request contexts.

Improved and added to support for context handler and Policy Information Point
interfaces including the ability for the PDP to call back to a PIP via a 
Context handler to retrieve additional subject attributes.

Release 0.2
-----------
Only the parts of the specification immediately required for CEDA have been 
implemented in this initial release:
 Policy Decision Point;
 Deny overrides and Permit overrides rule combining algorithms;
 AttributeDesignators;
 various function types: see ndg.xacml.core.functions;
 and attribute types: see ndg.xacml.core.attribute;
 incomplete support for <AttributeSelector>s, <VariableReference>, 
 <VariableDefinition>. <Obligations>;
 includes an ElementTree based parser for Policies. No support for writing
 out policies or read/write of XML representation of <Request> and <Response>;
   
See ndg.xacml.test for unit tests and examples.

The software follows a modular structure to allow it to be extended easily to 
include new parsers, functions and attribute types 

"""

setup(
    name =           		'ndg_xacml',
    version =        		'0.5.1',
    description =           'XACML 2.0 implementation for the NERC DataGrid',
    long_description =		_longDescription,
    author =         		'Philip Kershaw',
    author_email =   		'Philip.Kershaw@stfc.ac.uk',
    maintainer =         	'Philip Kershaw',
    maintainer_email =   	'Philip.Kershaw@stfc.ac.uk',
    url =            		'http://proj.badc.rl.ac.uk/ndg/wiki/Security/XACML',
    license =               'BSD - See LICENCE file for details',
#    install_requires =		[],
    dependency_links =		["http://ndg.nerc.ac.uk/dist"],
    packages =       		find_packages(),
    namespace_packages =	['ndg'],
    package_data =		    {
        'ndg.xacml.core': ['documentation/Makefile'],
        'ndg.xacml.test': ['*.xml', "urn*"],
        'ndg.xacml.test.faam_policyset': ['*.xml', "urn*"],
        'ndg.xacml.test.cmip5_policyset': ['*.xml', "urn*"],
        'ndg.xacml.test.functions': ['*.xml', "urn*"],
    },
    entry_points =          None,
    test_suite =		    'ndg.xacml.test',
    zip_safe =              False,
    classifiers =           [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
