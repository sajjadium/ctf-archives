import os

from celery_config import celery_app

from src.anonymize_faces import anonymize_faces

@celery_app.task
def process_image(temp_path, new_file_path, encrypted_exif):
    anonymize_faces(temp_path, 'data/msfrog.png', new_file_path, encrypted_exif)
    os.unlink(temp_path)

def clear_uploads_folder():
    print("Deleting files in /app/uploads")
    uploads_dir = '/app/uploads'
    for file in os.listdir(uploads_dir):
        file_path = os.path.join(uploads_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")