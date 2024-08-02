## Install

1. Install dependencies in a pip virtual environment. `pip cache purge` is meant to prevent errors when installing `pynput`.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip cache purge
    pip install pynput matplotlib
    ```

TEST FURTHER - It is unclear yet if installing from requirements.txt will work
pip install -r requirements.txt

1. Run the code:
    ```bash
    python3 main.py
    ```

`ctrl + c` to end script