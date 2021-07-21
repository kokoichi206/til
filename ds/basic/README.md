### Interpreting the Weights
- Neural nets have faced criticism for not being interpretable
- This lack of interpretability is not a limitation of neural networks, but a limitaion in understanding of geometry
- Neural networks are "not not interpretable"

### sigmoid and tanh
$$
\tanh(x) = \frac{e^{x}-e^{-x}}{e^{x}+e^{-x}} \\
= \frac{-(e^{-x}+e^{x})+2e^{x}}{e^{x}+e^{-x}} \\
= -1 + 2\frac{e^{x}}{e^{x}+e^{-x}} \\
= -1 + 2\frac{1}{1+e^{-2x}} \\
= -1 + 2\sigma(2x)
$$

### What about a neural network?
- sigmoid/tanh/etc.. makes it nonlinear
- cannot ignore nonlinearities
- Otherwise, we just end up with a linear model
- Which is just a single neuron

### One last oddity
- You know we like batch operations
- You now know how to do them

### How to train
1. Define the cost J
2. Find dJ/dw, will give us some expression for updating w
3. Implement (2) in code




## English
see the forest for the trees

This stuff looks totally crazy to me!
