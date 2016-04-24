from setuptools import setup, find_packages

setup(
    name='CRIcrawler',
    version='1.0',
    description='CRI audio crawler.',
    author='Qian Peili',
    author_email='qianperry@outlook.com',
    license='MIT',
    packages=find_packages(),
    py_modules=['CRIcrawler'],
    install_requires=['beautifulsoup4>=4.4.1'],
    entry_points={
        "console_scripts": [
            "CRIcrawler=CRIcrawler:main"
        ]},
)
