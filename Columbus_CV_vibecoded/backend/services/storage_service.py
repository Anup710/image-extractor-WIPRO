import os
import shutil
from typing import Optional
from datetime import datetime
from fastapi import UploadFile

class StorageService:
    def __init__(self):
        self.upload_dir = "backend/uploads"
        self.ensure_upload_directory()

    def ensure_upload_directory(self):
        """Ensure the upload directory exists"""
        os.makedirs(self.upload_dir, exist_ok=True)

    async def store_file(self, file: UploadFile, session_id: str) -> str:
        """
        Store uploaded file with user consent
        Returns the file path where the file is stored
        """
        try:
            # Create session directory
            session_dir = os.path.join(self.upload_dir, session_id)
            os.makedirs(session_dir, exist_ok=True)

            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(session_dir, filename)

            # Save file
            with open(file_path, "wb") as buffer:
                file.file.seek(0)  # Reset file pointer
                shutil.copyfileobj(file.file, buffer)

            return file_path

        except Exception as e:
            raise Exception(f"File storage error: {str(e)}")

    def get_stored_files(self, session_id: str) -> list:
        """Get list of stored files for a session"""
        session_dir = os.path.join(self.upload_dir, session_id)
        if not os.path.exists(session_dir):
            return []

        files = []
        for filename in os.listdir(session_dir):
            file_path = os.path.join(session_dir, filename)
            if os.path.isfile(file_path):
                files.append({
                    "filename": filename,
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "created": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                })

        return files

    def delete_session_files(self, session_id: str) -> bool:
        """Delete all files for a session"""
        session_dir = os.path.join(self.upload_dir, session_id)
        if os.path.exists(session_dir):
            try:
                shutil.rmtree(session_dir)
                return True
            except Exception:
                return False
        return False

    def cleanup_old_files(self, days_old: int = 30):
        """Clean up files older than specified days (for future caching implementation)"""
        # Placeholder for future implementation
        # This would be used to clean up old stored files periodically
        pass