"""ElementTree Utilities package for NDG Security

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "02/04/09"
__copyright__ = ""
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'

from ndg.xacml import Config, importElementTree
ElementTree = importElementTree()

from ndg.xacml.parsers.etree import QName

# Fred Lundh's customisation for C14N functionality - egg available from
# http://ndg.nerc.ac.uk/dist site
c14nWarning = ("Custom ElementC14N package is not installed, canonicalize "
               "function is disabled")
try:
    from elementtree import ElementC14N
    elementC14nNotInstalled = False
except ImportError:
    elementC14nNotInstalled = True
    import warnings
    warnings.warn(c14nWarning)
    
from cStringIO import StringIO


def canonicalize(elem, **kw):
    '''ElementTree based Canonicalization - See ElementC14N for keyword
    info.  Also useful for pretty printing XML
    @type elem: ElementTree.Element
    @param elem: element to be canonicalized
    @rtype: basestring
    @return: canonicalised output
    '''
    if elementC14nNotInstalled:
        raise NotImplementedError(c14nWarning)
    
    f = StringIO()
    ElementC14N.write(ElementC14N.build_scoped_tree(elem), f, **kw)
    return f.getvalue()


def prettyPrint(*arg, **kw):
    '''Lightweight pretty printing of ElementTree elements.  This function
    wraps the PrettyPrint class
    
    @param arg: arguments to pretty print function
    @type arg: tuple
    @param kw: keyword arguments to pretty print function
    @type kw: dict
    '''
    
    # Keep track of namespace declarations made so they're not repeated
    declaredNss = []
    if not Config.use_lxml:
        mappedPrefixes = dict.fromkeys(ElementTree._namespace_map.values(), True)
        namespace_map_backup = ElementTree._namespace_map.copy()
    else:
        mappedPrefixes = {}

    _prettyPrint = _PrettyPrint(declaredNss, mappedPrefixes)
    result = _prettyPrint(*arg, **kw)

    if not Config.use_lxml:
        ElementTree._namespace_map = namespace_map_backup

    return result


class _PrettyPrint(object):
    '''Class for lightweight pretty printing of ElementTree elements'''
    MAX_NS_TRIES = 256
    def __init__(self, declaredNss, mappedPrefixes):
        """
        @param declaredNss: declared namespaces
        @type declaredNss: iterable of string elements
        @param mappedPrefixes: map of namespace URIs to prefixes
        @type mappedPrefixes: map of string to string
        """
        self.declaredNss = declaredNss
        self.mappedPrefixes = mappedPrefixes
    
    @staticmethod
    def estrip(elem):
        '''Utility to remove unwanted leading and trailing whitespace 
        
        @param elem: ElementTree element
        @type elem: ElementTree.Element
        @return: element content with whitespace removed
        @rtype: basestring'''
        if elem is None:
            return ''
        else:
            # just in case the elem is another simple type - e.g. int - 
            # wrapper it as a string
            return str(elem).strip()
        
    def __call__(self, elem, indent='', html=0, space=' '*4):
        '''Most of the work done in this wrapped function - wrapped so that
        state can be maintained for declared namespace declarations during
        recursive calls using "declaredNss" above
        
        @param elem: ElementTree element
        @type elem: ElementTree.Element
        @param indent: set indent for output
        @type indent: basestring
        @param space: set output spacing
        @type space: basestring 
        @return: pretty print format for doc
        @rtype: basestring       
        '''  
        strAttribs = []
        for attr, attrVal in elem.attrib.items():
            nsDeclaration = ''
            
            attrNamespace = QName.getNs(attr)
            if attrNamespace:
                nsPrefix = self._getNamespacePrefix(elem, attrNamespace)
                
                attr = "%s:%s" % (nsPrefix, QName.getLocalPart(attr))
                
                if attrNamespace not in self.declaredNss:
                    nsDeclaration = ' xmlns:%s="%s"' % (nsPrefix,attrNamespace)
                    self.declaredNss.append(attrNamespace)
                
            strAttribs.append('%s %s="%s"' % (nsDeclaration, attr, attrVal))
            
        strAttrib = ''.join(strAttribs)
        
        namespace = QName.getNs(elem.tag)
        nsPrefix = self._getNamespacePrefix(elem, namespace)
            
        tag = "%s:%s" % (nsPrefix, QName.getLocalPart(elem.tag))
        
        # Put in namespace declaration if one doesn't already exist
        # FIXME: namespace declaration handling is wrong for handling child
        # element scope
        if namespace in self.declaredNss:
            nsDeclaration = ''
        else:
            nsDeclaration = ' xmlns:%s="%s"' % (nsPrefix, namespace)
            self.declaredNss.append(namespace)
            
        result = '%s<%s%s%s>%s' % (indent, tag, nsDeclaration, strAttrib, 
                                   _PrettyPrint.estrip(elem.text))
        
        children = len(elem)
        if children:
            for child in elem:
                declaredNss = self.declaredNss[:]
                _prettyPrint = _PrettyPrint(declaredNss, self.mappedPrefixes)
                result += '\n'+ _prettyPrint(child, indent=indent+space) 
                
            result += '\n%s%s</%s>' % (indent,
                                     _PrettyPrint.estrip(child.tail),
                                     tag)
        else:
            result += '</%s>' % tag
            
        return result

    if Config.use_lxml:
        def _getNamespacePrefix(self, elem, namespace):
            for nsPrefix, ns in elem.nsmap.iteritems():
                if ns == namespace:
                    return nsPrefix
            raise KeyError('prettyPrint: missing namespace "%s" for '
                               'elem.nsmap' % namespace)
    else:
        def _getNamespacePrefix(self, elem, namespace):
            nsPrefix = self._allocNsPrefix(namespace)
            if nsPrefix is None:
                raise KeyError('prettyPrint: missing namespace "%s" for '
                               'ElementTree._namespace_map' % namespace)
            return nsPrefix

        def _allocNsPrefix(self, nsURI):
            """Allocate a namespace prefix if one is not already set for the given
            Namespace URI
            """
            nsPrefix = ElementTree._namespace_map.get(nsURI)
            if nsPrefix is not None:
                return nsPrefix

            for i in range(self.__class__.MAX_NS_TRIES):
                nsPrefix = "ns%d" % i
                if nsPrefix not in self.mappedPrefixes:
                    ElementTree._namespace_map[nsURI] = nsPrefix
                    self.mappedPrefixes[nsPrefix] = True
                    break

            if nsURI not in ElementTree._namespace_map:                            
                raise KeyError('prettyPrint: error adding namespace '
                               '"%s" to ElementTree._namespace_map' % 
                               nsURI)   

            return nsPrefix
