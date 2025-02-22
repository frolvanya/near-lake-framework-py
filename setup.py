import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="near-lake-framework",
    version="0.1.3",
    author="Ivan Frolov",
    author_email="frolvanya@gmail.com",
    description="Python Library to connect to the NEAR Lake S3 and stream the data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frolvanya/near-lake-framework-py",
    project_urls={
        "Bug Tracker": "https://github.com/frolvanya/near-lake-framework-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "asyncio>=3.4.3",
        "dataclasses>=0.6",
        "dataclasses-json>=0.5.7",
        "aiobotocore>=2.3.0",
        "requests>=2.32.2",
    ],
    package_data={"near_lake_framework": ["py.typed"]},
)
