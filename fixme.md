# Step 1: Unblock scripts

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Step 2: Activate venv

.\.venv\Scripts\activate

# Step 3: Silence Matplotlib

$env:MPL_LOGGING_LEVEL='error'

# Step 4: Open a clean window

code .

# extra force:

Set-ExecutionPolicy Bypass -Scope Process

OR

in admin PS
Set-ExecutionPolicy RemoteSigned -Force
Get-ExecutionPolicy -List

# GG
