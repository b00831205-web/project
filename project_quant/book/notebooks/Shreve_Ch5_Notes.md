# Shreve《Stochastic Calculus for Finance I》Ch.5 学习笔记
## 随机游走 / Random Walk

> **一句话主线**:对称随机游走是**布朗运动的离散版**,本章用它打磨两件后面定价奇异期权要反复用的工具,再落到一个最优停止应用。三条线:
> 1. **首达时的鞅方法 (First passage via martingale)**:构造指数鞅 $S_n=e^{\sigma M_n}/(\cosh\sigma)^n$,停在首达时 $\tau_m$,推出 $\tau_m$ 的矩母函数与分布。惊人结论:$\mathbb{P}\{\tau_m<\infty\}=1$ 但 $\mathbb{E}\tau_m=\infty$(常返却"零常返")。
> 2. **反射原理 (Reflection principle)**:用路径反射数路径,给出 $\tau_m$ 分布的组合证明——连续时间里正是障碍/回望期权定价的钥匙。
> 3. **永续美式 put (Perpetual American put)**:无到期日 ⟹ 价只依赖股价不依赖时间,最优停止退化为一个 **Bellman 方程**(动态规划),衔接第 4 章离散与 Vol II 连续时间。
>
> 记号:$X_j=\pm1$(H/T),$M_0=0,M_n=\sum_{j=1}^nX_j$;$\tau_m=\min\{n:M_n=m\}$ 首达时;$p,q$ 上/下行概率(对称 $p=q=\tfrac12$);$\cosh\sigma=\tfrac{e^\sigma+e^{-\sigma}}{2}$。

---

# §0 速查公式表(写项目时直接查)/ Formula Cheat Sheet

### 0.1 随机游走与指数鞅 / Random walk & exponential martingale

| 量 | 公式 |
|---|---|
| 对称随机游走 | $M_n=\sum_{j=1}^n X_j$,$X_j=\pm1$,既是**鞅**也是**马尔可夫过程** |
| 首达时 | $\tau_m=\min\{n:M_n=m\}$(永不到达则 $=\infty$),是停时 |
| 指数鞅 (Lemma 5.2.1) | $S_n=e^{\sigma M_n}\Big(\dfrac{2}{e^\sigma+e^{-\sigma}}\Big)^n=\dfrac{e^{\sigma M_n}}{(\cosh\sigma)^n}$,对任意 $\sigma$ 是鞅 |

### 0.2 首达时分布(对称游走)/ First passage time distribution

| 量 | 公式 |
|---|---|
| 几乎必达 (Thm 5.2.2) | $\mathbb{P}\{\tau_m<\infty\}=1$(任意非零整数 $m$) |
| 期望无穷 (Cor 5.2.4) | $\mathbb{E}\tau_m=\infty$ —— **常返但零常返** |
| 矩母函数 (Thm 5.2.3) | $\mathbb{E}[\alpha^{\tau_m}]=\Big(\dfrac{1-\sqrt{1-\alpha^2}}{\alpha}\Big)^{\lvert m\rvert},\ \alpha\in(0,1)$ |
| $\tau_1$ 分布 (5.2.22) | $\mathbb{P}\{\tau_1=2j-1\}=\dfrac{(2j-2)!}{j!(j-1)!}\Big(\dfrac12\Big)^{2j-1}$ |
| 非对称 $\tau_1$ (5.2.23) | $\mathbb{P}\{\tau_1=2j-1\}=\dfrac{(2j-2)!}{j!(j-1)!}\,p^j q^{j-1}$ |

### 0.3 反射原理 / Reflection principle

$$\mathbb{P}\{\tau_1\le 2j-1\}=\mathbb{P}\{M_{2j-1}=1\}+2\,\mathbb{P}\{M_{2j-1}\ge3\}=1-\mathbb{P}\{M_{2j-1}=-1\}$$
> 思想:到达 $m$ 后把路径反射,"末端超过 $m$ 的反射路径"与"中途达 $m$、末端低于 $m$ 的路径"一一对应 ⟹ 可数出"曾达 $m$"的路径数。连续时间里用于**障碍期权 / 回望期权 / 走势与最大值联合分布**。

