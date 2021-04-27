from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as req:
    requirements = req.read().splitlines()

setup(
    name="pyWhapBot",  # Replace with your own username
    version="1.0.0",
    author="saizk",
    author_email="sergioaizcorbe@hotmail.com",
    description="WhatsApp Web API Wrapper for Chrome, Firefox, Opera, Brave and Edge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saizk/pyWhapBot",
    project_urls={
        "Bug Tracker": "https://github.com/saizk/pyWhapBot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    package_dir={"": "pywhapbot"},
    packages=find_packages(where="pywhapbot"),
    python_requires=">=3.6",
)
