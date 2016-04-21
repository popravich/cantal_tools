from setuptools import setup, find_packages

install_requires = ['cantal', 'werkzeug']

setup(name='cantal_tools',
      version='0.1.1',
      description=("High level cantal tools"),
      long_description="",
      # long_description="\n\n".join((read('README.rst'),
      #                               read('CHANGES.txt'))),
      classifiers=[],
      platforms=["POSIX"],
      author="Alexey Popravka",
      author_email="a.popravka@smartweb.com.ua",
      url="https://github.com/popravich/cantal_tools",
      license="MIT",
      packages=find_packages(exclude=["tests"]),
      install_requires=install_requires,
      include_package_data=True,
      )
