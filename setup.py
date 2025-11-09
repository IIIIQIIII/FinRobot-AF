"""
Setup configuration for FinRobot Agent Framework edition.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="finrobot-af",
    version="2.0.0",
    author="AI4Finance Foundation",
    author_email="contact@ai4finance.org",
    description="Multi-Agent Framework for Financial Analysis (Agent Framework Edition)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AI4Finance-Foundation/FinRobot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        # Agent Framework (install from local source)
        # "agent-framework-core",  # Installed separately

        # LLM providers
        "openai>=1.0.0",

        # Financial libraries
        "finnhub-python",
        "yfinance",
        "mplfinance",
        "backtrader",
        "sec_api",

        # Data handling
        "numpy>=1.26.4",
        "pandas>=2.0.3",
        "pyPDF2",
        "reportlab",

        # Historical data
        "praw",
        "tushare",
        "pandas_datareader",

        # PDF and document processing
        "pdfkit==1.0.0",
        "marker-pdf",

        # NLP and AI utilities
        "langchain>=0.1.20",
        "nltk>=3.8.1",
        "huggingface_hub",

        # Utilities
        "aiohttp>=3.8.5",
        "ratelimit>=2.2.1",
        "requests>=2.31.0",
        "scikit-learn>=1.5.0",
        "starlette>=0.37.2",
        "tenacity>=8.3.0",
        "tqdm>=4.66.1",
        "typing-extensions>=4.9.0",
        "unstructured>=0.8.1",

        # Visualization
        "matplotlib",

        # Vector store for RAG
        "chromadb",
        "sentence-transformers",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "jupyter": [
            "ipython",
            "jupyter",
            "notebook",
            "ipywidgets",
        ],
    },
    entry_points={
        "console_scripts": [
            "finrobot=finrobot.cli:main",  # Future CLI interface
        ],
    },
    include_package_data=True,
    package_data={
        "finrobot": [
            "data_source/**/*",
            "functional/**/*",
            "agents/**/*",
        ],
    },
    zip_safe=False,
)
