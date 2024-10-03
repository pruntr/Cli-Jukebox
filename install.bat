@echo off
pip install -r requirements.txt
setlocal EnableDelayedExpansion

REM Get the path to the Python Scripts folder dynamically
for /f "tokens=*" %%a in ('python -c "import site; print(site.getsitepackages()[0])"') do set scriptsPath=%%a\Scripts

REM Specify the URL for the Chrome-for-Testing page
set "website_url=https://googlechromelabs.github.io/chrome-for-testing/#stable"

REM Use curl to get the HTML content of the page and filter the latest stable ChromeDriver version and download URL for win64
for /f "tokens=*" %%i in ('curl -s "%website_url%" ^| findstr /i "Stable"') do (
    echo %%i
    set "html_content=%%i"
)

REM Extract the version number from the HTML content (e.g., 129.0.6668.89)
@REM for /f "tokens=3 delims=>< " %%j in ("!html_content!") do set "version=129.0.6668.89"

REM Construct the download URL for the latest stable ChromeDriver for win64
set "chromedriver_url=https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.89/win64/chromedriver-win64.zip"

REM Download ChromeDriver (win64) using curl
curl -L -o chromedriver.zip !chromedriver_url!

REM Extract the contents of the ZIP file using PowerShell
powershell -Command "Expand-Archive -Path chromedriver.zip -DestinationPath ."

REM Copy the ChromeDriver executable to the dynamically detected Python Scripts folder
copy play.bat "%scriptsPath%\play.bat"
xcopy /s /i ".\src" "%scriptsPath%\src"
move "chromedriver-win64\chromedriver.exe" "%scriptsPath%"

REM Cleanup extracted ZIP file
del chromedriver.zip

REM Cleanup extracted ZIP folder
rmdir /s /q "chromedriver-win64"

echo ChromeDriver version !version! downloaded and moved to: %scriptsPath%