### 0.4 永续美式 put 的 Bellman 方程 / Perpetual American put

模型 $u=2,d=\tfrac12,r=\tfrac14\Rightarrow\tilde p=\tilde q=\tfrac12$,$S_n=S_0 2^{M_n}$,put $K=4$,无到期。

| 量 | 公式 |
|---|---|
| 按"跌到 $4\cdot2^{-m}$ 才行权"的价 (5.4.3) | $V^{(\tau_{-m})}=4(1-2^{-m})\big(\tfrac12\big)^m$ ;在 $m=1$ 取最大 |
| **最优策略** | 股价**首次跌到 2** 时行权 |
| 价值函数 (5.4.6/5.4.11) | $v(s)=4-s\ (s\le2),\quad v(s)=\dfrac4s\ (s\ge4)$ |
| **Bellman 方程 (5.4.13)** | $v(s)=\max\Big\{4-s,\ \tfrac45\big[\tfrac12 v(2s)+\tfrac12 v(\tfrac s2)\big]\Big\}$ |
| 一般形式 (5.4.16) | $v(s)=\max\Big\{g(s),\ \tfrac{1}{1+r}\big[\tilde p\,v(us)+\tilde q\,v(ds)\big]\Big\}$ |
| put 边界条件 (5.4.17) | $\lim_{s\downarrow0}v(s)=K,\quad \lim_{s\to\infty}v(s)=0$ |
| call 边界条件 (5.4.18) | $\lim_{s\downarrow0}v(s)=0,\quad \lim_{s\to\infty}\tfrac{v(s)}{s}=1$ |

> Bellman 有**多余解**(如 $w(s)=4/s$ 也满足),必须用**边界条件**挑出我们要的最小解 $v$。

### 0.5 教材数值算例 / Canonical numbers
$V^{(\tau_{-1})}=1,\ V^{(\tau_{-2})}=\tfrac34,\ V^{(\tau_{-3})}=\tfrac7{16}$(故 $m=1$ 最优);价值函数 $v(0.5)=3.5,v(1)=3,v(2)=2,v(4)=1,v(8)=0.5,v(16)=0.25$(§6 的 DP 代码可对拍)。

---

# §1 随机游走基础 / Random Walk Basics(§5.1）
重复抛公平硬币,$X_j=+1$(H)或 $-1$(T),$M_n=\sum_{j=1}^n X_j$ 每步上/下一格。
- **对称随机游走**($p=\tfrac12$)既是**鞅**又是**马尔可夫过程**;$p\ne\tfrac12$ 则为**非对称**随机游走(路径集合相同,只是概率不同)。
- 它是**布朗运动的离散原型**:首达时、反射原理在连续时间里直接对应,并用于奇异期权定价。

---

# §2 首达时:鞅方法 / First Passage Times(§5.2）

### 2.1 指数鞅 / The exponential martingale(Lemma 5.2.1)
对任意 $\sigma$,$S_n=e^{\sigma M_n}\big(\tfrac{2}{e^\sigma+e^{-\sigma}}\big)^n$ 是鞅。
> 证:$\mathbb{E}_n[S_{n+1}]=S_n\cdot\tfrac{2}{e^\sigma+e^{-\sigma}}\cdot\mathbb{E}[e^{\sigma X_{n+1}}]=S_n\cdot\tfrac{1}{\cosh\sigma}\cdot\tfrac12(e^\sigma+e^{-\sigma})=S_n$(取出已知 + 独立性)。

