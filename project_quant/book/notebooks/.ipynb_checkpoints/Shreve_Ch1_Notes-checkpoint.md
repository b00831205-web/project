# Shreve《Stochastic Calculus for Finance I》Ch.1 学习笔记
## 二叉树无套利定价模型 / The Binomial No-Arbitrage Pricing Model

> **一句话主线**:整章用最简单的二叉树把一件事讲透——**衍生品价格由"复制"唯一确定**。三个等价视角串成一条线:
> 1. **无套利 (No-arbitrage)**:无套利 $\iff 0<d<1+r<u$,这是全书的基本假设。
> 2. **复制 / 对冲 (Replication / Hedging)**:卖出衍生品后用股票+货币市场动态交易,使期末财富在**所有路径上**都等于 payoff,所需初始资金 = 价格。
> 3. **风险中性 (Risk-neutral)**:把 $\tilde p,\tilde q$ 当作"概率",价格 = 折现后的风险中性期望——这只是**求解沿路径对冲方程组的计算捷径**。
>
> **核心反直觉**:定价只依赖移动幅度 $u,d$(连续时间里是**波动率**),**与真实概率 $p,q$ / 平均增长率无关**。
>
> 记号:$u$ 上涨因子,$d$ 下跌因子,$r$ 单期利率,$0<d<1+r<u$。$p,q$ 真实概率,$\tilde p,\tilde q$ 风险中性概率。

---

# §0 速查公式表(写项目时直接查)/ Formula Cheat Sheet

### 0.1 无套利与风险中性测度 / No-arbitrage & risk-neutral measure

| 量 | 公式 |
|---|---|
| 无套利条件 | $0<d<1+r<u$ |
| 上涨风险中性概率 $\tilde p$ | $\tilde p=\dfrac{1+r-d}{u-d}$ |
| 下跌风险中性概率 $\tilde q$ | $\tilde q=\dfrac{u-1-r}{u-d}$ |
| 归一(由无套利保证 $>0$) | $\tilde p+\tilde q=1,\quad \tilde p,\tilde q>0$ |
| 关键恒等式 | $\tilde p\,u+\tilde q\,d=1+r$ |

### 0.2 定价三件套(最常用)/ Pricing toolkit

**向后递推定价(backward induction)**
$$V_n=\frac{1}{1+r}\Big[\tilde p\,V_{n+1}(\omega_1\cdots\omega_n H)+\tilde q\,V_{n+1}(\omega_1\cdots\omega_n T)\Big]$$

**Delta 对冲份额(replication)**
$$\Delta_n=\frac{V_{n+1}(\omega_1\cdots\omega_n H)-V_{n+1}(\omega_1\cdots\omega_n T)}{S_{n+1}(\omega_1\cdots\omega_n H)-S_{n+1}(\omega_1\cdots\omega_n T)}$$

**财富方程(向前演化,verify replication)**
$$X_{n+1}=\Delta_n S_{n+1}+(1+r)(X_n-\Delta_n S_n)=(1+r)X_n+\Delta_n\big(S_{n+1}-(1+r)S_n\big)$$
令 $X_0=V_0$ 向前跑,则所有路径上 $X_N=V_N$(完备市场)。

**股价的"鞅"性质(sanity check)**
$$S_n=\frac{1}{1+r}\Big[\tilde p\,S_{n+1}(H)+\tilde q\,S_{n+1}(T)\Big]\quad\Longleftrightarrow\quad \tilde{\mathbb{E}}\text{下股票期望收益率}=r$$

### 0.3 马尔可夫化简(降复杂度,直接 coding)/ Markov reduction

朴素列举 $2^N$ 条路径 → 指数爆炸($N=100$ 约 $10^{30}$)。找**最小充分状态变量**降为多项式。

