"""
为宠物商城填充示例商品数据。
运行：python -c "from scripts.seed_shop import seed; seed()"
"""
from app import create_app, db
from app.models import Product, ProductCategory


CATEGORIES = [
    {"name": "宠物服装", "slug": "clothing", "icon": "👕", "sort_order": 1},
    {"name": "宠物食品", "slug": "food", "icon": "🍖", "sort_order": 2},
    {"name": "宠物玩具", "slug": "toys", "icon": "🧸", "sort_order": 3},
    {"name": "宠物窝笼", "slug": "beds", "icon": "🏠", "sort_order": 4},
    {"name": "清洁护理", "slug": "care", "icon": "🛁", "sort_order": 5},
    {"name": "配饰装饰", "slug": "accessories", "icon": "🎀", "sort_order": 6},
]

PRODUCTS = [
    # 宠物服装
    {"name": "法斗同款秋季连帽卫衣", "category": "宠物服装", "price": 89.0, "original_price": 129.0, "stock": 52, "brand": "萌宠优品", "spec": "M码 / 适合4-8kg", "image_url": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=400&fit=crop", "is_featured": True, "description": "采用优质纯棉面料，柔软舒适，保暖透气。时尚连帽设计，轻松穿出萌宠气质。精细做工，走线均匀，贴身不刺激。", "sales_count": 128},
    {"name": "柴犬条纹开衫毛衣", "category": "宠物服装", "price": 68.0, "stock": 38, "brand": "爪爪星球", "spec": "L码 / 适合8-15kg", "image_url": "https://images.unsplash.com/photo-1587764379873-97837921fd44?w=400&h=400&fit=crop", "is_featured": True, "description": "经典条纹设计，简约大方。柔软毛线面料，冬季保暖必备。多色可选，总有一款适合你家宝贝。", "sales_count": 96},
    {"name": "猫咪公主蓬蓬裙", "category": "宠物服装", "price": 45.0, "original_price": 68.0, "stock": 25, "brand": "萌宠优品", "spec": "S码 / 适合2-4kg", "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop", "description": "蕾丝花边点缀，甜美公主风。弹力面料，穿着舒适不紧绷。适合拍照和聚会。", "sales_count": 67},
    {"name": "柯基四脚雨衣", "category": "宠物服装", "price": 55.0, "stock": 30, "brand": "宠趣", "spec": "M码 / 适合5-10kg", "image_url": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=400&h=400&fit=crop", "description": "防水面料，雨天出行无忧。全包设计，保护腹部和四肢。可调节魔术贴，适合各种体型。", "sales_count": 45},

    # 宠物食品
    {"name": "皇家猫奶糕离乳期幼猫粮 2kg", "category": "宠物食品", "price": 168.0, "original_price": 198.0, "stock": 80, "brand": "皇家", "spec": "2kg 装", "image_url": "https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?w=400&h=400&fit=crop", "is_featured": True, "description": "专为1-4月龄幼猫设计，富含DHA促进脑部发育。细小颗粒，易于咀嚼和消化。提升免疫力，帮助幼猫健康成长。", "sales_count": 234},
    {"name": "渴望六种鱼全猫粮 3kg", "category": "宠物食品", "price": 358.0, "original_price": 428.0, "stock": 45, "brand": "渴望 Orijen", "spec": "3kg 装", "image_url": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=400&fit=crop", "is_featured": True, "description": "85%优质动物蛋白，添加六种新鲜深海鱼类。含猫咪必需的牛磺酸和氨基酸。无谷配方，减少过敏源。", "sales_count": 189},
    {"name": "麦富迪双拼狗粮成犬粮 10kg", "category": "宠物食品", "price": 198.0, "stock": 120, "brand": "麦富迪", "spec": "10kg 装", "image_url": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop", "description": "肉松+狗粮双拼，口感丰富。添加益生元，呵护肠胃。含真实鸡肉粒，营养均衡。", "sales_count": 156},
    {"name": "希宝金枪鱼猫罐头 85g×12", "category": "宠物食品", "price": 79.0, "original_price": 99.0, "stock": 200, "brand": "希宝 Sheba", "spec": "85g×12罐装", "image_url": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=400&fit=crop", "description": "精选金枪鱼，浓郁汤汁。富含优质蛋白和水分，帮助猫咪补水。明太鱼味，增强食欲。", "sales_count": 312},

    # 宠物玩具
    {"name": "逗猫激光笔充电款", "category": "宠物玩具", "price": 28.0, "original_price": 38.0, "stock": 150, "brand": "宠趣", "spec": "USB充电款", "image_url": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=400&fit=crop", "is_featured": True, "description": "多模式激光灯，可切换红光/绿光。USB充电，续航持久。轻巧便携，逗猫神器。", "sales_count": 203},
    {"name": "耐咬网球狗玩具 3只装", "category": "宠物玩具", "price": 36.0, "stock": 85, "brand": "星之童话", "spec": "3只装 / 直径6cm", "image_url": "https://images.unsplash.com/photo-1544568100-847a948585b9?w=400&h=400&fit=crop", "description": "高弹耐磨面料，咬不烂。鲜艳颜色，吸引狗狗注意力。适合接球、拔河等多种游戏。", "sales_count": 87},
    {"name": "多层猫爬架大型", "category": "宠物玩具", "price": 299.0, "original_price": 399.0, "stock": 20, "brand": "爪爪星球", "spec": "高120cm / 5层", "image_url": "https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=400&h=400&fit=crop", "is_featured": True, "description": "天然剑麻缠绕，耐磨耐抓。多层设计，满足猫咪攀爬和休息需求。稳固底座，不易倾倒。", "sales_count": 56},
    {"name": "发声小鸭子洗澡玩具", "category": "宠物玩具", "price": 19.0, "stock": 100, "brand": "萌宠优品", "spec": "单只装", "image_url": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=400&fit=crop", "description": "可爱小黄鸭造型，捏压发声。吸引宠物注意力，让洗澡变得轻松有趣。材质安全，无毒无味。", "sales_count": 134},

    # 宠物窝笼
    {"name": "法莱绒冬季保暖猫窝", "category": "宠物窝笼", "price": 88.0, "original_price": 128.0, "stock": 40, "brand": "宠趣", "spec": "直径50cm", "image_url": "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=400&h=400&fit=crop", "is_featured": True, "description": "法莱绒内里，加倍保暖。侧开门设计，猫咪进出方便。可拆洗外套，清洁方便。", "sales_count": 178},
    {"name": "大型犬铁艺围栏狗笼", "category": "宠物窝笼", "price": 258.0, "stock": 15, "brand": "星之童话", "spec": "100×70×80cm", "image_url": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop", "description": "加粗铁艺管材，坚固耐用。网格设计，通风透气。带托盘，易清理。适合中大型犬。", "sales_count": 32},
    {"name": "猫隧道玩具可折叠", "category": "宠物窝笼", "price": 45.0, "stock": 60, "brand": "爪爪星球", "spec": "展开长150cm / 2个出口", "image_url": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=400&fit=crop", "description": "可折叠设计，收纳方便。多个出人口，增加趣味性。内置响纸，吸引猫咪探索。", "sales_count": 99},

    # 清洁护理
    {"name": "宠物专用沐浴露500ml", "category": "清洁护理", "price": 39.0, "original_price": 58.0, "stock": 120, "brand": "多美洁", "spec": "500ml 装", "image_url": "https://images.unsplash.com/photo-1587764379873-97837921fd44?w=400&h=400&fit=crop", "is_featured": True, "description": "弱酸性配方，温和不刺激。深层清洁，驱虫除螨。留香持久，宠物毛发柔顺亮泽。", "sales_count": 245},
    {"name": "宠物电动剃毛器充电式", "category": "清洁护理", "price": 79.0, "stock": 50, "brand": "科德士", "spec": "USB充电款 / 配4个限位梳", "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400&h=400&fit=crop", "description": "低噪音设计，宠物不害怕。USB充电，一次充电可用2小时。陶瓷刀头，锋利耐磨，不伤皮肤。", "sales_count": 87},
    {"name": "宠物指甲剪套装", "category": "清洁护理", "price": 25.0, "stock": 90, "brand": "宠趣", "spec": "5件套", "image_url": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=400&h=400&fit=crop", "description": "不锈钢刀口，锋利耐用。配有止血粉，安全剪甲。符合人体工学手柄，握感舒适。", "sales_count": 156},

    # 配饰装饰
    {"name": "猫咪项圈铃铛款", "category": "配饰装饰", "price": 18.0, "original_price": 28.0, "stock": 200, "brand": "萌宠优品", "spec": "可调节S/M/L", "image_url": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=400&fit=crop", "description": "精美铃铛设计，声音清脆。优质PU材质，柔软不勒脖。可调节扣，方便穿戴。", "sales_count": 267},
    {"name": "柴犬头像刺绣胸背带", "category": "配饰装饰", "price": 42.0, "stock": 55, "brand": "爪爪星球", "spec": "M码 / 适合5-12kg", "image_url": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop", "description": "可爱柴犬头像刺绣，萌力十足。透气网布面料，穿着舒适。胸前扣设计，牵引不勒脖。", "sales_count": 78},
    {"name": "猫咪圣诞头饰发夹 4件套", "category": "配饰装饰", "price": 22.0, "stock": 80, "brand": "萌宠优品", "spec": "4件套", "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop", "description": "4种圣诞主题头饰，节日拍照必备。弹性发夹，佩戴方便。材质轻便，宠物无负担。", "sales_count": 45},
    {"name": "宠物外出双肩背带包", "category": "配饰装饰", "price": 128.0, "original_price": 168.0, "stock": 35, "brand": "星之童话", "spec": "适合5kg以下宠物", "image_url": "https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=400&h=400&fit=crop", "is_featured": True, "description": "前开口设计，宠物视野开阔。透气网布，舒适不闷。可单肩可双肩，多种背法。", "sales_count": 112},
]


def seed():
    app = create_app()
    with app.app_context():
        # 创建分类
        cat_map = {}
        for c in CATEGORIES:
            existing = ProductCategory.query.filter_by(slug=c["slug"]).first()
            if not existing:
                cat = ProductCategory(**c)
                db.session.add(cat)
                db.session.flush()
                cat_map[c["name"]] = cat.id
            else:
                cat_map[c["name"]] = existing.id
        db.session.commit()

        # 创建商品
        added = 0
        for p in PRODUCTS:
            existing = Product.query.filter_by(name=p["name"]).first()
            if existing:
                continue
            cat_name = p.pop("category")
            p["category_id"] = cat_map.get(cat_name)
            product = Product(**p)
            db.session.add(product)
            added += 1
        db.session.commit()
        print(f"商城数据填充完成：{added} 个新商品，{len(CATEGORIES)} 个分类。")


if __name__ == "__main__":
    seed()