### 2.2 几乎必达 / Reaches the level a.s.(Thm 5.2.2)
停在 $\tau_m$:$S_{n\wedge\tau_m}$ 仍是鞅,$\mathbb{E}[S_{n\wedge\tau_m}]=S_0=1$。设 $\sigma>0$,因 $0<\tfrac{2}{e^\sigma+e^{-\sigma}}<1$,令 $n\to\infty$ 再令 $\sigma\downarrow0$,得
$$\mathbb{P}\{\tau_m<\infty\}=1$$
即对称随机游走**几乎必然到达任意非零整数 $m$**。但仍有(不可数无穷多条)永不达 $m$ 的路径,只是总概率为 0。

### 2.3 矩母函数与期望 / MGF & expectation
**Thm 5.2.3**:$\mathbb{E}[\alpha^{\tau_m}]=\big(\tfrac{1-\sqrt{1-\alpha^2}}{\alpha}\big)^{\lvert m\rvert}$。由 $\alpha=\tfrac{2}{e^\sigma+e^{-\sigma}}$ 解出 $e^{-\sigma}=\tfrac{1-\sqrt{1-\alpha^2}}{\alpha}$ 代入而得。
**Cor 5.2.4**:$\mathbb{E}\tau_m=\infty$(对 $\mathbb{E}[\alpha^{\tau_1}]$ 求导、令 $\alpha\uparrow1$ 得)。
> **关键反直觉**:$\tau_m$ 以概率 1 有限,但**期望无穷**——这正是一维对称随机游走"**零常返 (null recurrent)**"的体现:必回来,但平均回来时间无穷长。

### 2.4 $\tau_1$ 的分布 / Distribution of $\tau_1$
$M_n$ 只能在奇数步首次达 1,$\mathbb{E}[\alpha^{\tau_1}]=\sum_{j\ge1}\alpha^{2j-1}\mathbb{P}\{\tau_1=2j-1\}$;对 $\tfrac{1-\sqrt{1-\alpha^2}}{\alpha}$ 做 Taylor 展开、逐项比较系数,得
$$\mathbb{P}\{\tau_1=2j-1\}=\frac{(2j-2)!}{j!(j-1)!}\Big(\frac12\Big)^{2j-1}$$
验证:$\mathbb{P}\{\tau_1=1\}=\tfrac12$(首掷 H);$\mathbb{P}\{\tau_1=3\}=(\tfrac12)^3$(THH);$\mathbb{P}\{\tau_1=5\}=2(\tfrac12)^5$(THTHH 或 TTHHH)。系数 $\tfrac{(2j-2)!}{j!(j-1)!}$ 数的是"$2j{-}1$ 步首次达 1"的路径数。非对称版把每条路径概率换成 $p^jq^{j-1}$(Thm 5.2.5)。

---

# §3 反射原理 / Reflection Principle(§5.3）
第二种证 $\tau_1$ 分布的方法,纯组合。对每条在 $\tau_1\le2j-1$ 达 1 的路径,从 $\tau_1$ 起做**镜像反射**(上下互换)。
- "末端超过 1 的反射路径" ↔ "中途达 1 但末端低于 1 的原路径",一一对应。
- 故 $\mathbb{P}\{\tau_1\le2j-1\}=\mathbb{P}\{M_{2j-1}=1\}+2\mathbb{P}\{M_{2j-1}\ge3\}=1-\mathbb{P}\{M_{2j-1}=-1\}$。
- 代入 $\mathbb{P}\{M_{2j-1}=-1\}=(\tfrac12)^{2j-1}\tfrac{(2j-1)!}{j!(j-1)!}$,做差 $\mathbb{P}\{\tau_1=2j-1\}=\mathbb{P}\{\tau_1\le2j-1\}-\mathbb{P}\{\tau_1\le2j-3\}$,重新得到 (5.2.22)。

> **为什么重要**:反射原理同时给出"游走当前值"与"其历史最大值"的**联合分布**——连续时间里这就是**障碍期权 (barrier) 与回望期权 (lookback)** 定价的核心(对应布朗运动的反射原理)。

---

# §4 永续美式 put:Bellman 方程 / Perpetual American Put(§5.4）

