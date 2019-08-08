import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


about = {}
with open('tkpy/__attrs__.py') as f:
    exec(f.read(), about)


setuptools.setup(
    name=about['__name__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/didadadida93/tkpy',
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=['tkpy'],
    include_package_data=True,
    package_data={
        '': ['schema.sql',],
    },
    install_requires=[
        'requests',
        'primordial @ git+https://github.com/lijok/primordial.git@master',
    ],
    license=about['__license__'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
)
