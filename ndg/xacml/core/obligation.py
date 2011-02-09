"""NDG Security Obligation type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "24/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.utils import TypedList
from ndg.xacml.core import XacmlCoreBase
from ndg.xacml.core.attributevalue import AttributeValue


class AttributeAssignment(AttributeValue):
    """XACML AttributeAssignment type"""
       

class Effect(object):
    """Define effect type for Obligation
    
    @cvar PERMIT_STR: permit decision string
    @type PERMIT_STR: string
    
    @cvar DENY_STR: deny decision string
    @type DENY_STR: string
    
    @cvar TYPES: list of valid effect strings
    @type TYPES: tuple
    
    @ivar __value: obligation effect
    @type value: None / basestring
    """
    
    # "Permit" effect type
    PERMIT_STR = "Permit"
    
    # "Deny" effect type
    DENY_STR = "Deny"
        
    TYPES = (PERMIT_STR, DENY_STR)
    
    __slots__ = ('__value',)
    
    def __init__(self, effectType):
        """Initialise attributes giving an effect type
        @param effectType: 
        @type effectType: 
        """
        self.__value = None
        self.value = effectType

    def __getstate__(self):
        '''Enable pickling
        
        @return: instance attributes dictionary
        @rtype: dict
        '''
        _dict = {}
        for attrName in Effect.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_Effect" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict
  
    def __setstate__(self, attrDict):
        '''Enable pickling
        @param attrDict: instance attributes dictionary
        @type attrDict: dict
        '''
        for attrName, val in attrDict.items():
            setattr(self, attrName, val)
            
    def _setValue(self, value):
        """Set effect
        
        @param value: effect
        @type value: ndg.xacml.core.obligation.Effect or basestring
        @raise TypeError: incorrect type for input
        @raise AttributeError: effect value not recognised
        """
        if isinstance(value, Effect):
            # Cast to string
            value = str(value)
            
        elif not isinstance(value, basestring):
            raise TypeError('Expecting string or Effect instance for '
                            '"value" attribute; got %r instead' % type(value))
            
        if value not in self.__class__.TYPES:
            raise AttributeError('Permissable effect types are %r; got '
                                 '%r instead' % (Effect.TYPES, value))
        self.__value = value
        
    def _getValue(self):
        """Get effect
        
        @return: effect value
        @rtype: ndg.xacml.core.obligation.Effect
        """
        return self.__value
    
    value = property(fget=_getValue, fset=_setValue, doc="Effect value")
    
    def __str__(self):
        """
        @return: effect as a string
        @rtype: basestring
        """
        return self.__value

    def __eq__(self, effect):
        """
        @param effect: ndg.xacml.core.obligation.Effect or basestring
        @raise TypeError: incorrect type for input
        @raise AttributeError: effect value not recognised
        """
        if isinstance(effect, Effect):
            # Cast to string
            value = effect.value
            
        elif isinstance(effect, basestring):
            value = effect
            
        else:
            raise TypeError('Expecting string or Effect instance for '
                            'input effect value; got %r instead' % type(value))
            
        if value not in self.__class__.TYPES:
            raise AttributeError('Permissable effect types are %r; got '
                                 '%r instead' % (Effect.TYPES, value))
            
        return self.__value == value
    

class Obligation(XacmlCoreBase):
    """XACML Obligation type
    
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    @cvar ATTRIBUTE_ASSIGNMENTS_ELEMENT_LOCAL_NAME: attribute assignments XML 
    attribute name
    @type ATTRIBUTE_ASSIGNMENTS_ELEMENT_LOCAL_NAME: string
    @cvar OBLIGATION_ID_ATTRIB_NAME: obligation ID XML attribute name
    @type OBLIGATION_ID_ATTRIB_NAME: string
    
    @ivar __attributeAssignments: list of attribute assignments
    @type __attributeAssignments: ndg.xacml.utils.TypedList
    @ivar __obligationId: obligation id
    @type __obligationId: NoneType / basestring
    @ivar __fulfillOn: fulfil on condition
    @type __fulfillOn: NoneType / basestring
    """
    ELEMENT_LOCAL_NAME = 'Obligation'
    ATTRIBUTE_ASSIGNMENTS_ELEMENT_LOCAL_NAME = 'AttributeAssignment'
    FULFILLON_ELEMENT_LOCAL_NAME = 'FulfillOn'
    OBLIGATION_ID_ATTRIB_NAME = 'ObligationId'
    
    __slots__ = ('__attributeAssignments', '__obligationId', '__fulfillOn')
    
    def __init__(self):
        """Initialise attributes"""
        self.__attributeAssignments = TypedList(AttributeAssignment)
        self.__obligationId = None
        self.__fulfillOn = None
        
    @property
    def attributeAssignments(self):
        """Obligation attribute assignments
        @return: attribute assignments
        @rtype: ndg.xacml.utils.TypedList
        """
        return self.__attributeAssignments
    
    @property
    def obligationId(self):
        """obligation Id
        @return: obligation id
        @rtype: NoneType / basestring
        """
        return self.__obligationId

    @obligationId.setter
    def obligationId(self, value):
        """obligation Id
        
        @param value: obligation id
        @type value: NoneType / basestring
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "obligationId" attribute; '
                            'got %r' % (basestring, type(value)))
            
        self.__obligationId = value        
    
    @property
    def fulfillOn(self):
        """Fulfill obligation on the given effect Permit/Deny
        
        @return: fulfil condition
        @rtype: NoneType / basestring
        """
        return self.__fulfillOn

    @fulfillOn.setter
    def fulfillOn(self, value):
        """Fulfill obligation on the given effect Permit/Deny
        @param value: fulfil condition
        @type value: NoneType / basestring
        @raise TypeError: incorrect type for input
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "fulfillOn" attribute; got '
                            '%r' % (Effect, type(value)))
            
        self.__fulfillOn = value
        
