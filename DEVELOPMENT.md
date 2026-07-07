# DEVELOPMENT.md

This document contains a few notes that may help while running, debugging, or contributing to **Aristeia Academy** on Windows.

---

# 1. Clone the repository

```bash
git clone <repository-url>
cd Aristeia-Academy
```

---

# 2. Create a virtual environment

```powershell
python -m venv .venv
```

---

# 3. Allow PowerShell scripts for the current session

If virtual environments refuse to activate:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

If that still doesn't work:

```powershell
Set-ExecutionPolicy Bypass -Scope Process
```

As a last resort (Administrator PowerShell):

```powershell
Set-ExecutionPolicy RemoteSigned -Force
Get-ExecutionPolicy -List
```

---

# 4. Activate the virtual environment

```powershell
.\.venv\Scripts\activate
```

---

# 5. Install dependencies

Install the required Python packages.

```powershell
pip install PySide6
pip install matplotlib
pip install mysql-connector-python
```

If a `requirements.txt` file exists, you can install everything at once instead:

```powershell
pip install -r requirements.txt
```

---

# 6. Reduce Matplotlib console noise (Optional)

Suppresses unnecessary Matplotlib logging while developing.

```powershell
$env:MPL_LOGGING_LEVEL='error'
```

---

# 7. Open the project in Visual Studio Code (Optional)

```powershell
code .
```

---

# 8. Launch Aristeia Academy

Start the application by running:

```powershell
python main.py
```

---

# Troubleshooting

### Virtual environment won't activate

- Verify the PowerShell execution policy.
- Confirm the `.venv` folder exists.
- Recreate the virtual environment if necessary.

---

### Missing Python packages

Install the dependencies again.

```powershell
pip install -r requirements.txt
```

or install them individually using `pip`.

---

### MySQL connection errors

- Ensure the MySQL server is running.
- Verify the database credentials in `database.py`.
- Confirm that `mysql-connector-python` is installed.
- Make sure the required database has been created before launching the application.

---

### PySide6 import errors

Activate the virtual environment before installing packages or running the application.

---

### Matplotlib warnings

Most warnings are harmless during development. The logging command above suppresses common non-critical messages.

---

### Application doesn't start

Run the project from the repository root:

```powershell
python main.py
```

Read any terminal output carefully. Python usually reports exactly what went wrong.

---

If something still refuses to cooperate, don't panic. Most startup issues come down to one of the following:

- Missing Python dependencies
- An inactive virtual environment
- Incorrect MySQL configuration
- Running the application from the wrong directory

Checking those first solves the majority of development issues.
