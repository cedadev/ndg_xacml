"""NDG XACML ElementTree based reader for ResourceAttributeDesignator type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "19/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.attributedesignator import ResourceAttributeDesignator
from ndg.xacml.parsers.etree.attributedesignatorreader import \
    AttributeDesignatorReaderBase


class ResourceAttributeDesignatorReader(AttributeDesignatorReaderBase): 
    '''ElementTree based XACML Resource Attribute Designator type parser
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: abc.ABCMeta
    '''
    TYPE = ResourceAttributeDesignator