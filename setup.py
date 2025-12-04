from setuptools import setup, find_packages

setup(
    name="systemicrisksimulator",
    version="0.1.0",
    description="一个金融系统的系统性风险模拟器。 A systemic risk simulator for financial systems.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ethan Lin",
    author_email="ElementsSystem@hunnu.edu.cn",
    url="https://gitee.com/EthanLingo/SystemicRiskSimulator",
    packages=find_packages(where="SystemicRiskSimulator"),
    package_dir={"": "SystemicRiskSimulator"},
    include_package_data=True,
    exclude_package_data={
        "": ["data/**/*"]
    },
    python_requires=">=3.11",
    install_requires=[
        "chardet==5.2.0",
        "drawsvg==2.4.0",
        "gymnasium>=1.1.1",
        "matplotlib==3.10.0",
        "networkx==3.4.2",
        "numpy==2.2.1",
        "openpyxl==3.1.5",
        "pandas==2.2.3",
        "pillow==11.1.0",
        "pip>=25.1",
        "pymupdf==1.25.3",
        "reportlab==4.2.5",
        "rpy2==3.5.17",
        "scipy==1.15.1",
        "screeninfo==0.8.1",
        "setuptools>=80.0.1",
    ],
    license="GNU AGPLv3",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "systemicrisksimulator=SystemicRiskSimulator.simulator:simulator",
        ],
    },
)
