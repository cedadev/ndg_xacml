"""NDG Security Context handler base class

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "24/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.context.handlerinterface import CtxHandlerInterface
from ndg.xacml.core.context.pdpinterface import PDPInterface
from ndg.xacml.core.context.pipinterface import PIPInterface
    

class CtxHandlerBase(CtxHandlerInterface):
    """Base class for Context handlers - extends Context handler interface to 
    include Policy Decision Point and Policy Information Point references
    """
    
    __slots__ = (
        '__pip',
        '__pdp', 
    )
      
    def __init__(self):
        self.__pip = None
        self.__pdp = None
        
    def _getPip(self):
        return self.__pip

    def _setPip(self, value):
        if not isinstance(value, PIPInterface):
            raise TypeError('Expecting %r type for "pip" attribute; got %r '
                            'instead' % 
                            (PIPInterface, value))
            
        self.__pip = value

    pip = property(_getPip, _setPip, None, "Policy Information Point")
          
    def _getPdp(self):
        return self.__pdp

    def _setPdp(self, value):
        if not isinstance(value, PDPInterface):
            raise TypeError('Expecting %r type for "pdp" attribute; got %r '
                            'instead' % 
                            (PDPInterface, value))
            
        self.__pdp = value

    pdp = property(_getPdp, _setPdp, None, "Policy Decision Point")
