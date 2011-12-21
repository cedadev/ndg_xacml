"""NDG Security Policy Set type definition

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "01/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
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
from ndg.xacml.core.obligation import Obligation
from ndg.xacml.core.policy_combining_alg import (PolicyCombiningAlgClassFactory,
                                                 PolicyCombiningAlgInterface)
from ndg.xacml.core.functions import (UnsupportedStdFunctionError,
                                      UnsupportedFunctionError)


class PolicySet(PolicyBase):
    """XACML Policy Set
    
    @cvar DEFAULT_XACML_VERSION: default is 2.0
    @type DEFAULT_XACML_VERSION: string
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    @cvar POLICY_SET_ID_ATTRIB_NAME: policy set id XML attribute name
    @type POLICY_SET_ID_ATTRIB_NAME: string
    @cvar POLICY_COMBINING_ALG_ID_ATTRIB_NAME: policy combining algorithm id
    XML attribute name
    @type POLICY_COMBINING_ALG_ID_ATTRIB_NAME: string
    @cvar VERSION_ATTRIB_NAME: version XML attribute name
    @type VERSION_ATTRIB_NAME: string
    @cvar DESCRIPTION_LOCAL_NAME: description XML element local name
    @type DESCRIPTION_LOCAL_NAME: string
    @cvar POLICY_SET_DEFAULTS_LOCAL_NAME: policy set defaults XML element local
    name
    @type POLICY_SET_DEFAULTS_LOCAL_NAME: string
    @cvar COMBINER_PARAMETERS_LOCAL_NAME: combiner parameter XML element local
    name
    @type COMBINER_PARAMETERS_LOCAL_NAME: string
    @cvar POLICY_COMBINER_PARAMETERS_LOCAL_NAME: policy combiner parameter XML
    element local name
    @type POLICY_COMBINER_PARAMETERS_LOCAL_NAME: string
    @cvar POLICY_SET_COMBINER_PARAMETERS_LOCAL_NAME: policy set combiner
    parameter XML element local name
    @type POLICY_SET_COMBINER_PARAMETERS_LOCAL_NAME: string
    @cvar OBLIGATIONS_LOCAL_NAME: obligations XML element local name
    @type OBLIGATIONS_LOCAL_NAME: string
    
    @ivar __policySetId: policy set id
    @type __policySetId: NoneType / basestring
    @ivar __version: policy version
    @type __version: NoneType / basestring
    @ivar __policyCombiningAlgId: policy combining algorithm ID
    @type __policyCombiningAlgId: NoneType / basestring
    @ivar __description: policy decription text
    @type __description: NoneType / basestring
    @ivar __target: target element
    @type __target: NoneType / ndg.xacml.core.target.Target
    @ivar __policies: list of policies and/or policy sets
    @type __policies: ndg.xacml.utils.TypedList
    @ivar __obligations: obligations
    @type __obligations: ndg.xacml.utils.TypedList
    @ivar __policyCombiningAlgFactory: policy combining algorithm factory
    @type __policyCombiningAlgFactory: ndg.xacml.core.policy_combining_alg.PolicyCombiningAlgClassFactory
    @ivar __policyCombiningAlg: policy combining algorithm
    @type __policyCombiningAlg: NoneType / ndg.xacml.core.policy_combining_alg.PolicyCombiningAlgInterface
    """ 

    DEFAULT_XACML_VERSION = "2.0"
    ELEMENT_LOCAL_NAME = "PolicySet"
    POLICY_SET_ID_ATTRIB_NAME = "PolicySetId"
    POLICY_COMBINING_ALG_ID_ATTRIB_NAME = "PolicyCombiningAlgId"
    VERSION_ATTRIB_NAME = "Version"

    DESCRIPTION_LOCAL_NAME = "Description"
    POLICY_SET_DEFAULTS_LOCAL_NAME = "PolicySetDefaults"
    COMBINER_PARAMETERS_LOCAL_NAME = "CombinerParameters"
    POLICY_COMBINER_PARAMETERS_LOCAL_NAME = "PolicyCombinerParameters"
    POLICY_SET_COMBINER_PARAMETERS_LOCAL_NAME = "PolicySetCombinerParameters"
    OBLIGATIONS_LOCAL_NAME = "Obligations"
    POLICY_SET_ID_REFERENCE = "PolicySetIdReference"

    __slots__ = (
        '__policySetId',
        '__version',
        '__policyCombiningAlgId',
        '__description',
        '__policySetDefaults',
        '__target',
        '__policies',
        '__obligations',
        '__policyCombiningAlgFactory',
        '__policyCombiningAlg'
    )

    def __init__(self, policyCombiningAlgFactory=None):
        '''
        Constructor
        '''
        super(PolicySet, self).__init__()
        self.__policySetId = None
        self.__version = None
        self.__policyCombiningAlgId = None
        self.__description = None
        self.__target = None
        self.__policySetDefaults = None

        # Attr should eventually allow a choice of Rule, CombinerParameter,
        # RuleCombinerParameter and VariableDefinition but only Rule type is
        # currently supported
        self.__policies = TypedList(PolicyBase)

        self.__obligations = TypedList(Obligation)

        self.__policyCombiningAlgFactory = None
        if policyCombiningAlgFactory is None:
            self.policyCombiningAlgFactory = PolicyCombiningAlgClassFactory()
        else:
            self.policyCombiningAlgFactory = policyCombiningAlgFactory

        self.__policyCombiningAlg = None

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

    def _getPolicyCombiningAlgFactory(self):
        """
        @return: policy combining algorithm factory
        @rtype: NoneType / ndg.xacml.core.policy_combining_alg.PolicyCombiningAlgClassFactory
        """
        return self.__policyCombiningAlgFactory

    def _setPolicyCombiningAlgFactory(self, value):
        """
        @param value: policy combining algorithm factory
        @type value: ndg.xacml.core.policy_combining_alg.PolicyCombiningAlgClassFactory
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, PolicyCombiningAlgClassFactory):
            raise TypeError('Expecting %r derived type for '
                            '"policyCombiningAlgFactory" attibute; got %r' %
                            (PolicyCombiningAlgClassFactory, type(value)))

        self.__policyCombiningAlgFactory = value

    policyCombiningAlgFactory = property(_getPolicyCombiningAlgFactory,
                                       _setPolicyCombiningAlgFactory,
                                       doc="Policy Combining Algorithm Factory")

    @property
    def policyCombiningAlg(self):
        """Policy Combining algorithm
        @return: policy combining algorithm class instance
        @rtype: ndg.xacml.core.policy_combining_alg.PolicyCombiningAlgInterface
        derived type
        """
        return self.__policyCombiningAlg

    def _getPolicySetId(self):
        '''
        @return: policy set id
        @rtype: NoneType / basestring
        '''
        return self.__policySetId

    def _setPolicySetId(self, value):
        '''@param value: policy set id
        @type value: basestring
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "policySetId" '
                            'attribute; got %r' % type(value))

        self.__policySetId = value

    policySetId = property(_getPolicySetId, _setPolicySetId, None, "Policy Set Id")
    # Generic property for ID of Policy and PolicySet
    ident = property(_getPolicySetId, None, None, "Policy Set Id")

    def _getVersion(self):
        '''@return: policy set version
        @rtype: NoneType / basestring
        '''
        return self.__version

    def _setVersion(self, value):
        '''@param value: policy set version
        @type value: basestring
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "version" '
                            'attribute; got %r' % type(value))

        self.__version = value

    version = property(_getVersion, _setVersion, None, "Policy Set Version")

    def _getPolicyCombiningAlgId(self):
        '''@return: policy combining algorithm ID
        @rtype: NoneType / basestring
        '''
        return self.__policyCombiningAlgId

    def _setPolicyCombiningAlgId(self, value):
        '''@param value: policy combining algorithm ID
        @type value: NoneType / basestring
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "policyCombiningAlgId" '
                            'attribute; got %r' % type(value))

        self.__policyCombiningAlgId = value
        self._setPolicyCombiningAlgFromId()

    def _setPolicyCombiningAlgFromId(self):
        """Set the policy combining algorithm implementation from the Id set in
        __policyCombiningAlgId the attribute

        @raise TypeError: incorrect input type
        @raise UnsupportedStdFunctionError: no implementation is avaliable for
        this XACML policy combining algorithm
        @raise UnsupportedFunctionError: the policy combining algorithm is not
        recognised as a standard XACML one
        """
        # Look up policy combining algorithm
        policyCombiningAlgClass = self.__policyCombiningAlgFactory(
                                                    self.__policyCombiningAlgId)
        if (not isinstance(policyCombiningAlgClass, type) or
            not issubclass(policyCombiningAlgClass,
                           PolicyCombiningAlgInterface)):
            raise TypeError('Expecting %r derived type for policy combining '
                            'algorithm class; got %r type' %
                            (PolicyCombiningAlgInterface,
                             policyCombiningAlgClass))

        self.__policyCombiningAlg = policyCombiningAlgClass()
        if self.__policyCombiningAlg is NotImplemented:
            raise UnsupportedStdFunctionError('The policy combining algorithm '
                                              '%r is not currently implemented'
                                               % self.__policyCombiningAlgId)

        elif self.__policyCombiningAlg is None:
            raise UnsupportedFunctionError('%r is not recognised as a valid '
                                           'XACML policy combining algorithm' %
                                           self.__policyCombiningAlgId)

    policyCombiningAlgId = property(_getPolicyCombiningAlgId,
                                    _setPolicyCombiningAlgId, None,
                                    doc="Policy Combining Algorithm Id")

    @property
    def combinerParameters(self):
        """@raise NotImplementedError: combiner parameters property is not
        currently implemented
        """
        raise NotImplementedError()

    @property
    def policyCombinerParameters(self):
        """@raise NotImplementedError: policy combiner parameters property is
        not currently implemented
        """
        raise NotImplementedError()

    @property
    def variableDefinitions(self):
        """@raise NotImplementedError: variable definitions parameters property
        is not currently implemented
        """
        raise NotImplementedError()

    @property
    def policies(self):
        """Return the list of policies / policy sets
        @return: list of policies / policy sets
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__policies

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

    def _getPolicySetDefaults(self):
        '''@return: policy set defaults
        @rtype: NoneType / ndg.xacml.core.policydefaults.PolicyDefaults
        '''
        return self.__policySetDefaults

    def _setPolicySetDefaults(self, value):
        '''@param value: policy set defaults
        @type value: ndg.xacml.core.policydefaults.PolicyDefaults
        @raise TypeError: incorrect input type
        '''
        if not isinstance(value, PolicyDefaults):
            raise TypeError('Expecting string type for "policyDefaults" '
                            'attribute; got %r' % type(value))

        self.__policySetDefaults = value

    policySetDefaults = property(_getPolicySetDefaults,
                                 _setPolicySetDefaults,
                                 None,
                                 "Policy Set PolicyDefaults element")

    def evaluateCombiningAlgorithm(self, context):
        """Evaluates the policy combining algorithm for this policy set.
        @param context: the request context
        @type context: ndg.xacml.core.request.Request
        @return: result of the evaluation - the decision for this policy set
        @rtype: ndg.xacml.core.context.result.Decision
        """
        return self.policyCombiningAlg.evaluate(self.policies, context)
