# BMEG Python UDC — Motion Analysis

A Python application that loads 3D motion-capture data from an Excel file and computes gait biomechanics: walking speed, knee angles, ankle angles, and head/neck angles over time. Results are plotted visually.

## Requirements

- **Python 3.9+** (tested on 3.9; works on 3.10–3.12 as well)
- The Excel data file: `motiondata.xlsx` (included in this folder)

## Quick Start (Windows & macOS)

### 1. Open a terminal

- **Windows**: PowerShell or Command Prompt
- **macOS**: Terminal.app

### 2. Get the project

**Option A — Clone from GitHub:**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

> Replace `YOUR_USERNAME/YOUR_REPO` with the actual GitHub repository path.

**Option B — If you already have the files locally:**

```bash
cd "BMEG Python UDC"
```

### 3. Create a virtual environment

**Windows (PowerShell / CMD):**
```bash
python -m venv .venv
```

**macOS:**
```bash
python3 -m venv .venv
```

> If `python` / `python3` is not found, install Python from [python.org](https://www.python.org/downloads/). Make sure to check **"Add Python to PATH"** during installation on Windows.

### 4. Activate the virtual environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

*If PowerShell complains about execution policy, run this first:*
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS:**
```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the app

```bash
python main.py
```

A plot window will open showing angle profiles over time. Close the window to exit.

## What the app does

| Metric | Description |
|---|---|
| **Walking speed** | Computed from the torso marker's start-to-end displacement over total time |
| **Right/Left Knee Angle** | Angle at the knee joint using hip, knee, and ankle markers |
| **Right/Left Ankle Angle** | Angle at the ankle joint using knee, ankle, and foot markers |
| **Head/Neck Angle** | Angle between head, neck, and torso markers |

All angles are displayed as a time-series plot in degrees vs. seconds.

## Data file

The Excel file `motiondata.xlsx` contains motion-capture marker coordinates (X, Y, Z) across time frames. The app reads sheet `S2` by default. To change the sheet, edit `sheet_name = 'S2'` in `main.py`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` not found | Install Python from [python.org](https://www.python.org/downloads/) |
| `pip` not found | Run `python -m pip install --upgrade pip` |
| `motiondata.xlsx` not found | Make sure the Excel file is in the same folder as `main.py` |
| Plot window doesn't appear | Try adding `import matplotlib; matplotlib.use('TkAgg')` at the top of `main.py` |
| `No module named 'pandas'` | Run `pip install -r requirements.txt` inside your activated venv |
