"""NDG XACML ElementTree based reader for action match type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.match import ActionMatch
from ndg.xacml.core.attributedesignator import ActionAttributeDesignator
from ndg.xacml.parsers.etree.matchreader import MatchReaderBase


class ActionMatchReader(MatchReaderBase):
    """ElementTree based parser for XACML ActionMatch
        
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: type
    
    @cvar ATTRIBUTE_DESIGNATOR_TYPE: type of attribute designator that this 
    match type holds
    @type ATTRIBUTE_DESIGNATOR_TYPE: abc.ABCMeta
    """
    TYPE = ActionMatch
    ATTRIBUTE_DESIGNATOR_TYPE = ActionAttributeDesignator
    
