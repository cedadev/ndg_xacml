"""NDG XACML module for context types

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "23/12/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"

import logging
log = logging.getLogger(__name__)

from ndg.xacml import importElementTree
ElementTree = importElementTree()

from ndg.xacml.core import Identifiers
from ndg.xacml.core.attribute import Attribute
from ndg.xacml.core.attributevalue import AttributeValueClassFactory
from ndg.xacml.core.context import XacmlContextBase
from ndg.xacml.core.context.action import Action
from ndg.xacml.core.context.environment import Environment
from ndg.xacml.core.context.request import Request
from ndg.xacml.core.context.resource import Resource
from ndg.xacml.core.context.response import Response
from ndg.xacml.core.context.result import Decision, Result
from ndg.xacml.core.context.subject import Subject
from ndg.xacml.parsers import XMLParseError
import ndg.xacml.parsers.etree as etree
from ndg.xacml.parsers.etree import QName, getElementChildren


class RequestElementTree(Request):
    """ElementTree based parser for XACML Request element
    """
    @classmethod
    def toXML(cls, request):
        """Create an XML representation of the input XACML Request object
        
        @type request: ndg.xacml.core.context.request.Request
        @param request: XACML request object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the request
        """
        if not isinstance(request, Request):
            raise TypeError("Expecting %r class got %r" % (Request, 
                                                           type(request)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))
        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS)

        # Subjects (should be at least one)
        for subject in request.subjects:
            subjectElem = SubjectElementTree.toXML(subject)
            elem.append(subjectElem)

        # Resource (should be at least one)
        for resource in request.resources:
            resourceElem = ResourceElementTree.toXML(resource)
            elem.append(resourceElem)

        # Action (should be one)
        actionElem = ActionElementTree.toXML(request.action)
        elem.append(actionElem)

        # Environment (should be one)
        environmentElem = EnvironmentElementTree.toXML(request.environment)
        elem.append(environmentElem)

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Request element into a
        Request object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the request
        @rtype: ndg.xacml.core.context.request.Request
        @return: Request object
        """
        request = Request()

        # Set a reference to the ElementTree element for use by
        # AttributeSelectors. The context element for an AttributeSelector is
        # always the request, so this is the only element for this is needed.
        request.elem = elem

        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        # Parse sub-elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)

            if localName == Subject.ELEMENT_LOCAL_NAME:
                subject = SubjectElementTree.fromXML(childElem)
                request.subjects.append(subject)

            elif localName == Resource.ELEMENT_LOCAL_NAME:
                resource = ResourceElementTree.fromXML(childElem)
                request.resources.append(resource)

            elif localName == Action.ELEMENT_LOCAL_NAME:
                request.action = ActionElementTree.fromXML(childElem)

            elif localName == Environment.ELEMENT_LOCAL_NAME:
                request.environment = EnvironmentElementTree.fromXML(childElem)

            else:
                raise XMLParseError("XACML context Request child element name %r"
                                    " not recognised" % localName)

        return request

class SubjectElementTree(Subject):
    """ElementTree based parser for XACML Request element
    """
    @classmethod
    def toXML(cls, subject):
        """Create an XML representation of the input XACML Subject object
        
        @type subject: ndg.xacml.core.context.subject.Subject
        @param subject: XACML subject object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the subject
        """
        if not isinstance(subject, Subject):
            raise TypeError("Expecting %r class got %r" % (Subject, 
                                                           type(subject)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))
        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS)

        for attribute in subject.attributes:
            attributeElem = AttributeElementTree.toXML(attribute)
            elem.append(attributeElem)

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Subject element into a
        Subject object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the subject
        @rtype: ndg.xacml.core.context.subject.Subject
        @return: Subject object
        """
        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        subject = Subject()

        subject.subjectCategory = elem.get(cls.SUBJECT_CATEGORY_ATTRIB_NAME,
                                    Identifiers.SubjectCategory.ACCESS_SUBJECT)

        # Parse sub-elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)
            if localName == Attribute.ELEMENT_LOCAL_NAME:
                attribute = AttributeElementTree.fromXML(childElem)
                subject.attributes.append(attribute)
        return subject

class ResourceElementTree(Resource):
    """ElementTree based parser for XACML Resource element
    """
    @classmethod
    def toXML(cls, resource):
        """Create an XML representation of the input XACML Resource object
        
        @type resource: ndg.xacml.core.context.resource.Resource
        @param resource: XACML resource object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the resource
        """
        if not isinstance(resource, Resource):
            raise TypeError("Expecting %r class got %r" % (Resource, 
                                                           type(resource)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))
        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS)

        # ResourceContent can have any attributes and contains a sequence of
        # any elements.
        # TODO Is this meant to be an element already? Assume so.
        # If not, need a representation of an element that includes its
        # attributes and child elements.
        if resource.resourceContent is not None:
            if not ElementTree.iselement(resource.resourceContent):
                raise TypeError("Expecting ElementTree element got %r" %
                                                type(resource.resourceContent))
            elem.append(resource.resourceContent)

        for attribute in resource.attributes:
            attributeElem = AttributeElementTree.toXML(attribute)
            elem.append(attributeElem)

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Resource element into a
        Resource object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the resource
        @rtype: ndg.xacml.core.context.resource.Resource
        @return: Resource object
        """
        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        resource = Resource()

        # Parse sub-elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)
            if localName == Attribute.ELEMENT_LOCAL_NAME:
                attribute = AttributeElementTree.fromXML(childElem)
                resource.attributes.append(attribute)
            elif localName == cls.RESOURCE_CONTENT_ELEMENT_LOCAL_NAME:
                ### TODO Store resource content as subtree.
                resource.resourceContent = childElem
        return resource

