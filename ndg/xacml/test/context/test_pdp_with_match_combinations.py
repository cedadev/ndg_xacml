'''
Created on 26 Aug 2011

@author: rwilkinson
'''
import logging
import unittest

from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import XACML_SUBJECTMATCH_FILEPATH
from ndg.xacml.test.context import XacmlContextBaseTestCase


logging.basicConfig(level=logging.DEBUG)

class Test(XacmlContextBaseTestCase):

    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'

    RESOURCE_ID = 'http://localhost/role-combinations'

    def setUp(self):
        self.pdp = PDP.fromPolicySource(XACML_SUBJECTMATCH_FILEPATH, ReaderFactory)


    # There is a single permit rule for which the subject must have:
    # role1, role2 and role3
    # or role4
    # or role5 and role6.

    def test01_01RoleCombination1(self):
        # All roles of first combination should result in permit decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role1', 'role2', 'role3'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test01_02RoleCombination1(self):
        # Any role missing from first combination should result in deny
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role1', 'role2'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test01_03RoleCombination1(self):
        # Any role missing from first combination should result in deny
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role1', 'role3'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test01_04RoleCombination1(self):
        # Any role missing from first combination should result in deny
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role2', 'role3'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test01_05RoleCombination1(self):
        # Any roles missing from first combination should result in deny
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role1',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test01_06RoleCombination1(self):
        # Any roles missing from first combination should result in deny
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role2',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test01_07RoleCombination1(self):
        # Any roles missing from first combination should result in deny
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role3',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")
    def test01_08RoleCombination1(self):
        # All roles of first combination plus another should result in permit
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role1', 'role2', 'role3', 'role5'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")


    def test02_01RoleCombination1(self):
        # The role in the second combination should result in permit
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role4',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test02_02RoleCombination1(self):
        # The role in the second combination plus another should result in
        # permit decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role2', 'role4'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")


    def test03_01RoleCombination3(self):
        # All roles of third combination should result in permit decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role5', 'role6'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test03_02RoleCombination3(self):
        # All roles of third combination plus others should result in permit
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role2', 'role3', 'role5', 'role6'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")

    def test03_03RoleCombination3(self):
        # Any role missing from third combination should result in deny
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role1', 'role3', 'role5'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")

    def test03_04RoleCombination3(self):
        # Any role missing from third combination should result in deny
        # decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role1', 'role3', 'role6'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY,
                        "Expecting Deny decision")


    def test04_01RoleAllCombinations(self):
        # All roles for all combinations should result in permit decision.
        request = self._createRequestCtx(
                            self.__class__.RESOURCE_ID,
                            subjectRoles=('role1', 'role2', 'role3', 'role4', 'role5', 'role6'))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT,
                        "Expecting Permit decision")


if __name__ == "__main__":
    unittest.main()
