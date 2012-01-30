"""NDG XACML Attribute type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "24/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.utils import TypedList
from ndg.xacml.core import XacmlCoreBase
from ndg.xacml.core.attributevalue import AttributeValue


class Attribute(XacmlCoreBase):
    """XACML Attribute type
    
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    @cvar ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME: XML local name for attribute value
    child element
    @type ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME: string
    @cvar DATA_TYPE_ATTRIB_NAME: XML attribute name for data type
    @type DATA_TYPE_ATTRIB_NAME: string
    @cvar ATTRIBUTE_ID_ATTRIB_NAME: attribute ID XML attribute name
    @type ATTRIBUTE_ID_ATTRIB_NAME: string
    @cvar ISSUER_ATTRIB_NAME: issuer XML attribute name
    @type ISSUER_ATTRIB_NAME: string
    
    @ivar __attributeValues: list of attribute values 
    @type __attributeValues: ndg.xacml.utils.TypedList
    @ivar __dataType: data type for this attribute
    @type __dataType: basestring / NoneType
    @ivar __attributeId: identifier for attribute
    @type __attributeId: basestring / NoneType
    @ivar __issuer: issuer id of this attribute
    @type __issuer: basestring / NoneType
    """
    ELEMENT_LOCAL_NAME = 'Attribute'
    ATTRIBUTE_VALUE_ELEMENT_LOCAL_NAME = 'AttributeValue'
    DATA_TYPE_ATTRIB_NAME = 'DataType'
    ATTRIBUTE_ID_ATTRIB_NAME = 'AttributeId'
    ISSUER_ATTRIB_NAME = 'Issuer'
    
    __slots__ = ('__attributeValues', '__dataType', '__attributeId', '__issuer')
    
    def __init__(self):
        super(Attribute, self).__init__()
        self.__attributeValues = TypedList(AttributeValue)
        self.__dataType = None
        self.__attributeId = None
        self.__issuer = None

    @property
    def attributeValues(self):
        """Get attribute values
        
        @return: list of attribute values
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__attributeValues
     
    @attributeValues.setter
    def attributeValues(self, value):
        """Set attribute values
        
        @param value: list of attribute values 
        @type value: ndg.xacml.utils.TypedList
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, TypedList):
            raise TypeError('Expecting %r type for "attributeValues" '
                            'attribute; got %r' % (TypedList, type(value)))
            
        self.__attributeValues = value
                   
    def _get_dataType(self):
        """Get data type
        @return: attribute data type
        @rtype: basestring / NoneType
        """
        return self.__dataType

    def _set_dataType(self, value):
        """Set data type
        @param value: attribute data type
        @type value: basestring
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "dataType" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__dataType = value   

    dataType = property(_get_dataType, _set_dataType, None, 
                        "Attribute data type") 
        
    @property
    def attributeId(self):
        """Get Attribute Id
        @return: attribute Id
        @rtype: basestring / NoneType
        """
        return self.__attributeId

    @attributeId.setter
    def attributeId(self, value):
        """Set Attribute Id
        @param value: attribute id
        @type value: basestring
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "attributeId" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__attributeId = value  
        
    @property
    def issuer(self):
        """Get Issuer
        @return: attribute issuer
        @rtype: basestring / NoneType
        """
        return self.__issuer

    @issuer.setter
    def issuer(self, value):
        """Set Issuer
        @param value: attribute issuer
        @type value: basestring
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "issuer" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__issuer = value

    def __getstate__(self):
        '''Enable pickling
        
        @return: class instance attributes dictionary
        @rtype: dict
        '''
        _dict = {}
        for attrName in Attribute.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_Attribute" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict
