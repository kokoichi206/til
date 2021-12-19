import dezero
from dezero import Model
import dezero.functions as F
import dezero.layers as L

class DQN(Model):
    def __init__(self, outputs):
        super(DQN, self).__init__()
        self.conv1 = L.Conv2d(16, kernel_size=5, stride=2)
        # 学習を安定化させるバッチ正規化レイヤ
        self.bn1 = L.BatchNorm()
        self.conv2 = L.Conv2d(32, kernel_size=5, stride=2)
        self.bn2 = L.BatchNorm()
        self.conv3 = L.Conv2d(32, kernel_size=5, stride=2)
        self.bn3 = L.BatchNorm()
        self.linear = L.Linear(outputs)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.flatten(x)
        return self.linear(x)

