from datetime import datetime

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.models import AdoptionRequest, Pet

bp = Blueprint("adoption", __name__)


@bp.route("/")
def list_adoptable():
    pets = (
        Pet.query
        .filter(Pet.adoption_status.in_(["available", "pending"]))
        .order_by(Pet.adoption_posted_at.desc().nullsfirst(), Pet.updated_at.desc())
        .all()
    )
    return render_template("adoption/list.html", pets=pets)


@bp.route("/<int:pet_id>")
def detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    requests = (
        pet.adoption_requests
        .filter(AdoptionRequest.status.in_(["approved", "rejected"]))
        .order_by(AdoptionRequest.reviewed_at.desc())
        .all()
    )
    return render_template("adoption/detail.html", pet=pet, requests=requests)


@bp.route("/<int:pet_id>/apply", methods=["GET", "POST"])
def apply(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if request.method == "POST":
        ar = AdoptionRequest(
            pet_id=pet.id,
            applicant_name=(request.form.get("applicant_name") or "").strip(),
            applicant_phone=(request.form.get("applicant_phone") or "").strip(),
            applicant_address=(request.form.get("applicant_address") or "").strip() or None,
            applicant_intent=(request.form.get("applicant_intent") or "").strip() or None,
        )
        if not ar.applicant_name:
            flash("请填写您的姓名", "warning")
        elif not ar.applicant_phone:
            flash("请填写联系电话", "warning")
        else:
            db.session.add(ar)
            if pet.adoption_status == "available":
                pet.adoption_status = "pending"
            db.session.commit()
            flash("申请已提交，请等待审核", "success")
            return redirect(url_for("adoption.list_adoptable"))
        return redirect(url_for("adoption.apply", pet_id=pet.id))
    return render_template("adoption/apply.html", pet=pet)


@bp.route("/my")
@login_required
def my_requests():
    from app.models import User
    user = User.query.filter_by(username="admin").first()
    requests_ = (
        AdoptionRequest.query
        .join(Pet)
        .order_by(AdoptionRequest.created_at.desc())
        .all()
    )
    return render_template("adoption/my_requests.html", requests_=requests_, requests=requests_)


@bp.route("/<int:req_id>/review/<action>", methods=["POST"])
@login_required
def review(req_id, action):
    ar = AdoptionRequest.query.get_or_404(req_id)
    if action == "approve":
        ar.status = "approved"
        ar.reviewed_at = datetime.utcnow()
        ar.pet.adoption_status = "adopted"
        flash("已批准该领养申请", "success")
    elif action == "reject":
        ar.status = "rejected"
        ar.reviewed_at = datetime.utcnow()
        if (
            ar.pet.adoption_status == "pending"
            and not ar.pet.adoption_requests.filter(
                AdoptionRequest.id != ar.id,
                AdoptionRequest.status == "pending"
            ).first()
        ):
            ar.pet.adoption_status = "available"
        flash("已拒绝该领养申请", "info")
    db.session.commit()
    return redirect(url_for("adoption.my_requests"))
