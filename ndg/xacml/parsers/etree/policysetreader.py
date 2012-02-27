"""NDG XACML ElementTree Policy Set Reader

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "01/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.core.policy import Policy
from ndg.xacml.core.policydefaults import PolicyDefaults
from ndg.xacml.core.policyset import PolicySet
from ndg.xacml.core.variabledefinition import VariableDefinition
from ndg.xacml.core.target import Target
from ndg.xacml.parsers.etree import QName, getElementChildren
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader
from ndg.xacml.parsers.etree.factory import ReaderFactory


class PolicySetReader(ETreeAbstractReader):
    """Parse a Policy Document using ElementTree
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type"""
    TYPE = PolicySet

    def __call__(self, obj, common):
        """Parse policy set object

        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.policy.PolicySet derived type
        @raise XMLParseError: error reading element
        @raise NotImplementedError: parsing is not implemented for rule
        combiner, combiner parameters and obligations elements.
        """
        elem = super(PolicySetReader, self)._parse(obj)

        return self.processElement(elem, common)

    def processElement(self, elem, common):
        """Parse policy set object

        @param elem: root element of policy set
        @type elem: ElementTree Element
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.policy.PolicySet derived type
        @raise XMLParseError: error reading element
        @raise NotImplementedError: parsing is not implemented for rule
        combiner, combiner parameters and obligations elements.
        """
        # XACML type to instantiate
        xacmlType = self.TYPE
        policySet = xacmlType()

        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" %
                                xacmlType.ELEMENT_LOCAL_NAME)

        # Unpack *required* attributes from top-level element
        attributeValues = []
        for attributeName in (xacmlType.POLICY_SET_ID_ATTRIB_NAME,
                              xacmlType.POLICY_COMBINING_ALG_ID_ATTRIB_NAME):
            attributeValue = elem.attrib.get(attributeName)
            if attributeValue is None:
                raise XMLParseError('No "%s" attribute found in "%s" '
                                        'element' %
                                        (attributeName,
                                         xacmlType.ELEMENT_LOCAL_NAME))

            attributeValues.append(attributeValue)

        policySet.policySetId, policySet.policyCombiningAlgId = attributeValues

        # Defaults to XACML version 1.0
        # TODO: version check
        policySet.version = (elem.attrib.get(xacmlType.VERSION_ATTRIB_NAME) or
                          xacmlType.DEFAULT_XACML_VERSION)

        # Parse sub-elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)

            if localName == xacmlType.DESCRIPTION_LOCAL_NAME:
                if childElem.text is not None:
                    policySet.description = childElem.text.strip()

            elif localName == xacmlType.POLICY_SET_DEFAULTS_LOCAL_NAME:
                PolicyDefaultsReader = ReaderFactory.getReader(PolicyDefaults)
                policySet.policyDefaults = PolicyDefaultsReader.parse(childElem,
                                                                      common)

            elif localName == Target.ELEMENT_LOCAL_NAME:
                TargetReader = ReaderFactory.getReader(Target)
                policySet.target = TargetReader.parse(childElem, common)

            elif localName == xacmlType.COMBINER_PARAMETERS_LOCAL_NAME:
                raise NotImplementedError()

            elif localName == xacmlType.POLICY_COMBINER_PARAMETERS_LOCAL_NAME:
                raise NotImplementedError()

            elif (localName ==
                  xacmlType.POLICY_SET_COMBINER_PARAMETERS_LOCAL_NAME):
                raise NotImplementedError()

            elif localName == VariableDefinition.ELEMENT_LOCAL_NAME:
                VariableDefinitionReader = ReaderFactory.getReader(
                                                            VariableDefinition)
                variableDefinition = VariableDefinitionReader.parse(childElem,
                                                                    common)

            elif localName == Policy.ELEMENT_LOCAL_NAME:
                PolicyReader = ReaderFactory.getReader(Policy)
                policy = PolicyReader.parse(childElem, common)
                policySet.policies.append(policy)

            elif localName == Policy.POLICY_ID_REFERENCE:
                policyIdReference = childElem.text
                policySet.policies.append(self._getReferencedPolicy(common,
                                                            policyIdReference))

            elif localName == PolicySet.ELEMENT_LOCAL_NAME:
                PolicySetReader = ReaderFactory.getReader(PolicySet)
                policySetChild = PolicySetReader.parse(childElem, common)
                policySet.policies.append(policySetChild)

            elif localName == PolicySet.POLICY_SET_ID_REFERENCE:
                policySetIdReference = childElem.text
                policySet.policies.append(self._getReferencedPolicySet(common,
                                                        policySetIdReference))

            elif localName == xacmlType.OBLIGATIONS_LOCAL_NAME:
                raise NotImplementedError('Parsing for Obligations element is '
                                          'not implemented')

            else:
                raise XMLParseError("XACML PolicySet child element name %r not "
                                    "recognised" % localName)

        # Record reference in case of references to this policy set.
        common.policyFinder.addPolicySetReference(policySet)

        return policySet

    def _getReferencedPolicy(self, common, policyIdReference):
        """Retrieve policy referenced by ID.
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @param policyIdReference: policy ID
        @type policyIdReference: str
        @return: policy
        @rtype: ndg.xacml.core.policy.Policy derived type
        """
        return common.policyFinder.findPolicy(policyIdReference, common)

    def _getReferencedPolicySet(self, common, policySetIdReference):
        """Retrieve policy set referenced by ID.
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @param policyIdReference: policy ID
        @type policyIdReference: str
        @return: policy set
        @rtype: ndg.xacml.core.policy.PolicySet derived type
        """
        return common.policyFinder.findPolicySet(policySetIdReference, common)