### 4.1 设定 / Setup
$u=2,d=\tfrac12,r=\tfrac14\Rightarrow\tilde p=\tilde q=\tfrac12$,$S_n=S_0 2^{M_n}$($M_n$ 在风险中性下对称),put $K=4$,**无到期日**。
"永续" ⟹ 价只依赖股价、不依赖时间;最优行权策略也只依赖股价。这是离散与连续时间最优停止之间的桥。

### 4.2 用首达时矩母函数算各行权策略的价 / Value of threshold policies
若"股价首次跌到 $4\cdot2^{-m}$"才行权(即随机游走首次到 $-m$),用 Thm 5.2.3 取 $\alpha=\tfrac45$($\tfrac{1-\sqrt{1-\alpha^2}}{\alpha}=\tfrac12$):
$$V^{(\tau_{-m})}=4(1-2^{-m})\tilde{\mathbb{E}}\big[(\tfrac45)^{\tau_{-m}}\big]=4(1-2^{-m})\big(\tfrac12\big)^m$$
$V^{(\tau_{-1})}=1,\ V^{(\tau_{-2})}=\tfrac34,\ V^{(\tau_{-3})}=\tfrac7{16}$ → **在 $m=1$ 最大** ⟹ 猜测最优:股价**首次跌到 2** 时行权。

### 4.3 价值函数与三条性质 / Value function & three properties
$$v(s)=\begin{cases}4-s,&s\le2\\[2pt]\dfrac4s,&s\ge4\end{cases}$$
验证(对应第 4 章 Thm 4.4.2):(i) $v(s)\ge(4-s)^+$;(ii) 折现 $(\tfrac45)^n v(S_n)$ 是上鞅;(iii) 最小。
- **行权区**($s\le2$):严格上鞅 → 立即行权;**等待区**($s\ge4$):鞅;**边界** $s=2$:严格上鞅 → 在 2 处就该行权。

### 4.4 Bellman 方程 / The Bellman equation
把上述三条压缩成一个方程(就是第 4 章美式逆推 (4.2.6) 的"去掉时间下标"版):
$$v(s)=\max\Big\{4-s,\ \tfrac45\big[\tfrac12 v(2s)+\tfrac12 v(\tfrac s2)\big]\Big\}$$
一般地:$v(s)=\max\{g(s),\ \tfrac{1}{1+r}[\tilde p\,v(us)+\tilde q\,v(ds)]\}$ (5.4.16)。
> **多余解问题**:$w(s)=4/s$ 也满足该方程。Bellman 方程不能唯一确定 $v$,必须叠加**边界条件**(put:$s\downarrow0\Rightarrow v\to K$,$s\to\infty\Rightarrow v\to0$)挑出最小解。这与连续时间里"自由边界 + smooth pasting / 光滑粘合"的思想一致。

---

# §5 面试速答 / Interview Quick-Fire

**Q1. 一维对称随机游走是常返的吗?$\mathbb{E}\tau_m$ 是多少?**
A:常返——$\mathbb{P}\{\tau_m<\infty\}=1$,几乎必然回到任意水平;但 $\mathbb{E}\tau_m=\infty$,即**零常返 (null recurrent)**:必回来,平均回来时间却无穷长。

**Q2. 怎么用鞅求首达时的分布?**
A:构造指数鞅 $S_n=e^{\sigma M_n}/(\cosh\sigma)^n$,停在 $\tau_m$ 用可选抽样保持期望 $=1$,令 $n\to\infty$ 得 $\mathbb{E}[\alpha^{\tau_m}]=(\tfrac{1-\sqrt{1-\alpha^2}}{\alpha})^{|m|}$,即矩母函数,展开即分布。

**Q3. 反射原理是什么?有什么用?**
A:到达水平后把路径镜像反射,使"曾达该水平"的路径可被计数。给出走势与其**历史最大值的联合分布**,是连续时间**障碍 / 回望期权**定价的核心工具。

