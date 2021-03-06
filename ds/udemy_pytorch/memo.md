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


### MLP: Multi-layer perceptron
- Simple perceptron can only solve linearly separable problems
- Input Layer -> Hidden Layers -> Output Layer

### loss fn
0 or 1 の分類 ⇨ binary cross entropy

One hidden layer can solve non-linearly separable problems


## FCNN: Fully Connected NN

### ReLU: Rectified Linear Unit
- Rectified: 修正済みの線形関数！
    - 線形だと、重ねる意味がなくなる
- sigmoid はほとんどで微分が０なので、多層になった場合に back propagation が効かない。
    - ReLU は正の部分で全て１！！

Why ReLU?

- Avoid the problem of vanishing gradients during back propagation as the dervative becomes 1


### Loss fn
Multi class classification task -> CrossEntropyLoss


## CNN
Convolutional Neural Network

Fashion MNIST

### Dropout
Overfitting can be avoided.

### 疑問
このやり方で、val データが train データに混ざってない？？


## RNN
- RNN has a structure with closed paths inside
- The state of the previous hidden layer and the current input determine the current hidden layer and output
- It can handle sequential data which has time dependency
- It can also handle image data
- LSTM/GRU can learn long time temporal relationships, but it has basically the same structure as RNN


## Sesame Street Transformers

### T5
Examples of text-to-text are

1. translation
1. question and answering
1. classification
1. summarization



## Pytorch

``` python
import torch

x = torch.Tensor([1, 2, 3])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(x)
x = x.to(device)
print(x)
```

### Data Preparation
``` python
fashon_mnist_train = FashionMNIST("FashionMNIST", train=True, download=True, transform=transforms.ToTensor())
fashon_mnist_test = FashionMNIST("FashionMNIST", train=False, download=True, transform=transforms.ToTensor())
```