**一维(payoff 仅依赖 $S_N$,如欧式 call/put)** — 状态数 $N+1$
$$v_n(s)=\frac{1}{1+r}\Big[\tilde p\,v_{n+1}(us)+\tilde q\,v_{n+1}(ds)\Big],\qquad
\delta_n(s)=\frac{v_{n+1}(us)-v_{n+1}(ds)}{us-ds}$$
终值:Call $v_N(s)=(s-K)^+$ ;Put $v_N(s)=(K-s)^+$。

**二维(路径依赖,如回望期权,状态加历史最大值 $M_n$)**
$$v_n(s,m)=\frac{1}{1+r}\Big[\tilde p\,v_{n+1}\big(us,\,m\vee us\big)+\tilde q\,v_{n+1}\big(ds,\,m\big)\Big],\qquad m\ge s$$
($x\vee y:=\max\{x,y\}$;因 $d<1$,下跌分支 $m\vee ds=m$)

### 0.4 教材数值算例(写单元测试时拿来对答案)/ Canonical test cases

统一参数:$S_0=4,\;u=2,\;d=\tfrac12,\;r=\tfrac14 \Rightarrow \tilde p=\tilde q=\tfrac12$。

| 例 | 衍生品 | payoff | 答案 |
|---|---|---|---|
| 1.1.1 | 单期欧式 Call,$K=5$ | $(S_1-5)^+$ | $V_0=1.20,\ \Delta_0=\tfrac12$ |
| 1.3.1 | 3 期欧式 Put,$K=5$ | $(5-S_3)^+$ | $v_0(4)=0.864$ |
| 1.2.4 / 1.3.2 | 3 期回望 lookback | $\max_{0\le n\le3}S_n-S_3$ | $V_0=1.376,\ \Delta_0=0.1733$ |

```
股价树 (S0=4, u=2, d=1/2):
                       S3(HHH)=32
            S2(HH)=16
   S1(H)=8            S3(HHT/HTH/THH)=8
S0=4       S2(HT/TH)=4
   S1(T)=2            S3(HTT/THT/TTH)=2
            S2(TT)=1
                       S3(TTT)=0.50
```

---

# §1 单期模型:无套利与复制定价 / One-Period: No-Arbitrage & Replication

### 1.1 基本设定 / Setup
- 时刻 0 股价 $S_0>0$;时刻 1 由一次抛掷决定 $S_1(H)$ 或 $S_1(T)$。
- 上涨/下跌因子 $u=\dfrac{S_1(H)}{S_0},\ d=\dfrac{S_1(T)}{S_0}$,数学上只需 $d<u$(直觉 $u>1>d$)。
- 真实概率 $p=P(H)>0,\ q=1-p>0$(**硬币不必公平**)。
- 货币市场利率 $r$:投 \$1 得 $1+r$,借贷同利率($r>-1$)。

### 1.2 套利与无套利条件 / Arbitrage & the no-arbitrage condition
**套利 (arbitrage)** = 初始资金为零、亏钱概率为零、赚钱概率为正的策略。含套利的模型不能用(可凭空造钱);真实市场套利转瞬即逝。

**无套利条件 (1.1.2)**:$\boxed{0<d<1+r<u}$。两个方向都必须成立:

| 若违反 | 套利构造 |
|---|---|
| $d\ge 1+r$ | 借钱买股:最差(T)也够还债,且 $u>d\ge1+r$ 有正概率赚 |
| $u\le 1+r$ | 卖空投货币市场:最好(H)回补成本也 $\le$ 货币收益,有正概率严格更少 |

> 反向也成立:满足 (1.1.2) 则一定无套利(习题 1.1)。常取 $d=1/u$,但模型只需 (1.1.2)。

### 1.3 复制定价 / Pricing by replication
**思路**:不用真实概率,用股票+货币市场**复制**衍生品收益,复制成本即无套利价格。

**例 1.1.1**:$S_0=4,u=2,d=\tfrac12,r=\tfrac14$,欧式 Call $K=5$ → $S_1(H)=8,S_1(T)=2$,payoff $=3$ 或 $0$。取 $X_0=1.20,\ \Delta_0=\tfrac12$(借 0.80):
$$X_1(H)=\tfrac12\cdot8+(1.25)(1.20-2)=3,\qquad X_1(T)=\tfrac12\cdot2+(1.25)(-0.80)=0$$
恰复现 payoff → 无套利价格 = **1.20**(报价偏离都可造套利)。

