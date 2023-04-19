# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = "2023.0.1"

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('LICENSE', encoding='utf-8') as f:
    license = f.read()

setup(
    name='arrendatools.modelo303',
    version=__version__,
    description='Módulo de Python que genera un string para la importación de datos en el modelo 303 de la Agencia Tributaria de España (PRE 303 - Servicio ayuda modelo 303)',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/hokus15/ArrendaToolsModelo303',
    author='hokus15',
    author_email='hokus@hotmail.com',
    packages=find_packages(exclude=('tests', '.vscode', '.github')),
    license=license,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
