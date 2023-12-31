from distutils.core import setup

setup(
    name='Amazon_spider',
    version='1.0',
    description='A light and high perforemence spider for Amazon.com',
    author='gogoolu',
    author_email='',
    url='https://github.com/gogoolu/amazon_spider',
    packages=[],
    install_requires=[
        'attrs==23.1.0',
        'certifi==2023.5.7',
        'cffi==1.15.1',
        'charset-normalizer==3.1.0',
        'colorama==0.4.6',
        'exceptiongroup==1.1.1',
        'h11==0.14.0',
        'idna==3.4',
        'outcome==1.2.0',
        'packaging==23.1',
        'pycparser==2.21',
        'PyMySQL==1.1.0',
        'PySocks==1.7.1',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'selenium==4.10.0',
        'sniffio==1.3.0',
        'sortedcontainers==2.4.0',
        'tqdm==4.65.0',
        'trio==0.22.1',
        'trio-websocket==0.10.3',
        'urllib3==2.0.3',
        'webdriver-manager==3.8.6',
        'wsproto==1.2.0',
    ],
)