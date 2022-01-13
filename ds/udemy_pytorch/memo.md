## DL
- dendride
    - Input
- Cell body
    - Output Judgement
- axon
    - Output

### The perceptron
- A mathematical model of a neuron
- The smallest component unit of DL

### Network trainable
1. Normalize data
2. Change Activation Function
3. Use Loss FUnction
4. Adjust weight by Gradient Descent



## Pytorch

```
import torch

x = torch.Tensor([1, 2, 3])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(x)
x = x.to(device)
print(x)
```

