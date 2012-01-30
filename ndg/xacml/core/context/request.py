"""NDG XACML module for Request type 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "23/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.utils import TypedList
from ndg.xacml.core.context import XacmlContextBase
from ndg.xacml.core.context.subject import Subject
from ndg.xacml.core.context.resource import Resource
from ndg.xacml.core.context.action import Action
from ndg.xacml.core.context.environment import Environment
from ndg.xacml.core.context.handlerinterface import CtxHandlerInterface
from ndg.xacml.utils.xpath_selector import XPathSelectorInterface


class Request(XacmlContextBase):
    """XACML Request class
    
    @cvar ELEMENT_LOCAL_NAME: XML local element name, derived classes should
    set
    @type ELEMENT_LOCAL_NAME: string
    
    @ivar __subjects: list of subjects corresponding to this request
    @type __subjects: ndg.xacml.utils.TypedList
    @ivar __resources: list of resources corresponding to this request
    @type __subjects: ndg.xacml.utils.TypedList
    @ivar __action: action for this request 
    @type __action: None / ndg.xacml.core.context.action.Action
    @ivar __environment: environment associated with this request 
    @type __environment: None / ndg.xacml.core.context.environment.Environment
    
    @ivar ctxHandler: reference to context handler to enable the PDP to
    query for additional attributes.  The Context Handler itself queries a
    Policy Information Point.  This handler setting may be omitted.  If so,
    the PDP will rely entirely on the input request context for making 
    access control decisions
    @type ctxHandler: ndg.xacml.core.context.handler.CtxHandlerInterface / 
    None
    """
    __slots__ = (
        '__subjects', 
        '__resources', 
        '__action', 
        '__environment',
        '__ctxHandler',
        '__attributeSelector',
    )
    ELEMENT_LOCAL_NAME = 'Request'
    
    def __init__(self):
        super(Request, self).__init__()
        
        self.__subjects = TypedList(Subject)
        self.__resources = TypedList(Resource)
        self.__action = None
        self.__environment = None
        
        self.__ctxHandler = None
        self.__attributeSelector = None
                    
    @property
    def subjects(self):
        """Get Request subjects
        @return: list of subjects
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__subjects
        
    @property
    def resources(self):
        """Get Request resources
        @return: list of resources
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__resources
                                    
    @property
    def action(self):
        """Get Request action
        @return: action type
        @rtype: None / ndg.xacml.core.context.action.Action
        """
        return self.__action
    
    @action.setter
    def action(self, value):
        """Set Request action
        @param value: action type
        @type value: ndg.xacml.core.context.action.Action
        """
        if not isinstance(value, Action):
            raise TypeError('Expecting %r type for request "action" '
                            'attribute; got %r' % (Action, type(value)))
            
        self.__action = value
                                    
    @property
    def environment(self):
        """Get Request environment
        @return: environment settings
        @rtype: None / ndg.xacml.core.context.environment.Environment
        """
        return self.__environment
    
    @environment.setter
    def environment(self, value):
        """Set Request environment
        @param value: environment settings
        @type value: ndg.xacml.core.context.environment.Environment
        """
        if not isinstance(value, Environment):
            raise TypeError('Expecting %r type for request "environment" '
                            'attribute; got %r' % (Environment, type(value)))
             
        self.__environment = value   

    @property
    def ctxHandler(self):
        """Get Context handler used by evaluate method to query the PIP for
        additional attribute values
        @return: context handler
        @rtype: None / ndg.xacml.core.context.handler.CtxHandlerInterface 
        derived type  
        """
        return self.__ctxHandler

    @ctxHandler.setter
    def ctxHandler(self, value):
        """Set Context handler used by evaluate method to query the PIP for
        additional attribute values
        @param value: context handler
        @type value: ndg.xacml.core.context.handler.CtxHandlerInterface 
        derived type  
        """
        if not isinstance(value, CtxHandlerInterface):
            raise TypeError('Expecting %r type for "ctxHandler" attribute; got '
                            '%r' % (CtxHandlerInterface, type(value)))
            
        self.__ctxHandler = value

    @property
    def attributeSelector(self):
        """Get attribute selector used to make XPath selections on request
        @return: attribute selector
        @rtype: None / ndg.xacml.utils.xpath_selector.XpathSelectorInterface
        derived type
        """
        return self.__attributeSelector

    @attributeSelector.setter
    def attributeSelector(self, value):
        """Set attribute selector used to make XPath selections on request
        @param value: attribute selector
        @type value: ndg.xacml.utils.xpath_selector.XpathSelectorInterface
        derived type
        """
        if not isinstance(value, XPathSelectorInterface):
            raise TypeError('Expecting %r type for "attributeSelector" '
                            'attribute; got %r' %
                            (XPathSelectorInterface, type(value)))
            
        self.__attributeSelector = value

    def __getstate__(self):
        '''Enable pickling
        
        @return: object's attribute dictionary
        @rtype: dict
        '''
        _dict = super(Request, self).__getstate__()
        for attrName in Request.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_Request" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict
