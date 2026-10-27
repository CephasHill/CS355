# CS 355 Labs

Coursework for **CS 355: Computer Graphics and Image Processing**. This repository
contains ten labs covering Python fundamentals, numerical vectorization, image
processing, geometric transformations, interactive graphics, image warping, and
Fourier analysis.

## Lab overview

| Lab | Topic | Format |
| --- | --- | --- |
| [Lab 1](./lab1/Lab1-PythonIntro.ipynb) | Python introduction | Jupyter notebook |
| [Lab 2](./lab2/Lab2-Vectorization-1.ipynb) | Vectorization and level operations | Jupyter notebook |
| [Lab 3](./lab3/Lab3-ImageProcessing.ipynb) | Image processing | Jupyter notebook |
| [Lab 4](./lab4/Lab4-ImageTransformations.ipynb) | Image transformations | Jupyter notebook |
| [Lab 5](./lab5/Lab5-OpenGL.py) | OpenGL fundamentals | Python script |
| [Lab 6](./lab6/Lab6-OpenGL.py) | Interactive OpenGL graphics | Python script |
| [Lab 7](./lab7/lab7.py) | 2D graphics and animation | Python script |
| [Lab 8](./lab8/lab8.py) | 3D wireframe rendering | Python script |
| [Lab 9](./lab9/Lab9-ImageWarping-v3.ipynb) | Image warping | Jupyter notebook |
| [Lab 10](./lab10/Lab10-FourierAnalysis.ipynb) | Fourier analysis and audio | Jupyter notebook |

The images, audio samples, and text data used by each assignment are stored
alongside the corresponding lab.

## Getting started

### 1. Create an environment

Python 3.8 or newer is recommended. From the repository root, create and
activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Run a notebook

Start Jupyter from the repository root:

```powershell
jupyter lab
```

Open any notebook in the lab table and run its cells. Notebook image and audio
inputs use relative paths, so launching Jupyter from this directory is
recommended.

### 3. Run an interactive lab

Run the script from its own lab directory so local helper modules and assets are
resolved correctly:

```powershell
Set-Location lab8
python lab8.py
```

Labs 5–8 open interactive graphics windows and may require a working OpenGL
driver. Lab 10’s audio section may additionally require an available audio
input/output device and operating-system audio support.

## Repository layout

```text
lab1/ ... lab4/   Notebook-based Python and image-processing labs
lab5/ ... lab8/   Interactive OpenGL/Pygame labs
lab9/ ... lab10/  Image-warping and Fourier-analysis labs
finalNotes.docx   Supplemental course notes
requirements.txt  Shared Python dependencies
```

## Notes

- `temp.py` files are retained as part of the original lab working materials.
- Notebook outputs and generated Python caches are not required to be committed;
  the repository ignores newly generated copies of these files.
- The course assignments may have requirements or restrictions beyond the
  runtime dependencies listed here. Follow the instructions in each notebook.
