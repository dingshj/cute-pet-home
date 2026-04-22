"""
将 Oxford-IIIT Pet 公开数据集整理为 data/train/<品种英文名>/ 结构，供 train_transfer.py 使用。

特点：
  - 无需自己从网页一张张存图；首次运行会自动下载数据集（学术用途常见，请保留论文中的数据集引用说明）。
  - 品种名为英文（如 Abyssinian、American_Bulldog），与论文中写「基于 Oxford-IIIT Pet」一致。

用法（在项目根目录）：
  python scripts/prepare_oxford_pet.py

默认输出到 data/train_oxford（不会覆盖你手写的 data/train）。训练时：
  python scripts/train_transfer.py --data-dir data/train_oxford

可选：每类最多拷贝多少张（加快试验）：
  python scripts/prepare_oxford_pet.py --max-per-class 50

--------------------------------------------------------------------
【下载太慢时：手动下载 + 解压（与 torchvision 一致）】

1）用浏览器、迅雷、IDM 等下载下面两个文件（与官方一致，约共 800MB）：
   https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
   https://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz

2）在项目下建好目录（默认 download-root 为 data/oxford_iiit_pet_raw）：
   data/oxford_iiit_pet_raw/oxford-iiit-pet/

3）把两个 .tar.gz 放进任意位置解压，使最终存在：
   data/oxford_iiit_pet_raw/oxford-iiit-pet/images/     （大量 .jpg）
   data/oxford_iiit_pet_raw/oxford-iiit-pet/annotations/（含 trainval.txt 等）

   若解压多出一层目录，请调整直到满足上面两个文件夹路径。

4）不再走在线下载，执行：
   python scripts/prepare_oxford_pet.py --no-download

若之前自动下载到一半，可先删掉不完整的 data/oxford_iiit_pet_raw 再按上面重来。
--------------------------------------------------------------------
"""
import argparse
import os
import shutil
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)


def safe_folder_name(name):
    for c in '\\/:*?"<>|':
        name = name.replace(c, "_")
    return name.strip() or "class"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=str,
        default=os.path.join(root, "data", "train_oxford"),
        help="输出 ImageFolder 根目录（存在则先删除再写入，请避免指向已手工整理的数据）",
    )
    parser.add_argument(
        "--download-root",
        type=str,
        default=os.path.join(root, "data", "oxford_iiit_pet_raw"),
        help="torchvision 下载与解压目录",
    )
    parser.add_argument(
        "--max-per-class",
        type=int,
        default=0,
        help="每类最多导出多少张，0 表示不限制",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="不联网下载；请先将数据集解压到 <download-root>/oxford-iiit-pet/（见脚本顶部说明）",
    )
    args = parser.parse_args()

    try:
        from torchvision.datasets import OxfordIIITPet
    except ImportError as e:
        print("请先安装: pip install torch torchvision", file=sys.stderr)
        raise SystemExit(1) from e

    if args.no_download:
        print("使用本地数据（--no-download），不联网下载…")
    else:
        print("正在下载或加载 Oxford-IIIT Pet（trainval）…")
    ds = OxfordIIITPet(
        root=args.download_root,
        split="trainval",
        target_types="category",
        download=not args.no_download,
    )

    if os.path.isdir(args.out):
        shutil.rmtree(args.out)
    os.makedirs(args.out, exist_ok=True)

    counts = {}
    for i in range(len(ds)):
        img, label = ds[i]
        label = int(label)
        cls_name = safe_folder_name(ds.classes[label])
        if args.max_per_class > 0:
            counts.setdefault(cls_name, 0)
            if counts[cls_name] >= args.max_per_class:
                continue
            counts[cls_name] += 1

        sub = os.path.join(args.out, cls_name)
        os.makedirs(sub, exist_ok=True)
        out_path = os.path.join(sub, f"{i:05d}.jpg")
        img.save(out_path, quality=95)

    n_classes = len({d for d in os.listdir(args.out) if os.path.isdir(os.path.join(args.out, d))})
    n_files = sum(
        len([f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        for _, _, files in os.walk(args.out)
    )
    print(f"完成：{n_classes} 个类别，共 {n_files} 张图，已写入：{args.out}")
    print("下一步：")
    print(f'  python scripts/train_transfer.py --data-dir "{args.out}" --epochs 15')


if __name__ == "__main__":
    main()
