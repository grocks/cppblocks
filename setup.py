from distutils.core import setup

setup(
    name='CppBlocks',
    version='0.1.0',
    author='Sascha Friedmann',
    author_email='sascha.friedmann@exmaple.com',
    packages=['cppblocks', 'cppblocks.test'],
    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='A C preprocessor parser that evaluates conditional blocks and returns, which parts of a file are excluded from the compilation.',
    long_description=open('README.txt').read(),
    install_requires=[
#       "Django >= 1.1.1",
#       "caldav == 0.1.4",
    ],
)
