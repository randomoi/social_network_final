import subprocess
import shutil
import os

# START - code was developed with the help of documentation and other external research, please see referenced links. 

MEDIA_DIR = "media"  # path to media directory
BACKUP_DIR = "exported_data" # path to exported data directory
JSON_FILENAME = "exported_database_dump.json"  # exported JSON name
media_archive = "exported_media_archive" # exported media zip name

# handles backup/export of entire database
def export_database(output_file):
    subprocess.run(["python", "manage.py", "dumpdata",
                    "auth.User",
                    "social.Post", "social.Friend", "social.Comment",
                    "social.GalleryImageItem", "social.Message", "users.Profile",
                    "--output=" + output_file])

# handles archiving into zip file all media
def export_media(media_path=MEDIA_DIR, archive_name=media_archive):
    shutil.make_archive(archive_name, 'zip', media_path)

# handles confirmation before overwritting existing files
def confirm_before_overwrite(file_path):
    # checks if file exists
    if os.path.exists(file_path):
         # displays message to user and asking to select yes or no
        user_response = input(f"IMPORTANT: '{file_path}' already exists. Do you want to overwrite it? (yes/no): ").lower()
        # if user said no, let them know that export will be cancelled
        if user_response != 'yes':
            print(f"You selected no, so export for '{file_path}' was canceled.")
            return False
    # otherwise, overwritte file (in case the file doesnt exist or if user said yes)
    return True

# executes the above functions
def main():
    # checks if exported directory exists, if it doesnt exisits it will create it
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # paths for exports
    database_export_path = os.path.join(BACKUP_DIR, JSON_FILENAME)
    media_export_path = os.path.join(BACKUP_DIR, media_archive)

    # checks to confirm that "exported_database_dump.json" file overwiting is agreed by user 
    if confirm_before_overwrite(database_export_path):
        # if yes, exports database to "exported_database_dump.json" to "exported_data" folder
        export_database(database_export_path)
    
    # checks to confirm that "exported_media_archive".zip file overwiting is agreed by user 
    if confirm_before_overwrite(media_export_path):
        # if yes, exports "exported_media_archive" in zip format to "exported_data" folder
        export_media(archive_name=os.path.join(BACKUP_DIR, media_archive))

if __name__ == "__main__":
    main()

# # References:
# # https://docs.djangoproject.com/en/4.2/topics/files/
# # https://docs.djangoproject.com/en/4.2/ref/django-admin/#dumpdata
# # https://docs.python.org/3/library/subprocess.html#subprocess.run
# # https://docs.python.org/3/library/shutil.html#shutil.make_archive
# # https://docs.python.org/3/library/__main__.html
# # https://docs.python.org/3/library/os.html
# # https://docs.python.org/3/library/os.path.html#os.path.exists
# # https://docs.python.org/3/library/os.html#os.makedirs

#  END - code was developed with the help of documentation and other external research, please see referenced links. 