### 1.4 一般单期公式 / General one-period formulas
组合财富 $X_1=(1+r)X_0+\Delta_0\big(S_1-(1+r)S_0\big)$,令 $X_1(H)=V_1(H),X_1(T)=V_1(T)$ 解两方程两未知数 $(X_0,\Delta_0)$,得三个结果:

1. **风险中性概率 (1.1.8)**:$\tilde p=\dfrac{1+r-d}{u-d},\ \tilde q=\dfrac{u-1-r}{u-d}$
2. **Delta 对冲 (1.1.9)**:$\Delta_0=\dfrac{V_1(H)-V_1(T)}{S_1(H)-S_1(T)}$("收益差 / 股价差")
3. **风险中性定价 (1.1.10)**:$\boxed{V_0=\dfrac{1}{1+r}[\tilde p\,V_1(H)+\tilde q\,V_1(T)]}$

### 1.5 关键洞见(务必记牢)/ Key insights
- $\tilde p,\tilde q$ **不是真实概率**。真实下股票平均增长率 $>r$(补偿风险);$\tilde p,\tilde q$ 被特意选成让股票期望增长率**恰等于 $r$**,从而消掉财富方程里 $\Delta_0$ 的系数项。
- **真实概率与价格无关**:对冲在涨/跌两情形都要成立,与涨跌**发生的概率**无关。决定价格的是移动**幅度** $u,d$,而非其概率。
- 连续时间对应:价格依赖股价**波动率**,不依赖**平均增长率**(Vol II Ch.4–5)。
- 多头对冲与空头对称,持股数取 (1.1.9) 的相反数。

### 1.6 模型假设 / Assumptions(前三条 BSM 也用)
① 股票可任意细分;② 借贷同利率;③ 零买卖价差(实务常不成立);④ 每期股价只取两值(BSM 换成几何布朗运动)。

---

# §2 多期模型:动态对冲与复制定理 / Multiperiod: Dynamic Hedging & Replication

### 2.1 股价树与动态对冲 / Stock tree & dynamic hedging
反复抛掷,H 乘 $u$、T 乘 $d$;唯一假设仍是 (1.1.2)。股价 $S_n(\omega_1\cdots\omega_n)$ 依赖前 $n$ 次(如 $S_2(HT)=S_2(TH)=udS_0$)。
卖出期权得 $V_0$,先买 $\Delta_0$ 股,**每抛一次后可重新调整持仓** $\Delta_n(\omega_1\cdots\omega_n)$(允许依赖已知结果)。
**财富方程 (1.2.14)**:$X_{n+1}=\Delta_n S_{n+1}+(1+r)(X_n-\Delta_n S_n)$。

### 2.2 定理 1.2.2 多期复制定理(本章核心)/ Replication theorem
给定 $0<d<1+r<u$ 与 $\tilde p,\tilde q$,对时刻 $N$ 付 $V_N(\omega_1\cdots\omega_N)$ 的衍生品:
- **向后递推定价 (1.2.16)**:$V_n=\dfrac{1}{1+r}[\tilde p\,V_{n+1}(\cdots H)+\tilde q\,V_{n+1}(\cdots T)]$
- **逐点 Delta (1.2.17)**:$\Delta_n=\dfrac{V_{n+1}(\cdots H)-V_{n+1}(\cdots T)}{S_{n+1}(\cdots H)-S_{n+1}(\cdots T)}$
- 令 $X_0=V_0$ 用财富方程向前演化,则**所有路径** $X_N=V_N$。

> **证明思路**:对 $n$ 做**向前归纳**证 $X_n=V_n$。归纳步把 $\Delta_n$ 代入财富方程、结合 $V_n$ 定义,分别验证 $X_{n+1}(H)=V_{n+1}(H)$、$X_{n+1}(T)=V_{n+1}(T)$。关键代数:$\dfrac{u-(1+r)}{u-d}=\tilde q$。

