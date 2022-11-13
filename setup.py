# -*- coding: utf-8 -*-
"""Installer for the collective.netopia package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.netopia',
    version='1.0a1',
    description="Netopia Payments for Plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='Alin Voinea',
    author_email='contact@avoinea.com',
    url='https://github.com/collective/collective.netopia',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.netopia',
        'Source': 'https://github.com/collective/collective.netopia',
        'Tracker': 'https://github.com/collective/collective.netopia/issues',
        # 'Documentation': 'https://collective.netopia.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        'setuptools',
        'pycryptodome',
        'pyopenssl',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.netopia.locales.update:update_locale
    """,
)
