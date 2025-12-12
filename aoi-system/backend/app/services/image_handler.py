import cv2, base64, uuid, os
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff"}
class ImageHandler:
    @staticmethod
    def allowed_file(f): return "." in f and f.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    @staticmethod
    def save_uploaded_image(file, folder):
        if not ImageHandler.allowed_file(file.filename): raise ValueError("Bad type")
        id = str(uuid.uuid4()); ext = file.filename.rsplit(".", 1)[1].lower(); path = os.path.join(folder, f"{id}.{ext}")
        file.save(path); img = cv2.imread(path)
        if img is None: os.remove(path); raise ValueError("Bad image")
        h, w = img.shape[:2]
        return id, path, {"image_id": id, "filename": secure_filename(file.filename), "path": path, "width": int(w), "height": int(h), "channels": 3 if len(img.shape)==3 else 1}
    @staticmethod
    def image_to_base64(img): return base64.b64encode(cv2.imencode(".png", img)[1]).decode("utf-8")
    @staticmethod
    def get_image_path(id, folder):
        for e in ALLOWED_EXTENSIONS:
            p = os.path.join(folder, f"{id}.{e}")
            if os.path.exists(p): return p
        return None
