#!/usr/bin/env python
"""NDG XACML Policy unit tests 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import unittest
from os import path
import logging
logging.basicConfig(level=logging.DEBUG)

from ndg.xacml.core.policy import Policy
from ndg.xacml.core.functions import functionMap
from ndg.xacml.core.attributedesignator import SubjectAttributeDesignator
from ndg.xacml.core.attributeselector import AttributeSelector
from ndg.xacml.core.attributevalue import AttributeValueClassFactory
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.parsers.etree.attributevaluereader import \
                                                DataTypeReaderClassFactory

from ndg.xacml.test import (XACML_NDGTEST1_FILEPATH, THIS_DIR, 
                            GroupRoleAttributeValue, 
                            ETreeGroupRoleDataTypeReader,
                            GroupRoleBag,
                            GroupRoleAtLeastOneMemberOf)
                               
    
class XACMLPolicyTestCase(unittest.TestCase):
    """Unit tests for NDG XACML Policy class"""
    XACML_TEST1_FILENAME = "rule1.xml"
    XACML_TEST1_FILEPATH = path.join(THIS_DIR, XACML_TEST1_FILENAME)
    XACML_TEST2_FILENAME = "rule2.xml"
    XACML_TEST2_FILEPATH = path.join(THIS_DIR, XACML_TEST2_FILENAME)
    XACML_TEST3_FILENAME = "rule3.xml"
    XACML_TEST3_FILEPATH = path.join(THIS_DIR, XACML_TEST3_FILENAME)
    XACML_TEST4_FILENAME = "rule4.xml"
    XACML_TEST4_FILEPATH = path.join(THIS_DIR, XACML_TEST4_FILENAME)
    XACML_ESGFTEST1_FILENAME = "esgf1.xml"
    XACML_ESGFTEST1_FILEPATH = path.join(THIS_DIR, XACML_ESGFTEST1_FILENAME)
    
    def test01ETreeParseRule1Policy(self):
        PolicyReader = ReaderFactory.getReader(Policy)
        policy = PolicyReader.parse(XACMLPolicyTestCase.XACML_TEST1_FILEPATH)
        self.assert_(policy)
        
        self.assert_(
            policy.policyId == "urn:oasis:names:tc:example:SimplePolicy1")
        
        self.assert_(policy.ruleCombiningAlgId == \
        "urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:deny-overrides")
        
        self.assert_(
            "Med Example Corp access control policy" in policy.description)
        
        self.assert_(len(policy.target.subjects) == 0)
        
        self.assert_(policy.rules[0].id == \
                     "urn:oasis:names:tc:xacml:2.0:example:SimpleRule1")
        
        self.assert_(policy.rules[0].effect == 'Permit')
        
        self.assert_(
            'Any subject with an e-mail name in the med.example.com domain' in \
            policy.rules[0].description)
        
        self.assert_(len(policy.rules[0].target.subjects) == 1)
        self.assert_(len(policy.rules[0].target.actions) == 0)
        self.assert_(len(policy.rules[0].target.resources) == 0)
        self.assert_(len(policy.rules[0].target.environments) == 0)
        
        self.assert_(len(policy.rules[0].target.subjects[0
                                                         ].subjectMatches) == 1)
        
        self.assert_(policy.rules[0].target.subjects[0].subjectMatches[0
            ].matchId == \
            "urn:oasis:names:tc:xacml:1.0:function:rfc822Name-match")
        
        self.assert_(policy.rules[0].target.subjects[0].subjectMatches[0
            ].attributeValue.dataType == \
            "urn:oasis:names:tc:xacml:1.0:data-type:rfc822Name")
        
        self.assert_(policy.rules[0].target.subjects[0].subjectMatches[0
            ].attributeDesignator.dataType == \
            "urn:oasis:names:tc:xacml:1.0:data-type:rfc822Name")
        
        # Attribute ID
        self.assert_(policy.rules[0].target.subjects[0].subjectMatches[0
            ].attributeDesignator.attributeId == \
            "urn:oasis:names:tc:xacml:1.0:subject:subject-id")
         
    def test02ETreeParseRule2Policy(self):
        PolicyReader = ReaderFactory.getReader(Policy)
        policy = PolicyReader.parse(XACMLPolicyTestCase.XACML_TEST2_FILEPATH)
        self.assert_(policy)
        
        self.assert_(
        policy.policyId == "urn:oasis:names:tc:xacml:2.0:example:policyid:2")
        
        self.assert_(policy.ruleCombiningAlgId == \
        "urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:deny-overrides")
        
        self.assert_(policy.description is None)
        
        self.assert_(len(policy.target.actions) == 0)
        
        self.assert_(policy.rules[0].id == \
                     "urn:oasis:names:tc:xacml:2.0:example:ruleid:2")
        
        self.assert_(policy.rules[0].effect == 'Permit')
        
        self.assert_(policy.rules[0].description == """\
A person may read any medical record in the
            http://www.med.example.com/records.xsd namespace
            for which he or she is the designated parent or guardian, 
            and for which the patient is under 16 years of age""")
        
        self.assert_(len(policy.rules[0].target.subjects) == 0)
        self.assert_(len(policy.rules[0].target.actions) == 1)
        self.assert_(len(policy.rules[0].target.resources) == 1)
        self.assert_(len(policy.rules[0].target.environments) == 0)
        
        self.assert_(len(policy.rules[0].target.resources[0
                                                    ].resourceMatches) == 2)
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[0
            ].matchId == "urn:oasis:names:tc:xacml:1.0:function:string-equal")
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[0
            ].attributeValue.dataType == \
                                    "http://www.w3.org/2001/XMLSchema#string")
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[0
            ].attributeValue.value == 'urn:med:example:schemas:record')
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[0
            ].attributeDesignator.dataType == \
                                    "http://www.w3.org/2001/XMLSchema#string")
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[1
            ].attributeDesignator.attributeId == \
                            "urn:oasis:names:tc:xacml:1.0:resource:xpath")
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[1
            ].matchId == \
                "urn:oasis:names:tc:xacml:1.0:function:xpath-node-match")
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[1
            ].attributeValue.dataType == \
                                    "http://www.w3.org/2001/XMLSchema#string")
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[1
            ].attributeValue.value == '/md:record')
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[1
            ].attributeDesignator.dataType == \
                                    "http://www.w3.org/2001/XMLSchema#string")
        
        self.assert_(policy.rules[0].target.resources[0].resourceMatches[1
            ].attributeDesignator.attributeId == \
                                "urn:oasis:names:tc:xacml:1.0:resource:xpath")
        
        # Verify Action
        self.assert_(len(policy.rules[0].target.actions[0
                                                    ].actionMatches) == 1)
        
        self.assert_(policy.rules[0].target.actions[0].actionMatches[0
            ].matchId == "urn:oasis:names:tc:xacml:1.0:function:string-equal")
        
        self.assert_(policy.rules[0].target.actions[0].actionMatches[0
            ].attributeValue.dataType == \
                                    "http://www.w3.org/2001/XMLSchema#string")
        
        self.assert_(policy.rules[0].target.actions[0].actionMatches[0
            ].attributeValue.value == "read")
        
        self.assert_(policy.rules[0].target.actions[0].actionMatches[0
            ].attributeDesignator.dataType == \
                                    "http://www.w3.org/2001/XMLSchema#string")
        
        self.assert_(policy.rules[0].target.actions[0].actionMatches[0
            ].attributeDesignator.attributeId == \
                            "urn:oasis:names:tc:xacml:1.0:action:action-id")

        self.assert_(policy.rules[0].condition)        
        self.assert_(policy.rules[0].condition.expression.functionId == \
                     "urn:oasis:names:tc:xacml:1.0:function:and")
        
        self.assert_(len(policy.rules[0].condition.expression.expressions) == 1)
        
        self.assert_(policy.rules[0].condition.expression.expressions[0
            ].functionId == \
                'urn:oasis:names:tc:xacml:1.0:function:string-equal')
        
        self.assert_(len(policy.rules[0].condition.expression.expressions) == 1)
        
        self.assert_(len(policy.rules[0].condition.expression.expressions[0
                     ].expressions) == 2)
        
        self.assert_(policy.rules[0].condition.expression.expressions[0
            ].expressions[0].functionId == \
                "urn:oasis:names:tc:xacml:1.0:function:string-one-and-only")
        
        self.assert_(isinstance(
                        policy.rules[0].condition.expression.expressions[0
                            ].expressions[0
                            ].expressions[0], SubjectAttributeDesignator))
        
        self.assert_(policy.rules[0].condition.expression.expressions[0
                            ].expressions[0
                            ].expressions[0].attributeId == \
                            "urn:oasis:names:tc:xacml:2.0:example:attribute:"
                            "parent-guardian-id")

        self.assert_(policy.rules[0].condition.expression.expressions[0
                            ].expressions[0
                            ].expressions[0].dataType == \
                            "http://www.w3.org/2001/XMLSchema#string")
        
        self.assert_(policy.rules[0].condition.expression.expressions[0
                            ].expressions[0
                            ].expressions[0].attributeId == \
                            "urn:oasis:names:tc:xacml:2.0:example:attribute:"
                            "parent-guardian-id")
        
        self.assert_(isinstance(policy.rules[0
                            ].condition.expression.expressions[0
                            ].expressions[1
                            ].expressions[0], AttributeSelector))
       
        self.assert_(policy.rules[0
                            ].condition.expression.expressions[0
                            ].expressions[1
                            ].expressions[0].requestContextPath == \
                            "//md:record/md:parentGuardian/md:parentGuardianId/"
                            "text()")
        
        self.assert_(policy.rules[0
                            ].condition.expression.expressions[0
                            ].expressions[1
                            ].expressions[0].dataType == \
                            "http://www.w3.org/2001/XMLSchema#string")

    def test03ETreeParseRule3Policy(self):
        PolicyReader = ReaderFactory.getReader(Policy)
        
        try:
            policy = PolicyReader.parse(
                                    XACMLPolicyTestCase.XACML_TEST3_FILEPATH)
            self.assert_(policy)
        except NotImplementedError, e:
            print("Expecting Obligations not implemented exception: %s" %e)
                    
    def test04ETreeParseRule4Policy(self):
        PolicyReader = ReaderFactory.getReader(Policy)
        policy = PolicyReader.parse(XACMLPolicyTestCase.XACML_TEST4_FILEPATH)
        self.assert_(policy)
                    
    def test05ETreeParseNdg1Policy(self):
        # Example policy for URI Regular expression based matching of
        # resources for NDG
        PolicyReader = ReaderFactory.getReader(Policy)
        policy = PolicyReader.parse(XACML_NDGTEST1_FILEPATH)
        self.assert_(policy)    
                    
    def test05ETreeParsePolicyWithCustomAttributeTypes(self):
        # Example policy with custom attribute value type used with ESGF
        
        # Add new type
        AttributeValueClassFactory.addClass('urn:grouprole', 
                                            GroupRoleAttributeValue)
        
        # Add new parser for this type
        DataTypeReaderClassFactory.addReader('urn:grouprole', 
                                ETreeGroupRoleDataTypeReader)
        
        # Add extra matching and bag functions
        functionMap['urn:grouprole-bag'] = GroupRoleBag
        functionMap['urn:grouprole-at-least-one-member-of'
                    ] = GroupRoleAtLeastOneMemberOf
                            
        PolicyReader = ReaderFactory.getReader(Policy)
        policy = PolicyReader.parse(self.__class__.XACML_ESGFTEST1_FILEPATH)
        self.assert_(policy)  
        
        
if __name__ == "__main__":
    unittest.main()