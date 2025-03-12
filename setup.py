from setuptools import setup, find_packages

setup(
    name="iceberg_codes",
    version="0.1.0",
    description="A quantum error detection library for compiling and decoding quantum circuits with Iceberg codes.",
    author="Tom Ginsberg",
    author_email="tom@beit.tech",
    url="https://github.com/beittech/iceberg.git",
    packages=find_packages(),
    install_requires=[
        "qiskit>=1.4.0",
        "qiskit-aer>=0.16.4",
        "requests",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "iceberg_codes": ["*.py"],
    },
    extras_require={
        "dev": ["jupyter", "matplotlib", "tqdm", "seaborn", "pandas"],
    },
)
