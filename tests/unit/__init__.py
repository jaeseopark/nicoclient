import unittest
from abc import ABC

from tests.helper import get_test_scope


@unittest.skipUnless('unit' in get_test_scope(), "unit")
class UnitTest(unittest.TestCase, ABC):
    pass