### 2.3 三个随机过程 / Three stochastic processes
$(\Delta_n),\ (X_n),\ (V_n)$ 都是随机过程(按时间索引的随机变量序列),下标 = 依赖的抛掷次数。

### 2.4 完备性 / Completeness
多期二叉树是**完备市场**:**任何**衍生品都能被复制 → 每个衍生品都有**唯一**无套利价格。

### 2.5 路径依赖期权也适用 / Path-dependent payoffs
定理 1.2.2 不要求 payoff 只依赖末端股价。
**例 1.2.4 回望期权 (lookback)**:$\tilde p=\tilde q=\tfrac12$,payoff $V_3=\max_{0\le n\le3}S_n-S_3$。逐节点向后递推得 $V_0=1.376$,$\Delta_0=\dfrac{2.24-1.20}{8-2}=0.1733$,可逐期对冲到 $X_3\equiv V_3$。

---

# §3 计算考量:马尔可夫化简 / Computational Considerations(通向第 2 章)

### 3.1 指数爆炸 / Exponential blow-up
朴素按抛掷序列列举有 $2^N$ 条路径($N=100$ 约 $10^{30}$,不可行)。

### 3.2 马尔可夫化简 / Markov reduction
若价格在时刻 $n$ **只是当前股价的函数** $V_n=v_n(S_n)$,则时刻 $N$ 只有 $N+1$ 个可能股价,而非 $2^N$ 条路径。
**例 1.3.1 欧式 Put $K=5$**:$v_n(s)=\dfrac{1}{1+r}[\tilde p\,v_{n+1}(us)+\tilde q\,v_{n+1}(ds)]$,逐层算出 $v_0(4)=0.864$;持股 $\delta_n(s)=\dfrac{v_{n+1}(2s)-v_{n+1}(\frac12 s)}{2s-\frac12 s}$。

### 3.3 路径依赖也能化简 / Reduction for path-dependent
把状态扩展为**低维充分统计量**。
**例 1.3.2 回望期权**:用 $(S_n,M_n)$,$M_n=\max_{0\le k\le n}S_k$。时刻 3 仅 6 个 $(s,m)$ 组合。递推 $v_n(s,m)=\tfrac{1}{1+r}[\tilde p\,v_{n+1}(2s,m\vee2s)+\tilde q\,v_{n+1}(\tfrac12 s,m)]$,得 $v_0(4,4)=1.376$(与例 1.2.4 一致)。

> **要点**:找到能让价格成为其函数的**最小状态变量**,把指数复杂度降为多项式。这正是第 2 章**马尔可夫过程**的引子——$S_n$ 单独是马尔可夫的,$(S_n,M_n)$ 也是,而 $M_n$ 单独不是。

---

# §4 面试速答 / Interview Quick-Fire

> 用法:遮住答案先复述,再核对。中英关键词都给,适配双语面试。

**Q1. 无套利条件为什么必须是双向不等式 $0<d<1+r<u$?**
A:任一方向被破坏都能造套利。$d\ge1+r$ → 借钱买股稳赚不赔;$u\le1+r$ → 卖空投货币市场。两侧都要严格,才使股票既不能始终跑赢、也不能始终跑输无风险利率。

**Q2. 什么是复制 / 对冲定价?为什么它给出唯一价格?**
A:用股票+货币市场动态交易,使期末财富在**所有路径**上等于 payoff;所需初始资金即价格。在完备市场里每个衍生品都可复制,故价格唯一——否则可在衍生品与复制组合间套利。

**Q3. 风险中性概率是真实概率吗?为什么定价与真实概率无关?**
A:不是。$\tilde p,\tilde q$ 是被选来让股票期望收益率 $=r$ 的"数字"。对冲方程沿每条正概率路径都要成立,方程里**根本没有概率**;真实概率帮不上忙,因为组合期望收益依赖于还未确定的组合本身。风险中性概率只是求解这组方程的捷径。

