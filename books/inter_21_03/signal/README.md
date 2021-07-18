# Pythonで信号処理
Garbage in, Garbage out

## 時系列データには信号処理が必須
- 一般にセンサから取得した時系列信号には目的外の信号が混入している

## 脳波？
- 人は閉眼すると視覚関連の活動が停止するため、脳のアイドリング状態を示す8~13Hzのα波が観測される
- 脳波は睡眠深度によって周波数が変わるため、周波数解析は睡眠ステージの判定など、実際の臨床の場でも用いられる
- 基礎律動と呼ばれる脳波は0.5~30Hz

## フィルタ

### バンドパスフィルタ
- ハイパスフィルタ * ローパスフィルタ


### ハイパス/ローパスのリアルでの回路
[記事書いた](https://koko206.hatenablog.com/entry/2021/07/18/232743?_ga=2.237843015.699704037.1626609650-1799626807.1626609650)

## calc
$$
V_{in}(t) = \frac{1}{C}\int I(t)dt + V_{out}(t)
$$

$V_{out}$の部分は出力電圧を測定するのみで、電流は流れないと考えると、抵抗側にも$I(t)$の電流が流れるから
$$
V_{out}(t) = RI(t)
$$

$$
V_{in}(t) = \frac{1}{RC}\int_{-\infty}^{t} V_{out}(t')dt' + V_{out}(t)
$$

$$
\lim_{p\to \infty}\frac{1}{2\pi i}\int_{c-ip}^{c+ip}f(t)e^{st}dt
$$

$$
F(s) = \int_0^\infty f(t)e^{-st}dt
$$

$$
\int V_{in}(s)e^{st}ds = \frac{1}{RC}\int V_{out}(s)\left(\int_{-\infty}^{t} e^{st'}dt'\right)ds + \int V_{out}(s)e^{st}ds
$$

$$
\int_0^\infty e^{st'}dt' = \left[\frac{1}{s} e^{st'}\right]_{t'=-\infty}^{t'=t} = \frac{1}{s}e^{st}
$$

$$
\int V_{in}(s)e^{st}ds = \frac{1}{sRC}\int V_{out}(s)e^{st}ds + \int V_{out}(s)e^{st}ds
$$

単純に中身だけ比較して良いのか？（ラプラス変換２回で戻る性質！）

$$
V_{in}(s) = \left(\frac{1}{sRC} + 1\right)V_{out}(t)
$$

$$
\left|\frac{V_{out}}{V_{out}}\right| = \left|\frac{1}{\frac{1}{i\omega RC} + 1}\right| = \frac{1}{\sqrt{1+(\frac{1}{\omega RC})^2}}
$$

$$
\left|\frac{V_{out}}{V_{out}}\right| \to 1 \quad (\omega\to 0) \\
\left|\frac{V_{out}}{V_{out}}\right| \to 0 \quad (\omega\to\infty)
$$

$$
\left|\frac{V_{out}}{V_{out}}\right| = \left|\frac{1}{\frac{i\omega L}{R} + 1}\right| = \frac{1}{\sqrt{1+(\frac{\omega L}{R})^2}}
$$

$$

$$
