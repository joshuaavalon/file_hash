from setuptools import find_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(name="file_hash",
      version="1.0.1",
      author="Joshua Avalon",
      url="https://git.joshuaavalon.io/joshuaavalon/file_hash",
      description="Simple hashing script for files.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      python_requires=">=3.7",
      packages=find_packages(exclude=["tests"]),
      install_requires=["Jinja2==2.10"],
      classifiers=(
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent"
      ),
      include_package_data=True,
      entry_points={
          "console_scripts": ["file_hash = file_hash.__main__:main"]
      },
      project_urls={
          "Bug Tracker": "https://github.com/joshuaavalon/file_hash",
          "Documentation": "https://git.joshuaavalon.io/joshuaavalon/file_hash/blob/master/README.md",
          "Source Code": "https://git.joshuaavalon.io/joshuaavalon/file_hash",
      }
      )
