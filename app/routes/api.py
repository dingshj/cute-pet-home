import os
import uuid

from flask import Blueprint, current_app, jsonify, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.services.breed_classifier import BreedClassifierService

bp = Blueprint("api", __name__)


def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "webp"}


@bp.route("/recognize", methods=["POST"])
@login_required
def recognize():
    f = request.files.get("image")
    if not f or not f.filename:
        return jsonify({"ok": False, "error": "缺少图片"}), 400
    if not allowed_file(f.filename):
        return jsonify({"ok": False, "error": "仅支持 png/jpg/jpeg/webp"}), 400
    clf = BreedClassifierService(
        current_app.config["MODEL_PATH"],
        current_app.config["BREEDS_FILE"],
    )
    if not clf.is_ready():
        return jsonify(
            {
                "ok": False,
                "error": "模型未就绪：请准备 instance/breeds.txt 与训练生成的权重 instance/breed_classifier.pt",
            }
        ), 503
    ext = secure_filename(f.filename).rsplit(".", 1)[-1].lower()
    fn = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], fn)
    f.save(path)
    try:
        tops = clf.predict_topk(path, k=5)
        return jsonify(
            {
                "ok": True,
                "predictions": [{"breed": b, "confidence": c} for b, c in tops],
                "saved_as": fn,
            }
        )
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
