from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="emailev",
    version="1.0.0",
    author="Ibrahem abo kila",
    author_email="ibrahemabokila@gmail.com",
    description="Advanced Email Enumeration & Validation Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hemaabokila/email-enumeration-validation",
    packages=find_packages(),
    install_requires=[
        "dnspython",
        "PyHunter",
        "stem",
        "PySocks",
        "aiohttp",
        "colorama",
        "pyfiglet",
    ],
    entry_points={
        "console_scripts": [
            "emailev=emailev_tool.main:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)