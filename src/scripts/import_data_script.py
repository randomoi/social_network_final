import os
import shutil
import subprocess

# START - code was developed with the help of documentation and other external research, please see referenced links. 

MEDIA_DIR = "media"  # path to media directory
BACKUP_DIR = "exported_data" # path to exported data directory
JSON_FILENAME = "exported_database_dump.json"  # exported JSON name
media_archive = "exported_media_archive" # exported media zip name

# imports data 
def import_database(input_file):
    subprocess.run(["python", "manage.py", "loaddata", input_file])

#  unzips file and imports its content (media: images, video)
def import_media(archive_name=media_archive, extraction_path=MEDIA_DIR):
    shutil.unpack_archive(os.path.join(BACKUP_DIR, archive_name) + '.zip', extraction_path)

# handles confirmation before importing data
def confirm_before_import():
    # displays message to user and asking to select yes or no
    user_response = input("IMPORTANT: Importing files will overwrite existing data. Do you want to continue? (yes/no): ").lower()
    # returns yes
    return user_response == 'yes'

def main():
    # checks with user to confirm before importing data, if they said yes  
    if confirm_before_import():
        # imports database by using "loaddata" from "exported_database_dump.json" located in "exported_data" folder
        import_database(os.path.join(BACKUP_DIR, JSON_FILENAME))
         #  unzips file and imports its content (media: images, video) by using "shutil.unpack_archive"
        import_media()
    else: # if user selected no, import is canceled
        print("Import is canceled.")

if __name__ == "__main__":
    main()

# References: 
# https://docs.python.org/3/library/os.html
# https://docs.python.org/3/library/shutil.html
# https://docs.python.org/3/library/shutil.html#shutil.unpack_archive
# https://docs.python.org/3/library/subprocess.html
# https://docs.python.org/3/library/subprocess.html#subprocess.run
# https://docs.djangoproject.com/en/4.2/ref/django-admin/
# https://docs.djangoproject.com/en/3.2/ref/django-admin/#loaddata
# https://docs.djangoproject.com/en/4.2/topics/files/

# END - code was developed with the help of documentation and other external research, please see referenced links. 