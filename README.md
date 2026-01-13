# Parking MCP

A parking service with MCP (Model Context Protocol) integration.

## Prerequisites

- Python 3.13 or higher

## Setup

### macOS

1. **Create a virtual environment:**

   ```bash
   python3.13 -m venv env
   ```

2. **Activate the virtual environment:**

   ```bash
   source env/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Deactivate when done:**

   ```bash
   deactivate
   ```

### Windows

1. **Create a virtual environment:**

   ```powershell
   python -m venv env
   ```

   > Note: Make sure `python` points to Python 3.13. You can verify with `python --version`. If you have multiple Python versions installed, you may need to use `py -3.13 -m venv env` instead.

2. **Activate the virtual environment:**

   ```powershell
   .\env\Scripts\Activate.ps1
   ```

   > If you're using Command Prompt instead of PowerShell:
   > ```cmd
   > env\Scripts\activate.bat
   > ```

3. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Deactivate when done:**

   ```powershell
   deactivate
   ```

## Troubleshooting

### PowerShell Execution Policy (Windows)

If you encounter an error about running scripts being disabled, run PowerShell as Administrator and execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
