from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), default="staff")
    created_at = db.Column(db.DateTime, default=utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    species = db.Column(db.String(32), default="狗")
    breed = db.Column(db.String(128))
    breed_confidence = db.Column(db.Float)
    photo_filename = db.Column(db.String(256))
    owner_name = db.Column(db.String(64))
    owner_phone = db.Column(db.String(32))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    adoption_status = db.Column(db.String(32), default="available")
    adoption_fee = db.Column(db.Numeric(10, 2), default=0)
    adoption_description = db.Column(db.Text)
    adoption_posted_at = db.Column(db.DateTime)

    orders = db.relationship("ServiceOrder", backref="pet", lazy="dynamic", cascade="all, delete-orphan")
    adoption_requests = db.relationship("AdoptionRequest", backref="pet", lazy="dynamic", cascade="all, delete-orphan")


class AdoptionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)
    applicant_name = db.Column(db.String(64), nullable=False)
    applicant_phone = db.Column(db.String(32), nullable=False)
    applicant_address = db.Column(db.String(256))
    applicant_intent = db.Column(db.Text)
    status = db.Column(db.String(32), default="pending")
    reviewer_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)
    reviewed_at = db.Column(db.DateTime)


class ServiceOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)
    service_type = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), default="pending")
    scheduled_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    amount = db.Column(db.Numeric(10, 2), default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    icon = db.Column(db.String(32))
    sort_order = db.Column(db.Integer, default=0)
    products = db.relationship("Product", backref="category", lazy="dynamic")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("product_category.id"))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    original_price = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(256))
    description = db.Column(db.Text)
    brand = db.Column(db.String(64))
    spec = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    sales_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)

    order_items = db.relationship("ShopOrderItem", backref="product", lazy="dynamic")


class ShopOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(32), unique=True, nullable=False)
    user_name = db.Column(db.String(64), nullable=False)
    user_phone = db.Column(db.String(32), nullable=False)
    user_address = db.Column(db.String(256), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(32), default="pending")
    remark = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)

    items = db.relationship("ShopOrderItem", backref="order", lazy="dynamic", cascade="all, delete-orphan")


class ShopOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("shop_order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_name = db.Column(db.String(128), nullable=False)
    product_image = db.Column(db.String(256))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, default=1)
