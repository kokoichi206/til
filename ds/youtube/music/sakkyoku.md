# AI による作曲を学ぼう

## Work
- [音を鳴らしてみる](https://colab.research.google.com/drive/1psJDwYKibGn3SRvSEQCYJ8GxXruETvqz#scrollTo=-f3NugXcctpn)


## AI による作曲
- AI が学習する
  - 大量の曲の譜面を AI に読み込ませ、パターンを学習する
  - 作曲の３要素：スケール、コード、メロディ
- AI が曲を生成する
  - 曲調などの指示に基づき曲を生成
- 使われる AI 技術
  - RNN, VAE, GAN, Transformer, etc...

### AI による自動作曲サービス
- amper
- AWS DeepComposer
- Flow Machine Model


### [Magenta](https://magenta.tensorflow.org/)
- ライブラリ
- シンプルな曲を作る
- RNN による作曲
- 生成モデル（GAN、VAE）による作曲
- Music Transformer の利用

### Magenta のモデル
- Melody RNN
  - 再帰型ニューラルネットワークの一種、LSTM を用いたメロディの生成
  - 直近の note の並びから次の note が予想される
- Music VAE
  - 変分オートエンコーダ（VAE）を用いた音楽生成
- GANSynth
  - 敵対的生成ネットワークを用いてオーディオを合成
- Image Stylization
  - アーティスティックに表現された写真を生成
- Sketch RNN
  - スケッチを生成する RNN


## sec 3

### RNN
- Reccurent Neural Network
- 入力と正解が「時系列データ」となる
- 中間層が「再帰」の構造を持つ
  - 全てのパラメータは共有される

### LSTM
- Long Short-Term Memory
- RNN の一種
  - RNN のの全結合層の代わりに、LSTM 層が使われている
- 記憶セルの導入による、長期の情報保持
- Magenta でも多く使われている

### Magenta の RNN 音楽生成モデル
- Melody RNN
- Drums RNN
- Improv RNN
- Polyphony RNN
  - バッハ風の、和音を繋いで進行する曲を生成する
- Pianoroll RNN-NADE
- Performance RNN
  - 音の強弱やタイミングなどの微妙な表現まで変化する高度な曲の生成

