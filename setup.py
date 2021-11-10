from setuptools import setup

scripts = ['bin/giga-analysis']

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='giga',
      version='0.0.1',
      description='Internet models for Giga',
      url='https://www.actualhq.com/',
      author='Actual',
      author_email='hello@actualhq.com',
      license='Apache License 2.0',
      packages=['giga'],
      install_requires=install_requires,
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False,
      scripts=scripts,
      )
