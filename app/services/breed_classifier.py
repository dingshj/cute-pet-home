import os


def load_class_names(breeds_file):
    if not breeds_file or not os.path.isfile(breeds_file):
        return []
    with open(breeds_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def build_model(num_classes):
    import torch.nn as nn
    from torchvision import models

    m = models.resnet18(weights=None)
    m.fc = nn.Linear(m.fc.in_features, num_classes)
    return m


class BreedClassifierService:
    def __init__(self, model_path, breeds_file, device=None):
        self.model_path = model_path
        self.breeds_file = breeds_file
        self._device_str = device
        self._model = None
        self._device = None
        self._classes = load_class_names(breeds_file)
        self._transform = None

    def is_ready(self):
        return bool(self._classes) and os.path.isfile(self.model_path)

    def _lazy_torch(self):
        import torch
        from torchvision import transforms

        if self._device is None:
            self._device = self._device_str or (
                "cuda" if torch.cuda.is_available() else "cpu"
            )
        if self._transform is None:
            self._transform = transforms.Compose(
                [
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225],
                    ),
                ]
            )
        return torch

    def _ensure_model(self):
        if self._model is not None:
            return
        torch = self._lazy_torch()
        n = len(self._classes)
        if n == 0:
            return
        self._model = build_model(n)
        state = torch.load(self.model_path, map_location=self._device)
        self._model.load_state_dict(state)
        self._model.to(self._device)
        self._model.eval()

    def predict_topk(self, image_path, k=5):
        if not self.is_ready():
            return []
        try:
            torch = self._lazy_torch()
        except ImportError:
            return []
        self._ensure_model()
        from PIL import Image

        img = Image.open(image_path).convert("RGB")
        x = self._transform(img).unsqueeze(0).to(self._device)
        with torch.no_grad():
            logits = self._model(x)
            probs = torch.softmax(logits, dim=1)[0]
        top = torch.topk(probs, min(k, probs.numel()))
        out = []
        for i in range(top.indices.numel()):
            idx = int(top.indices[i])
            out.append((self._classes[idx], float(top.values[i])))
        return out
