from datetime import datetime
from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.models import Pet, ServiceOrder

bp = Blueprint("services", __name__)


def parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


@bp.route("/")
@login_required
def list_orders():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    query = ServiceOrder.query
    if status in ("pending", "in_progress", "completed", "cancelled"):
        query = query.filter_by(status=status)
    orders = query.order_by(ServiceOrder.created_at.desc()).all()
    return render_template("services/list.html", orders=orders, status=status, keyword=q)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new_order():
    pets = Pet.query.order_by(Pet.name).all()
    if request.method == "POST":
        pet_id = int(request.form.get("pet_id") or 0)
        pet = Pet.query.get(pet_id)
        if not pet:
            flash("请选择宠物", "danger")
            return render_template("services/form.html", pets=pets, order=None)
        try:
            amt = Decimal(str(request.form.get("amount") or "0"))
        except Exception:
            amt = Decimal("0")
        o = ServiceOrder(
            pet_id=pet.id,
            service_type=request.form.get("service_type", "groom"),
            status=request.form.get("status", "pending"),
            scheduled_at=parse_dt(request.form.get("scheduled_at")),
            amount=amt,
            notes=(request.form.get("notes") or "").strip() or None,
        )
        db.session.add(o)
        db.session.commit()
        flash("工单已创建", "success")
        return redirect(url_for("services.list_orders"))
    return render_template("services/form.html", pets=pets, order=None)


@bp.route("/<int:order_id>/edit", methods=["GET", "POST"])
@login_required
def edit_order(order_id):
    order = ServiceOrder.query.get_or_404(order_id)
    pets = Pet.query.order_by(Pet.name).all()
    if request.method == "POST":
        order.pet_id = int(request.form.get("pet_id") or order.pet_id)
        order.service_type = request.form.get("service_type", order.service_type)
        order.status = request.form.get("status", order.status)
        order.scheduled_at = parse_dt(request.form.get("scheduled_at"))
        if request.form.get("completed_at"):
            order.completed_at = parse_dt(request.form.get("completed_at"))
        elif order.status == "completed" and not order.completed_at:
            order.completed_at = datetime.now()
        try:
            order.amount = Decimal(str(request.form.get("amount") or "0"))
        except Exception:
            pass
        order.notes = (request.form.get("notes") or "").strip() or None
        db.session.commit()
        flash("已保存", "success")
        return redirect(url_for("services.list_orders"))
    return render_template("services/form.html", pets=pets, order=order)
