@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Setup Python venv
if not exist ".venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [!] Failed to create venv. Ensure Python 3.9+ is installed.
        exit /b 1
    )
    echo [*] Installing dependencies...
    call .venv\Scripts\activate.bat
    pip install -q -r requirements.txt
    if errorlevel 1 (
        echo [!] Failed to install dependencies.
        exit /b 1
    )
    echo [+] Venv created and dependencies installed.
) else (
    call .venv\Scripts\activate.bat
)

REM Validate .env file
if not exist ".env" (
    echo.
    echo [!] Missing .env file!
    echo     1. Copy .env.example to .env
    echo     2. Edit .env and set your CLOUD_API_KEY and CLOUD_BASE_URL
    echo     3. See .env.example for Poe, OpenRouter, and custom endpoint examples
    echo.
    pause
    exit /b 1
)

REM Check CLOUD_API_KEY (also accept legacy POE_API_KEY)
set CLOUD_API_KEY=
for /f "tokens=2 delims==" %%A in ('findstr "^CLOUD_API_KEY" .env') do set CLOUD_API_KEY=%%A
if "!CLOUD_API_KEY!"=="" (
    for /f "tokens=2 delims==" %%A in ('findstr "^POE_API_KEY" .env') do set CLOUD_API_KEY=%%A
)
if "!CLOUD_API_KEY!"=="" (
    echo [!] CLOUD_API_KEY not set in .env
    echo     Edit .env and set CLOUD_API_KEY to your provider's API key.
    pause
    exit /b 1
)

echo [+] CLOUD_API_KEY found

REM Check Ollama (optional — only needed if you select Ollama backend during model setup)
where ollama >nul 2>&1
if errorlevel 1 (
    echo [~] Ollama not found. You can still run using Cloud API only.
    echo     To enable local Ollama models: download from https://ollama.ai
) else (
    ollama list >nul 2>&1
    if errorlevel 1 (
        echo [~] Ollama installed but not running. Start it with: ollama serve
        echo     You can still run using Cloud API only.
    ) else (
        echo [+] Ollama is running
    )
)

echo.

REM If args passed directly, skip menu
if not "%1"=="" (
    python -m src.main %*
    exit /b %errorlevel%
)

REM Interactive mode menu
echo ============================================
echo   AutoResearch - AI Research Automation
echo ============================================
echo.
echo   1. Standard     - single research pass
echo   2. Breakthrough - iterative + reformulation + HTML report
echo   3. Batch        - run all problem files from a folder
echo   4. Exit
echo.
set /p MODE_CHOICE="Select mode (1-4): "

if "!MODE_CHOICE!"=="1" goto :standard
if "!MODE_CHOICE!"=="2" goto :breakthrough
if "!MODE_CHOICE!"=="3" goto :batch
if "!MODE_CHOICE!"=="4" exit /b 0
echo [!] Invalid choice. Please enter 1, 2, 3, or 4.
goto :eof

:standard
echo.
set /p PROBLEM_FILE="Problem file (press Enter for problem.md): "
if "!PROBLEM_FILE!"=="" set PROBLEM_FILE=problem.md

echo.
python -m src.main standard --problem "!PROBLEM_FILE!"
exit /b %errorlevel%

:breakthrough
echo.
set /p ITERATIONS="Number of iterations (press Enter for 3): "
if "!ITERATIONS!"=="" set ITERATIONS=3

echo.
set /p PROBLEM_FILE="Problem file (press Enter for problem.md): "
if "!PROBLEM_FILE!"=="" set PROBLEM_FILE=problem.md

echo.
python -m src.main breakthrough --iterations !ITERATIONS! --problem "!PROBLEM_FILE!"
exit /b %errorlevel%

:batch
echo.
set /p BATCH_FOLDER="Folder containing problem files (required): "
if "!BATCH_FOLDER!"=="" (
    echo [!] Folder path is required for batch mode.
    exit /b 1
)

echo.
echo   1. Standard     - single pass per problem
echo   2. Breakthrough - iterative with reformulation
echo.
set /p BATCH_MODE_CHOICE="Research mode (1-2, press Enter for 1): "
if "!BATCH_MODE_CHOICE!"=="" set BATCH_MODE_CHOICE=1
if "!BATCH_MODE_CHOICE!"=="1" set BATCH_MODE=standard
if "!BATCH_MODE_CHOICE!"=="2" set BATCH_MODE=breakthrough
if "!BATCH_MODE_CHOICE!"=="standard" set BATCH_MODE=standard
if "!BATCH_MODE_CHOICE!"=="breakthrough" set BATCH_MODE=breakthrough
if "!BATCH_MODE!"=="" (
    echo [!] Invalid choice.
    exit /b 1
)

if /i "!BATCH_MODE!"=="breakthrough" (
    echo.
    set /p ITERATIONS="Number of iterations (press Enter for 3): "
    if "!ITERATIONS!"=="" set ITERATIONS=3
    echo.
    python -m src.main !BATCH_MODE! --batch "!BATCH_FOLDER!" --iterations !ITERATIONS!
) else (
    echo.
    python -m src.main !BATCH_MODE! --batch "!BATCH_FOLDER!"
)
exit /b %errorlevel%
