"""NDG XACML core package 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.utils import TypedList

    
class XacmlCoreBase(object):
    """Base class for all XACML types
    
    @cvar XACML_1_0_NS_PREFIX: XACML version 1.0 namespace prefix
    @type XACML_1_0_NS_PREFIX: string
    @cvar XACML_2_0_NS_PREFIX: XACML version 2.0 namespace prefix
    @type XACML_2_0_NS_PREFIX: string
    @cvar XMLNS: list of valid XACML namespaces
    @type XMLNS: tuple
    @cvar ELEMENT_LOCAL_NAME: XML element local name for the given type
    @type ELEMENT_LOCAL_NAME: NoneType but implement as string in derived 
    classes
    
    @ivar __xmlns: XML namespace for the XACML type
    @type __xmlns: NoneType / basestring
        
    @ivar __elem: XML element 
    @type __elem: NoneType / dependent on Python XML parser used
    """
    XACML_1_0_NS_PREFIX = "urn:oasis:names:tc:xacml:1.0"
    XACML_2_0_NS_PREFIX = "urn:oasis:names:tc:xacml:2.0"
    
    XMLNS = (XACML_1_0_NS_PREFIX, XACML_2_0_NS_PREFIX)
    
    __slots__ = ('__xmlns', '__reader', '__writer', '__elem')

    ELEMENT_LOCAL_NAME = None
    
    def __init__(self):
        """Element local name check makes this a virtual method
        
        @raise NotImplementedError: derived classes must set 
        ELEMENT_LOCAL_NAME to a string
        """
        self.__xmlns = None
        self.__elem = None
        self.__reader = None
        self.__writer = None
        
        if not isinstance(self.__class__.ELEMENT_LOCAL_NAME, basestring):
            raise NotImplementedError('"ELEMENT_LOCAL_NAME" must be defined in '
                                      'a derived class')
        
    def _getXmlns(self):
        """Get XML Namespace for this XACML type
        @return: the XML namespace set
        @rtype: basestring/NoneType        
        """
        return self.__xmlns

    def _setXmlns(self, value):
        """Set XML Namespace for this XACML type
        @param value: the XML namespace to set
        @type value: basestring/NoneType                 
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting string type for "xmlns" '
                            'attribute; got %r' % type(value))
        self.__xmlns = value

    xmlns = property(_getXmlns, _setXmlns, 
                     doc="XML Namespace for policy the document")
    
    @property
    def isValidXmlns(self):
        """Check XML namespace fits with the known XACML namespaces
        @return: True if valid, False otherwise
        @rtype: bool
        """
        return self.xmlns in XacmlCoreBase.XMLNS
        
    @property
    def elem(self):
        """XML Node for as represented by parser/writer specified with the 
        reader/writer attributes.  Readers of context elements should set this
        element if a policy uses AttributeSelectors to do XPath queries into
        the request context
        """
        return self.__elem
        
    @elem.setter
    def elem(self, value):
        """"XML Node for as represented by parser/writer specified with the 
        reader/writer attributes
        
        @param value: XML node instance
        @type value: type (governed by reader/writer set for this XACML object)
        """
        self.__elem = value

    def __getstate__(self):
        '''Enable pickling
        
        @return: object's attribute dictionary
        @rtype: dict
        '''
        _dict = {}
        for attrName in XacmlCoreBase.__slots__:
            # Ugly hack to allow for derived classes setting private member
            # variables
            if attrName.startswith('__'):
                attrName = "_XacmlCoreBase" + attrName
                
            _dict[attrName] = getattr(self, attrName)
            
        return _dict
            

class XacmlPolicyBase(XacmlCoreBase):
    """Base class for policy types
    
    @cvar XACML_2_0_POLICY_NS: XACML 2.0 policy XML namespace
    @type XACML_2_0_POLICY_NS: string
    """
    XACML_2_0_POLICY_NS = (XacmlCoreBase.XACML_2_0_NS_PREFIX +
                           ":policy:schema:os")
    __slots__ = ()
    
    def __init__(self):
        """Initialise parent class xmlns attribute based on this classes'
        policy namespace
        """
        super(XacmlPolicyBase, self).__init__()
        self.xmlns = XacmlPolicyBase.XACML_2_0_POLICY_NS
            
        
