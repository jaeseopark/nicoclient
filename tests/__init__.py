import os
import unittest
from abc import ABC


def get_root_prefix():
    prefix = ''
    cwd = os.getcwd().split('/')
    while cwd[-1] != 'nico_client':
        cwd = cwd[:-1]
        prefix += '../'
    return prefix


def get_test_scope():
    scope = ['integration', 'unit']
    test_scope = os.getenv('TEST_SCOPE')
    if test_scope is not None:
        scope = [x.strip() for x in test_scope.split(',')]
    return scope


class TestCase(unittest.TestCase, ABC):
    def get_file_content_as_string(self, filename):
        full_path = get_root_prefix() + 'tests/resources/' + filename
        with open(full_path, 'r') as f:
            return f.read()


@unittest.skipUnless('unit' in get_test_scope(), "unit")
class UnitTest(TestCase, ABC):
    pass


@unittest.skipUnless('integration' in get_test_scope(), "Integration")
class IntegrationTest(TestCase, ABC):
    pass
