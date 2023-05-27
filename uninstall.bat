:: Get the Python scripts folder path
for /f "tokens=*" %%a in ('python -c "import site; print(site.getsitepackages()[0])"') do set scripts_path=%%a\Scripts
:: remove the dependencies
rmdir /s /q %scripts_path%\\src\\
del %scripts_path%\\chromedriver.exe
del %scripts_path%\\play.bat
