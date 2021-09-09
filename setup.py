import os
from pathlib import Path

from setuptools import find_packages, setup

README = Path("README.md").read_text()

setup(name="milkviz",
      packages=find_packages(),
      description="self-opinionated miscellaneous visualizations library in python",
      long_description=README,
      long_description_content_type="text/markdown",
      version="0.2.0",
      author="Mr-Milk",
      url="https://github.com/Mr-Milk/milkviz",
      author_email="yb97643@um.edu.mo",
      license="MIT",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering :: Bio-Informatics",
      ],
      python_requires='>=3.7',
      install_requires=['numpy', 'pandas', 'matplotlib', 'seaborn', 'networkx', 'natsort', 'matplotlib-venn', 'upsetplot'],
      )
