@echo off
pip install -r requirements.txt
setlocal EnableDelayedExpansion
REM Get latest Chrome driver URL
set "url=https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
for /f "tokens=* usebackq" %%f in (`curl -L %url%`) do set "latest=%%f"
set "latest_url=https://chromedriver.storage.googleapis.com/%latest%/chromedriver_win32.zip"
REM Download latest Chrome driver
curl -L -o chromedriver.zip %latest_url%
REM Extract and copy to Python scripts directory
powershell -Command "Expand-Archive -Path chromedriver.zip -DestinationPath ."
:: Get the Python scripts folder path
for /f "tokens=*" %%a in ('python -c "import site; print(site.getsitepackages()[0])"') do set scripts_path=%%a\Scripts
:: Copy the ChromeDriver executable to Python scripts folder
copy play.bat "%scripts_path%"
xcopy /s /i ".\src" "%scripts_path%\src"
move chromedriver.exe "%scripts_path%"
:: Cleanup
del chromedriver.zip
del LICENSE.chromedriver
