"""NDG XACML ElementTree based Resource Element reader 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "18/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.resource import Resource
from ndg.xacml.parsers.etree.subjectreader import TargetChildReader


class ResourceReader(TargetChildReader):
    '''ElementTree based XACML Rule parser
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type
    '''
    TYPE = Resource
