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

import os
THIS_DIR = os.path.dirname(__file__)

# Read succeeds for sdist creation but fails for build with pip install.  Added
# catch here for latter case.
try:
    LONG_DESCR = open(os.path.join(THIS_DIR, 'README.md')).read()
except IOError:
    LONG_DESCR = ('XACML 2.0 implementation for CEDA (the Centre for '
                  'Environmental Data Analysis) STFC, Rutherford Appleton '
                  'Laboratory.')

setup(
    name =           		'ndg_xacml',
    version =        		'0.5.2',
    description =           'XACML 2.0 implementation for the NERC DataGrid',
    long_description =		LONG_DESCR,
    author =         		'Philip Kershaw',
    author_email =   		'Philip.Kershaw@stfc.ac.uk',
    maintainer =         	'Philip Kershaw',
    maintainer_email =   	'Philip.Kershaw@stfc.ac.uk',
    url =            		'https://github.com/cedadev/ndg_xacml',
    license =               'BSD - See LICENCE file for details',
#    install_requires =		[],
    extras_require =        {'improved_xpath_support': 'lxml'},
    packages =       		find_packages(),
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