class ActionElementTree(Action):
    """ElementTree based parser for XACML Action element
    """
    @classmethod
    def toXML(cls, action):
        """Create an XML representation of the input XACML Action object
        
        @type action: ndg.xacml.core.context.action.Action
        @param action: XACML action object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the action
        """
        if not isinstance(action, Action):
            raise TypeError("Expecting %r class got %r" % (Action, 
                                                           type(action)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))
        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS)

        for attribute in action.attributes:
            attributeElem = AttributeElementTree.toXML(attribute)
            elem.append(attributeElem)

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Action element into a
        Action object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the action
        @rtype: ndg.xacml.core.context.action.Action
        @return: Action object
        """
        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        action = Action()

        # Parse sub-elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)
            if localName == Attribute.ELEMENT_LOCAL_NAME:
                attribute = AttributeElementTree.fromXML(childElem)
                action.attributes.append(attribute)
        return action

class EnvironmentElementTree(Environment):
    """ElementTree based parser for XACML Environment element
    """
    @classmethod
    def toXML(cls, environment):
        """Create an XML representation of the input XACML Environment object
        
        @type environment: ndg.xacml.core.context.environment.Environment
        @param environment: XACML environment object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the environment
        """
        if not isinstance(environment, Environment):
            raise TypeError("Expecting %r class got %r" % (Environment, 
                                                           type(environment)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))
        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS)

        for attribute in environment.attributes:
            attributeElem = AttributeElementTree.toXML(attribute)
            elem.append(attributeElem)

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Environment element into a
        Environment object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the environment
        @rtype: ndg.xacml.core.context.environment.Environment
        @return: Environment object
        """
        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        environment = Environment()

        # Parse sub-elements
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)
            if localName == Attribute.ELEMENT_LOCAL_NAME:
                attribute = AttributeElementTree.fromXML(childElem)
                environment.attributes.append(attribute)
        return environment

