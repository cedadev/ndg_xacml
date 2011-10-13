"""NDG Security Rule type definition

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "25/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import traceback
import logging
log = logging.getLogger(__name__)

from ndg.xacml.core import XacmlCoreBase
from ndg.xacml.core.target import Target
from ndg.xacml.core.condition import Condition
from ndg.xacml.core.context.result import Decision


class Effect(object):
    """Rule Effect
    
    @cvar PERMIT_STR: permit decision string
    @type PERMIT_STR: string
    
    @cvar DENY_STR: deny decision string
    @type DENY_STR: string
    
    @cvar TYPES: list of valid effect strings
    @type TYPES: tuple
    
    @ivar value: effect value
    @type value: string
    """
    DENY_STR = 'Deny'
    PERMIT_STR = 'Permit'
    TYPES = (DENY_STR, PERMIT_STR)
    __slots__ = ('__value',)
    
    def __init__(self, effect=DENY_STR):
        """@param effect: initialise effect value, defaults to deny
        @type effect: basestring / ndg.xacml.core.rule.Effect
        """
        self.__value = None
        self.value = effect

    def __getstate__(self):
        '''Enable pickling
        
        @return: class instance attributes dictionary
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
        
        @param attrDict: class instance attributes dictionary
        @type attrDict: dict
        '''
        for attrName, val in attrDict.items():
            setattr(self, attrName, val)
            
    def _setValue(self, value):
        """Set effect value
        
        @param value: effect value - constrained vocabulary to Effect.TYPES
        @type value: string or ndg.xacml.core.rule.Effect
        @raise AttributeError: invalid decision string value input
        @raise TypeError: invalid type for input decision value
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
        """Get effect value
        
        @return: effect value 
        @rtype: string
        """
        return self.__value
    
    value = property(fget=_getValue, fset=_setValue, doc="Effect value")
    
    def __str__(self):
        """represent decision as a string
        
        @return: decision value 
        @rtype: string 
        """
        return self.__value

    def __eq__(self, effect):
        """
        @param effect: effect value to compare with self's
        @type effect: string or ndg.xacml.core.rule.Effect
        @return: True if the decision values match, False otherwise
        @rtype: bool
        @raise AttributeError: invalid decision string value input
        @raise TypeError: invalid type for input decision value
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
    
    def __nonzero__(self):
        """Boolean evaluation of a rule effect - True = Allow; False = Deny
        
        @return: True if the effect value is permit, False otherwise
        @rtype: bool
        """
        return self.__value == Effect.PERMIT_STR       


class PermitEffect(Effect):
    """Permit authorisation Effect"""
    __slots__ = ()

    def __init__(self):
        """Initialise set with Permit value"""
        super(PermitEffect, self).__init__(Effect.PERMIT_STR)
        
    def _setValue(self, value):  
        """Make value read-only
        @raise AttributeError: value can't be set
        """
        raise AttributeError("can't set attribute")


class DenyEffect(Effect):
    """Deny authorisation Effect"""
    __slots__ = ()
    
    def __init__(self):
        """Initialise set with Permit value"""
        super(DenyEffect, self).__init__(Effect.DENY_STR)
        
    def _setValue(self, value):  
        """Make value read-only
        @raise AttributeError: value can't be set
        """
        raise AttributeError("can't set attribute")

# Add instances of each for convenience
Effect.PERMIT = PermitEffect()
Effect.DENY = DenyEffect()


class Rule(XacmlCoreBase):
    """XACML Policy Rule
    
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    @cvar DESCRIPTION_LOCAL_NAME: XML local name for the description element
    @type DESCRIPTION_LOCAL_NAME: string
    @cvar RULE_ID_ATTRIB_NAME: rule id XML attribute name
    @type RULE_ID_ATTRIB_NAME: string
    @cvar EFFECT_ATTRIB_NAME: effect XML attribute name
    @type EFFECT_ATTRIB_NAME: string

    @ivar __target: rule target
    @type __target: ndg.xacml.core.target.Target / NoneType
    @ivar __condition: rule condition
    @type __condition: ndg.xacml.core.condition.Condition / NoneType
    @ivar __description: rule description text
    @type __description: basestring / NoneType
    @ivar __id: rule ID
    @type __id: basestring / NoneType
    @ivar __effect: rule effect
    @type __effect: ndg.xacml.core.rule.Effect / NoneType
    """
    ELEMENT_LOCAL_NAME = 'Rule'
    RULE_ID_ATTRIB_NAME = 'RuleId'
    EFFECT_ATTRIB_NAME = 'Effect'
    
    DESCRIPTION_LOCAL_NAME = 'Description'
    
    __slots__ = (
        '__target', 
        '__condition', 
        '__description', 
        '__id', 
        '__effect'
    )
    
    def __init__(self):
        """Initialise attributes"""
        super(Rule, self).__init__()
        
        self.__id = None
        self.__effect = None
        self.__target = None
        self.__condition = None
        
    @property
    def target(self):
        """Get Rule target
        @return: rule target
        @rtype: ndg.xacml.core.target import Target / NoneType 
        """
        return self.__target
    
    @target.setter
    def target(self, value):
        """Set rule target
        @param value: rule target
        @type value: ndg.xacml.core.target import Target 
        @raise TypeError: incorrect type set
        """
        if not isinstance(value, Target):
            raise TypeError('Expecting %r type for "id" '
                            'attribute; got %r' % (Target, type(value))) 
        self.__target = value
           
    @property
    def condition(self):
        """Get rule condition
        
        @return: rule condition
        @rtype: ndg.xacml.core.condition.Condition / NoneType
        """
        return self.__condition
    
    @condition.setter
    def condition(self, value):
        """Set rule condition
        
        @param value: rule condition
        @type value: ndg.xacml.core.condition.Condition
        @raise TypeError: incorrect type set
        """
        if not isinstance(value, Condition):
            raise TypeError('Expecting %r type for "id" attribute; got %r' % 
                            (Condition, type(value))) 
            
        self.__condition = value
             
    def _get_id(self):
        """Get rule ID
        
        @return: rule ID
        @rtype: ndg.xacml.core.condition.Condition / NoneType
        """
        return self.__id

    def _set_id(self, value):
        """Set rule ID
        
        @param value: rule ID
        @type value: basestring
        @raise TypeError: incorrect type set
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "id" attribute; got %r' % 
                            (basestring, type(value)))
         
        self.__id = value   

    id = property(_get_id, _set_id, None, "Rule identifier attribute")  
      
    def _get_effect(self):
        """Get rule effect
        
        @return: rule effect
        @rtype: ndg.xacml.core.rule.Effect / NoneType
        """
        return self.__effect

    def _set_effect(self, value):
        """Set rule effect
        
        @param value: rule effect
        @type value: ndg.xacml.core.rule.Effect
        @raise TypeError: incorrect type set
        """
        if not isinstance(value, Effect):
            raise TypeError('Expecting %r type for "effect" '
                            'attribute; got %r' % (Effect, type(value)))
            
        self.__effect = value   

    effect = property(_get_effect, _set_effect, None, 
                      "Rule effect attribute")  

    def _getDescription(self):
        """Get rule description
        
        @return: rule description
        @rtype: basestring / NoneType
        """
        return self.__description

    def _setDescription(self, value):
        """Set rule description
        
        @param value: rule description
        @type value: basestring
        @raise TypeError: incorrect type set
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "description" '
                            'attribute; got %r' % type(value))
        self.__description = value

    description = property(_getDescription, _setDescription, 
                           doc="Rule Description text")
    
    def evaluate(self, context):
        """Evaluate a rule
        @param context: the request context
        @type context: ndg.xacml.core.request.Request
        @return: result of the evaluation - the decision for this rule
        @rtype: ndg.xacml.core.context.result.Decision
        """
        
        # Place exception block to enable rule combining algorithm which calls
        # this method to correctly handle Indeterminate results
        try:
            log.debug('Evaluating rule %r ...', self.id)
            
            # Instantiation implicitly sets to default value of Indeterminate
            decision = Decision()
            
            # Check for a rule target
            if self.target is not None:
                targetMatch = self.target.match(context)
                if targetMatch:
                    log.debug('Match to request context for target in rule '
                              '%r', self.id)
            else:
                log.debug('No target set in rule %r', self.id)
                targetMatch = True
      
            if not targetMatch:
                log.debug('No match to request context for target in rule '
                          '%r returning NotApplicable status', self.id)
                decision = Decision.NOT_APPLICABLE
                return decision
            
            # Apply the condition if present
            if self.condition is not None:
                conditionStatus = self.condition.evaluate(context)
            else:
                # No condition set to True - 7.8 in spec.:
                #
                # The condition value SHALL be "True" if the <Condition> element
                # is absent
                log.debug('No condition set for rule %r: setting condition '
                          'status True', self.id)
                conditionStatus = True
                
            # Ref. Spec. 7.9 Rule evaluation, Nb. to get this far, the target
            # must evaluated as True
            if conditionStatus:
                decision = Decision(decision=self.effect.value)
            else:
                decision = Decision.NOT_APPLICABLE
               
            log.debug('Rule %r evaluates to %s', self.id, decision) 
            return decision
        
        except Exception:
            _traceback = traceback.format_exc()
            log.error('Error occurred evaluating rule %r, returning '
                      'Indeterminate result to caller: %s',
                      self.id, _traceback)
            return Decision.INDETERMINATE
