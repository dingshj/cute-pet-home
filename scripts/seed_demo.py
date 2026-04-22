"""
向数据库写入演示用的宠物档案与服务工单（便于看板、列表展示毕设效果）。

用法（在项目根目录）：
  python scripts/seed_demo.py

若已有宠物档案则默认跳过，避免重复；若要强制再写一份可加 --force
"""
import argparse
import os
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from decimal import Decimal

from app import create_app, db
from app.models import Pet, ServiceOrder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="即使已有数据也继续追加")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        if Pet.query.count() > 0 and not args.force:
            print("已有宠物数据，未写入。若要追加演示数据请运行: python scripts/seed_demo.py --force")
            return

        samples = [
            {
                "name": "豆豆",
                "species": "狗",
                "breed": "泰迪",
                "owner_name": "王女士",
                "owner_phone": "13800138001",
                "notes": "演示数据：性格温顺，定期驱虫。",
            },
            {
                "name": "雪球",
                "species": "狗",
                "breed": "萨摩耶",
                "owner_name": "李先生",
                "owner_phone": "13800138002",
                "notes": "演示数据：毛发较厚，夏季注意散热。",
            },
            {
                "name": "咪咪",
                "species": "猫",
                "breed": "英短",
                "owner_name": "赵同学",
                "owner_phone": "13800138003",
                "notes": "演示数据：室内饲养，已绝育。",
            },
        ]

        pets = []
        for s in samples:
            p = Pet(**s)
            db.session.add(p)
            pets.append(p)
        db.session.flush()

        orders_spec = [
            (0, "groom", "completed", Decimal("120.00")),
            (0, "boarding", "completed", Decimal("200.00")),
            (1, "groom", "in_progress", Decimal("150.00")),
            (2, "boarding", "pending", Decimal("180.00")),
        ]
        for idx, stype, status, amount in orders_spec:
            o = ServiceOrder(
                pet_id=pets[idx].id,
                service_type=stype,
                status=status,
                amount=amount,
                notes="演示工单",
            )
            db.session.add(o)

        db.session.commit()
        print(f"已写入 {len(samples)} 条宠物档案与 {len(orders_spec)} 条服务工单。刷新网页即可查看。")


if __name__ == "__main__":
    main()
