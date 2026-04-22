import uuid
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db
from app.models import Product, ProductCategory, ShopOrder, ShopOrderItem

bp = Blueprint("shop", __name__, url_prefix="/shop")


def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


@bp.route("/")
def index():
    categories = ProductCategory.query.order_by(ProductCategory.sort_order).all()
    featured = Product.query.filter_by(is_featured=True, is_active=True).order_by(Product.sales_count.desc()).limit(8).all()
    newest = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(8).all()
    return render_template(
        "shop/index.html",
        categories=categories,
        featured=featured,
        newest=newest,
    )


@bp.route("/list")
def list():
    cat_id = request.args.get("category", type=int)
    keyword = request.args.get("q", "").strip()
    sort = request.args.get("sort", "default")

    query = Product.query.filter_by(is_active=True)
    if cat_id:
        query = query.filter_by(category_id=cat_id)
    if keyword:
        query = query.filter(Product.name.contains(keyword) | Product.description.contains(keyword))

    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "sales":
        query = query.order_by(Product.sales_count.desc())
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.sort_order.desc() if hasattr(Product, "sort_order") else Product.id.desc())

    products = query.all()
    categories = ProductCategory.query.order_by(ProductCategory.sort_order).all()
    return render_template("shop/list.html", products=products, categories=categories, cat_id=cat_id, keyword=keyword, sort=sort)


@bp.route("/detail/<int:product_id>")
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = (
        Product.query
        .filter_by(category_id=product.category_id, is_active=True)
        .filter(Product.id != product_id)
        .limit(4)
        .all()
    )
    return render_template("shop/detail.html", product=product, related=related)


@bp.route("/cart")
def cart():
    cart_items = []
    cart = get_cart()
    total = 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            item_total = float(p.price) * qty
            total += item_total
            cart_items.append({"product": p, "quantity": qty, "item_total": item_total})
    return render_template("shop/cart.html", cart_items=cart_items, total=total)


@bp.route("/cart/add/<int:product_id>", methods=["POST"])
def cart_add(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get("quantity", 1, type=int)
    if quantity < 1:
        quantity = 1
    if quantity > product.stock:
        flash(f"库存不足，当前仅剩 {product.stock} 件", "warning")
        return redirect(url_for("shop.detail", product_id=product_id))

    cart = get_cart()
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + quantity
    save_cart(cart)
    flash(f"已添加「{product.name}」到购物车", "success")
    return redirect(url_for("shop.cart"))


@bp.route("/cart/update/<int:product_id>", methods=["POST"])
def cart_update(product_id):
    quantity = request.form.get("quantity", 1, type=int)
    product = Product.query.get_or_404(product_id)
    cart = get_cart()
    pid = str(product_id)
    if pid in cart:
        if quantity <= 0:
            del cart[pid]
        elif quantity > product.stock:
            flash(f"库存不足，当前仅剩 {product.stock} 件", "warning")
        else:
            cart[pid] = quantity
        save_cart(cart)
    return redirect(url_for("shop.cart"))


@bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def cart_remove(product_id):
    cart = get_cart()
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        save_cart(cart)
        flash("已从购物车移除", "info")
    return redirect(url_for("shop.cart"))


@bp.route("/cart/clear", methods=["POST"])
def cart_clear():
    save_cart({})
    flash("购物车已清空", "info")
    return redirect(url_for("shop.cart"))


@bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()
    if not cart:
        flash("购物车是空的", "warning")
        return redirect(url_for("shop.list"))

    cart_items = []
    total = 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if not p:
            continue
        item_total = float(p.price) * qty
        total += item_total
        cart_items.append({"product": p, "quantity": qty, "item_total": item_total})

    if request.method == "POST":
        user_name = request.form.get("user_name", "").strip()
        user_phone = request.form.get("user_phone", "").strip()
        user_address = request.form.get("user_address", "").strip()
        remark = request.form.get("remark", "").strip()

        if not all([user_name, user_phone, user_address]):
            flash("请填写完整的收货信息", "danger")
            return render_template("shop/checkout.html", cart_items=cart_items, total=total,
                                   user_name=user_name, user_phone=user_phone, user_address=user_address, remark=remark)

        order = ShopOrder(
            order_no=f"SHOP{uuid.uuid4().hex[:12].upper()}",
            user_name=user_name,
            user_phone=user_phone,
            user_address=user_address,
            total_amount=total,
            remark=remark,
            status="pending",
        )
        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            order_item = ShopOrderItem(
                order_id=order.id,
                product_id=item["product"].id,
                product_name=item["product"].name,
                product_image=item["product"].image_url,
                price=item["product"].price,
                quantity=item["quantity"],
            )
            db.session.add(order_item)
            item["product"].stock = max(0, item["product"].stock - item["quantity"])
            item["product"].sales_count += item["quantity"]

        db.session.commit()
        save_cart({})
        flash(f"订单提交成功！订单号：{order.order_no}", "success")
        return redirect(url_for("shop.orders"))

    return render_template("shop/checkout.html", cart_items=cart_items, total=total,
                           user_name="", user_phone="", user_address="", remark="")


@bp.route("/orders")
def orders():
    orders_list = ShopOrder.query.order_by(ShopOrder.created_at.desc()).all()
    return render_template("shop/orders.html", orders=orders_list)
