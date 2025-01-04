import uuid
from fastapi import File, UploadFile
import os
import shutil

class ImageStorage():

    def get_image():
        return

    def save_scan(file: UploadFile = File(...)):
        unique_id = str(uuid.uuid4())  # Generate a UUID
        file_extension = file.filename.split(".")[-1]  # Extract the file extension
        unique_filename = f"{unique_id}.{file_extension}"  # Combine UUID with file extension
        
        # Define the directory and file path
        upload_directory = "./uploaded_files/scan/"
        file_location = f"{upload_directory}{unique_filename}"

        # Ensure the directory exists
        os.makedirs(upload_directory, exist_ok=True)

        # Save the uploaded file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return unique_filename