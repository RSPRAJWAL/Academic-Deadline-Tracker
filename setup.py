"""
Setup script for the Academic Deadline Tracker.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="academic-deadline-tracker",
    version="1.0.0",
    author="Academic Deadline Tracker Team",
    author_email="example@example.com",
    description="A simple desktop application for tracking academic deadlines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/academic-deadline-tracker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "academic-deadline-tracker=main:main",
        ],
    },
)