"""NDG Security Policy type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "24/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.utils import TypedList
from ndg.xacml.parsers import AbstractReaderFactory, AbstractReader
from ndg.xacml.core.policybase import PolicyBase
from ndg.xacml.core.policydefaults import PolicyDefaults
from ndg.xacml.core.target import Target
from ndg.xacml.core.rule import Rule
from ndg.xacml.core.obligation import Obligation
from ndg.xacml.core.rule_combining_alg import (RuleCombiningAlgClassFactory,
                                               RuleCombiningAlgInterface)
from ndg.xacml.core.functions import (UnsupportedStdFunctionError,
                                      UnsupportedFunctionError)


class PolicyParseError(Exception):
    """Error reading policy attributes from file"""


class InvalidPolicyXmlNsError(PolicyParseError):
    """Invalid XML namespace for policy document"""


class Policy(PolicyBase):
    """XACML Policy
    
    @cvar DEFAULT_XACML_VERSION: default is 2.0
    @type DEFAULT_XACML_VERSION: string
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    @cvar POLICY_ID_ATTRIB_NAME: policy id XML attribute name
    @type POLICY_ID_ATTRIB_NAME: string
    @cvar RULE_COMBINING_ALG_ID_ATTRIB_NAME: rule combining algorithm id XML
    attribute name
    @type RULE_COMBINING_ALG_ID_ATTRIB_NAME: string
    @cvar VERSION_ATTRIB_NAME: version XML attribute name
    @type VERSION_ATTRIB_NAME: string
    @cvar DESCRIPTION_LOCAL_NAME: description XML element local name
    @type DESCRIPTION_LOCAL_NAME: string
    @cvar POLICY_DEFAULTS_LOCAL_NAME: policy defaults XML element local name
    @type POLICY_DEFAULTS_LOCAL_NAME: string
    @cvar COMBINER_PARAMETERS_LOCAL_NAME: combiner parameter XML element local
    name
    @type COMBINER_PARAMETERS_LOCAL_NAME: string
    @cvar RULE_COMBINER_PARAMETERS_LOCAL_NAME: rule combiner parameter XML
    element local name
    @type RULE_COMBINER_PARAMETERS_LOCAL_NAME: string
    @cvar OBLIGATIONS_LOCAL_NAME: obligations XML element local name
    @type OBLIGATIONS_LOCAL_NAME: string
    
    @ivar __policyId: policy id
    @type __policyId: NoneType / basestring
    @ivar __version: policy version
    @type __version: NoneType / basestring
    @ivar __ruleCombiningAlgId: rule combining algorithm ID
    @type __ruleCombiningAlgId: NoneType / basestring
    @ivar __description: policy decription text
    @type __description: NoneType / basestring
    @ivar __target: target element
    @type __target: NoneType / ndg.xacml.core.target.Target
    @ivar __attr: list of rules
    @type __attr: ndg.xacml.utils.TypedList
    @ivar __obligations: obligations
    @type __obligations: ndg.xacml.utils.TypedList
    @ivar __ruleCombiningAlgFactory: rule combining algorithm factory
    @type __ruleCombiningAlgFactory: ndg.xacml.core.rule_combining_alg.RuleCombiningAlgClassFactory
    @ivar __ruleCombiningAlg: rule combining algorithm
    @type __ruleCombiningAlg: NoneType / ndg.xacml.core.rule_combining_alg.RuleCombiningAlgInterface
    """ 
    DEFAULT_XACML_VERSION = "2.0"
    ELEMENT_LOCAL_NAME = "Policy"
    POLICY_ID_ATTRIB_NAME = "PolicyId"
    RULE_COMBINING_ALG_ID_ATTRIB_NAME = "RuleCombiningAlgId"
    VERSION_ATTRIB_NAME = "Version"

    DESCRIPTION_LOCAL_NAME = "Description"
    POLICY_DEFAULTS_LOCAL_NAME = "PolicyDefaults"
    COMBINER_PARAMETERS_LOCAL_NAME = "CombinerParameters"
    RULE_COMBINER_PARAMETERS_LOCAL_NAME = "RuleCombinerParameters"
    OBLIGATIONS_LOCAL_NAME = "Obligations"
    POLICY_ID_REFERENCE = "PolicyIdReference"
    
    __slots__ = (
        '__policyId',
        '__version',
        '__ruleCombiningAlgId',
        '__description',
        '__policyDefaults',
        '__target',
        '__attr',
        '__obligations',
        '__ruleCombiningAlgFactory',
        '__ruleCombiningAlg'
    )
    
    def __init__(self, ruleCombiningAlgFactory=None):
        """Customise rule combining behaviour by passing in a custom combining
        algorithm factory.  This is invoked when the combining algorithm Id
        property is set in order to create the corresponding combining algorithm
        object
        
        @param ruleCombiningAlgFactory: factory object for return a rule 
        combining algorithm class for a given URI.  Defaults to 
        @type ruleCombiningAlgFactory: NoneType / defaults to 
        ndg.xacml.core.rule_combining_alg.RuleCombiningAlgClassFactory
        """
        super(Policy, self).__init__()
        self.__policyId = None
        self.__version = None
        self.__ruleCombiningAlgId = None
        self.__description = None
        self.__target = None
        self.__policyDefaults = None
        
        # Attr should eventually allow a choice of Rule, CombinerParameter, 
        # RuleCombinerParameter and VariableDefinition but only Rule type is 
        # currently supported
        self.__attr = TypedList(Rule)
        
        self.__obligations = TypedList(Obligation)
        
        self.__ruleCombiningAlgFactory = None
        if ruleCombiningAlgFactory is None:
            self.ruleCombiningAlgFactory = RuleCombiningAlgClassFactory()
        else:
            self.ruleCombiningAlgFactory = ruleCombiningAlgFactory

        self.__ruleCombiningAlg = None

    def _getRuleCombiningAlgFactory(self):
        """
        @return: rule combining algorithm factory
        @rtype: NoneType / ndg.xacml.core.rule_combining_alg.RuleCombiningAlgClassFactory
        """
        return self.__ruleCombiningAlgFactory

    def _setRuleCombiningAlgFactory(self, value):
        """
        @param value: rule combining algorithm factory
        @type value: ndg.xacml.core.rule_combining_alg.RuleCombiningAlgClassFactory
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, RuleCombiningAlgClassFactory):
            raise TypeError('Expecting %r derived type for '
                            '"ruleCombiningAlgFactory" attibute; got %r' % 
                            (RuleCombiningAlgClassFactory, type(value)))
            
        self.__ruleCombiningAlgFactory = value

    ruleCombiningAlgFactory = property(_getRuleCombiningAlgFactory, 
                                       _setRuleCombiningAlgFactory, 
                                       doc="Rule Combining Algorithm Factory")
    
    @property
    def ruleCombiningAlg(self):
        """Rule Combining algorithm
        @return: rule combining algorithm class instance
        @rtype: ndg.xacml.core.rule_combining_alg.RuleCombiningAlgInterface 
        derived type
        """
        return self.__ruleCombiningAlg
    
    @classmethod
    def fromSource(cls, source, readerFactory):
        """Create a new policy from the input source parsing it using a 
        reader from the required reader factory e.g. ETreeReaderFactory to use
        ElementTree based parsing
        
        @param source: source from which to read the policy - file path,
        file object, XML node or other dependent on the reader factory selected
        @type source: string, file, XML node type
        @param readerFactory: factory class returns reader class used to parse 
        the policy
        @type readerFactory: ndg.xacml.parsers.AbstractReaderFactory
        @return: new policy instance
        @rtype: ndg.xacml.core.policy.Policy
        """
        if not issubclass(readerFactory, AbstractReaderFactory):
            raise TypeError('Expecting %r derived class for reader factory '
                            'method; got %r' % (AbstractReaderFactory, 
                                                readerFactory))
            
        reader = readerFactory.getReader(cls)
        if not issubclass(reader, AbstractReader):
            raise TypeError('Expecting %r derived class for reader class; '
                            'got %r' % (AbstractReader, reader))
            
        return reader.parse(source)
        
    def _getPolicyId(self):
        '''
        @return: policy id
        @rtype: NoneType / basestring
        '''
        return self.__policyId

    def _setPolicyId(self, value):
        '''@param value: policy id
        @type value: basestring
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "policyId" '
                            'attribute; got %r' % type(value))
            
        self.__policyId = value

    policyId = property(_getPolicyId, _setPolicyId, None, "Policy Id")
    # Generic property for ID of Policy and PolicySet
    ident = property(_getPolicyId, None, None, "Policy Id")

    def _getVersion(self):
        '''@return: policy version
        @rtype: NoneType / basestring
        '''
        return self.__version

    def _setVersion(self, value):
        '''@param value: policy version
        @type value: basestring
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "version" '
                            'attribute; got %r' % type(value))
            
        self.__version = value

    version = property(_getVersion, _setVersion, None, "Policy Version")

    def _getRuleCombiningAlgId(self):
        '''@return: rule combining algorithm ID
        @rtype: NoneType / basestring
        '''
        return self.__ruleCombiningAlgId

    def _setRuleCombiningAlgId(self, value):
        '''@param value: rule combining algorithm ID
        @type value: NoneType / basestring
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "ruleCombiningAlgId" '
                            'attribute; got %r' % type(value))
            
        self.__ruleCombiningAlgId = value
        self._setRuleCombiningAlgFromId()
        
    def _setRuleCombiningAlgFromId(self):
        """Set the rule combining algorithm implementation from the Id set in
        __ruleCombiningAlgId the attribute
        
        @raise TypeError: incorrect input type
        @raise UnsupportedStdFunctionError: no implementation is avaliable for
        this XACML rule combining algorithm 
        @raise UnsupportedFunctionError: the rule combining algorithm is not
        recognised as a standard XACML one
        """
        # Look-up rule combining algorithm
        ruleCombiningAlgClass = self.__ruleCombiningAlgFactory(
                                                    self.__ruleCombiningAlgId)
        if (not isinstance(ruleCombiningAlgClass, type) or 
            not issubclass(ruleCombiningAlgClass, RuleCombiningAlgInterface)):
            raise TypeError('Expecting %r derived type for rule combining '
                            'algorithm class; got %r type' %
                            (RuleCombiningAlgInterface, ruleCombiningAlgClass))
            
        self.__ruleCombiningAlg = ruleCombiningAlgClass()
        if self.__ruleCombiningAlg is NotImplemented:
            raise UnsupportedStdFunctionError('The rule combining algorithm %r '
                                              'is not currently implemented' % 
                                              self.__ruleCombiningAlgId)
            
        elif self.__ruleCombiningAlg is None:
            raise UnsupportedFunctionError('%r is not recognised as a valid '
                                           'XACML rule combining algorithm' % 
                                           self.__ruleCombiningAlgId) 

    ruleCombiningAlgId = property(_getRuleCombiningAlgId, 
                                  _setRuleCombiningAlgId, None, 
                                  doc="Rule Combining Algorithm Id")

    @property
    def combinerParameters(self):
        """@raise NotImplementedError: combiner parameters property is not
        currently implemented
        """
        raise NotImplementedError()
    
    @property
    def ruleCombinerParameters(self):
        """@raise NotImplementedError: rule combiner parameters property is not
        currently implemented
        """
        raise NotImplementedError()
    
    @property
    def variableDefinitions(self):
        """@raise NotImplementedError: variable definitions parameters property 
        is not currently implemented
        """
        raise NotImplementedError()
    
    @property
    def rules(self):
        """Return the list of rules
        @return: list of rules
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__attr
    
    @property
    def obligations(self):
        """@return: obligations
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__obligations 

    def _getTarget(self):
        """@return: target element
        @rtype: NoneType / ndg.xacml.core.target.Target
        """
        return self.__target

    def _setTarget(self, value):
        """@param value: target element
        @type value: ndg.xacml.core.target.Target
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, Target):
            raise TypeError('Expecting Target for "target" '
                            'attribute; got %r' % type(value))
        self.__target = value

    target = property(_getTarget, _setTarget, doc="list of Policy targets")

    def _getDescription(self):
        '''@return: policy description text
        @rtype: NoneType / basestring
        '''
        return self.__description

    def _setDescription(self, value):
        '''@param value: policy description text
        @type value: basestring
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "description" '
                            'attribute; got %r' % type(value))
        self.__description = value

    description = property(_getDescription, _setDescription, 
                           doc="Policy Description text")

    def _getPolicyDefaults(self):
        '''@return: policy defaults
        @rtype: NoneType / ndg.xacml.core.policydefaults.PolicyDefaults
        '''
        return self.__policyDefaults

    def _setPolicyDefaults(self, value):
        '''@param value: policy defaults
        @type value: ndg.xacml.core.policydefaults.PolicyDefaults
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, PolicyDefaults):
            raise TypeError('Expecting string type for "policyDefaults" '
                            'attribute; got %r' % type(value))
            
        self.__policyDefaults = value

    policyDefaults = property(_getPolicyDefaults, 
                              _setPolicyDefaults, 
                              None, 
                              "Policy PolicyDefaults element")   

    def evaluateCombiningAlgorithm(self, context):
        """Evaluates the rule combining algorithm for this policy.
        @param context: the request context
        @type context: ndg.xacml.core.request.Request
        @return: result of the evaluation - the decision for this policy
        @rtype: ndg.xacml.core.context.result.Decision
        """
        return self.ruleCombiningAlg.evaluate(self.rules, context)
