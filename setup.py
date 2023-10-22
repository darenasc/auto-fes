from setuptools import find_packages, setup

setup(
    name="afes",
    description="Automated File Exploration System",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version="0.0.1",
    author="Diego Arenas",
    author_email="darenasc@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
