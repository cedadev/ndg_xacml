"""NDG XACML ElementTree based generic reader for subject, resource, action and
environment match types

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.attributevalue import AttributeValue
from ndg.xacml.core.attributeselector import AttributeSelector
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName, getElementChildren
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader
from ndg.xacml.parsers.etree.factory import ReaderFactory


class MatchReaderBase(ETreeAbstractReader):
    '''ElementTree based XACML generic Match parser for subject, resource, 
    action and environment match types
    
    @cvar ATTRIBUTE_DESIGNATOR_TYPE: type for attribute designator sub-elements:
    derived class should set to relevant type e.g. for SubjectMatch,
    SubjectAttributeDesignator
    @type ATTRIBUTE_DESIGNATOR_TYPE: NoneType
    '''
    ATTRIBUTE_DESIGNATOR_TYPE = None
    
    def __init__(self):
        """Virtual method
        
        @raise NotImplementedError: ATTRIBUTE_DESIGNATOR_TYPE must be set in a 
        derived class
        """
        if self.__class__.ATTRIBUTE_DESIGNATOR_TYPE is None:
            raise NotImplementedError('Extend this class setting the '
                                      '"ATTRIBUTE_DESIGNATOR_TYPE" class '
                                      'variable')
            
        super(MatchReaderBase, self).__init__()
        
    def __call__(self, obj, common):
        """Parse *Match object (where * = Subject, Resource, Environment or
        Action
        
        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: new XACML match instance
        @rtype: ndg.xacml.core.matchreader.MatchReaderBase derived type 
        @raise XMLParseError: error reading element                 
        """
        elem = super(MatchReaderBase, self)._parse(obj)
        
        xacmlType = self.__class__.TYPE
        match = xacmlType()
        
        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" % 
                                xacmlType.ELEMENT_LOCAL_NAME)
        
        # Unpack *required* attributes from top-level element
        attributeValues = []
        for attributeName in (xacmlType.MATCH_ID_ATTRIB_NAME, ):
            attributeValue = elem.attrib.get(attributeName)
            if attributeValue is None:
                raise XMLParseError('No "%s" attribute found in "%s" '
                                    'element' % (attributeName,
                                                 xacmlType.ELEMENT_LOCAL_NAME))
                
            attributeValues.append(attributeValue) 
                   
        match.matchId, = attributeValues
         
        # Assign specific attribute designator type from derived class
        attributeDesignatorType = self.__class__.ATTRIBUTE_DESIGNATOR_TYPE
        attributeDesignatorReaderType = ReaderFactory.getReader(
                                                        attributeDesignatorType)
     
        # Parse match elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)
            
            if localName == xacmlType.ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME:
                AttributeValueReader = ReaderFactory.getReader(AttributeValue)
                match.attributeValue = AttributeValueReader.parse(childElem,
                                                                  common)
                
            elif localName == attributeDesignatorType.ELEMENT_LOCAL_NAME:
                if match.attributeSelector is not None:
                    raise XMLParseError("XACML %r child element may only be "
                                        "either a %r or %r element NOT both" %
                            (xacmlType.ELEMENT_LOCAL_NAME,
                             attributeDesignatorType.ELEMENT_LOCAL_NAME,
                             AttributeSelector.ELEMENT_LOCAL_NAME))
                    
                match.attributeDesignator = attributeDesignatorReaderType.parse(
                                                            childElem, common)
                        
            elif localName == AttributeSelector.ELEMENT_LOCAL_NAME:
                if match.attributeDesignator is not None:
                    raise XMLParseError("XACML %r child element may only be "
                                        "either a %r or %r element NOT both" %
                            (xacmlType.ELEMENT_LOCAL_NAME,
                             attributeDesignatorType.ELEMENT_LOCAL_NAME,
                             AttributeSelector.ELEMENT_LOCAL_NAME))
                    
                AttributeSelectorReader = ReaderFactory.getReader(
                                                            AttributeSelector)
                
                match.attributeSelector = AttributeSelectorReader.parse(
                                                            childElem, common)
            else:
                raise XMLParseError("XACML %r child element name %r not "
                                    "recognised" % 
                                    (xacmlType.MATCH_TYPE.ELEMENT_LOCAL_NAME,
                                     localName))
                    
        return match

    
        

