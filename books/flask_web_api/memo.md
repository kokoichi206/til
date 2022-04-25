## sec 13
``` sh
# for mac
pip install torch torchvision torchaudio
```

``` sh
python
>>
import torch
import torchvision
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
torch.save(model, "model.pt")
```


