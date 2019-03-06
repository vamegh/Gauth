#!/usr/bin/env python3

### (c) Vamegh Hedayati LGPL License please read the License file for more info.
from setuptools import setup

setup(
    name='gauth',
    version='0.0.1',
    description='gauth a tool to automate google authenticator, to help with seamless automation',
    author='Vamegh Hedayati',
    author_email='gh_vhedayati@ev9.io',
    url='https://github.com/vamegh',
    include_package_data=True,
    packages=['gauth_libs'],
    scripts=[
        'bin/gauth',
    ],
    package_data={'gauth_libs': ['LICENSE', 'README.md'], },
    data_files=[('/etc/gauth', ['configs/color_map.yaml',
                                'configs/config.yaml',
                                'configs/git_config.yaml',
                                'README.md'])]
)
