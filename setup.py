import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='tkpy',
    version='0.0.1',
    description='Travian: Kingdom utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/didadadida93/tkpy',
    author='https://github.com/didadadida93',
    author_email='didadadida93@gmail.com',
    packages=setuptols.find_packages(
        exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']
    ),
    classifier=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT',
    ],
)
