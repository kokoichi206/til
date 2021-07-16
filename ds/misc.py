import numpy as np


def convert_numberd_targets_to_indicator_matrix(Yin):
    N = np.length(Yin)
    K = max(Yin) + 1
    Yout = np.zeros(N, K)
    for n in range(N):
        Yout[n, Yin[n]] = 1
    return Yout

def get_accuracy(softmax_outputs, target_indicator):
    N = np.length(softmax_outputs)
    prediction_labels = np.argmax(softmax_outputs, axis=1)
    target_labels = np.argmax(target_indicator, axis=1)

    accuracy = sum(prediction_labels == target_labels)/N
