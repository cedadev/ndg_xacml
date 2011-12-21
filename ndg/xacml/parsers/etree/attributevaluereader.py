"""NDG XACML ElementTree based reader for AttributeValue type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.attributevalue import (AttributeValue, 
                                           AttributeValueClassFactory)
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName
from ndg.xacml.parsers.etree.expressionreader import ExpressionReader
from ndg.xacml.utils import VettedDict


class AttributeValueReader(ExpressionReader):
    '''ElementTree based XACML AttributeValue type parser
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: abc.ABCMeta
    
    @cvar FACTORY: factory function for returning an Attribute value type for a 
    given XACML Attribute value URI
    @type FACTORY: ndg.xacml.core.attributevalue.AttributeValueClassFactory
    '''
    TYPE = AttributeValue
    FACTORY = AttributeValueClassFactory()
    
    def __call__(self, obj, common):
        """Parse *AttributeValue type element - override this method instead of
        _parseExtension since AttributeValue class is virtual.  A sub-type can
        be instantiated only once the data type attribute is parsed
        
        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: new XACML attribute value instance
        @rtype: ndg.xacml.core.attributevalue.AttributeValue derived type 
        @raise XMLParseError: error reading element       
        """
        elem = super(AttributeValueReader, self)._parse(obj)
        
        xacmlType = self.__class__.TYPE
        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" % 
                                xacmlType.ELEMENT_LOCAL_NAME)
            
        # Unpack *required* attributes from top-level element
        elemAttributeValues = []
        for attributeName in (xacmlType.DATA_TYPE_ATTRIB_NAME,):
            attributeValue = elem.attrib.get(attributeName)
            if attributeValue is None:
                raise XMLParseError('No "%s" attribute found in "%s" element' %
                                    (attributeName, 
                                     xacmlType.ELEMENT_LOCAL_NAME))
                
            elemAttributeValues.append(attributeValue)
             
        attributeValueClass = self.__class__.FACTORY(elemAttributeValues[0])
        if attributeValueClass is None:
            raise XMLParseError("No Attribute Value class available for "
                                "parsing %r type" % elemAttributeValues[0])
            
        attributeValue = attributeValueClass()
        attributeValue.dataType = elemAttributeValues[0]
        self._parseExtension(elem, attributeValue)
        
        return attributeValue
    
    def _parseExtension(self, elem, attributeValue):
        """Parse XML Attribute value element
        
        @param elem: ElementTree XML element
        @type elem: xml.etree.Element
        
        @param attributeValue: attribute selector to be updated with parsed
        values
        @type attributeValue: ndg.xacml.core.attributevalue.AttributeValue
        
        @raise XMLParseError: error parsing attribute ID XML attribute
        """
        reader = DataTypeReaderClassFactory.getReader(attributeValue)
        reader.parse(elem, attributeValue)
        

class ETreeDataTypeReaderBase(object):  
    @classmethod
    def parse(cls, elem, attributeValue):
        if elem.text is None:
            raise XMLParseError('No attribute value element found parsing %r' % 
                                AttributeValueReader.TYPE.ELEMENT_LOCAL_NAME) 
            
        attributeValue.value = elem.text

        
class ETreeDataTypeReaderClassMap(VettedDict):
    """Specialised dictionary to hold mappings of XACML AttributeValue DataTypes
    and their equivalent ElementTree reader classes
    """
    
    def __init__(self):
        """Force entries to derive from AttributeValue and IDs to
        be string type
        """        
        # Filters are defined as staticmethods but reference via self here to 
        # enable derived class to override them as standard methods without
        # needing to redefine this __init__ method            
        VettedDict.__init__(self, self.keyFilter, self.valueFilter)
        
    @staticmethod
    def keyFilter(key):
        """Enforce string type keys for Attribute Value DataType URIs
        
        @param key: URN for attribute
        @type key: basestring
        @return: boolean True indicating key is OK
        @rtype: bool
        @raise TypeError: incorrect input type
        """
        if not isinstance(key, basestring):
            raise TypeError('Expecting %r derived type for key; got %r' % 
                            (basestring, type(key))) 
        return True 
    
    @staticmethod
    def valueFilter(value):
        """Enforce ElementTree abstract reader derived types for values
        @param value: attribute value
        @type value: 
        ndg.xacml.parsers.etree.attributevaluereader.ETreeDataTypeReaderBase to 
        their derived type
        @return: boolean True indicating attribute value is correct type
        @rtype: bool
        @raise TypeError: incorrect input type
        """
        if not issubclass(value, ETreeDataTypeReaderBase):
            raise TypeError('Expecting %r derived type for value; got %r' % 
                            (ETreeDataTypeReaderBase, type(value))) 
        return True 
    
              
class DataTypeReaderClassFactory(object):
    """Return class to parse the content of the Attribute value based on the 
    DataType setting"""
    MAP = ETreeDataTypeReaderClassMap()
    _id = None
    for _id in AttributeValue.TYPE_URIS:
        MAP[_id] = ETreeDataTypeReaderBase
        
    del _id
    
    @classmethod
    def addReader(cls, identifier, readerClass):
        cls.MAP[identifier] = readerClass
        
    @classmethod
    def getReader(cls, attributeValue):
        return cls.MAP[attributeValue.dataType]
    
