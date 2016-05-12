import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(["--cov", "http_filter", "--pep8"])
        sys.exit(errno)


setup(name='http-filter',
      version='0.1',
      description='',
      url='http://github.com/LuXuryPro/tkom',
      packages=['http_filter'],
      tests_require=['pytest', 'pytest-cov', 'pytest-pep8'],
      cmdclass={'test': PyTest},
      zip_safe=False)