class AttributeElementTree(Attribute):
    """ElementTree based parser for XACML Attribute element
    """
    attributeValueClassFactory = AttributeValueClassFactory()
    @classmethod
    def toXML(cls, attribute):
        """Create an XML representation of the input XACML Attribute object
        
        @type attribute: ndg.xacml.core.attribute.Attribute
        @param attribute: XACML attribute object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the attribute
        """
        if not isinstance(attribute, Attribute):
            raise TypeError("Expecting %r class got %r" % (Attribute, 
                                                           type(attribute)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))
        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS)

        # Handle attributes.
        ### TODO Check for mandatory attributes.
        elem.set(Attribute.ATTRIBUTE_ID_ATTRIB_NAME, attribute.attributeId)
        elem.set(Attribute.DATA_TYPE_ATTRIB_NAME, attribute.dataType)
        if attribute.issuer is not None:
            elem.set(Attribute.ISSUER_ATTRIB_NAME, attribute.issuer)

        # Handle attribute value sub-elements.
        for attributeValue in attribute.attributeValues:
            valueTag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                                 Attribute.ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME))
            valueElem = etree.makeEtreeElement(valueTag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               Attribute.ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME)
            valueElem.text = attributeValue.value
            elem.append(valueElem)
            ### TODO AttributeValue is a sequence of xs:any with xs:anyAttribute

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Attribute element into a
        Attribute object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the attribute
        @rtype: ndg.xacml.core.attribute.Attribute
        @return: Attribute object
        """
        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        attribute = Attribute()

        # Handle attributes.
        attribute.attributeId = elem.get(Attribute.ATTRIBUTE_ID_ATTRIB_NAME)
        attribute.dataType = elem.get(Attribute.DATA_TYPE_ATTRIB_NAME)
        issuer = elem.get(Attribute.ISSUER_ATTRIB_NAME)
        if issuer is not None:
            attribute.issuer = issuer

        # Parse sub-elements
        if len(elem.getchildren()) == 0:
            raise XMLParseError("XACML context Attribute element has no "
                                "AttributeValues")
        AttributeValueClass = cls.attributeValueClassFactory(attribute.dataType)
        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)

            if localName == Attribute.ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME:
                attributeValue = AttributeValueClass(childElem.text)
                attribute.attributeValues.append(attributeValue)

            else:
                raise XMLParseError("XACML context Request child element name "
                                    "%r not recognised" % localName)
        return attribute

class ResponseElementTree(Response):
    """ElementTree based parser for XACML Response element
    """
    @classmethod
    def toXML(cls, response):
        """Create an XML representation of the input XACML Response object
        
        @type response: ndg.xacml.core.context.response.Response
        @param response: XACML response object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the response
        """
        if not isinstance(response, Response):
            raise TypeError("Expecting %r class got %r" % (Response, 
                                                           type(response)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))
        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS)

        for result in response.results:
            resultElem = ResultElementTree.toXML(result)
            elem.append(resultElem)

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Response element into a
        Response object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the response
        @rtype: ndg.xacml.core.context.response.Response
        @return: Response object
        """
        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        response = Response()

        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)

            if localName == Result.ELEMENT_LOCAL_NAME:
                result = ResultElementTree.fromXML(childElem)
                response.results.append(result)
            else:
                raise XMLParseError("XACML context Request child element name "
                                    "%r not recognised" % localName)
        return response

class ResultElementTree(Result):
    """ElementTree based parser for XACML Result element
    """
    @classmethod
    def toXML(cls, result):
        """Create an XML representation of the input XACML Result object
        
        @type result: ndg.xacml.core.context.result.Result
        @param result: XACML result object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the result
        """
        if not isinstance(result,
                          Result):
            raise TypeError("Expecting %r class got %r" %
                            (Result, 
                            type(result)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))

        attrib = {}
        # ResourceId attribute is optional.
        if result.resourceId is not None:
            attrib.append[cls.RESOURCE_ID_ATTRIB_NAME] = result.resourceId

        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS, **attrib)

        decisionElem = DecisionElementTree.toXML(result.decision)
        elem.append(decisionElem)

        ### TODO Handle status and obligations

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Result element into a
        Result object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the result
        @rtype: ndg.xacml.core.context.result.Result
        @return: Result object
        """
        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        result = Result()

        resourceId = elem.get(Result.RESOURCE_ID_ATTRIB_NAME)
        if resourceId is not None:
            result.resourceId = resourceId

        for childElem in getElementChildren(elem):
            localName = QName.getLocalPart(childElem.tag)

            if localName == Decision.ELEMENT_LOCAL_NAME:
                decision = DecisionElementTree.fromXML(childElem)
                result.decision = decision
            else:
                raise XMLParseError("XACML context Request child element name "
                                    "%r not recognised" % localName)

            ### TODO Handle status and obligations

        return result

class DecisionElementTree(Decision):
    """ElementTree based parser for XACML Decision element
    """
    @classmethod
    def toXML(cls, decision):
        """Create an XML representation of the input XACML Decision object
        
        @type decision: ndg.xacml.core.context.decision.Decision
        @param decision: XACML decision object
        @rtype: ElementTree.Element
        @return: ElementTree element containing the decision
        """
        if not isinstance(decision,
                          Decision):
            raise TypeError("Expecting %r class got %r" %
                            (Decision, 
                            type(decision)))

        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS,
                        cls.ELEMENT_LOCAL_NAME))

        elem = etree.makeEtreeElement(tag,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX,
                               XacmlContextBase.XACML_2_0_CONTEXT_NS)
        elem.text = decision.value

        return elem

    @classmethod
    def fromXML(cls, elem):
        """Parse an ElementTree XACML Decision element into a
        Decision object
        
        @type elem: ElementTree.Element
        @param elem: ElementTree element containing the decision
        @rtype: ndg.xacml.core.context.decision.Decision
        @return: Decision object
        """
        localName = QName.getLocalPart(elem.tag)
        if localName != cls.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % 
                                cls.ELEMENT_LOCAL_NAME)

        decision = Decision()

        decision.value = elem.text

        return decision
