# w+m1

A program that collects keyboard and mouse presses for frequency analysis.

w+m1 runs in the background, so it can be active while you are using any application on your computer. After you end the monitoring session, the session data is saved to a file on your computer. You can use w+m1 to automatically generate a graph of the session data file.

## Install

*Some installation steps may vary between different devices and operating systems.*

Installing and using this program requires using your computer's terminal. To run a command in the terminal, have the terminal window active, type or paste the command, and press enter.

If a command starting with `python` doesn't work, try starting the command with `python3` instead.

1. Open a new terminal window. On Mac, open the Terminal application. On Windows, open PowerShell or Command Prompt.
1. Check if you have Python installed. Run the command:
    ```bash
    python --version
    ```
    If you see you a version number, you have Python installed. If you get an error, you need to [install Python](https://www.python.org/downloads/).
1. Check if you have Git installed. Run:
    ```bash
    git version
    ```
    If you see a version number, you have Git installed. If you get an error, you need to [install Git](https://git-scm.com/downloads).
1. Download w+m1 with Git. Run:
    ```bash
    git clone https://github.com/zgstumpf/w-plus-m1.git "w+m1"
    ```
1. Change directories (cd) or "go inside" w+m1. Run:
   ```bash
   cd w+m1
   ```
1. Run the following commands in the order they appear:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip cache purge
    pip install pynput matplotlib
    ```
    *For advanced Python users: w+m1 requires the pynput Python package. pynput uses C extensions, which makes it more vulnerable to installation errors and segmentation faults. Usually, installing pynput with pip works for the first time, but installing it again may result in an error. `pip cache purge` is meant to prevent any installation errors. For more specific package information, view the requirements.txt file.*

**w+m1 is now installed and ready for use.**

*Note: If you move the w+m1 folder to a different location on your computer, you will need to `cd` to that location every time you want to use w+m1. If you are not familiar with terminal commands, do not move the w+m1 folder.*

## Use

Start a monitoring session. Run:
```bash
python startsession.py
```
You will be prompted to name the session.

<br>

View a graph of a session data file. Run:
```bash
python graph.py
```
You will see a list of session data files, and you will be prompted to enter the name of the file you want to analyze.

<hr>

<p align="center">Built in 2024 with Python.</p>