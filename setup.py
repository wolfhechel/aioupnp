from setuptools import setup

from aioupnp import __version__

setup(
    name='aioupnp',
    version=__version__,
    description='UPnP library for Python 3.5 using asyncio',
    keywords='upnp ssdp asyncio gena',
    url='https://github.com/wolfhechel/aioupnp',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Topic :: System :: Networking'
    ],
    license='MIT',
    author='Pontus Karlsson',
    author_email='pontus@jensenkarlsson.se',
    packages=[
        'aioupnp'
    ],
    install_requires=[
    ],
    setup_requires=[
        'pytest-runner',
        'sphinx',
        'flake8'
    ],
    tests_require=[
        'pytest',
        'pytest-describe',
        'pytest-cov',
        'lxml'
    ],
)
