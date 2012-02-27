"""NDG XACML ElementTree based Generic Target Child Element reader - for
Reosurce, Subject, Action and Environment

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "18/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName, getElementChildren
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader
from ndg.xacml.parsers.etree.factory import ReaderFactory


class TargetChildReader(ETreeAbstractReader):
    '''ElementTree based XACML generic target child element parser
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type
    '''

    def __call__(self, obj, common):
        """Parse target child element object
        
        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.TargetChildBase derived type 
        @raise XMLParseError: error reading element               
        """
        elem = super(TargetChildReader, self)._parse(obj)
        
        xacmlType = self.__class__.TYPE
        targetChild = xacmlType()
        
        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError("No \"%s\" element found" % 
                                xacmlType.ELEMENT_LOCAL_NAME)
            
        # Parse match elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)
            
            if localName == xacmlType.MATCH_TYPE.ELEMENT_LOCAL_NAME:
                # Get reader for the match type
                matchReader = ReaderFactory.getReader(xacmlType.MATCH_TYPE)
                targetChild.matches.append(matchReader.parse(childElem, common))
            
            else:
                raise XMLParseError("XACML %r child element name %r not "
                                    "recognised" % (xacmlType.ELEMENT_LOCAL_NAME,
                                                    localName))
                       
        return targetChild
