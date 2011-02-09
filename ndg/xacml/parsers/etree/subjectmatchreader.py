"""NDG XACML ElementTree based reader for subject match type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.match import SubjectMatch
from ndg.xacml.core.attributedesignator import SubjectAttributeDesignator
from ndg.xacml.parsers.etree.matchreader import MatchReaderBase


class SubjectMatchReader(MatchReaderBase):
    """ElementTree based parser for XACML SubjectMatch
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: abc.ABCMeta
    
    @cvar ATTRIBUTE_DESIGNATOR_TYPE: type for attribute designator sub-elements
    @type ATTRIBUTE_DESIGNATOR_TYPE: abc.ABCMeta
    """
    TYPE = SubjectMatch
    ATTRIBUTE_DESIGNATOR_TYPE = SubjectAttributeDesignator