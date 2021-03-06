try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name' : 'pitm',
    'description' : 'A simple HTTP/HTTPS packet intecepter',
    'maintainer' : 'Atmaram Shetye',
    'url' : 'http://localhost/',
    'download_url' : 'http://localhost/',
    'maintainer_email' : 'atmaram.shetye@gmail.com',
    'version' : '0.1',
    'install_requires' : ['nose'],
    'packages' : ['pitm'],
    'scripts' : [],
}

setup(**config)