**Q4. 什么是永续美式期权?为什么它的价不依赖时间?**
A:无到期日的美式期权。由于没有"剩余期限"这个状态,价与最优行权策略都只依赖当前股价,最优停止退化成一个时间无关的 **Bellman 方程**。

**Q5. Bellman 方程怎么解最优停止?行权区 vs 等待区?**
A:$v(s)=\max\{g(s),\ \text{折现等待价值}\}$。$v=g$ 处是**行权区**(折现价严格上鞅);$v>g$ 处是**等待区**(折现价鞅)。两区边界即最优行权阈值。

**Q6. 为什么 Bellman 方程要配边界条件?**
A:方程本身有多余解(如永续 put 里 $w(s)=4/s$)。需用边界条件($s\downarrow0\Rightarrow v\to K$,$s\to\infty\Rightarrow v\to0$)及格子结构挑出**最小解**,即真实价值函数。连续时间里对应自由边界 + smooth pasting。

**Q7. 随机游走与布朗运动什么关系?**
A:对称随机游走是布朗运动的离散版;首达时、反射原理、最优停止/自由边界等结论都能从离散平移到连续(Vol II)。永续美式 put 正是这种"离散→连续"过渡的范例。

---

# §6 Bellman 方程的动态规划实现 / DP Implementation

下面用 **value iteration(值迭代)** 解 §4.4 的 Bellman 方程。因为有折现因子 $\tfrac{1}{1+r}<1$,Bellman 算子是压缩映射;在截断格子 $s=2^j$ 上配好边界条件后,从内在价值出发**自下而上**迭代,收敛到**最小解**(即真实价值函数)。这套写法可直接推广到一般 $u,d,r,K$ 与任意 payoff $g$。

```python
def perpetual_american_put_dp(K=4.0, u=2.0, d=0.5, r=0.25,
                              j_min=-12, j_max=40, tol=1e-13, max_iter=200000):
    """
    动态规划求解永续美式 put 的 Bellman 方程:
        v(s) = max{ (K-s)^+ , (1/(1+r)) [ p~ v(u s) + q~ v(d s) ] }
    格子 s = 2^j (因 u=2, d=1/2);风险中性 p~=q~=1/2。
    边界条件:s->0 时 v->K(深度价内,立即行权);s->inf 时 v->0。
    返回最小解(真实价值函数)。
    """
    p = (1 + r - d) / (u - d)          # 风险中性上行概率 p~
    q = 1 - p                          # 风险中性下行概率 q~
    disc = 1.0 / (1 + r)               # 单步折现因子
    js = list(range(j_min, j_max + 1))
    s = {j: 2.0 ** j for j in js}                  # 股价格子 s=2^j
    g = {j: max(K - s[j], 0.0) for j in js}        # 内在价值 (put 的 payoff)
    v = dict(g)                                    # 初值取内在价值 → 收敛到最小解

    for it in range(max_iter):
        diff = 0.0
        v_new = dict(v)
        for j in js:
            if j == j_min or j == j_max:           # 固定边界(体现边界条件)
                continue
            cont = disc * (p * v[j + 1] + q * v[j - 1])   # 等待价值 continuation
            val = max(g[j], cont)                          # Bellman: 行权 vs 等待
            diff = max(diff, abs(val - v[j]))
            v_new[j] = val
        v = v_new
        if diff < tol:                              # 收敛即停
            break
    return s, g, v, it

# --- 运行并对拍教材 (5.4.6) ---
s, g, v, iters = perpetual_american_put_dp()
print(f"converged in {iters} iterations\n")
print(f"{'s=2^j':>8} {'intrinsic':>10} {'DP v(s)':>9} {'textbook':>9} {'region':>10}")
for j in range(-1, 5):
    sj = 2.0 ** j
    book = (4 - sj) if j <= 1 else 4.0 / sj
    region = "exercise" if v[j] <= g[j] + 1e-9 and g[j] > 0 else "continue"
    print(f"{sj:>8.3f} {g[j]:>10.4f} {v[j]:>9.4f} {book:>9.4f} {region:>10}")
```

