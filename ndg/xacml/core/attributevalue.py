"""NDG XACML attribute type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "25/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from datetime import datetime, timedelta

from ndg.xacml.utils import VettedDict
from ndg.xacml.core.expression import Expression
    

class AttributeValue(Expression):
    """XACML Attribute Value type
    
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string  
    @cvar CLASS_NAME_SUFFIX: all attribute value classes end with this suffix
    @type CLASS_NAME_SUFFIX: string
    @cvar IDENTIFIER_PREFIX: geberic prefix for attribute value URNs
    @type IDENTIFIER_PREFIX: string
    @cvar IDENTIFIER: URN for attribute value in derived class 
    @type IDENTIFIER: NoneType - derived classes should set to appropriate 
    string
    @cvar TYPE_URIS: URIs for all the different supported types
    @type TYPE_URIS: tuple
    @cvar TYPE_NAMES: corresponding short names for all the types
    @type TYPE_NAMES: tuple
    @cvar NATIVE_TYPES: equivalent python types as implemented
    @cvar TYPE_MAP: mapping from type names to python types
    @type TYPE_MAP: dict
    @cvar TYPE_URI_MAP: mapping from type names to type URIs
    @type TYPE_URI_MAP: dict
    @cvar TYPE: type name for derived type - set to None in this parent class
    @type TYPE: NoneType / string in derived type
    
    @ivar __value: setting for this attribute value
    @type __value: any - constrained in derived classes
    """
    ELEMENT_LOCAL_NAME = 'AttributeValue'
    CLASS_NAME_SUFFIX = 'AttributeValue'
    IDENTIFIER_PREFIX = 'http://www.w3.org/2001/XMLSchema#'
  
    IDENTIFIER = None
    
    STRING_TYPE_URI = IDENTIFIER_PREFIX + 'string'
    ANY_TYPE_URI = IDENTIFIER_PREFIX + 'anyURI'
    INTEGER_TYPE_URI = IDENTIFIER_PREFIX + 'integer'
    BOOLEAN_TYPE_URI = IDENTIFIER_PREFIX + 'boolean'
    DOUBLE_TYPE_URI = IDENTIFIER_PREFIX + 'double'
    DATE_TYPE_URI = IDENTIFIER_PREFIX + 'date'
    DATETIME_TYPE_URI = IDENTIFIER_PREFIX + 'dateTime'
    TIME_TYPE_URI = IDENTIFIER_PREFIX + 'time'
    DAYTIMEDURATION_TYPE_URI = \
    'http://www.w3.org/TR/2002/WD-xquery-operators-20020816#dayTimeDuration'
    YEARMONTHDURATION_TYPE_URI = \
    'http://www.w3.org/TR/2002/WD-xquery-operators-20020816#yearMonthDuration'
    X500NAME_TYPE_URI = 'urn:oasis:names:tc:xacml:1.0:data-type:x500Name'
    RFC822NAME_TYPE_URI = 'urn:oasis:names:tc:xacml:1.0:data-type:rfc822Name'
    HEXBINARY_TYPE_URI = IDENTIFIER_PREFIX + 'hexBinary'
    BASE64BINARY_TYPE_URI = IDENTIFIER_PREFIX + 'base64Binary'
    IPADDRESS_TYPE_URI = 'urn:oasis:names:tc:xacml:2.0:data-type:ipAddress'
    DNSNAME_TYPE_URI = 'urn:oasis:names:tc:xacml:2.0:data-type:dnsName'

    TYPE_URIS = (
        STRING_TYPE_URI,
        ANY_TYPE_URI,
        INTEGER_TYPE_URI,
        BOOLEAN_TYPE_URI,
        DOUBLE_TYPE_URI,
        DATE_TYPE_URI,
        DATETIME_TYPE_URI,
        TIME_TYPE_URI,
        DAYTIMEDURATION_TYPE_URI,
        YEARMONTHDURATION_TYPE_URI,
        X500NAME_TYPE_URI,
        RFC822NAME_TYPE_URI,
        HEXBINARY_TYPE_URI,
        BASE64BINARY_TYPE_URI,
        IPADDRESS_TYPE_URI,
        DNSNAME_TYPE_URI
    )
    TYPE_NAMES = (
        'String',
        'AnyURI',
        'Integer',
        'Boolean',
        'Double',
        'Date',
        'DateTime',
        'Time',
        'DayTimeDuration',
        'YearMonthDuration',
        'X500Name',
        'Rfc822Name',
        'HexBinary',
        'Base64Binary',
        'IpAddress',
        'DnsName',
    )
    NATIVE_TYPES = (
        basestring,
        basestring,
        int,
        bool,
        float,
        datetime,
        datetime,
        datetime,
        timedelta,
        timedelta,
        basestring,
        basestring,
        int,
        NotImplemented,
        basestring,
        basestring
    )
    TYPE_MAP = dict(zip(TYPE_NAMES, NATIVE_TYPES))
    TYPE_URI_MAP = dict(zip(TYPE_NAMES, TYPE_URIS))
    TYPE = None
    
    __slots__ = ('__value',) 
    
    def __init__(self, value=None):
        """Derived classes must override setting TYPE class variable
        
        @param value: initialise the attribute value by setting this keyword
        @type value: (set by self.__class__.TYPE)
        """
        
        super(AttributeValue, self).__init__()
        if self.__class__.TYPE is None:
            raise NotImplementedError('TYPE class variable must be set to a '
                                      'valid type in a derived class')
            
        self.__value = None
        
        # Allow derived classes to make an implicit data type setting
        self.dataType = self.__class__.IDENTIFIER
        
        if value is not None:
            self.value = value

    def __repr__(self):
        return "%s = %r " % (super(AttributeValue, self).__repr__(),
                             self.value)

    def __eq__(self, attrVal):
        """Check for equality by comparing the value attributes"""
        if not isinstance(attrVal, self.__class__):
            raise TypeError('Expecting %r type for "value" '
                            'attribute; got %r' % (self.__class__.TYPE, 
                                                   type(attrVal)))
            
        return self.__value == attrVal.value
    
    def _get_value(self):
        """Get value
        @return: setting for this attribute value
        @rtype: any - constrained in derived classes
        """
        return self.__value

    def _set_value(self, value):
        """Set value
        
        @param value: setting for this attribute value
        @type value: any - constrained in derived classes
        @raise TypeError: if type doesn't match TYPE class variable.  Derived
        classes should set this
        """
        if not isinstance(value, self.__class__.TYPE):
            raise TypeError('Expecting %r type for "value" '
                            'attribute; got %r' % (self.__class__.TYPE, 
                                                   type(value)))
            
        self.__value = value  

    value = property(_get_value, _set_value, None, "expression value") 
    
    def evaluate(self, context):
        """Evaluate the result of the expression in a condition.  In the case of
        an attribute value it's simply itself
        
        @param context: the request context
        @type context: ndg.xacml.core.context.request.Request
        @return: this attribute value
        @rtype: AttributeValue  
        """ 
        return self

    def __getstate__(self):
        '''Enable pickling
        
        @return: object's attribute dictionary
        @rtype: dict
        '''
        _dict = super(AttributeValue, self).__getstate__()
        for attrName in AttributeValue.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_AttributeValue" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict


class AttributeValueClassMap(VettedDict):
    """Specialised dictionary to hold mappings of XML attribute type URIs to 
    their equivalent classes
    """
    
    def __init__(self):
        """Force entries to derive from AttributeValue and IDs to
        be string type
        """        
        # Filters are defined as staticmethods but reference via self here to 
        # enable derived class to override them as standard methods without
        # needing to redefine this __init__ method            
        VettedDict.__init__(self, self.keyFilter, self.valueFilter)
        
    @staticmethod
    def keyFilter(key):
        """Enforce string type keys
        
        @param key: URN for attribute
        @type key: basestring
        @return: boolean True indicating key is OK
        @rtype: bool
        @raise TypeError: incorrect input type
        """
        if not isinstance(key, basestring):
            raise TypeError('Expecting %r type for key; got %r' % 
                            (basestring, type(key))) 
        return True 
    
    @staticmethod
    def valueFilter(value):
        """Enforce AttributeValue derived types for values
        @param value: attribute value
        @type value: ndg.xacml.core.attributevalue.AttributeValue derived type
        @return: boolean True indicating attribute value is correct type
        @rtype: bool
        @raise TypeError: incorrect input type
        """
        if not issubclass(value, AttributeValue):
            raise TypeError('Expecting %r derived type for value; got %r' % 
                            (AttributeValue, type(value))) 
        return True 


class AttributeValueClassFactory(object):
    """Create AttributeValue types based on the XML namespace identifier
    
    Convenience wrapper for IDENTIFIER2CLASS_MAP instance of 
    AttributeValueClassMap
    
    @ivar __classMap: mapping object to map attribute value URIs to their 
    implementations as classes
    @type __classMap: ndg.xacml.core.attributevalue.AttributeValueClassMap
    """
    __slots__ = ('__classMap',)
    
    # Dynamically Create classes based on AttributeValue for all the XACML 
    # primitive types
    IDENTIFIER2CLASS_MAP = AttributeValueClassMap()
    _typeName, _type, _identifier, _className, _classVars, \
        _attributeValueClass = (None,)*6
        
    for _typeName, _type in AttributeValue.TYPE_MAP.items():
        _identifier = AttributeValue.TYPE_URI_MAP[_typeName]
    
        _className = _typeName + AttributeValue.CLASS_NAME_SUFFIX               
        _classVars = {'TYPE': _type, 'IDENTIFIER': _identifier}
        
        _attributeValueClass = type(_className, (AttributeValue, ), _classVars)
        AttributeValue.register(_attributeValueClass)
        IDENTIFIER2CLASS_MAP[_identifier] = _attributeValueClass
    
    del _typeName, _type, _identifier, _className, _classVars, \
        _attributeValueClass
        
    def __init__(self, classMap=None):
        """Set a mapping object to map attribute value URIs to their 
        implementations as classes
        
        @param classMap: input an alternative to the default class mapping 
        object IDENTIFIER2CLASS_MAP, if None, it will default to this setting
        @type classMap: ndg.xacml.core.attributevalue.AttributeValueClassMap
        """
        if classMap is None:
            self.__classMap = self.__class__.IDENTIFIER2CLASS_MAP
        elif isinstance(classMap, AttributeValueClassMap):
            self.__classMap = classMap
        else:
            raise TypeError('Expecting %r derived type for "map" input; got %r'
                            % (AttributeValueClassMap, type(map)))
            
    def __call__(self, identifier):
        """Return <type>AttributeValue class for given identifier URI or None
        if no match is found
        
        @return: attribute value class
        @rtype: NoneType / ndg.xacml.core.attributevalue.AttributeValue derived
        type
        """
        return self.__classMap.get(identifier)
    
    @classmethod
    def addClass(cls, identifier, attributeValueClass, overwrite=False):
        """Extend Default AttributeValue Class Map with custom types.  This 
        enables the policy to support additional attribute types
        
        @param identifier: ID for candidate Attribute Value class
        @type identifier: ndg.xacml.core.attributevalue.AttributeValueClassMap 
        @param attributeValueClass: new Attribute Value class to be added
        @type attributeValueClass: ndg.xacml.core.attributevalue.AttributeValue
        @param overwrite: set to True to allow overwriting of existing map 
        entries, defaults to disable overwrite
        @type overwrite: bool
        """
        # Instantiate class map to validate input types.
        classMap = AttributeValueClassMap()
        classMap[identifier] = attributeValueClass
        
        if overwrite:
            cls.IDENTIFIER2CLASS_MAP.update(classMap)
        else:
            for k, v in classMap.items():
                if k not in cls.IDENTIFIER2CLASS_MAP:
                    cls.IDENTIFIER2CLASS_MAP[k] = v        
                    
