"""NDG XACML ElementTree based reader for resource match type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.match import ResourceMatch
from ndg.xacml.core.attributedesignator import ResourceAttributeDesignator
from ndg.xacml.parsers.etree.matchreader import MatchReaderBase


class ResourceMatchReader(MatchReaderBase):
    """ElementTree based parser for XACML ResourceMatch
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: abc.ABCMeta
    
    @cvar ATTRIBUTE_DESIGNATOR_TYPE: type for attribute designator sub-elements
    @type ATTRIBUTE_DESIGNATOR_TYPE: abc.ABCMeta
    """
    TYPE = ResourceMatch
    ATTRIBUTE_DESIGNATOR_TYPE = ResourceAttributeDesignator
    
