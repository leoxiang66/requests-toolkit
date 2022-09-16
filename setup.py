from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["lxml",'requests'] # 这里填依赖包信息

setup(
    name="requests-tutorial",
    version="2.0.0",
    author="Tao Xiang",
    author_email="tao.xiang@tum.de",
    description="A package of APIs",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/requests-tutorial",
    packages=find_packages(),
    # Single module也可以：
    # py_modules=['timedd']
    install_requires=requirements,
    classifiers=[
	"Programming Language :: Python :: 3.8",
	"License :: OSI Approved :: MIT License",
    ],
)