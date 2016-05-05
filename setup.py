import os
import re
from setuptools import setup, find_packages


def read(*parts):
    with open(os.path.join(*parts), 'rt') as f:
        return f.read().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'cantal_tools', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError(
                'Cannot find version in cantal_tools/__init__.py')


install_requires = ['cantal']


classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries',
    ]


setup(name='cantal_tools',
      version=read_version(),
      description=("High level cantal tools"),
      long_description=read('README.rst'),
      classifiers=classifiers,
      platforms=["POSIX"],
      author="Alexey Popravka",
      author_email="alexey.popravka@horsedevel.com",
      url="https://github.com/popravich/cantal_tools",
      license="MIT",
      packages=find_packages(exclude=["tests"]),
      install_requires=install_requires,
      include_package_data=True,
      )
