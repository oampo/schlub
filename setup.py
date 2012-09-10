from distutils.core import setup

setup(
    name='Schlub',
    version='0.1',
    author='Joe Turner',
    author_email='joe@oampo.co.uk',
    packages=['schlub', 'schlub.test'],
    scripts=['bin/schlub'],
    license='LICENSE.txt',
    description='A crappy static website generator',
    long_description=open('README.md').read(),
    install_requires=[
        "pystache >= 0.5.2"
    ]
)
