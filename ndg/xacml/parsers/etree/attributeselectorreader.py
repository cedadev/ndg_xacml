"""NDG XACML ElementTree Attribute Selector Reader  

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "18/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.utils import str2Bool
from ndg.xacml.core.attributeselector import AttributeSelector
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName
from ndg.xacml.parsers.etree.expressionreader import ExpressionReader


class AttributeSelectorReader(ExpressionReader):
    '''ElementTree based parser for XACML Attribute Selector type
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: abc.ABCMeta
    '''
    TYPE = AttributeSelector
    
    def _parseExtension(self, elem, attributeSelector):
        """Parse XML Attribute Selector element
        
        @param elem: ElementTree XML element
        @type elem: xml.etree.Element
        
        @param attributeSelector: attribute selector to be updated with parsed
        values
        @type attributeSelector: ndg.xacml.core.attributeSelector.AttributeSelector
        
        @raise XMLParseError: error parsing attribute ID XML attribute
        
        @return: updated attribute selector
        @rtype: ndg.xacml.core.attributeSelector.AttributeSelector
        """
        
        xacmlType = self.__class__.TYPE
        
        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" % 
                                xacmlType.ELEMENT_LOCAL_NAME)
            
        # Unpack *required* attributes from top-level element
        attributeValues = []
        for attributeName in (xacmlType.REQUEST_CONTEXT_PATH_ATTRIB_NAME,):
            attributeValue = elem.attrib.get(attributeName)
            if attributeValue is None:
                raise XMLParseError('No "%s" attribute found in "%s" element' %
                                    (attributeName, 
                                     xacmlType.ELEMENT_LOCAL_NAME))
                
            attributeValues.append(attributeValue)
             
        attributeSelector.requestContextPath, = attributeValues
        
        mustBePresent = elem.attrib.get(xacmlType.MUST_BE_PRESENT_ATTRIB_NAME)
        if mustBePresent is not None:
            attributeSelector.mustBePresent = str2Bool(mustBePresent)
         
        return attributeSelector

                