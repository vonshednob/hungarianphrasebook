from distutils.core import setup

from hungarianphrasebook import version


with open('README.md', encoding='utf-8') as fd:
    long_description = fd.read()

with open('LICENSE', encoding='utf-8') as fd:
    license = fd.read()


setup(name='hungarianphrasebook',
      version=version.VERSION,
      description="An RFC1751-like implementation",
      long_description=long_description,
      url="https://github.com/vonshednob/hungarianphrasebook",
      author="R",
      author_email="devel+hungarianphrasebook-this-is-spam@kakaomilchkuh.de",
      license=license,
      entry_points={'console_scripts': ['hpb=hungarianphrasebook:run']},
      packages=['hungarianphrasebook'],
      python_requires='>=3',
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3'])
