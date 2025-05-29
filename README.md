# Dunwoody Engineering Tools  

This repository contains Python-based **Marimo** files that power the engineering tools available on [**Dunwoody Engineering**](dunwoodyengineering.com). These tools are designed to assist with bulk materials handling, conveyor design, numerical simulation, Discrete Element Method (DEM) analysis, and Finite Element Analysis (FEA).  

## Features  
- Python **Marimo** notebooks for interactive engineering calculations and simulations  
- Tools for conveyor design, DEM analysis, and FEA modeling  
- Open-source utilities for engineering professionals and researchers  

## Getting Started  
The easiest way to use these tools is to use github pages: [https://pdunwoody.github.io/dunwoody_tools/](https://pdunwoody.github.io/dunwoody_tools/)

To install and run the tools locally either:
1. Install VS Code and Docker.
2. Clone the repository. In a terminal, run

```bash
git clone https://github.com/pdunwoody/dunwoody_tools.git dunwoody_tools
```
3. Open the cloned repo in VS Code.

```bash
cd dunwoody_tools
code ./
```

6. It _should_ detect the Dev Container configuration file and prompt you to reopen the folder to develop in the container. Do this and it will create and open the tools folder in a Docker container with all the requirements automatically installed.

7. Click on the Marimo extension and then run or edit any of the notebooks listed to use that tool.

Alternatively, you can install Marimo locally.

1. Install Marimo. In a terminal, run

```bash
pip install marimo
```

2. Clone this repository and cd into its directory

```bash
git clone https://github.com/pdunwoody/dunwoody_tools.git dunwoody_tools
cd dunwoody_tools
code ./
```

3. Install the required packages

```bash
pip install .
```

4. Run the tool you want. For example:

```bash
marimo run apps/lifting_lug_check.py
```
