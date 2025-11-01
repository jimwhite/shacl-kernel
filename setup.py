"""Setup script for SHACL kernel."""

from setuptools import setup, find_packages
import os

# Read the README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='shacl-kernel',
    version='1.0.0',
    description='A Jupyter kernel for SHACL (Shapes Constraint Language)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SHACL Kernel Contributors',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'ipykernel>=6.0.0',
        'rdflib>=6.0.0',
        'pyshacl>=0.20.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'install-shacl-kernel = shacl_kernel.install:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System :: Shells',
    ],
    python_requires='>=3.8',
)
