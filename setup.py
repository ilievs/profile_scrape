import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='profile-scrape',
    version='1.0',
    author='Slavey Iliev',
    description="A package for scraping, browsing and analyzing a dating website's profiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilievss/profile-scrape",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'requests-futures',
        'bs4',
        'Flask',
        'mysql-connector-python>=8.0.15',
        'SQLAlchemy>=1.3.5'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
