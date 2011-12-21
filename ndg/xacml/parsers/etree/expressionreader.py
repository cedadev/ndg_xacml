"""NDG XACML ElementTree based reader for Expression type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "18/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from abc import abstractmethod

from ndg.xacml.core.expression import Expression
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader


class ExpressionReader(ETreeAbstractReader):
    '''ElementTree based XACML Expression type parser
    
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: abc.ABCMeta
    '''
    TYPE = Expression
    
    def __call__(self, obj, common):
        """Parse Expression object
        
        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.expression.Expression derived type 
        @raise XMLParseError: error reading element               
        """
        elem = super(ExpressionReader, self)._parse(obj)
        
        xacmlType = self.__class__.TYPE
        expression = xacmlType()
        
        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" % 
                                xacmlType.ELEMENT_LOCAL_NAME)
            
        # Unpack *required* attributes from top-level element
        attributeValues = []
        for attributeName in (xacmlType.DATA_TYPE_ATTRIB_NAME,):
            attributeValue = elem.attrib.get(attributeName)
            if attributeValue is None:
                raise XMLParseError('No "%s" attribute found in "%s" element' %
                                    (attributeName, 
                                     xacmlType.ELEMENT_LOCAL_NAME))
                
            attributeValues.append(attributeValue)
             
        expression.dataType, = attributeValues
                   
        self._parseExtension(elem, expression)
        
        return expression
        
    @abstractmethod
    def _parseExtension(self, elem, expression):
        """Derived classes should implement this method to read any remaining
        attributes and elements specific to their type
        
        @param elem: ElementTree XML element
        @type elem: xml.etree.Element
        
        @param expression: attribute selector to be updated with parsed
        values
        @type expression: ndg.xacml.core.attributevalue.AttributeValue
        
        
        @raise NotImplementedError: Derived classes should implement
        """
        raise NotImplementedError()
          
# Set up new class as an abstract base itself             
ETreeAbstractReader.register(ExpressionReader)
