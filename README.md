# AutoPressPDF

Optimize, split, and auto-fix your PDFs effortlessly with AutoPressPDF—the smart CLI tool for navigating size restrictions without sacrificing quality.

## Overview

AutoPressPDF is a command-line tool designed to optimize, split, and auto-fix large PDF files, ensuring they meet size restrictions without compromising quality. Built on Python 3.10, AutoPressPDF is designed for modern systems and can be easily integrated into web apps.

## Features

- **Optimize**: Use GhostScript to significantly reduce PDF size while maintaining good quality.
- **Split**: Manually split PDFs into smaller parts, each under a specified size limit.
- **Autofix**: Smartly optimize and split PDFs to make them fit under size limits in the least intrusive manner.

## Quick Start

```bash
# Optimize a PDF file
autopresspdf optimize --input input.pdf --output optimized.pdf

# Split a PDF file
autopresspdf split --input input.pdf --output-dir splits/ --max-size 10

# Auto-fix a PDF file
autopresspdf autofix --input input.pdf --output-dir autofix/ --max-size 10
```


## Installation

pip install autopresspdf


## Dependencies

### GhostScript

AutoPressPDF uses GhostScript for PDF optimization. It assumes that GhostScript is installed on your local machine and can be invoked using the gs command.

To install GhostScript, please follow the installation instructions for your specific operating system:

    * macOS: `brew install ghostscript`
    * Linux: Use your distribution's package manager, for example `sudo apt-get install ghostscript`
    * Windows: Download and install from GhostScript Official Website

Once installed, you can test if GhostScript is available by running:

```bash

gs --version

```

This should return the installed version of GhostScript, confirming it's correctly installed and accessible.
