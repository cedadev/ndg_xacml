"""NDG XACML unit test package 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from os import path

from ndg.xacml.core.attributevalue import (AttributeValueClassFactory, 
                                           AttributeValue)
from ndg.xacml.core.functions.v1.bag import BagBase
from ndg.xacml.core.functions.v1.at_least_one_member_of import \
    AtLeastOneMemberOfBase 
    
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName
from ndg.xacml.parsers.etree.attributevaluereader import (
                                                DataTypeReaderClassFactory,
                                                ETreeDataTypeReaderBase)

THIS_DIR = path.dirname(__file__)
XACML_NDGTEST1_FILENAME = "ndg1.xml"
XACML_NDGTEST1_FILEPATH = path.join(THIS_DIR, XACML_NDGTEST1_FILENAME)
XACML_ESGFTEST1_FILENAME = "esgf1.xml"
XACML_ESGFTEST1_FILEPATH = path.join(THIS_DIR, XACML_ESGFTEST1_FILENAME)
XACML_ATTRIBUTESELECTOR1_FILENAME = 'policy_attributeselector_1.xml'
XACML_ATTRIBUTESELECTOR1_FILEPATH = path.join(THIS_DIR,
                                             XACML_ATTRIBUTESELECTOR1_FILENAME)
XACML_ATTRIBUTESELECTOR2_FILENAME = 'policy_attributeselector_2.xml'
XACML_ATTRIBUTESELECTOR2_FILEPATH = path.join(THIS_DIR,
                                             XACML_ATTRIBUTESELECTOR2_FILENAME)
XACML_ATTRIBUTESELECTOR3_FILENAME = 'policy_attributeselector_3.xml'
XACML_ATTRIBUTESELECTOR3_FILEPATH = path.join(THIS_DIR,
                                             XACML_ATTRIBUTESELECTOR3_FILENAME)
XACML_ATTRIBUTESELECTOR4_FILENAME = 'policy_attributeselector_4.xml'
XACML_ATTRIBUTESELECTOR4_FILEPATH = path.join(THIS_DIR,
                                             XACML_ATTRIBUTESELECTOR4_FILENAME)
XACML_ATTRIBUTESELECTOR5_FILENAME = 'policy_attributeselector_5.xml'
XACML_ATTRIBUTESELECTOR5_FILEPATH = path.join(THIS_DIR,
                                             XACML_ATTRIBUTESELECTOR5_FILENAME)
XACML_ATTRIBUTESELECTOR6_FILENAME = 'policy_attributeselector_6.xml'
XACML_ATTRIBUTESELECTOR6_FILEPATH = path.join(THIS_DIR,
                                             XACML_ATTRIBUTESELECTOR6_FILENAME)
XACML_FIRSTAPPLICABLE_FILENAME = "firstapplicable.xml"
XACML_FIRSTAPPLICABLE_FILEPATH = path.join(THIS_DIR,
                                           XACML_FIRSTAPPLICABLE_FILENAME)
XACML_SUBJECTMATCH_FILENAME = "subjectmatch.xml"
XACML_SUBJECTMATCH_FILEPATH = path.join(THIS_DIR, XACML_SUBJECTMATCH_FILENAME)


class GroupRoleAttributeValue(AttributeValue):
    """Example Custom Attribute Value"""
    IDENTIFIER = 'urn:grouprole'
    TYPE = dict
    GROUPROLE_ELEMENT_LOCAL_NAME = 'groupRole'
    GROUP_ELEMENT_LOCAL_NAME = 'group'
    ROLE_ELEMENT_LOCAL_NAME = 'role'
    ROLE_DEFAULT_VALUE = 'default'
    
    __slots__ = ('group', 'role')
    
    def __init__(self):
        super(GroupRoleAttributeValue, self).__init__()
        self.group = None
        self.role = self.__class__.ROLE_DEFAULT_VALUE
        
    @property
    def value(self):
        """Override default value property to give custom result.  Also,
        'value' becomes a read-only property.  Making this change is critical
        to the function of the GroupRoleAtLeastOneMemberOf class below - it
        relies on being able to make comparison of the value attribute of 
        different GroupRoleAttributeValue instances.  Defined this way, 
        comparison is by group,role to group,role tuple
        """
        return self.group, self.role
    

class GroupRoleBag(BagBase):
    """Bag function for Group/Role custom attribute value type"""
    TYPE = GroupRoleAttributeValue
    FUNCTION_NS = 'urn:grouprole-bag'

  
class GroupRoleAtLeastOneMemberOf(AtLeastOneMemberOfBase):
    """At least one member of function for Group/Role custom attribute value 
    type"""
    TYPE = GroupRoleAttributeValue
    FUNCTION_NS = 'urn:grouprole-bag'

    
class ETreeGroupRoleDataTypeReader(ETreeDataTypeReaderBase):
    """Example custom parser to read custom attribute value data type"""
    
    @classmethod
    def parse(cls, elem, attributeValue):
        """Parse ESG Group/Role type object

        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: ElementTree element
        @rtype: xml.etree.Element
        """
        if len(elem) != 1:
            raise XMLParseError("Expecting single groupRole child element but " 
                                "found only %d element(s)" % len(elem))
                     
        groupRoleElem = elem[0]
        
        if (QName.getLocalPart(groupRoleElem.tag) != 
            attributeValue.__class__.GROUPROLE_ELEMENT_LOCAL_NAME):
            raise XMLParseError("%r element found, expecting \"%s\" element "  
                        "instead" % 
                        attributeValue.__class__.GROUPROLE_ELEMENT_LOCAL_NAME)
        
        # Allow for any of the defined Expression sub-types in the child 
        # elements
        for subElem in groupRoleElem:
            localName = QName.getLocalPart(subElem.tag)
            if localName == attributeValue.__class__.ROLE_ELEMENT_LOCAL_NAME:
                attributeValue.role = subElem.text
            elif localName == attributeValue.__class__.GROUP_ELEMENT_LOCAL_NAME:
                attributeValue.group = subElem.text
            else:
                raise XMLParseError('%r ESG Group/Role sub-element not '
                                    'recognised' % localName) 
