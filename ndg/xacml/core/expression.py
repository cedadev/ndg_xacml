"""NDG Security Expression type definition

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

from ndg.xacml.core import XacmlCoreBase


class Expression(XacmlCoreBase):
    """XACML Expression type
    
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    @cvar DATA_TYPE_ATTRIB_NAME: XML attribute name for data type
    @type DATA_TYPE_ATTRIB_NAME: string
    
    @ivar __dataType: data type for this expression
    @type __dataType: None / basestring
    """
    __metaclass__ = ABCMeta
    ELEMENT_LOCAL_NAME = None
    DATA_TYPE_ATTRIB_NAME = 'DataType'
    
    __slots__ = ('__dataType', )
    
    def __init__(self):
        super(Expression, self).__init__()
        self.__dataType = None
        
    def _get_dataType(self):
        return self.__dataType

    def _set_dataType(self, value):
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "dataType" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__dataType = value   

    dataType = property(_get_dataType, _set_dataType, None, 
                        "expression value data type")  
    
    @abstractmethod
    def evaluate(self, context):
        """Evaluate the result of the expression in a condition.  Derived 
        classes must implement
        
        @param context: the request context
        @type context: ndg.xacml.core.context.request.Request
        @return: attribute value(s) resulting from execution of this expression
        in a condition
        @rtype: AttributeValue/NoneType
        """
        raise NotImplementedError()

    def __getstate__(self):
        '''Enable pickling
        
        @return: object's attribute dictionary
        @rtype: dict
        '''
        _dict = super(Expression, self).__getstate__()
        for attrName in Expression.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_Expression" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict
