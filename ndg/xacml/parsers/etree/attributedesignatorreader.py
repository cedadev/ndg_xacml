"""NDG XACML ElementTree based reader for AttributeDesignator type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.utils import str2Bool
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName
from ndg.xacml.parsers.etree.expressionreader import ExpressionReader


class AttributeDesignatorReaderBase(ExpressionReader):
    '''ElementTree based XACML Attribute Designator base class type parser
    '''
    def _parseExtension(self, elem, attributeDesignator):
        """Parse Attribute Designator element
        
        @param elem: ElementTree XML element
        @type elem: xml.etree.Element
        
        @param attributeDesignator: attribute designator
        @type attributeDesignator: ndg.xacml.core.attributedesignator.AttributeDesignator
        
        @raise XMLParseError: error parsing attribute ID XML attribute
        
        @return: updated attribute designator
        @rtype: ndg.xacml.core.attributedesignator.AttributeDesignator
        """
        xacmlType = self.__class__.TYPE
        
        # Unpack additional *required* attributes from top-level element
        attributeValues = []
        for attributeName in (xacmlType.ATTRIBUTE_ID_ATTRIB_NAME,):
            attributeValue = elem.attrib.get(attributeName)
            if attributeValue is None:
                raise XMLParseError('No "%s" attribute found in "%s" element' %
                                    (attributeName, 
                                     xacmlType.ELEMENT_LOCAL_NAME))
                
            attributeValues.append(attributeValue)
             
        attributeDesignator.attributeId, = attributeValues
              
        # Optional attributes
        issuer = elem.attrib.get(xacmlType.ISSUER_ATTRIB_NAME)
        if issuer is not None:
            attributeDesignator.issuer = issuer
             
        mustBePresent = elem.attrib.get(xacmlType.MUST_BE_PRESENT_ATTRIB_NAME)
        if mustBePresent is not None:
            attributeDesignator.mustBePresent = str2Bool(mustBePresent)
   
        return attributeDesignator

