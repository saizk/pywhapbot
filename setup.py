from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pywhapbot",
    version="1.1",
    author="saizk",
    author_email="sergioaizcorbe@hotmail.com",
    description="WhatsApp Web API Wrapper for Chrome, Firefox, Opera, Brave and Edge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saizk/pywhapbot",
    project_urls={
        "Bug Tracker": "https://github.com/saizk/pywhapbot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['auto-selenium>=1.0.0'],
    package_dir={".": ""},
    packages=["pywhapbot"],
    include_package_data=True,
    python_requires=">=3.6",
)
