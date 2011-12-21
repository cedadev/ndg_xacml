"""NDG Security Policy and PolicySet base class

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "01/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"

from abc import ABCMeta, abstractmethod, abstractproperty
import traceback
import logging
log = logging.getLogger(__name__)

from ndg.xacml.finder.policyfinderbase import PolicyFinderBase
from ndg.xacml.parsers import AbstractReaderFactory, AbstractReader
from ndg.xacml.parsers.common import Common
from ndg.xacml.core import XacmlCoreBase

# Evaluation of a request context
from ndg.xacml.core.context.response import Response
from ndg.xacml.core.context.result import Result, Decision
from ndg.xacml.core.context.exceptions import XacmlContextError


class PolicyBase(XacmlCoreBase):
    __metaclass__ = ABCMeta
    '''
    Base class for Policy and PolicySet, each of which can be nested within
    PolicySets and evaluated with policy combining algorithms.
    '''

    __slots__ = ()

    def __init__(self):
        super(PolicyBase, self).__init__()

    @abstractproperty
    def ident(self):
        """Subclasses return the identifier appropriate to the class.
        """
        return None

    @classmethod
    def fromSource(cls, source, readerFactory, finder):
        """Create a new policy or policy set from the input source parsing it
        using a reader from the required reader factory e.g. ETreeReaderFactory
        to use ElementTree based parsing.

        @param source: source from which to read the policy - file path,
        file object, XML node or other dependent on the reader factory selected
        @type source: string, file, XML node type
        @param readerFactory: factory class returns reader class used to parse
        the policy
        @type readerFactory: ndg.xacml.parsers.AbstractReaderFactory
        @param finder: policy finder
        @type finder: ndg.xacml.finder.PolicyFinderBase subclass
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

        if not isinstance(finder, PolicyFinderBase):
            raise TypeError('Expecting %r derived object for policy finder; '
                            'got %r' % (PolicyFinderBase, type(finder)))
        finder.setReader(reader)

        common = Common(finder)
        return reader.parse(source, common)

    @classmethod
    def fromNestedSource(cls, source, common):
        """Create a new policy or policy set from the input source parsing it
        using a reader from the required reader factory e.g. ETreeReaderFactory
        to use ElementTree based parsing.

        @param source: source from which to read the policy - file path,
        file object, XML node or other dependent on the reader factory selected
        @type source: string, file, XML node type
        @param readerFactory: factory class returns reader class used to parse
        the policy
        @type readerFactory: ndg.xacml.parsers.AbstractReaderFactory
        @return: new policy instance
        @rtype: ndg.xacml.core.policy.Policy
        """
        reader = common.policyFinder.reader
        return reader.parse(source, common)

    def evaluateResponse(self, request):
        """Make an access control decision for the given request based on this
        policy or policy set, returning a response object.

        @param request: XACML request context
        @type request: ndg.xacml.core.context.request.Request
        @return: XACML response instance
        @rtype: ndg.xacml.core.context.response.Response
        """
        response = Response()
        result = Result.createInitialised(decision=Decision.NOT_APPLICABLE)
        response.results.append(result)

        try:
            result.decision = self.evaluate(request)
        except XacmlContextError, e:
            log.error('Exception raised evaluating request context, returning '
                      '%r decision:%s',
                      e.response.results[0].decision,
                      traceback.format_exc())

            result = e.response.results[0]

        return response

    def evaluate(self, context):
        """Evaluate the decision for this policy or policy set and context.

        @param context: XACML request context
        @type context: ndg.xacml.core.context.request.Request
        @return: XACML response instance
        @rtype: ndg.xacml.core.context.result.Decision
        @raise XacmlContextError: error evaluating input request context
        """
        # Exception block around all rule processing in order to set
        # INDETERMINATE response from any exceptions raised
        try:
            log.debug('Evaluating %s %r ...', self.ELEMENT_LOCAL_NAME,
                      self.ident)

            # Instantiation implicitly sets to default value of Indeterminate.
            decision = Decision()

            # Check for a policy(set) target.
            if self.target is not None:
                targetMatch = self.target.match(context)
                if targetMatch:
                    log.debug('Match to request context for target in %s '
                              '%r', self.ELEMENT_LOCAL_NAME, self.ident)
            else:
                log.debug('No target set in %s %r', self.ELEMENT_LOCAL_NAME,
                          self.ident)
                targetMatch = True
      
            if not targetMatch:
                log.debug('No match to request context for target in %s '
                          '%r returning NotApplicable status',
                          self.ELEMENT_LOCAL_NAME, self.ident)
                decision = Decision.NOT_APPLICABLE
                return decision

            # Apply the rule combining algorithm here combining the
            # effects from the rules evaluated into an overall decision
            decision = self.evaluateCombiningAlgorithm(context)

        except Exception:
            # Catch all so that nothing is handled from within the scope of this
            # method
            log.error('No PDPError type exception raised evaluating request '
                      'context, returning %r decision:%s',
                      Decision.INDETERMINATE_STR,
                      traceback.format_exc())

            decision = Decision.INDETERMINATE

        return decision

    @abstractmethod
    def evaluateCombiningAlgorithm(self, context):
        """Evaluates the appropriate combining algorithm for this policy or
        policy set.
        @param context: the request context
        @type context: ndg.xacml.core.request.Request
        @return: result of the evaluation - the decision for this rule
        @rtype: ndg.xacml.core.context.result.Decision
        """
        return Decision.INDETERMINATE
