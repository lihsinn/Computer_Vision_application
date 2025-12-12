#!/usr/bin/env python3
"""Create all backend files for AOI system"""
import os

os.chdir('aoi-system/backend/app')

# Create all backend service and route files
print("Creating backend files...")

# 1. Create image_handler.py - simplified version
image_handler_code = """import cv2
import base64
import numpy as np
import uuid
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

class ImageHandler:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def save_uploaded_image(file, upload_folder):
        if not ImageHandler.allowed_file(file.filename):
            raise ValueError("File type not allowed")
        image_id = str(uuid.uuid4())
        ext = file.filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(upload_folder, f"{image_id}.{ext}")
        file.save(file_path)
        img = cv2.imread(file_path)
        if img is None:
            os.remove(file_path)
            raise ValueError("Failed to read image")
        h, w = img.shape[:2]
        return image_id, file_path, {
            'image_id': image_id,
            'filename': secure_filename(file.filename),
            'path': file_path,
            'width': int(w),
            'height': int(h),
            'channels': 3 if len(img.shape) == 3 else 1
        }

    @staticmethod
    def image_to_base64(cv_image):
        _, buffer = cv2.imencode('.png', cv_image)
        return base64.b64encode(buffer).decode('utf-8')

    @staticmethod
    def get_image_path(image_id, upload_folder):
        for ext in ALLOWED_EXTENSIONS:
            path = os.path.join(upload_folder, f"{image_id}.{ext}")
            if os.path.exists(path):
                return path
        return None
"""

with open('services/image_handler.py', 'w', encoding='utf-8') as f:
    f.write(image_handler_code)
print("✓ services/image_handler.py")

# 2. Create aoi_service.py
aoi_service_code = """import cv2
import numpy as np

class AOIService:
    @staticmethod
    def detect_defects(image_path, template_path=None, threshold=30):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        template = cv2.GaussianBlur(img, (15, 15), 5)
        diff = cv2.absdiff(template, img)
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        defects = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 50:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.drawContours(result, [cnt], -1, (0, 0, 255), 2)
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
            defects.append({
                'id': len(defects)+1,
                'position': {'x': int(x+w//2), 'y': int(y+h//2)},
                'area': float(area),
                'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
            })
        return {'defects': defects, 'defect_count': len(defects), 'annotated_image': result}

    @staticmethod
    def measure_dimensions(image_path, pixel_to_mm=0.1):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        edges = cv2.Canny(img, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        measurements = []
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area < 100:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
            perimeter = cv2.arcLength(cnt, True)
            circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
            m = {
                'object_id': i+1,
                'shape': 'circle' if circularity > 0.8 else 'rectangle',
                'width_mm': round(w * pixel_to_mm, 2),
                'height_mm': round(h * pixel_to_mm, 2),
                'area_mm2': round(area * pixel_to_mm**2, 2),
                'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
            }
            if circularity > 0.8:
                m['diameter_mm'] = round(2 * np.sqrt(area / np.pi) * pixel_to_mm, 2)
            measurements.append(m)
        return {'measurements': measurements, 'annotated_image': result}

    @staticmethod
    def detect_fiducial_marks(image_path, min_radius=5, max_radius=25):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        blur = cv2.GaussianBlur(img, (5, 5), 1.5)
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=30,
                                   minRadius=min_radius, maxRadius=max_radius)
        result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        marks, angle = [], None
        if circles is not None:
            for i, (cx, cy, r) in enumerate(np.uint16(np.around(circles))[0]):
                cv2.circle(result, (cx, cy), r, (0, 255, 0), 2)
                marks.append({'id': i+1, 'position': {'x': int(cx), 'y': int(cy)}, 'radius': int(r)})
            if len(marks) >= 2:
                p1, p2 = marks[0]['position'], marks[1]['position']
                angle = float(np.degrees(np.arctan2(p2['y']-p1['y'], p2['x']-p1['x'])))
        return {'marks': marks, 'rotation_angle': round(angle, 2) if angle else None, 'annotated_image': result}
"""

with open('services/aoi_service.py', 'w', encoding='utf-8') as f:
    f.write(aoi_service_code)
print("✓ services/aoi_service.py")

# 3. Create upload.py
upload_code = """from flask import Blueprint, request, jsonify, current_app
from app.services.image_handler import ImageHandler

bp = Blueprint('upload', __name__)

@bp.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': {'code': 'NO_FILE', 'message': 'No file'}}), 400
        file = request.files['image']
        if not file.filename:
            return jsonify({'success': False, 'error': {'code': 'NO_FILE', 'message': 'No file'}}), 400
        image_id, _, info = ImageHandler.save_uploaded_image(file, current_app.config['UPLOAD_FOLDER'])
        return jsonify({
            'success': True,
            'image_id': info['image_id'],
            'filename': info['filename'],
            'size': {'width': info['width'], 'height': info['height']}
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': {'code': 'ERROR', 'message': str(e)}}), 500
"""

with open('routes/upload.py', 'w', encoding='utf-8') as f:
    f.write(upload_code)
print("✓ routes/upload.py")

# 4. Create process.py
process_code = """from flask import Blueprint, request, jsonify, current_app
from app.services.image_handler import ImageHandler
from app.services.aoi_service import AOIService

bp = Blueprint('process', __name__)

@bp.route('/process/defect-detection', methods=['POST'])
def defect_detection():
    try:
        data = request.get_json()
        path = ImageHandler.get_image_path(data['image_id'], current_app.config['UPLOAD_FOLDER'])
        if not path:
            return jsonify({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Image not found'}}), 404
        result = AOIService.detect_defects(path, None, data.get('threshold', 30))
        return jsonify({
            'success': True,
            'defects': result['defects'],
            'defect_count': result['defect_count'],
            'annotated_image': ImageHandler.image_to_base64(result['annotated_image'])
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': {'code': 'ERROR', 'message': str(e)}}), 500

@bp.route('/process/measurement', methods=['POST'])
def measurement():
    try:
        data = request.get_json()
        path = ImageHandler.get_image_path(data['image_id'], current_app.config['UPLOAD_FOLDER'])
        if not path:
            return jsonify({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Image not found'}}), 404
        cal = data.get('calibration', {}).get('pixel_to_mm', 0.1)
        result = AOIService.measure_dimensions(path, cal)
        return jsonify({
            'success': True,
            'measurements': result['measurements'],
            'annotated_image': ImageHandler.image_to_base64(result['annotated_image'])
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': {'code': 'ERROR', 'message': str(e)}}), 500

@bp.route('/process/fiducial-detection', methods=['POST'])
def fiducial_detection():
    try:
        data = request.get_json()
        path = ImageHandler.get_image_path(data['image_id'], current_app.config['UPLOAD_FOLDER'])
        if not path:
            return jsonify({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Image not found'}}), 404
        result = AOIService.detect_fiducial_marks(path, data.get('min_radius', 5), data.get('max_radius', 25))
        return jsonify({
            'success': True,
            'marks': result['marks'],
            'rotation_angle': result['rotation_angle'],
            'annotated_image': ImageHandler.image_to_base64(result['annotated_image'])
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': {'code': 'ERROR', 'message': str(e)}}), 500
"""

with open('routes/process.py', 'w', encoding='utf-8') as f:
    f.write(process_code)
print("✓ routes/process.py")

print("\n✅ All backend files created successfully!")
