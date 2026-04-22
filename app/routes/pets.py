from datetime import datetime

import os
import uuid

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db
from app.models import Pet, ServiceOrder, AdoptionRequest
from app.services.breed_classifier import BreedClassifierService

bp = Blueprint("pets", __name__)


def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "webp", "gif"}


def get_classifier():
    return BreedClassifierService(
        current_app.config["MODEL_PATH"],
        current_app.config["BREEDS_FILE"],
    )


@bp.route("/")
@login_required
def list_pets():
    q = request.args.get("q", "").strip()
    query = Pet.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Pet.name.ilike(like))
            | (Pet.breed.ilike(like))
            | (Pet.owner_name.ilike(like))
            | (Pet.owner_phone.ilike(like))
        )
    species = request.args.get("species", "").strip()
    if species in ("狗", "猫"):
        query = query.filter(Pet.species == species)
    pets = query.order_by(Pet.updated_at.desc()).all()
    keyword = request.args.get("keyword", "").strip()
    species = request.args.get("species", "").strip()
    return render_template("pets/list.html", pets=pets, keyword=keyword, species=species)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new_pet():
    if request.method == "POST":
        p = Pet(
            name=request.form.get("name", "").strip() or "未命名",
            species=request.form.get("species", "狗").strip(),
            breed=(request.form.get("breed") or "").strip() or None,
            owner_name=(request.form.get("owner_name") or "").strip() or None,
            owner_phone=(request.form.get("owner_phone") or "").strip() or None,
            notes=(request.form.get("notes") or "").strip() or None,
            adoption_status=request.form.get("adoption_status", "available").strip(),
            adoption_fee=float(request.form.get("adoption_fee") or 0),
            adoption_description=(request.form.get("adoption_description") or "").strip() or None,
        )
        f = request.files.get("photo")
        if f and f.filename and allowed_file(f.filename):
            ext = secure_filename(f.filename).rsplit(".", 1)[-1].lower()
            fn = f"{uuid.uuid4().hex}.{ext}"
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], fn)
            f.save(path)
            p.photo_filename = fn
            clf = get_classifier()
            if clf.is_ready():
                tops = clf.predict_topk(path, k=1)
                if tops:
                    p.breed = tops[0][0]
                    p.breed_confidence = tops[0][1]
        bc = request.form.get("breed_confidence")
        if bc:
            try:
                p.breed_confidence = float(bc)
            except ValueError:
                pass
        if p.adoption_status in ("available", "pending"):
            p.adoption_posted_at = datetime.utcnow()
        db.session.add(p)
        db.session.commit()
        flash("档案已创建", "success")
        return redirect(url_for("pets.detail", pet_id=p.id))
    prefill_breed = request.args.get("breed", "").strip()
    prefill_conf = request.args.get("suggest_conf", type=float)
    prefill_adoption = request.args.get("for_adoption", "").strip()
    return render_template(
        "pets/form.html",
        pet=None,
        title="新建宠物档案",
        prefill_breed=prefill_breed,
        prefill_conf=prefill_conf,
        prefill_adoption=prefill_adoption,
    )


@bp.route("/<int:pet_id>")
@login_required
def detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    orders = (
        pet.orders.order_by(ServiceOrder.created_at.desc()).limit(30).all()
    )
    adoption_requests = (
        pet.adoption_requests.order_by(AdoptionRequest.created_at.desc()).limit(30).all()
    )
    return render_template("pets/detail.html", pet=pet, orders=orders, adoption_requests=adoption_requests)


@bp.route("/<int:pet_id>/edit", methods=["GET", "POST"])
@login_required
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if request.method == "POST":
        pet.name = request.form.get("name", "").strip() or pet.name
        pet.species = request.form.get("species", pet.species).strip()
        pet.breed = (request.form.get("breed") or "").strip() or None
        pet.owner_name = (request.form.get("owner_name") or "").strip() or None
        pet.owner_phone = (request.form.get("owner_phone") or "").strip() or None
        pet.notes = (request.form.get("notes") or "").strip() or None
        pet.adoption_status = request.form.get("adoption_status", pet.adoption_status).strip()
        pet.adoption_fee = float(request.form.get("adoption_fee") or 0)
        pet.adoption_description = (request.form.get("adoption_description") or "").strip() or None
        f = request.files.get("photo")
        if f and f.filename and allowed_file(f.filename):
            ext = secure_filename(f.filename).rsplit(".", 1)[-1].lower()
            fn = f"{uuid.uuid4().hex}.{ext}"
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], fn)
            f.save(path)
            pet.photo_filename = fn
            clf = get_classifier()
            if clf.is_ready():
                tops = clf.predict_topk(path, k=1)
                if tops:
                    pet.breed = tops[0][0]
                    pet.breed_confidence = tops[0][1]
        db.session.commit()
        flash("已保存", "success")
        return redirect(url_for("pets.detail", pet_id=pet.id))
    return render_template("pets/form.html", pet=pet, title="编辑档案")


@bp.route("/<int:pet_id>/delete", methods=["POST"])
@login_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash("已删除", "info")
    return redirect(url_for("pets.list_pets"))
