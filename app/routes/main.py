from decimal import Decimal

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from app import db
from app.models import Pet, ServiceOrder, AdoptionRequest

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    pet_count = Pet.query.count()
    order_count = ServiceOrder.query.count()
    revenue = (
        db.session.query(func.coalesce(func.sum(ServiceOrder.amount), 0))
        .filter(ServiceOrder.status == "completed")
        .scalar()
    )
    if revenue is None:
        revenue = Decimal("0")

    pending_count    = ServiceOrder.query.filter_by(status="pending").count()
    in_progress_count = ServiceOrder.query.filter_by(status="in_progress").count()
    completed_count  = ServiceOrder.query.filter_by(status="completed").count()
    cancelled_count  = ServiceOrder.query.filter_by(status="cancelled").count()

    adoption_count    = AdoptionRequest.query.count()
    adoption_pending  = AdoptionRequest.query.filter_by(status="pending").count()
    adoption_approved = AdoptionRequest.query.filter_by(status="approved").count()
    adoption_rejected = AdoptionRequest.query.filter_by(status="rejected").count()

    recent_orders = (
        ServiceOrder.query.order_by(ServiceOrder.created_at.desc()).limit(8).all()
    )

    return render_template(
        "dashboard.html",
        pet_count=pet_count,
        order_count=order_count,
        total_revenue=revenue,
        adoption_count=adoption_count,
        pending_count=pending_count,
        in_progress_count=in_progress_count,
        completed_count=completed_count,
        cancelled_count=cancelled_count,
        adoption_pending=adoption_pending,
        adoption_approved=adoption_approved,
        adoption_rejected=adoption_rejected,
        recent_orders=recent_orders,
    )
