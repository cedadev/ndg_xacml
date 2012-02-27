"""NDG XACML ElementTree based Target Element reader 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.target import Target
from ndg.xacml.core.subject import Subject
from ndg.xacml.core.resource import Resource
from ndg.xacml.core.action import Action
from ndg.xacml.core.environment import Environment
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName, getElementChildren
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader
from ndg.xacml.parsers.etree.factory import ReaderFactory


class TargetReader(ETreeAbstractReader):
    """ElementTree based parser for XACML Target elements
    
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type
    """
    TYPE = Target
    
    def __call__(self, obj, common):
        """Parse Target object
        
        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.target.Target derived type 
        @raise XMLParseError: error reading element               
        """
        elem = super(TargetReader, self)._parse(obj)
        
        xacmlType = TargetReader.TYPE
        target = xacmlType()
        
        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                xacmlType.ELEMENT_LOCAL_NAME)
        
        # Parse sub-elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)
            
            if localName == xacmlType.SUBJECTS_ELEMENT_LOCAL_NAME:
                for subjElem in getElementChildren(childElem):
                    SubjectReader = ReaderFactory.getReader(Subject)
                    target.subjects.append(SubjectReader.parse(subjElem,
                                                               common))
                                
            elif localName == xacmlType.RESOURCES_ELEMENT_LOCAL_NAME:
                for resourceElem in getElementChildren(childElem):
                    ResourceReader = ReaderFactory.getReader(Resource)
                    target.resources.append(ResourceReader.parse(resourceElem,
                                                                 common))
                
            elif localName == xacmlType.ACTIONS_ELEMENT_LOCAL_NAME:
                for targetElem in getElementChildren(childElem):
                    ActionReader = ReaderFactory.getReader(Action)
                    target.actions.append(ActionReader.parse(targetElem,
                                                             common))
                
            elif localName == xacmlType.ENVIRONMENTS_ELEMENT_LOCAL_NAME:
                for environElem in getElementChildren(childElem):
                    EnvironmentReader = ReaderFactory.getReader(Environment)
                    target.environments.append(EnvironmentReader.parse(
                                                        environElem, common))
            else:
                raise XMLParseError("XACML Target child element name %r not "
                                    "recognised" % localName)
                
        return target
