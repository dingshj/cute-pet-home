"""
迁移学习训练脚本：按文件夹类别组织图片后运行。

目录结构示例：
  data/train/金毛寻回犬/*.jpg
  data/train/泰迪/*.jpg

训练完成后会写入：
  - instance/breed_classifier.pt（权重）
  - instance/breeds.txt（与训练类别顺序一致，供 Web 推理使用）
"""
import argparse
import os
import sys

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, models, transforms


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=str,
        default=os.path.join(root, "data", "train"),
        help="ImageFolder 根目录（子文件夹名为品种名）",
    )
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument(
        "--out-weights",
        type=str,
        default=os.path.join(root, "instance", "breed_classifier.pt"),
    )
    parser.add_argument(
        "--out-breeds",
        type=str,
        default=os.path.join(root, "instance", "breeds.txt"),
    )
    args = parser.parse_args()

    if not os.path.isdir(args.data_dir):
        print(f"数据目录不存在: {args.data_dir}", file=sys.stderr)
        sys.exit(1)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tfm = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    full = datasets.ImageFolder(args.data_dir, transform=tfm)
    if len(full.classes) < 2:
        print("至少需要 2 个类别文件夹用于分类任务。", file=sys.stderr)
        sys.exit(1)

    n = len(full)
    n_val = max(1, int(0.15 * n))
    n_train = n - n_val
    g = torch.Generator().manual_seed(42)
    train_set, val_set = random_split(full, [n_train, n_val], generator=g)

    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False, num_workers=0)

    num_classes = len(full.classes)
    try:
        w = models.ResNet18_Weights.IMAGENET1K_V1
        model = models.resnet18(weights=w)
    except Exception:
        model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.to(device)

    for name, param in model.named_parameters():
        if not name.startswith("fc"):
            param.requires_grad = False

    opt = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=args.lr)
    crit = nn.CrossEntropyLoss()

    best_acc = 0.0
    for epoch in range(args.epochs):
        model.train()
        total_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            opt.zero_grad()
            logits = model(x)
            loss = crit(logits, y)
            loss.backward()
            opt.step()
            total_loss += loss.item() * x.size(0)

        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                pred = model(x).argmax(dim=1)
                correct += (pred == y).sum().item()
                total += y.size(0)
        acc = correct / max(total, 1)
        avg_loss = total_loss / max(n_train, 1)
        print(f"epoch {epoch + 1}/{args.epochs}  loss={avg_loss:.4f}  val_acc={acc:.4f}")
        if acc >= best_acc:
            best_acc = acc
            torch.save(model.state_dict(), args.out_weights)

    os.makedirs(os.path.dirname(args.out_weights), exist_ok=True)
    with open(args.out_breeds, "w", encoding="utf-8") as f:
        for c in full.classes:
            f.write(c + "\n")
    print(f"已保存权重: {args.out_weights}")
    print(f"已写入品种列表: {args.out_breeds}（顺序须与训练时 ImageFolder 一致）")


if __name__ == "__main__":
    main()
