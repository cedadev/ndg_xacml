"""NDG XACML ElementTree reader module containing reader base class 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "19/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

from ndg.xacml.parsers import AbstractReaderFactory
from ndg.xacml.utils.factory import importModuleObject
from ndg.xacml.utils import VettedDict
from ndg.xacml.core import XacmlCoreBase
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader


class ETreeReaderClassMap(VettedDict):
    """Specialised dictionary to hold mappings of XACML classes to their
    equivalent ElementTree reader classes
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
        """Enforce XACML base class type keys
        
        @param key: URN for attribute
        @type key: basestring
        @return: boolean True indicating key is OK
        @rtype: bool
        @raise TypeError: incorrect input type
        """
        if not issubclass(key, XacmlCoreBase):
            raise TypeError('Expecting %r derived type for key; got %r' % 
                            (XacmlCoreBase, type(key))) 
        return True 
    
    @staticmethod
    def valueFilter(value):
        """Enforce ElementTree abstract reader derived types for values
        @param value: attribute value
        @type value: ndg.xacml.core.attributevalue.AttributeValue derived type
        @return: boolean True indicating attribute value is correct type
        @rtype: bool
        @raise TypeError: incorrect input type
        """
        if not issubclass(value, ETreeAbstractReader):
            raise TypeError('Expecting %r derived type for value; got %r' % 
                            (ETreeAbstractReader, type(value))) 
        return True 
    
    
class ReaderFactory(AbstractReaderFactory):
    """Parser factory for ElementTree based parsers for XACML types"""
    READER_CLASS_MAP = ETreeReaderClassMap()
    
    @classmethod
    def addReader(cls, xacmlType, readerClass):
        """Add custom classes and readers
        
        @param xacmlType: XACML type to return a parser class for
        @type xacmlType: type
        @param readerClass: ElementTree based reader for the input XACML type.  
        @type readerClass: ndg.xacml.parsers.etree.reader.ETreeAbstractReader 
        derived type
        """
        cls.READER_CLASS_MAP[xacmlType] = readerClass
    
    @classmethod
    def getReader(cls, xacmlType):
        """Return ElementTree based Reader class for the given input
        
        @param xacmlType: XACML type to return a parser class for
        @type xacmlType: type
        @return: ElementTree based reader for the input XACML type.  The class
        and module containing the class are inferred from the XACML class name
        input e.g. 
        
        ndg.xacml.core.Subject => ndg.xacml.parsers.etree.subjectreader.SubjectReader
        
        @rtype: ndg.xacml.parsers.etree.reader.ETreeAbstractReader derived
        type
        @raise ImportError: if no reader class found for input type
        """
        if xacmlType in cls.READER_CLASS_MAP:
            # Retrieve from mapping
            return cls.READER_CLASS_MAP[xacmlType]
        else:
            # Infer from the package structure
            xacmlTypeName = xacmlType.__name__
            readerClassName = 'ndg.xacml.parsers.etree.%sreader.%sReader' % (
                                                        xacmlTypeName.lower(),
                                                        xacmlTypeName)
            readerClass = importModuleObject(readerClassName)
            return readerClass
            
