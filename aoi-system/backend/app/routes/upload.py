from flask import Blueprint,request,jsonify,current_app
from app.services.image_handler import ImageHandler
bp=Blueprint("upload",__name__)
@bp.route("/upload",methods=["POST"])
def upload_image():
    try:
        if "image" not in request.files: return jsonify({"success":False,"error":{"code":"NO_FILE","message":"No file"}}),400
        file=request.files["image"]
        if not file.filename: return jsonify({"success":False,"error":{"code":"NO_FILE","message":"No file"}}),400
        id,_,info=ImageHandler.save_uploaded_image(file,current_app.config["UPLOAD_FOLDER"])
        return jsonify({"success":True,"image_id":info["image_id"],"filename":info["filename"],"size":{"width":info["width"],"height":info["height"]}}),200
    except Exception as e: return jsonify({"success":False,"error":{"code":"ERROR","message":str(e)}}),500
