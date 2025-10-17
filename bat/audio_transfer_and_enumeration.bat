@echo off

call C:\Users\Asus\Desktop\GitHub\My-Script-Collection\py\.venv\Scripts\activate.bat
cd /d C:\Users\Asus\Desktop\GitHub\My-Script-Collection\py
py transfer_audio_to_cloud.py

call C:\Users\Asus\Desktop\GitHub\My-Script-Collection\py\.venv\Scripts\activate.bat
cd /d "C:\Users\Asus\Proton Drive\hans.rudi.giger\My files\FL Studio Tracks"
py C:\Users\Asus\Desktop\GitHub\My-Script-Collection\py\enumerate_all_files_here_plus_in_subdirs.py

pause
