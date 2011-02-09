"""NDG XACML Policy Information Point interface definition

"""
__author__ = "P J Kershaw"
__date__ = "15/07/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id:$"
from abc import ABCMeta, abstractmethod


class PIPInterface(object):
    """Interface class for XACML Policy Information Point.  The PDP can relay 
    attribute queries back via the Context handler to the PIP in order to help
    it in making an access control decision
    """
    __metaclass__ = ABCMeta
    __slots__ = ()
    
    @abstractmethod
    def attributeQuery(self, context, attributeDesignator):
        """Query this PIP for attributes"""
        return []