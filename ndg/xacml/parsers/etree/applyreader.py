"""NDG XACML ElementTree based Apply type reader 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "19/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.core.apply import Apply
from ndg.xacml.core.attributevalue import AttributeValue
from ndg.xacml.core.condition import Condition
from ndg.xacml.core.variablereference import VariableReference
from ndg.xacml.core.attributeselector import AttributeSelector
from ndg.xacml.core.attributedesignator import (SubjectAttributeDesignator,
                                                ResourceAttributeDesignator,
                                                ActionAttributeDesignator,
                                                EnvironmentAttributeDesignator)
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName, getElementChildren
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader
from ndg.xacml.parsers.etree.factory import ReaderFactory


class ApplyReader(ETreeAbstractReader):
    '''ElementTree based XACML Apply type parser
    
    @cvar FUNCTION_ELEMENT_LOCAL_NAME: XML local name for function element
    @type FUNCTION_ELEMENT_LOCAL_NAME: string
    
    @cvar VARIABLE_REFERENCE_ELEMENT_LOCAL_NAME: XML local name for variable
    reference element
    @type VARIABLE_REFERENCE_ELEMENT_LOCAL_NAME: string
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: abc.ABCMeta
    '''
    TYPE = Apply
    
    # These two are not currently implemented.  When an implementation is made
    # the ELEMENT_LOCAL_NAME may be referenced from the native class rather than
    # a class variable here
    FUNCTION_ELEMENT_LOCAL_NAME = 'Function'
    VARIABLE_REFERENCE_ELEMENT_LOCAL_NAME = 'VariableReference'
    
    def __call__(self, obj, common):
        """Parse Apply type object

        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: ElementTree element
        @rtype: xml.etree.Element
        """
        elem = super(ApplyReader, self)._parse(obj)
        
        xacmlType = self.__class__.TYPE
        applyObj = xacmlType()
        
        if QName.getLocalPart(elem.tag) != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" % 
                                xacmlType.ELEMENT_LOCAL_NAME)
            
        # Unpack *required* attributes from top-level element
        attributeValues = []
        for attributeName in (xacmlType.FUNCTION_ID_ATTRIB_NAME, ):
            attributeValue = elem.attrib.get(attributeName)
            if attributeValue is None:
                raise XMLParseError('No "%s" attribute found in "%s" '
                                    'element' % (attributeName,
                                                 xacmlType.ELEMENT_LOCAL_NAME))
                
            attributeValues.append(attributeValue) 
                   
        applyObj.functionId, = attributeValues
        
        # Allow for any of the defined Expression sub-types in the child 
        # elements
        for subElem in getElementChildren(elem):
            localName = QName.getLocalPart(subElem.tag)
            if localName == xacmlType.ELEMENT_LOCAL_NAME:
                applyObj.expressions.append(ApplyReader.parse(subElem, common))
             
            elif localName == AttributeValue.ELEMENT_LOCAL_NAME:
                AttributeValueReader = ReaderFactory.getReader(AttributeValue) 
                applyObj.expressions.append(AttributeValueReader.parse(subElem,
                                                                       common))
                 
            elif localName == SubjectAttributeDesignator.ELEMENT_LOCAL_NAME:
                SubjectAttributeDesignatorReader = ReaderFactory.getReader(
                                                SubjectAttributeDesignator)
                applyObj.expressions.append(
                                SubjectAttributeDesignatorReader.parse(subElem,
                                                                       common))
                
            elif localName == ResourceAttributeDesignator.ELEMENT_LOCAL_NAME:
                ResourceAttributeDesignatorReader = ReaderFactory.getReader(
                                                ResourceAttributeDesignator)
                applyObj.expressions.append(
                                ResourceAttributeDesignatorReader.parse(subElem,
                                                                        common))
                
            elif localName == EnvironmentAttributeDesignator.ELEMENT_LOCAL_NAME:
                EnvironmentAttributeDesignatorReader = ReaderFactory.getReader(
                                                EnvironmentAttributeDesignator)
                applyObj.expressions.append(
                            EnvironmentAttributeDesignatorReader.parse(subElem,
                                                                       common))
                
            elif localName == ActionAttributeDesignator.ELEMENT_LOCAL_NAME:
                ActionAttributeDesignatorReader = ReaderFactory.getReader(
                                                ActionAttributeDesignator)
                applyObj.expressions.append(
                                ActionAttributeDesignatorReader.parse(subElem,
                                                                      common))
                
            elif localName == EnvironmentAttributeDesignator.ELEMENT_LOCAL_NAME:
                EnvironmentAttributeDesignatorReader = ReaderFactory.getReader(
                                                EnvironmentAttributeDesignator)
                applyObj.expressions.append(
                            EnvironmentAttributeDesignatorReader.parse(subElem,
                                                                       common))
                
            elif localName == AttributeSelector.ELEMENT_LOCAL_NAME:
                AttributeSelectorReader = ReaderFactory.getReader(
                                                            AttributeSelector)
                applyObj.expressions.append(
                                        AttributeSelectorReader.parse(subElem,
                                                                      common))
            
            elif localName == Condition.ELEMENT_LOCAL_NAME:
                ConditionReader = ReaderFactory.getReader(Condition)
                applyObj.expressions.append(ConditionReader.parse(subElem,
                                                                  common))
                
            elif localName == self.__class__.FUNCTION_ELEMENT_LOCAL_NAME:
                raise NotImplementedError('%r Apply sub-element not '
                                          'implemented', localName)
            
            elif (localName == VariableReference.ELEMENT_LOCAL_NAME):
                raise NotImplementedError('%r Apply sub-element not '
                                          'implemented', localName)
            else:
                raise XMLParseError('%r Apply sub-element not recognised', 
                                    localName)
   
        return applyObj
