"""NDG XACML ElementTree based reader for PolicyDefaults type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "18/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.policydefaults import PolicyDefaults
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader


class PolicyDefaultsReader(ETreeAbstractReader):
    '''ElementTree based XACML PolicyDefaults type parser
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: type
    '''
    TYPE = PolicyDefaults
    
    def __call__(self, obj, common):
        """Parse Policy defaults object
        
        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @param common: parsing common data
        @type common: from ndg.xacml.parsers.common.Common
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.policydefaults.PolicyDefaults derived type 
        @raise XMLParseError: error reading element               
        """
        elem = super(PolicyDefaultsReader, self)._parse(obj)
        
        xacmlType = self.__class__.TYPE
        policyDefaults = xacmlType()
        
        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" % 
                                xacmlType.ELEMENT_LOCAL_NAME)
        
        if len(elem) != 1:
            raise XMLParseError('Expecting a single child element for '
                                'PolicyDefaults element')
            
        if (QName.getLocalPart(elem[0].tag) != 
            xacmlType.XPATH_VERSION_ELEMENT_NAME):
            raise XMLParseError('Expecting a %r child element for '
                                'PolicyDefaults element' % 
                                xacmlType.XPATH_VERSION_ELEMENT_NAME)
        
        xpathVersion = elem[0].text 
        if xpathVersion is None:
            raise XMLParseError('No %r child element value set for '
                                'PolicyDefaults element' % 
                                xacmlType.XPATH_VERSION_ELEMENT_NAME) 
             
        policyDefaults.xpathVersion = xpathVersion
        
        return policyDefaults


