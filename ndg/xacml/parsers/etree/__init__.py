"""NDG XACML ElementTree parsers package 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)
import re

from ndg.xacml import Config, importElementTree
ElementTree = importElementTree()

class SerialisedElementTree(unicode):
    """Marks a unicode string as being serialised ElementTree XML.
    """
    pass

if Config.use_lxml:
    def makeEtreeElement(tag, ns_prefix, ns_uri, attrib={}, **extra):
        """Makes an ElementTree element handling namespaces in the way
        appropriate for the ElementTree implementation in use.
        """
        elem = ElementTree.Element(tag, {ns_prefix: ns_uri}, attrib, **extra)
        return elem

    def serialiseIfElementTree(obj):
        if ElementTree.iselement(obj):
            return SerialisedElementTree(ElementTree.tostring(obj,
                                                              encoding=unicode))
        else:
            return obj
    
    def deserialiseIfElementTree(obj):
        if isinstance(obj, SerialisedElementTree):
            return ElementTree.XML(obj)
        else:
            return obj
else:
    def makeEtreeElement(tag, ns_prefix, ns_uri, attrib={}, **extra):
        """Makes an ElementTree element handling namespaces in the way
         appropriate for the ElementTree implementation in use.
        """
        elem = ElementTree.Element(tag, attrib, **extra)
        ElementTree._namespace_map[ns_uri] = ns_prefix
        return elem

    def serialiseIfElementTree(obj):
        return obj

    def deserialiseIfElementTree(obj):
        return obj

def getElementChildren(element):
    """Iterator over children of an element that are elements, not, e.g.,
    comments.
    """
    for childElem in element:
        if (not hasattr(childElem, 'tag') or
            not isinstance(childElem.tag, basestring)):
            continue
        yield childElem


# Generic ElementTree Helper classes
class QName(ElementTree.QName):
    """Extend ElementTree implementation for improved attribute access support
    """ 

    # ElementTree tag is of the form {namespace}localPart.  getNs extracts the
    # namespace from within the brackets but if not found returns ''
    getNs = staticmethod(lambda tag: getattr(re.search('(?<=\{).+(?=\})', tag),
                                             'group', 
                                             str)())
                                             
    getLocalPart = staticmethod(lambda tag: tag.rsplit('}', 1)[-1])

    def __init__(self, input, tag=None, prefix=None):
        """
        @type input: basestring
        @param input: ElementTree style namespace URI + tag name -
        {namespace URI}tag - OR if tag keyword is set, the namespace URI alone
        @type tag: basestring / None
        @param tag: element tag name.  If None, input must contain the 
        namespace URI and tag name in the ElementTree form {namespace URI}tag.
        @type prefix: basestring / None
        @param prefix: namespace prefix
        """
        
        ElementTree.QName.__init__(self, input, tag=tag)
        
        if tag:
            self.namespaceURI = input
            self.localPart = tag
        else:
            # No tag provided namespace and localPart of QN must be parsed from
            # the namespace
            self.namespaceURI = QName.getNs(input)
            self.localPart = QName.getLocalPart(input)
            
        self.prefix = prefix
    
    def _getPrefix(self):
        """Get prefix
        @return: prefix
        @rtype: string
        """
        return self.__prefix

    def _setPrefix(self, value):
        """Set prefix
        @param value: prefix
        @type value: string
        @raise TypeError: invalid input value type
        """
        self.__prefix = value
    
    prefix = property(_getPrefix, _setPrefix, None, "Prefix")

    def _getLocalPart(self):
        """Get local part
        @return: local part
        @rtype: string
        """
        return self.__localPart
    
    def _setLocalPart(self, value):
        """Set local part
        @param value: local part
        @type value: string
        @raise TypeError: invalid input value type
        """
        self.__localPart = value
        
    localPart = property(_getLocalPart, _setLocalPart, None, "LocalPart")

    def _getNamespaceURI(self):
        """Get namespace URI
        @return: namespace URI
        @rtype: string
        """
        return self.__namespaceURI

    def _setNamespaceURI(self, value):
        """Set namespace URI
        @param value: namespace URI
        @type value: string
        @raise TypeError: invalid input value type
        """
        self.__namespaceURI = value
  
    namespaceURI = property(_getNamespaceURI, _setNamespaceURI, None, 
                            "Namespace URI'")

    def __eq__(self, qname):
        """Enable equality check for QName.  Note that prefixes don't need to
        match
        
        @type qname: ndg.xacml.utils.etree.QName
        @param qname: Qualified Name to compare with self 
        @return: True if input and this object match
        @rtype: bool
        """
        if not isinstance(qname, QName):
            raise TypeError('Expecting %r; got %r' % (QName, type(qname)))
                   
        # Nb. prefixes don't need to agree!         
        return (self.namespaceURI, self.localPart) == \
               (qname.namespaceURI, qname.localPart)

    def __ne__(self, qname):
        """Enable equality check for QName.  Note that prefixes don't need to
        match
        
        @type qname: ndg.xacml.utils.etree.QName
        @param qname: Qualified Name to compare with self 
        """
        return not self.__eq__(qname)
