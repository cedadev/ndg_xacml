"""NDG XACML Action type definition 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "16/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from ndg.xacml.core import TargetChildBase
from ndg.xacml.core.match import ActionMatch


class Action(TargetChildBase):
    """XACML Action Target Policy element
    
    @cvar MATCH_TYPE: Sets the type for match attributes in this 
    TargetChildBase derived class
    implementation e.g. ResourceMatch, SubjectMatch etc.
    @type MATCH_TYPE: ndg.xacml.core.match.ActionMatch
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    """
    MATCH_TYPE = ActionMatch
    ELEMENT_LOCAL_NAME = 'Action'
    ID = "urn:oasis:names:tc:xacml:1.0:action:action-id"
    __slots__ = ()
    
    @property
    def actionMatches(self):
        """Convenience wrapper to base class method
        @return: list of matches
        @rtype: ndg.xacml.utils.TypedList 
        """
        return self.matches
