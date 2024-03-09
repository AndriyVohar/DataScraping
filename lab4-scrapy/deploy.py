from setuptools import setup, find_packages
setup(
    name="lab2",
entry_points={'scrapy': ['settings = lab2.settings']},
    version="1.0.1",
    packages=find_packages(),
)