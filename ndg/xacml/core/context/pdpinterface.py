"""NDG Security Policy Decision Point interface definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "25/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from abc import ABCMeta, abstractmethod
from ndg.xacml.core.context.request import Request


class PDPInterface(object):
    """Interface class for XACML Policy Enforcement Point"""
    __metaclass__ = ABCMeta
    __slots__ = ()
    
    @abstractmethod
    def evaluate(self, request):
        '''evaluate the input request and return an access control decision
        in the returned response
        
        @param request: XACML context request
        @type request: ndg.xacml.core.context.request.Request
        @return: XACML context response
        @rtype: None (this abstract method) expecting 
        ndg.xacml.core.context.response.Response type in implementations of this
        class
        '''
        if not isinstance(request, Request):
            raise TypeError('Expecting %r type for input request; got %r '
                            'instead' % (Request, type(request)))