**Q4. Delta 对冲公式的直觉?**
A:$\Delta_n=\dfrac{V_{n+1}(H)-V_{n+1}(T)}{S_{n+1}(H)-S_{n+1}(T)}$,用股票在两情形的差额去匹配期权差额,本质是离散版的 $\partial V/\partial S$。

**Q5. 什么是完备市场?二叉树为什么完备?**
A:完备 = 任何衍生品都可被基础资产复制。二叉树每期只有两个结果,而有股票+货币市场两种工具,自由度刚好够每步解出 $(X_n,\Delta_n)$,故任意 payoff 可复制 → 完备 → 价格唯一。

**Q6. 朴素 $2^N$ 路径怎么降复杂度?**
A:若价格可写成当前股价的函数 $v_n(S_n)$(马尔可夫化简),状态从 $2^N$ 路径降到 $N+1$ 个股价,递归 $v_n(s)=\tfrac{1}{1+r}[\tilde p v_{n+1}(us)+\tilde q v_{n+1}(ds)]$。

**Q7. 路径依赖期权(如回望)怎么高效定价?**
A:扩展状态变量为低维充分统计量,如用 $(S_n,M_n)$,$M_n$ 为历史最大值。状态空间多项式增长,递归 $v_n(s,m)$ 即可。关键是找**最小**充分状态。

**Q8. 风险中性测度下股票/任意组合的期望收益率是多少?**
A:都等于无风险利率 $r$:$S_n=\tfrac{1}{1+r}[\tilde p S_{n+1}(H)+\tilde q S_{n+1}(T)]$。这是 $\tilde p,\tilde q$ 被如此选取的直接结果,也是"折现股价是鞅"(第 2 章)的雏形。

**Q9. CRR 模型与 Black–Scholes–Merton 的关系?**
A:二叉树源自 Cox–Ross–Rubinstein;当期数 $N\to\infty$、参数适当标定时,二叉树极限收敛到 BSM(股价对数正态),可由此重新导出 BSM 公式。

**Q10. 为什么"反事实"的无概率论证有效?**
A:对冲要在所有正概率路径成立,解的是沿路径的方程组(无概率)。引入 $\tilde p,\tilde q$ 只是让"无论怎么投期望收益率都是 $r$"成立,把求解变简单;也可完全不提概率、只把 $\tilde p,\tilde q$ 当定义出来的数字(如定理 1.2.2)。

---

### 附:文献注记 / Historical notes
无套利思想隐含于 Black–Scholes;**Merton** 首次以无套利为公理显式发展。连续时间由 **Harrison–Kreps / Harrison–Pliska** 完善,引入鞅与风险中性定价。二叉树模型源自 **Cox–Ross–Rubinstein (CRR)**;$N\to\infty$ 时由二叉树极限重新导出 BSM。

### 附:符号对照表 / Notation
| 符号 | 含义 |
|---|---|
| $S_0,\ S_n$ | 初始股价、时刻 $n$ 股价 |
| $u,\ d,\ r$ | 上涨因子、下跌因子、单期利率 |
| $p,\ q$ / $\tilde p,\ \tilde q$ | 真实概率 / 风险中性概率 |
| $V_n$ | 衍生品在时刻 $n$ 的价格 |
| $X_n$ | 复制组合(财富)价值 |
| $\Delta_n$ | 第 $n$ 期持股份额 |
| $M_n$ | 历史最大值 $\max_{0\le k\le n}S_k$ |
| $v_n(\cdot)$ | 马尔可夫化简后的定价函数 |
| $x\vee y$ | $\max\{x,y\}$ |

---

**一句话本章精髓**:衍生品价格由**复制**唯一确定;只依赖移动幅度 $u,d$(连续时间里是波动率),**与真实概率 / 平均增长率无关**;风险中性概率是"沿所有路径求解对冲方程组"的计算捷径。
