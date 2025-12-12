from flask import Blueprint,request,jsonify,current_app
from app.services.image_handler import ImageHandler
from app.services.aoi_service import AOIService
bp=Blueprint("process",__name__)
@bp.route("/process/defect-detection",methods=["POST"])
def defect_detection():
    try:
        d=request.get_json(); p=ImageHandler.get_image_path(d["image_id"],current_app.config["UPLOAD_FOLDER"])
        if not p: return jsonify({"success":False,"error":{"code":"NOT_FOUND","message":"Image not found"}}),404
        r=AOIService.detect_defects(p,None,d.get("threshold",30))
        return jsonify({"success":True,"defects":r["defects"],"defect_count":r["defect_count"],"annotated_image":ImageHandler.image_to_base64(r["annotated_image"])}),200
    except Exception as e: return jsonify({"success":False,"error":{"code":"ERROR","message":str(e)}}),500
@bp.route("/process/measurement",methods=["POST"])
def measurement():
    try:
        d=request.get_json(); p=ImageHandler.get_image_path(d["image_id"],current_app.config["UPLOAD_FOLDER"])
        if not p: return jsonify({"success":False,"error":{"code":"NOT_FOUND","message":"Image not found"}}),404
        cal=d.get("calibration",{}).get("pixel_to_mm",0.1); r=AOIService.measure_dimensions(p,cal)
        return jsonify({"success":True,"measurements":r["measurements"],"annotated_image":ImageHandler.image_to_base64(r["annotated_image"])}),200
    except Exception as e: return jsonify({"success":False,"error":{"code":"ERROR","message":str(e)}}),500
@bp.route("/process/fiducial-detection",methods=["POST"])
def fiducial_detection():
    try:
        d=request.get_json(); p=ImageHandler.get_image_path(d["image_id"],current_app.config["UPLOAD_FOLDER"])
        if not p: return jsonify({"success":False,"error":{"code":"NOT_FOUND","message":"Image not found"}}),404
        r=AOIService.detect_fiducial_marks(p,d.get("min_radius",5),d.get("max_radius",25))
        return jsonify({"success":True,"marks":r["marks"],"rotation_angle":r["rotation_angle"],"annotated_image":ImageHandler.image_to_base64(r["annotated_image"])}),200
    except Exception as e: return jsonify({"success":False,"error":{"code":"ERROR","message":str(e)}}),500
