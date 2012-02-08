"""XPath selection for XACML AttributeSelector
"""
__author__ = "R B Wilkinson"
__date__ = "23/12/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"

from abc import ABCMeta, abstractmethod

from ndg.xacml import Config, importElementTree
ElementTree = importElementTree()

class XPathSelectorInterface(object):
    """Interface for XPath selectors.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, contextElem):
        """
        @type contextElem: type of an XML element appropriate to implementation
        @param contextElem: context element on which searches are based
        """
        pass

    @abstractmethod
    def selectText(self, path):
        """Performs an XPath search and returns text content of matched
        elements.
        @type path: str
        @param path: XPath path expression
        @rtype: list of basestr
        @return: text from selected elements
        """
        pass

class EtreeXPathSelector(XPathSelectorInterface):
    """XPathSelectorInterface using ElementTree XPath selection.
    """
    def __init__(self, contextElem):
        """
        @type contextElem: ElementTree.Element
        @param contextElem: context element on which searches are based
        """
        if not ElementTree.iselement(contextElem):
            raise TypeError("Expecting %r input type for parsing; got %r" %
                            (ElementTree.Element, contextElem))
        self.contextElem = contextElem

    if Config.use_lxml:
        def selectText(self, path):
            """Performs an XPath search and returns text content of matched
            elements.
            @type path: str
            @param path: XPath path expression
            @rtype: list of basestring
            @return: text from selected elements
            """
            # ElementTree XPath doesn't support absolute paths. Make it relative
            # to context element.
            if path.startswith('/'):
                relPath = '.' + path
            else:
                relPath = path
            find = ElementTree.ETXPath(relPath)
            elems = find(self.contextElem)
            returnList = []
            for m in elems:
                # Allow for XPath expression selecting element text or attribute
                # values.
                if hasattr(m, 'text'):
                    returnList.append(m.text)
                else:
                    returnList.append(m.__str__())
            return returnList
    else:
        def selectText(self, path):
            """Performs an XPath search and returns text content of matched
            elements.
            @type path: str
            @param path: XPath path expression
            @rtype: list of basestring
            @return: text from selected elements
            """
            # ElementTree XPath doesn't support absolute paths. Make it relative
            # to context element.
            if path.startswith('/'):
                relPath = '.' + path
            else:
                relPath = path
            elems = self.contextElem.findall(relPath)
            return [e.text for e in elems]
