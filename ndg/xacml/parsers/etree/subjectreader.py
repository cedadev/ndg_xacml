"""NDG XACML ElementTree based Subject Element reader 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.subject import Subject
from ndg.xacml.parsers.etree.targetchildreader import TargetChildReader
    

class SubjectReader(TargetChildReader):
    '''ElementTree based XACML Rule parser
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type
    '''
    TYPE = Subject
