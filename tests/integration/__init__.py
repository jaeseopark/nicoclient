import unittest
from abc import ABC

from tests.helper import get_test_scope


@unittest.skipUnless('integration' in get_test_scope(), "Integration")
class IntegrationTest(unittest.TestCase, ABC):
    pass
