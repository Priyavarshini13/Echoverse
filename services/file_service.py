import os
from werkzeug.utils import secure_filename

def handle_file_upload(file):
    filename = secure_filename(file.filename)
    path = os.path.join("uploads/files", filename)
    file.save(path)
    return {"status": "success", "path": path}
