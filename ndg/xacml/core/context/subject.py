"""NDG XACML Context Subject type

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "24/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core.context import RequestChildBase


class Subject(RequestChildBase):
    """XACML Context Subject type
    
    @cvar ELEMENT_LOCAL_NAME: XML Local Name of this element 
    @type ELEMENT_LOCAL_NAME: string
    
    @cvar SUBJECT_CATEGORY_ATTRIB_NAME: subject category XML attribute name
    @type SUBJECT_CATEGORY_ATTRIB_NAME: string
    
    @ivar __subjectCategory: subject category XML attribute name
    @type __subjectCategory: string    
    """
    ELEMENT_LOCAL_NAME = 'Subject'
    SUBJECT_CATEGORY_ATTRIB_NAME = 'SubjectCategory'
    
    __slots__ = ('__subjectCategory',)
    
    def __init__(self):
        super(Subject, self).__init__()
        self.__subjectCategory = None

    def _get_subjectCategory(self):
        """Get subject category
        
        @return: subject category XML attribute name
        @rtype: string 
        """   
        return self.__subjectCategory

    def _set_subjectCategory(self, value):
        """Set subject category
        
        @param value: subject category XML attribute name
        @type value: string    
        
        @raise TypeError: incorrect type for input
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "subjectCategory" '
                            'attribute; got %r' % (basestring, type(value)))
            
        self.__subjectCategory = value   

    subjectCategory = property(_get_subjectCategory, _set_subjectCategory, None, 
                               "Subject category")