class TargetChildBase(XacmlPolicyBase):
    """Abstract Base class for XACML Policy Subject, Resource, Action and 
    Environment types: e.g. ndg.xacml.core.subject.Subject
    
    @cvar MATCH_TYPE: Set the type for match attributes in the derived class
    implementation e.g. ResourceMatch, SubjectMatch etc.
    @type MATCH_TYPE: NoneType - derived class must implement
    
    @ivar __matches: list of matches for this target
    @type __matches: ndg.xacml.core.utils.TypedList
    """
    MATCH_TYPE = None
    
    __slots__ = ('__matches', )
    
    def __init__(self):
        super(TargetChildBase, self).__init__()
        
        # Derived types can specify the type for matches via the MATCH_TYPE
        # class variable
        if self.__class__.MATCH_TYPE is None:
            raise NotImplementedError('Match type attribute must be specified '
                                      'in a derived class')
        self.__matches = TypedList(self.__class__.MATCH_TYPE)
        
    @property
    def matches(self):
        """Get matches list for this target
        """
        return self.__matches
    
    
XACML_1_0_PREFIX = "urn:oasis:names:tc:xacml:1.0:"

class Identifiers(object):
    """XACML Identifiers"""
    class Subject(object):
        """XAMCL Subject Identifiers"""
        AUTHN_LOCALITY_DNS_NAME = XACML_1_0_PREFIX + \
            "subject:authn-locality:dns-name"
        AUTHN_LOCALITY_IP_ADDRESS = XACML_1_0_PREFIX + \
            "subject:authn-locality:ip-address"
        AUTHN_METHOD = XACML_1_0_PREFIX + "subject:authentication-method"
        AUTHN_TIME = XACML_1_0_PREFIX + "subject:authentication-time"
        KEY_INFO = XACML_1_0_PREFIX + "subject:key-info"
        REQUEST_TIME = XACML_1_0_PREFIX + "subject:request-time"
        SESSION_START_TIME = XACML_1_0_PREFIX + "subject:session-start-time"
        SUBJECT_ID = XACML_1_0_PREFIX + "subject:subject-id"
        SUBJECT_ID_QUALIFIER = XACML_1_0_PREFIX + "subject:subject-id-qualifier"
        
    class SubjectCategory(object):
        """XACML Subject Category Identifiers"""
        ACCESS_SUBJECT = XACML_1_0_PREFIX + "subject-category:access-subject"
        CODEBASE = XACML_1_0_PREFIX + "subject-category:codebase"
        INTERMEDIARY_SUBJECT = XACML_1_0_PREFIX + \
            "subject-category:intermediary-subject"
        RECIPIENT_SUBJECT = XACML_1_0_PREFIX + \
            "subject-category:recipient-subject"
        REQUESTING_MACHINE = XACML_1_0_PREFIX + \
            "subject-category:requesting-machine"
        
    class Resource(object):
        """XACML Resource Identifiers"""
        RESOURCE_LOCATION = XACML_1_0_PREFIX + "resource:resource-location"
        RESOURCE_ID = XACML_1_0_PREFIX + "resource:resource-id"
        SIMPLE_FILE_NAME = XACML_1_0_PREFIX + "resource:simple-file-name"
        
    class Action(object):
        """XACML Action Identifiers"""
        ACTION_ID = XACML_1_0_PREFIX + "action:action-id"
        IMPLIED_ACTION = XACML_1_0_PREFIX + "action:implied-action"
     
    class Environment(object):
        """XACML Environment Identifiers"""
        CURRENT_TIME = XACML_1_0_PREFIX + "environment:current-time"
        CURRENT_DATE = XACML_1_0_PREFIX + "environment:current-date"
        CURRENT_DATETIME = XACML_1_0_PREFIX + "environment:current-dateTime"



