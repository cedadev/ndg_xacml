'''
Created on 24 Feb 2010

@author: pjkersha
'''
from ndg.xacml.utils import TypedList
"""NDG Security Target type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "25/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.core import XacmlCoreBase
from ndg.xacml.core.action import Action
from ndg.xacml.core.resource import Resource
from ndg.xacml.core.subject import Subject
from ndg.xacml.core.environment import Environment


class Target(XacmlCoreBase):
    """XACML Target element
    
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    @cvar SUBJECTS_ELEMENT_LOCAL_NAME: XML local name for the subjects element
    @type SUBJECTS_ELEMENT_LOCAL_NAME: string
    @cvar ACTIONS_ELEMENT_LOCAL_NAME: XML local name for the actions element
    @type ACTIONS_ELEMENT_LOCAL_NAME: string
    @cvar RESOURCES_ELEMENT_LOCAL_NAME: XML local name for the resources element
    @type RESOURCES_ELEMENT_LOCAL_NAME: string
    @cvar ENVIRONMENTS_ELEMENT_LOCAL_NAME: XML local name for the environments
    element
    @type ENVIRONMENTS_ELEMENT_LOCAL_NAME: string
    @cvar CHILD_ATTRS: list of the XML child element names for <Target/>
    @type CHILD_ATTRS: tuple
    
    @ivar __subjects: list of subjects for this target
    @type __subjects: ndg.xacml.utils.TypedList
    @ivar __resources: list of resources for this target
    @type __resources: ndg.xacml.utils.TypedList
    @ivar __actions: list of actions for this target
    @type __actions: ndg.xacml.utils.TypedList
    @ivar __environments: list of environment settings for this target
    @type __environments: ndg.xacml.utils.TypedList
    """
    ELEMENT_LOCAL_NAME = "Target"
    SUBJECTS_ELEMENT_LOCAL_NAME = "Subjects"
    ACTIONS_ELEMENT_LOCAL_NAME = "Actions"
    RESOURCES_ELEMENT_LOCAL_NAME = "Resources"
    ENVIRONMENTS_ELEMENT_LOCAL_NAME = "Environments"
    CHILD_ATTRS = ('subjects', 'resources', 'actions', 'environments')
   
    __slots__ = ('__subjects', '__resources', '__actions', '__environments')
    
    def __init__(self):
        """Initial attributes"""
        self.__subjects = TypedList(Subject)
        self.__resources = TypedList(Resource)
        self.__actions = TypedList(Action)
        self.__environments = TypedList(Environment)
    
    @property
    def subjects(self):
        """Get subjects
        @return: list of subjects for this target
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__subjects
    
    @property
    def resources(self):
        """Get resources
        @return: list of resources for this target
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__resources
    
    @property
    def actions(self):
        """Get actions
        @return: list of actions for this target
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__actions
    
    @property
    def environments(self):
        """Get environments
        @return: list of environments for this target
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__environments
            
    def match(self, request):
        """Generic method to match a <Target> element to the request context
        
        @param request: XACML request context
        @type request: ndg.xacml.core.context.request.Request
        @return: True if request context matches the given target, 
        False otherwise
        @rtype: bool
        """
        
        # From section 5.5 of the XACML 2.0 Core Spec:
        #
        # For the parent of the <Target> element to be applicable to the 
        # decision request, there MUST be at least one positive match between 
        # each section of the <Target> element and the corresponding section of 
        # the <xacml-context:Request> element.
        # 
        # Also, 7.6:
        #
        # The target value SHALL be "Match" if the subjects, resources, actions 
        # and environments specified in the target all match values in the 
        # request context. 
        statusValues = [False]*len(self.__class__.CHILD_ATTRS) 
        
        # Iterate for target subjects, resources, actions and environments 
        # elements
        for i, attrName in enumerate(self.__class__.CHILD_ATTRS):
            # If any one of the <Target> children is missing then it counts as
            # a match e.g. for <Subjects> child element - Section 5.5:
            #
            # <Subjects> [Optional] Matching specification for the subject 
            # attributes in the context. If this element is missing,
            # then the target SHALL match all subjects.
            targetElem = getattr(self, attrName)
            if len(targetElem) == 0:
                statusValues[i] = True
                continue
            
            # Iterate over each for example, subject in the list of subjects:
            # <Target>
            #     <Subjects>
            #          <Subject>
            #              ...
            #          </Subject>
            #          <Subject>
            #              ...
            #          </Subject>
            #     ...
            # or resource in the list of resources and so on
            for targetSubElem in targetElem:
                if self._matchChild(targetSubElem, request):
                    # Within the list of e.g. subjects if one subject 
                    # matches then this counts as a subject match overall 
                    # for this target
                    statusValues[i] = True
 
        # Target matches if all the children (i.e. subjects, resources, actions
        # and environment sections) have at least one match.  Otherwise it 
        # doesn't count as a match
        return all(statusValues)
    
    def _matchChild(self, targetChild, request):
        """Match a request child element (a <Subject>, <Resource>, <Action> or 
        <Environment>) with the corresponding target's <Subject>, <Resource>, 
        <Action> or <Environment>.
        
        @param targetChild: Target Subject, Resource, Action or Environment
        object
        @type targetChild: ndg.xacml.core.TargetChildBase
        @param request: Request context object
        @type request: ndg.xacml.core.context.request.Request
        @return: True if request context matches something in the target
        @rtype: bool
        @raise UnsupportedStdFunctionError: policy references a function type 
        which is in the XACML spec. but is not supported by this implementation
        @raise UnsupportedFunctionError: policy references a function type which
        is not supported by this implementation
        """
        if targetChild is None:
            # Default if target child is not set is to match all children
            return True
        
        matchStatusValues = [True]*len(targetChild.matches)
        
        # Section 7.6
        #
        # A subject, resource, action or environment SHALL match a value in the
        # request context if the value of all its <SubjectMatch>, 
        # <ResourceMatch>, <ActionMatch> or <EnvironmentMatch> elements, 
        # respectively, are "True".
        #
        # e.g. for <SubjectMatch>es in <Subject> ...
        for i, childMatch in enumerate(targetChild.matches):
            matchStatusValues[i] = childMatch.evaluate(request)
            
        # All match => overall match      
        return all(matchStatusValues)

