"""NDG XACML ElementTree Policy Reader  

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.core.policy import Policy
from ndg.xacml.core.policydefaults import PolicyDefaults
from ndg.xacml.core.variabledefinition import VariableDefinition
from ndg.xacml.core.rule import Rule
from ndg.xacml.core.target import Target
from ndg.xacml.parsers.etree import QName, getElementChildren
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader
from ndg.xacml.parsers.etree.factory import ReaderFactory
    
    
class PolicyReader(ETreeAbstractReader):
    """Parse a Policy Document using ElementTree
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type"""
    TYPE = Policy
    
    def __call__(self, obj, common):
        """Parse policy object
        
        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.policy.Policy derived type 
        @raise XMLParseError: error reading element  
        @raise NotImplementedError: parsing is not implemented for rule
        combiner, combiner parameters and obligations elements.         
        """
        elem = super(PolicyReader, self)._parse(obj)

        return self.processElement(elem, common)

    @classmethod
    def parse(cls, obj, common=None):
        """Parse from input object and return new XACML object
        As a special case, allow the common data to be None. This is because for
        parsing a policy rather than a policy set, no common data is needed.
        @param obj: input source - file name, stream object or other
        @type obj: string, stream or other
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: new XACML object
        @rtype: XacmlCoreBase sub type
        """
        return super(ETreeAbstractReader, cls).parse(obj, common)

    def processElement(self, elem, common):
        """Parse policy object
        
        @param elem: root element of policy
        @type elem: ElementTree Element
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.policy.Policy derived type 
        @raise XMLParseError: error reading element  
        @raise NotImplementedError: parsing is not implemented for rule
        combiner, combiner parameters and obligations elements.         
        """
        # XACML type to instantiate
        xacmlType = self.TYPE
        policy = xacmlType()

        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" % 
                                xacmlType.ELEMENT_LOCAL_NAME)

        # Unpack *required* attributes from top-level element
        attributeValues = []
        for attributeName in (xacmlType.POLICY_ID_ATTRIB_NAME,
                              xacmlType.RULE_COMBINING_ALG_ID_ATTRIB_NAME):
            attributeValue = elem.attrib.get(attributeName)
            if attributeValue is None:
                raise XMLParseError('No "%s" attribute found in "%s" '
                                        'element' %
                                        (attributeName,
                                         xacmlType.ELEMENT_LOCAL_NAME))
                
            attributeValues.append(attributeValue) 
                   
        policy.policyId, policy.ruleCombiningAlgId = attributeValues
        
        # Defaults to XACML version 1.0
        # TODO: version check
        policy.version = (elem.attrib.get(xacmlType.VERSION_ATTRIB_NAME) or 
                          xacmlType.DEFAULT_XACML_VERSION)
            
        # Parse sub-elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)
            
            if localName == xacmlType.DESCRIPTION_LOCAL_NAME:
                if childElem.text is not None:
                    policy.description = childElem.text.strip()
                    
            elif localName == xacmlType.POLICY_DEFAULTS_LOCAL_NAME:
                PolicyDefaultsReader = ReaderFactory.getReader(PolicyDefaults)
                policy.policyDefaults = PolicyDefaultsReader.parse(childElem,
                                                                   common)
                   
            elif localName == Target.ELEMENT_LOCAL_NAME:
                TargetReader = ReaderFactory.getReader(Target)
                policy.target = TargetReader.parse(childElem, common)
             
            elif localName == xacmlType.COMBINER_PARAMETERS_LOCAL_NAME:
                raise NotImplementedError()
             
            elif localName == xacmlType.RULE_COMBINER_PARAMETERS_LOCAL_NAME:
                raise NotImplementedError()
            
            elif localName == VariableDefinition.ELEMENT_LOCAL_NAME:
                VariableDefinitionReader = ReaderFactory.getReader(
                                                            VariableDefinition)
                variableDefinition = VariableDefinitionReader.parse(childElem,
                                                                    common)
                
            elif localName == Rule.ELEMENT_LOCAL_NAME:
                RuleReader = ReaderFactory.getReader(Rule)
                rule = RuleReader.parse(childElem, common)
                if rule.id in [_rule.id for _rule in policy.rules]:
                    raise XMLParseError("Duplicate Rule ID %r found" % rule.id)
                    
                policy.rules.append(rule)
                   
            elif localName == xacmlType.OBLIGATIONS_LOCAL_NAME:
                raise NotImplementedError('Parsing for Obligations element is '
                                          'not implemented')
            
            else:
                raise XMLParseError("XACML Policy child element name %r not "
                                    "recognised" % localName)

        # Record reference in case of references to this policy.
        # Allow for there not being a policy finder since this is not needed if
        # if the root is a policy rather than a policy set.
        if common is not None and hasattr(common, 'policyFinder'):
            common.policyFinder.addPolicyReference(policy)

        return policy
