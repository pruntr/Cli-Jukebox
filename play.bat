@echo off
:: Get the Python scripts folder path
for /f "tokens=*" %%a in ('python -c "import site; print(site.getsitepackages()[0])"') do set scripts_path=%%a\Scripts
@echo off
python %scripts_path%/src/app.py %*
