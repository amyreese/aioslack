from setuptools import setup

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requires = [line.strip() for line in f if line]

with open("aioslack/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split('"')[1]

setup(
    name="aioslack",
    description="asyncio slack api",
    long_description=readme,
    long_description_content_type="text/markdown",
    version=version,
    author="John Reese",
    author_email="john@noswap.com",
    url="https://github.com/jreese/aioslack",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
    packages=["aioslack"],
    setup_requires=["setuptools>=38.6.0"],
    install_requires=requires,
)
