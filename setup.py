from distutils.core import setup

with open('README.md', 'r') as fh:
    long_descrition = fh.read()

setup(
    name='dbprime',
    version='0.1dev',
    author='Dalton Dirkson',
    author_email='sodakdoubled@gmail.com',
    packages=['dbprime',],
)
