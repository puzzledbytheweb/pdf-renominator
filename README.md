# PDF Renominator

This little script renames your PDFs based in its contents, it has the ability to extract text from images so don't worry if your PDFs are just prints of something. 

## Prerequisites
It uses OpenAI API so you'll need to [create an account](https://auth.openai.com/create-account) and pay them 5$ (they stopped their free tier 😔).

You'll also need to have Poppler and Tesseract installed globally:

### Windows
- [Poppler](https://github.com/oschwartz10612/poppler-windows)
- [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki#tesseract-at-ub-mannheim)

### MacOS
```sh
brew install poppler
brew install tesseract
```

### Ubuntu
```sh
sudo apt update
sudo apt install poppler-utils tesseract-ocr
```

## Setup

1. Set up a virtual environment to encapsulate your Python packages, otherwise running the next command installs the dependecies globally:
    ```sh
    python -m venv .venv
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set your OpenAI API key:
    ```sh
    export OPENAI_API_KEY=YOUR_API_KEY
    ```

4. Run the main script:
    ```sh
    python main.py
    ```