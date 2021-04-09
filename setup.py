import os.path
from setuptools import setup

REQUIRES_PYTHON = ">=3.9.0"

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md"), encoding="utf-8") as fid:
    README = fid.read()

with open(os.path.join(HERE, "requirements.txt")) as fid:
    REQUIREMENTS = [req for req in fid.read().split("\n") if req]

from mindpile import __version__

setup(
    name="mindpile",
    version=__version__,
    description="Transpiles Mindstorms to ev3dev2 python.",
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires=REQUIRES_PYTHON,
    url="https://github.com/MelbourneHighSchoolRobotics/mindpile",
    author="Angus Trau, Richard Huang, Jackson Goerner, Peter Drew",
    author_email="contact@angus.ws, me@huangrichard.com, jgoerner@outlook.com, peter@pdrew.com",
    license="BSD-3-Clause",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["mindpile"],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "mindpile=mindpile.main:main",
        ]
    },
)
