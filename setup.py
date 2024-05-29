import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="near-lake-framework",
    version="0.0.9",
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
        "dataclasses-json>=0.6.6",
        "botocore>=1.34.70",
        "aiobotocore>=2.13.0",
        "requests>=2.32.2",
        "types-botocore>=1.0.2",
        "types-aiobotocore>=2.13.0",
        "types-requests>=2.32.0.20240523",
    ],
    package_data={"near_lake_framework": ["py.typed"]},
)
