import setuptools

import tkpy


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name=tkpy.__name__,
    version=tkpy.__version__,
    description=tkpy.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/didadadida93/tkpy',
    author=tkpy.__author__,
    author_email=tkpy.__author_email__,
    packages=['tkpy'],
    include_package_data=True,
    package_data={
        '': ['schema.sql',],
    },
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': ['tkpy-init=tkpy.database:init_db'],
    },
    license=tkpy.__license__,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
)