**运行结果**(完全复现教材 5.4.6):

```
converged in 112 iterations

   s=2^j  intrinsic   DP v(s)  textbook     region
   0.500     3.5000    3.5000    3.5000   exercise
   1.000     3.0000    3.0000    3.0000   exercise
   2.000     2.0000    2.0000    2.0000   exercise
   4.000     0.0000    1.0000    1.0000   continue
   8.000     0.0000    0.5000    0.5000   continue
  16.000     0.0000    0.2500    0.2500   continue
```

**几个实现要点**:
1. **格子选 $s=2^j$**:因 $u=2,d=\tfrac12$,股价乘 $u$/除 $d$ 都只是 $j\mapsto j\pm1$,Bellman 更新天然落在格点上,无需插值。
2. **边界条件 = 固定两端不更新**:$j_{\min}$ 端深度价内,$v\approx K$;$j_{\max}$ 端深度价外,$v\approx0$。这一步正是排除多余解 $w(s)=4/s$ 的关键。
3. **从内在价值初始化、自下而上迭代** ⟹ 收敛到 Bellman 算子**最小不动点**,即满足三性质 (i)(ii)(iii) 的真实价值。
4. **行权区/等待区自动浮现**:输出里 $s\le2$ 标 `exercise`($v=g$,折现价严格上鞅)、$s\ge4$ 标 `continue`($v>g$,折现价鞅),边界阈值正是 $s=2$。
5. **可推广**:把 `g` 换成 call 的 $(s-K)^+$、改边界条件 (5.4.18),即可定价永续美式 call(见 Ex 5.8);改 $u,d,r$ 适配任意二叉树。

---

### 附:小结 / Summary(§5.5）
对称随机游走首达时 $\tau_m$:$\mathbb{P}\{\tau_m<\infty\}=1$ 但 $\mathbb{E}\tau_m=\infty$;矩母函数 (5.2.13)、分布 (5.2.23) 可由鞅方法或反射原理求得。永续美式 put 用首达时矩母函数评估阈值策略、取最优阈值,再验证三性质(支配内在价值 / 折现上鞅 / 最小);也可解 Bellman 方程 (5.4.13) 配边界条件求解。

### 附:文献注记 / Notes(§5.6）
永续美式 put 的解由 Irene Villegas(1994 CMU SUMI 项目)给出;最优停止经典参考 **Shiryaev**;一般永续美式 put 的二叉树处理见 **Shiryaev–Kabanov–Kramkov–Melnikov**。

### 附:符号对照表 / Notation
| 符号 | 含义 |
|---|---|
| $X_j=\pm1$ | 第 $j$ 步增量(H/T) |
| $M_n=\sum_{j=1}^n X_j$ | 对称随机游走(鞅 + 马尔可夫) |
| $\tau_m=\min\{n:M_n=m\}$ | 首达水平 $m$ 的首达时(停时) |
| $\cosh\sigma=\tfrac{e^\sigma+e^{-\sigma}}{2}$ | 双曲余弦 |
| $S_n=e^{\sigma M_n}/(\cosh\sigma)^n$ | 指数鞅 |
| $\alpha\in(0,1)$ | 矩母函数变量($\alpha=e^u,u<0$) |
| $v(s)$ | 永续期权价值函数(时间无关) |
| $g(s)$ | 内在价值(put 为 $K-s$) |

---

**一句话本章精髓**:对称随机游走是布朗运动的离散原型;**首达时**几乎必然有限却期望无穷(零常返),其分布由**指数鞅**或**反射原理**求得;把这套工具用到**永续美式 put**,最优停止收敛为一个**Bellman 方程**(动态规划),配边界条件挑出最小解——这正是 Vol II 连续时间最优停止 / 自由边界问题的离散预演。
