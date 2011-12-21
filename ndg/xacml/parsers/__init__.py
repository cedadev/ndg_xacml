"""NDG XACML parsers package 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "15/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)
from abc import ABCMeta, abstractmethod

from ndg.xacml import XacmlError
from ndg.xacml.core import XacmlCoreBase

    
class XMLParseError(XacmlError):
    """XACML package XML Parsing error"""


class AbstractReader(object):
    """Abstract base class for XACML reader"""
    __metaclass__ = ABCMeta
    
    @classmethod
    def __subclasshook__(cls, C):
        """Derived class must implement __call__"""
        if cls is AbstractReader:
            if any("__call__" in B.__dict__ for B in C.__mro__):
                return True
            
        return NotImplemented
        
    @abstractmethod
    def __call__(self, obj, common):
        """Abstract Parse XACML method
        @raise NotImplementedError: 
        """
        raise NotImplementedError()
    
    @classmethod
    def parse(cls, obj, common):
        """Parse from input object and return new XACML object
        @param obj: input source - file name, stream object or other
        @type obj: string, stream or other
        @return: new XACML object
        @rtype: XacmlCoreBase sub type
        """
        reader = cls()
        return reader(obj, common)
    
    
class AbstractReaderFactory(object):
    """Abstract base class XACML reader factory"""
    __metaclass__ = ABCMeta
    
    @classmethod
    @abstractmethod
    def getReader(cls, xacmlType):
        """Get the reader class for the given XACML input type
        @param xacmlType: XACML type to retrieve a reader for
        @type xacmlType: ndg.xaml.core.XacmlCoreBase derived
        @return: reader class
        @rtype: ndg.xacml.parsers.AbstractReader derived type
        """
        if not issubclass(xacmlType, XacmlCoreBase):
            raise TypeError('Expecting %r derived class for getReader method; '
                            'got %r' % (XacmlCoreBase, xacmlType))
