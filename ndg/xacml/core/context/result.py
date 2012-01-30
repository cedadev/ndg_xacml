"""NDG XACML module for Result type 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "23/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.core.context import XacmlContextBase
from ndg.xacml.core.obligation import Obligation


class StatusCode(XacmlContextBase):
    '''XACML Response Result StatusCode.
    
    @cvar ELEMENT_LOCAL_NAME: XML Local Name of StatusCode element 
    @type ELEMENT_LOCAL_NAME: string
    
    @cvar IDENTIFIER_PREFIX: namespace prefix for status codes
    @type IDENTIFIER_PREFIX: string
    
    @cvar OK: OK response status
    @type OK: string
    
    @cvar MISSING_ATTRIBUTE: missing attribute response status
    @type MISSING_ATTRIBUTE: string
    
    @cvar PROCESSING_ERROR: response status indicating a processing error
    @type PROCESSING_ERROR: string
    
    @cvar SYNTAX_ERROR: response status for a syntax error
    @type SYNTAX_ERROR: string
    
    @cvar CODES: list of recognised codes
    @type CODES: tuple
    
    @ivar __value: status code value
    @type __value: basestring
    
    @ivar __childStatusCode: child status code
    @type __childStatusCode: ndg.xacml.core.result.StatusCode
    '''
    
    ELEMENT_LOCAL_NAME = "StatusCode"

    IDENTIFIER_PREFIX = XacmlContextBase.XACML_1_0_NS_PREFIX + ':status'
    
    OK = IDENTIFIER_PREFIX + ":ok"
    MISSING_ATTRIBUTE = IDENTIFIER_PREFIX + ":missing-attribute"
    PROCESSING_ERROR = IDENTIFIER_PREFIX + ":processing-error"
    SYNTAX_ERROR = IDENTIFIER_PREFIX + ":syntax-error"
    
    CODES = (OK, MISSING_ATTRIBUTE, PROCESSING_ERROR, SYNTAX_ERROR)
    
    __slots__ = ('__value', '__childStatusCode',)
    
    def __init__(self, **kw):
        super(StatusCode, self).__init__(**kw)
        
        # Value attribute URI.
        self.__value = None
    
        # Nested secondary StatusCode child element.
        self.__childStatusCode = None

    def _getStatusCode(self): 
        '''@return: child status code
        @rtype: ndg.xacml.core.result.StatusCode
        '''
        return self.__childStatusCode
    
    def _setStatusCode(self, value):
        '''@param value: child status code
        @type value: ndg.xacml.core.result.StatusCode
        '''
        if not isinstance(value, StatusCode):
            raise TypeError('Child "statusCode" must be a %r derived type, '
                            "got %r" % (StatusCode, type(value)))
            
        self.__childStatusCode = value

    value = property(fget=_getStatusCode, 
                     fset=_setStatusCode, 
                     doc="Child Status code")
              
    def _getValue(self):
        '''@return: status code value
        @rtype: basestring
        '''
        return self.__value
        
    def _setValue(self, value):
        '''@param value: status code value
        @type value: basestring
        '''
        if not isinstance(value, basestring):
            raise TypeError("\"value\" must be a basestring derived type, "
                            "got %r" % value.__class__)
        
        if value not in self.__class__.CODES:
            raise AttributeError('Status code expected values are %r; got %r' %
                                 (self.__class__.CODES, value))
                
        self.__value = value

    value = property(fget=_getValue, fset=_setValue, doc="Status code value")
    

class Status(XacmlContextBase): 
    '''XACML Response Result Status

    @cvar ELEMENT_LOCAL_NAME: XML Local Name of Status element 
    @type ELEMENT_LOCAL_NAME: string
    
    @ivar __statusCode: Status code element
    @type __statusCode: None / ndg.xacml.core.context.result.StatusCode
    @ivar __statusMessage: Status message element
    @type __statusMessage: None / basestring
    @ivar __statusDetail: Status detail element
    @type __statusDetail: None / any type
    '''
    
    # Local Name of Status.
    ELEMENT_LOCAL_NAME = "Status"

    __slots__ = ('__statusCode', '__statusMessage', '__statusDetail', )
    
    def __init__(self, **kw):
        super(Status, self).__init__(**kw)
        
        # StatusCode element.
        self.__statusCode = None
    
        # StatusMessage element.
        self.__statusMessage = None
    
        # StatusDetail element. 
        self.__statusDetail = None
    
    @classmethod
    def createInitialised(cls, code=StatusCode.OK, message='', detail=''):
        """Create with an empty StatusCode object set

        @param code: Status code - defaults to OK code
        @type code: basestring
        @param message: Status Message
        @type message: basestring
        @param detail: Status detail
        @type detail: string / any
        @return: Status instance
        @rtype: ndg.xacml.core.context.Status
        """
        status = cls()
        status.statusCode = StatusCode()
        status.statusCode.value = code
        status.statusMessage = message
        status.statusDetail = detail
        
        return status
        
    def _getStatusCode(self):
        '''
        Gets the Code of this Status.
        
        @return: Status StatusCode
        @rtype: ndg.xacml.core.context.StatusCode
        '''
        return self.__statusCode

    def _setStatusCode(self, value):
        '''
        Sets the Code of this Status.
        
        @param value: the Code of this Status
        @type value: ndg.xacml.core.context.StatusCode
        '''
        if not isinstance(value, StatusCode):
            raise TypeError('"statusCode" must be a %r derived type, '
                            "got %r" % (StatusCode, type(value)))
            
        self.__statusCode = value
        
    statusCode = property(fget=_getStatusCode,
                          fset=_setStatusCode,
                          doc="status code object")
    
    def _getStatusMessage(self):
        '''
        Gets the Message of this Status.
        
        @return: Status StatusMessage
        @rtype: basestring
        '''
        return self.__statusMessage

    def _setStatusMessage(self, value):
        '''
        Sets the Message of this Status.
        
        @param value: the Message of this Status
        @type value: basestring
        '''
        if not isinstance(value, basestring):
            raise TypeError('"statusMessage" must be a %r derived type, '
                            "got %r" % (basestring, type(value)))
            
        self.__statusMessage = value
        
    statusMessage = property(fget=_getStatusMessage,
                             fset=_setStatusMessage,
                             doc="status message")

    def _getStatusDetail(self):
        '''
        Gets the Detail of this Status.
        
        @return: Status detail
        @rtype: any
        '''
        return self.__statusDetail
    
    def _setStatusDetail(self, value):
        '''
        Sets the Detail of this Status.
        
        @param value: the Detail of this Status
        @type value: any type
        '''
        self.__statusDetail = value
        
    statusDetail = property(fget=_getStatusDetail,
                            fset=_setStatusDetail,
                            doc="status message")
            

class Decision(object):
    """Define decision types for Response Result
    
    @cvar ELEMENT_LOCAL_NAME: XML Local Name of StatusCode element 
    @type ELEMENT_LOCAL_NAME: string
    
    @cvar PERMIT_STR: permit decision string
    @type PERMIT_STR: string
    
    @cvar DENY_STR: deny decision string
    @type DENY_STR: string
    
    @cvar INDETERMINATE_STR: indeterminate decision string
    @type INDETERMINATE_STR: string
    
    @cvar NOT_APPLICABLE_STR: not applicable decision string
    @type NOT_APPLICABLE_STR: string
    
    @cvar TYPES: list of valid decision strings
    @type TYPES: tuple
    
    @cvar PERMIT: "Permit" decision type instance
    @type PERMIT: PermitDecision
    
    @cvar DENY: "Deny" decision type instance
    @type DENY: DenyDecision
    
    @cvar INDETERMINATE: "Indeterminate" decision type instance
    @type INDETERMINATE: IndeterminateDecision
        
    @cvar NOT_APPLICABLE: "NotApplicable" decision type instance
    @type NOT_APPLICABLE: NotApplicableDecision
       
    @ivar __value: decision value
    @type __value: string
    """
    ELEMENT_LOCAL_NAME  = 'Decision'
    
    # "Permit" decision type string
    PERMIT_STR = "Permit"
    
    # "Deny" decision type string
    DENY_STR = "Deny"
    
    # "Indeterminate" decision type string
    INDETERMINATE_STR = "Indeterminate"
    
    # "NotApplicable" decision type string
    NOT_APPLICABLE_STR = "NotApplicable"
        
    TYPES = (PERMIT_STR, DENY_STR, INDETERMINATE_STR, NOT_APPLICABLE_STR)
    
    # "Permit" decision type as an instance of PermitDecision - see 
    # re-assignment later after definition of PermitDecision class
    PERMIT = None
    
    # "Deny" decision type as instance of DenyDecision - see 
    # re-assignment later after definition of DenyDecision class
    DENY = None
    
    # "Indeterminate" decision type as instance of IndeterminateDecision - see 
    # re-assignment later after definition of IndeterminateDecision class
    INDETERMINATE = None
        
    # "NotApplicable" decision type as instance of NotApplicableDecision - see 
    # re-assignment later after definition of NotApplicableDecision class
    NOT_APPLICABLE = None
    
    __slots__ = ('__value',)
    
    def __init__(self, decision=INDETERMINATE_STR):
        self.__value = None
        self.value = decision

    def __getstate__(self):
        '''Enable pickling
        
        @return: class instance attributes dictionary
        @rtype: dict
        '''
        _dict = {}
        for attrName in Decision.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_Decision" + attrName
                
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
        """Set decision value
        
        @param value: decision value - constrained vocabulary to Decision.TYPES
        @type value: string or ndg.xacml.core.context.result.Decision
        @raise AttributeError: invalid decision string value input
        @raise TypeError: invalid type for input decision value
        """
        if isinstance(value, Decision):
            # Cast to string
            value = str(value)
            
        elif not isinstance(value, basestring):
            raise TypeError('Expecting string or Decision instance for '
                            '"value" attribute; got %r instead' % type(value))
            
        if value not in self.__class__.TYPES:
            raise AttributeError('Permissable decision types are %r; got '
                                 '%r instead' % (Decision.TYPES, value))
        self.__value = value
        
    def _getValue(self):
        """Get decision value
        
        @return: decision value 
        @rtype: string
        """
        return self.__value
    
    value = property(fget=_getValue, fset=_setValue, doc="Decision value")
    
    def __str__(self):
        """represent decision as a string
        
        @return: decision value 
        @rtype: string 
        """
        return self.__value

    def __repr__(self):
        """Overridden to show the decision value
        
        @return: decision representation 
        @rtype: string 
        """
        return "%s = %r" % (super(Decision, self).__repr__(), self.__value)
    
    def __eq__(self, decision):
        """
        @param decision: decision value to compare with self's
        @type decision: string or ndg.xacml.core.context.result.Decision
        @return: True if the decision values match, False otherwise
        @rtype: bool
        @raise AttributeError: invalid decision string value input
        @raise TypeError: invalid type for input decision value
        """
        if isinstance(decision, Decision):
            # Cast to string
            value = decision.value
            
        elif isinstance(decision, basestring):
            value = decision
            
        else:
            raise TypeError('Expecting string or Decision instance for '
                            'input decision value; got %r instead' % type(value))
            
        if value not in self.__class__.TYPES:
            raise AttributeError('Permissable decision types are %r; got '
                                 '%r instead' % (Decision.TYPES, value))
            
        return self.__value == value   


class PermitDecision(Decision):
    """Permit authorisation Decision"""
    __slots__ = ()

    def __init__(self):
        """Initialise set with Permit value"""
        super(PermitDecision, self).__init__(Decision.PERMIT_STR)
        
    def _setValue(self):  
        """Make value read-only
        @raise AttributeError: value can't be set
        """
        raise AttributeError("can't set attribute")


class DenyDecision(Decision):
    """Deny authorisation Decision"""
    __slots__ = ()
    
    def __init__(self):
        """Initialise set with deny value"""
        super(DenyDecision, self).__init__(Decision.DENY_STR)
        
    def _setValue(self, value):  
        """Make value read-only
        @raise AttributeError: value can't be set
        """
        raise AttributeError("can't set attribute")


class IndeterminateDecision(Decision):
    """Indeterminate authorisation Decision"""
    __slots__ = ()
    
    def __init__(self):
        """Initialise set with indeterminate value"""
        super(IndeterminateDecision, self).__init__(Decision.INDETERMINATE_STR)
        
    def _setValue(self, value):  
        """Make value read-only
        @raise AttributeError: value can't be set
        """
        raise AttributeError("can't set attribute")


class NotApplicableDecision(Decision):
    """NotApplicable authorisation Decision"""
    __slots__ = ()
    
    def __init__(self):
        """Initialise set with not applicable value"""
        super(NotApplicableDecision, self).__init__(Decision.NOT_APPLICABLE_STR)
        
    def _setValue(self, value):  
        """Make value read-only
        @raise AttributeError: value can't be set
        """
        raise AttributeError("can't set attribute")
    
    
# Add instances of each for convenience
Decision.PERMIT = PermitDecision()
Decision.DENY = DenyDecision()
Decision.INDETERMINATE = IndeterminateDecision()
Decision.NOT_APPLICABLE = NotApplicableDecision()


class Result(XacmlContextBase):
    """XACML Result type - element in a Response
    
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    
    @cvar OBLIGATIONS_ELEMENT_LOCAL_NAME: obligations XML element local name
    @type OBLIGATIONS_ELEMENT_LOCAL_NAME: string
    
    @cvar RESOURCE_ID_ATTRIB_NAME: resource ID XML attribute name
    @type RESOURCE_ID_ATTRIB_NAME: string
    
    @ivar __resourceId: resource id
    @type __resourceId: None/basestring
    
    @ivar __decision: decision for this result
    @type __decision: ndg.xacml.core.context.result.Decision
    
    @ivar __status: result status
    @type __status: ndg.xacml.core.context.result.Status
       
    @ivar __obligations: obligations associated with this result
    @type __obligations: ndg.xacml.core.obligation.Obligation
    """
    __slots__ = ('__resourceId', '__decision', '__status', '__obligations')
    
    ELEMENT_LOCAL_NAME  = 'Result'
    OBLIGATIONS_ELEMENT_LOCAL_NAME = 'Obligations'
    RESOURCE_ID_ATTRIB_NAME = 'ResourceId'
    
    def __init__(self):
        super(Result, self).__init__()
        self.__decision = None
        self.__status = None
        self.__resourceId = None
        self.__obligations = None
        
    @classmethod
    def createInitialised(cls, 
                          decision=Decision.NOT_APPLICABLE,
                          resourceId='', 
                          obligations=None,
                          **kw):
        """Create a result object populated with all it's child elements
        rather than set to None as is the default from __init__
        
        @param decision: decision for this result
        @type decision: ndg.xacml.core.context.result.Decision
        
        @param resourceId: resource id for associated resource
        @type resourceId: basestring
        
        @param obligations: obligations associated with this result
        @type obligations: None/ndg.xacml.core.obligation.Obligation
        
        @param kw: keywords for status attribute initialisation
        @type kw: dict
        
        @return: new result object with all its child attributes created
        @rtype: ndg.xacml.core.context.result.Result
        """
        result = cls()
        result.decision = Decision()
        result.decision.value = decision
        result.status = Status.createInitialised(**kw)
        
        if obligations is not None:
            result.obligations = obligations
            
        return result
        
    @property
    def resourceId(self):
        """Get Result resource Id
        
        @return: resource Id
        @rtype: basestring
        """
        return self.__resourceId

    @resourceId.setter
    def resourceId(self, value):
        """Set Result resource Id
        
        @param value: resource Id
        @type value: basestring
        @raise TypeError: incorrect type for input
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "resourceId" '
                            'result; got %r' % (basestring, type(value)))
            
        self.__resourceId = value
                        
    @property
    def decision(self):
        """Get Result decision
        
        @return: decision for this result
        @rtype: ndg.xacml.core.context.result.Decision
        """
        return self.__decision
    
    @decision.setter
    def decision(self, value):
        """Set Request decision
        
        @param value: decision for this result
        @type value: ndg.xacml.core.context.result.Decision
        @raise TypeError: incorrect type for input
        """
        if not isinstance(value, Decision):
            raise TypeError('Expecting %r type for result "decision" '
                            'attribute; got %r' % (Decision, type(value)))
        self.__decision = value
        
    @property
    def status(self):
        """Get Result status
        
        @return: status for this result
        @rtype: ndg.xacml.core.context.result.Status
        """
        return self.__status
    
    @status.setter
    def status(self, value):
        """Set Result status
        
        @param value: status for this result
        @type value: ndg.xacml.core.context.result.Status
        @raise TypeError: incorrect type for input
        """
        if not isinstance(value, Status):
            raise TypeError('Expecting %r type for result "status" '
                            'attribute; got %r' % (Status, type(value)))
            
        self.__status = value
                                    
    @property
    def obligations(self):
        """Get Result obligations
        
        @return: obligations associated with this result
        @rtype: ndg.xacml.core.obligations.Obligations        
        """
        return self.__obligations
    
    @obligations.setter
    def obligations(self, value):
        """Set Result obligations
        
        @param value: obligations associated with this result
        @type value: ndg.xacml.core.obligations.Obligations        
        
        @raise TypeError: incorrect type for input
        """
        if not isinstance(value, Obligation):
            raise TypeError('Expecting %r type for result "obligations" '
                            'attribute; got %r' % (Obligation, type(value)))
            
        self.__obligations = value

    def __getstate__(self):
        '''Enable pickling
        
        @return: object's attribute dictionary
        @rtype: dict
        '''
        _dict = super(Result, self).__getstate__()
        for attrName in Result.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_Result" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict
