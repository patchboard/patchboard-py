from setuptools import setup, find_packages

setup(name='patchboard',
      version='0.1.0',
      description='Python client for Patchboard APIs',
      url='http://github.com/patchboard/patchboard-py',
      author='Dustin Laurence',
      author_email='dustin@pandastrike.com',
      license='MIT',
      packages=find_packages(exclude=[
          u'*.tests', u'*.tests.*', u'tests.*', u'tests']),
      install_requires=[
          'pytest', 'requests',
      ],
      zip_safe=False)

