import hashlib
import os
import random
import uuid

from flask import Blueprint, current_app, flash, render_template, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.services.breed_classifier import BreedClassifierService, load_class_names

bp = Blueprint("recognize", __name__)


def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "webp", "gif"}


def get_classifier():
    return BreedClassifierService(
        current_app.config["MODEL_PATH"],
        current_app.config["BREEDS_FILE"],
    )


def mock_topk(breeds_file, image_path, k=5):
    """无模型时按图片路径生成稳定的假概率，仅用于演示（非真实识别）。"""
    classes = load_class_names(breeds_file)
    if len(classes) < 1:
        return []
    digest = hashlib.sha256(os.path.abspath(image_path).encode("utf-8")).digest()
    seed = int.from_bytes(digest[:8], "big")
    rng = random.Random(seed)
    idxs = list(range(len(classes)))
    rng.shuffle(idxs)
    take = idxs[: min(k, len(idxs))]
    raw = [rng.random() + 0.05 for _ in take]
    s = sum(raw) or 1.0
    probs = [x / s for x in raw]
    pairs = sorted(zip(take, probs), key=lambda x: -x[1])
    return [(classes[i], p) for i, p in pairs]


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    results = None
    preview_name = None
    mock_mode = False
    clf = get_classifier()
    model_ready = clf.is_ready()
    mock_allowed = current_app.config.get("MOCK_RECOGNITION", False)

    if request.method == "POST":
        f = request.files.get("photo")
        if not f or not f.filename:
            flash("请选择一张图片", "warning")
        elif not allowed_file(f.filename):
            flash("仅支持 png、jpg、jpeg、webp、gif", "danger")
        else:
            ext = secure_filename(f.filename).rsplit(".", 1)[-1].lower()
            fn = f"rec_{uuid.uuid4().hex}.{ext}"
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], fn)
            f.save(path)
            preview_name = fn
            if model_ready:
                results = clf.predict_topk(path, k=5)
            elif mock_allowed and load_class_names(current_app.config["BREEDS_FILE"]):
                results = mock_topk(current_app.config["BREEDS_FILE"], path, k=5)
                mock_mode = True
                flash("模拟识别", "info")
            else:
                flash("模型未加载", "warning")

    return render_template(
        "recognize/index.html",
        results=results,
        preview=preview_name,
        model_ready=model_ready,
        mock_mode=mock_mode,
        mock_allowed=mock_allowed,
        model_path=current_app.config["MODEL_PATH"],
        breeds_file=current_app.config["BREEDS_FILE"],
    )
