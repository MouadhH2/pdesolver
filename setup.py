from setuptools import setup, find_packages

setup(
    name="pdesolver",
    version="0.1.0",
    description="2D heat equation solver using sparse linear algebra",
    author="Hamdouni",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.26",
        "scipy>=1.11",
        "matplotlib>=3.8",
        "pillow>=10.0",
        "pytest>=8.0",
    ],
)
