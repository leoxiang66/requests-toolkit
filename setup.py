from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "lxml==4.9.1",
    'requests==2.28.1',
    "xmltodict==0.13.0"
]

setup(
    name="requests-tutorial",
    version="0.4.1",
    author="Tao Xiang",
    author_email="tao.xiang@tum.de",
    description="A package of APIs using requests.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/requests-toolkit",
    packages=find_packages(),
    # py_modules=['timedd']
    install_requires=requirements,
    classifiers=[
	"Programming Language :: Python :: 3.8",
	"License :: OSI Approved :: MIT License",
    ],
)
