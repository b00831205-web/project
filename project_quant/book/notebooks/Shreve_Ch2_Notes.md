# Shreve《Stochastic Calculus for Finance I》Ch.2 学习笔记
## 硬币空间上的概率论 / Probability Theory on Coin Toss Space

> **一句话主线**:整章在做一件事——为二叉树资产定价提供概率论语言。两条核心定理线:
> 1. **鞅 (Martingale)**:在风险中性测度 $\tilde{\mathbb{P}}$ 下,**折现股价 / 折现财富 / 折现衍生品价**都是鞅 → 推出无套利与定价公式。
> 2. **马尔可夫 (Markov)**:若标的过程是马尔可夫的,衍生品价就是当前状态的函数 $V_n=v_n(X_n)$ → 定价可以**递归且无需存路径**,这是写代码时的关键。
>
> 记号约定:$u$ 上涨因子,$d$ 下跌因子,$r$ 利率,$0<d<1+r<u$(无套利)。$\mathbb{P}$ 为真实测度(实际概率 $p,q$),$\tilde{\mathbb{P}}$ 为风险中性测度(概率 $\tilde p,\tilde q$)。

---

# §0 速查公式表(写项目时直接查)/ Formula Cheat Sheet

### 0.1 风险中性测度 / Risk-neutral measure

| 量 | 公式 |
|---|---|
| 上涨风险中性概率 $\tilde p$ | $\tilde p = \dfrac{1+r-d}{u-d}$ |
| 下跌风险中性概率 $\tilde q$ | $\tilde q = \dfrac{u-1-r}{u-d}$ |
| 归一 | $\tilde p+\tilde q=1$ |
| 关键恒等式 | $\tilde p\,u+\tilde q\,d=1+r \;\Longleftrightarrow\; \dfrac{\tilde p u+\tilde q d}{1+r}=1$ |

### 0.2 定价核心(三条最常用)/ Pricing core

**单步逆推(backward induction,最常用)**
$$V_n=\frac{1}{1+r}\Big[\tilde p\,V_{n+1}(H)+\tilde q\,V_{n+1}(T)\Big]$$

**任意期定价(risk-neutral pricing formula)**
$$V_n=\tilde{\mathbb{E}}_n\!\left[\frac{V_N}{(1+r)^{N-n}}\right]$$

**Delta 对冲份额(replication)**
$$\Delta_n=\frac{V_{n+1}(\omega_1\cdots\omega_n H)-V_{n+1}(\omega_1\cdots\omega_n T)}{S_{n+1}(\omega_1\cdots\omega_n H)-S_{n+1}(\omega_1\cdots\omega_n T)}$$

### 0.3 马尔可夫递归算法(无路径依赖,直接 coding)/ Markov recursion

**一维(payoff 只依赖 $S_N$,如欧式 call/put)**
$$v_n(s)=\frac{1}{1+r}\Big[\tilde p\,v_{n+1}(us)+\tilde q\,v_{n+1}(ds)\Big],\quad n=N-1,\dots,0$$
终值:Call $v_N(s)=(s-K)^+$ ;Put $v_N(s)=(K-s)^+$。

**二维(payoff 依赖 $S_N$ 与历史最大值 $M_N$,如回望期权)**
$$v_n(s,m)=\frac{1}{1+r}\Big[\tilde p\,v_{n+1}\big(us,\;m\vee us\big)+\tilde q\,v_{n+1}\big(ds,\;m\big)\Big],\quad m\ge s$$
($m\vee ds=m$ 因 $d\le 1$;$x\vee y:=\max\{x,y\}$)

### 0.4 财富 / 现金流演化 / Wealth & cash-flow

| 场景 | 递推 |
|---|---|
| 自融资财富 | $X_{n+1}=\Delta_n S_{n+1}+(1+r)(X_n-\Delta_n S_n)$ |
| 带现金流 $C_n$ | $X_{n+1}=\Delta_n S_{n+1}+(1+r)(X_n-C_n-\Delta_n S_n)$ |
| 多期现金流定价 | $V_n=\tilde{\mathbb{E}}_n\!\left[\sum_{k=n}^{N}\dfrac{C_k}{(1+r)^{k-n}}\right]$ |

### 0.5 教材数值算例(写单元测试时拿来对答案)/ Canonical test tree

$S_0=4,\;u=2,\;d=\tfrac12,\;r=\tfrac14 \Rightarrow \tilde p=\tilde q=\tfrac12$。
真实测度常取 $p=\tfrac23,\;q=\tfrac13$。

```
                       S3(HHH)=32
            S2(HH)=16
   S1(H)=8            S3(HHT/HTH/THH)=8
S0=4       S2(HT/TH)=4
   S1(T)=2            S3(HTT/THT/TTH)=2
            S2(TT)=1
                       S3(TTT)=0.50
```
- 验证鞅:$S_1(T)=2=\tfrac12 S_2(TH)+\tfrac12 S_2(TT)$ 折现后成立。
- 验证算法:用 0.3 一维公式跑这棵树,任何 payoff 都能对拍。

---

# §1 马丁格尔 / Martingales(本章重心)

### 1.1 适应过程与定义 / Adapted process & definition
**适应过程 (adapted process)**:序列 $M_0,M_1,\dots,M_N$,每个 $M_n$ **只依赖前 $n$ 次抛掷**($M_0$ 为常数)。

在真实测度 $\mathbb{P}$ 下(换成 $\tilde{\mathbb{E}}_n$ 即为风险中性版本):

| 类型 | 条件 | 直觉 |
|---|---|---|
| **鞅 Martingale** | $M_n=\mathbb{E}_n[M_{n+1}]$ | 无涨跌倾向,"公平赌局" |
| **下鞅 Submartingale** | $M_n\le \mathbb{E}_n[M_{n+1}]$ | 有上升倾向(如真实测度下折现股价) |
| **上鞅 Supermartingale** | $M_n\ge \mathbb{E}_n[M_{n+1}]$ | 有下降倾向 |

### 1.2 两条要记住的性质 / Two key consequences
- **多步性质 (multistep)**:$M_n=\mathbb{E}_n[M_m]$,对任意 $0\le n\le m\le N$。(由塔性质迭代得到)
- **期望恒定 (constant expectation)**:$\mathbb{E}M_n=M_0$,对所有 $n$。

### 1.3 三大定理 / The three theorems

**Thm 2.4.4 折现股价是鞅**(无分红股票,风险中性测度下)
$$\frac{S_n}{(1+r)^n}=\tilde{\mathbb{E}}_n\!\left[\frac{S_{n+1}}{(1+r)^{n+1}}\right]$$
> 证明要点:把 $\tilde{\mathbb{E}}_n[S_{n+1}]=\tilde p\,uS_n+\tilde q\,dS_n=(1+r)S_n$ 代入即可。第二种证法用"取出已知 + 独立性"(可推广到连续时间)。

**Thm 2.4.5 折现财富是鞅**(任意适应组合策略 $\Delta_n$)
$$\frac{X_n}{(1+r)^n}=\tilde{\mathbb{E}}_n\!\left[\frac{X_{n+1}}{(1+r)^{n+1}}\right]$$
> 含义:风险中性测度下,无论怎么配置股票/货币市场,**平均增长率都等于利率 $r$**。
> 推论 2.4.6:$\tilde{\mathbb{E}}\!\left[\dfrac{X_n}{(1+r)^n}\right]=X_0$。

**Thm 2.4.7 风险中性定价公式 + 折现衍生品价是鞅**
$$V_n=\tilde{\mathbb{E}}_n\!\left[\frac{V_N}{(1+r)^{N-n}}\right],\qquad
\frac{V_n}{(1+r)^n}=\tilde{\mathbb{E}}_n\!\left[\frac{V_{n+1}}{(1+r)^{n+1}}\right]$$

**Thm 2.4.8 现金流估值 (cash-flow valuation)**:支付序列 $C_n,\dots,C_N$
$$V_n=\tilde{\mathbb{E}}_n\!\left[\sum_{k=n}^{N}\frac{C_k}{(1+r)^{k-n}}\right],\qquad V_N=C_N$$
对冲份额仍用 Delta 公式(见 §0.2),财富递推用带现金流版本。

### 1.4 资产定价第一基本定理 / First Fundamental Theorem of Asset Pricing
> **存在风险中性测度 ⟹ 无套利。** 逻辑:风险中性测度下折现财富期望恒定,不可能从 $X_0=0$ 出发、终值 $X_N\ge0$ 且某路径 $>0$ 而无负值可能。后续在利率期限结构模型里用来推出 HJM 无套利条件。

---

# §2 马尔可夫过程 / Markov Processes(写代码降复杂度的关键)

### 2.1 定义 / Definition
$X_0,\dots,X_N$ 是**马尔可夫过程**,若对每个函数 $f$ 都存在另一函数 $g$(依赖 $n,f$)使
$$\mathbb{E}_n[f(X_{n+1})]=g(X_n)$$
> 直觉:估计未来只需当前状态 $X_n$,**路径信息无用**。重点不是求出 $g$,而是它"存在"——这保证定价算法不必存路径(见 Thm 2.5.8)。

**多维版 (Def 2.5.5)**:$\mathbb{E}_n[f(X^1_{n+1},\dots,X^K_{n+1})]=g(X^1_n,\dots,X^K_n)$。

### 2.2 独立性引理(验证马尔可夫的钥匙)/ Independence Lemma 2.5.3
设 $X^1,\dots,X^K$ 只依赖前 $n$ 次,$Y^1,\dots,Y^L$ 只依赖第 $n+1$ 到 $N$ 次。定义
$$g(x^1,\dots,x^K)=\mathbb{E}\,f(x^1,\dots,x^K,Y^1,\dots,Y^L)$$
则
$$\mathbb{E}_n[f(X^1,\dots,X^K,Y^1,\dots,Y^L)]=g(X^1,\dots,X^K)$$
> **用法套路**(三步):① 已知量($X$,前 $n$ 次)换成哑变量;② 独立量($Y$,后续抛掷)取**无条件期望**;③ 算完再把哑变量换回随机变量。
> 这是"取出已知"(Thm 2.3.2(ii))的推广——因为 $X$ 嵌在 $f$ 内部,不能直接提出。

### 2.3 例子:谁是马尔可夫 / Worked examples

| 过程 | 是否马尔可夫 | 关键 |
|---|---|---|
| 股价 $S_n$ | ✅ | $g(x)=\tilde p f(ux)+\tilde q f(dx)$ |
| 历史最大值 $M_n=\max_{k\le n}S_k$ **单独** | ❌ | 只记 $M_2=4$ 无法区分 $TH/TT$ 后续演化 |
| 二维 $(S_n,M_n)$ | ✅ | 加"状态变量"恢复马尔可夫性 |

> $M_n$ 不是鞅也不是马尔可夫的典型反例:$M_2(TH)=M_2(TT)=4$,但 $\mathbb{E}_2[M_3](TH)=6\tfrac23\neq 4=\mathbb{E}_2[M_3](TT)$,故不存在 $g$。**修复方法:加状态变量** → 用 $(S_n,M_n)$。

### 2.4 定价定理 / Thm 2.5.8
若 $X_0,\dots,X_N$ 在 $\tilde{\mathbb{P}}$ 下马尔可夫,且 $V_N=v_N(X_N)$,则每期价格都是当前状态的函数:
$$V_n=v_n(X_n),\quad n=0,\dots,N$$
存在递归算法计算 $v_n$(一维见 §0.3,二维见 §0.3)。连续时间下该递归的对应物是 **PDE**,桥梁是 **Feynman–Kac 定理**。

### 2.5 鞅 vs 马尔可夫(易混点)/ Martingale vs Markov
- 鞅是 $f(x)=x,\,g(x)=x$ 的特例;但**不是每个鞅都是马尔可夫**,也**不是每个马尔可夫都是鞅**。
- 股价在两种测度下都马尔可夫,但通常都不是鞅;仅当 $pu+qd=1$ 时,股价才同时是鞅与马尔可夫(真实测度下)。

---

# §3 其他章节(基础与背景)/ Foundations & Misc

### 3.1 有限概率空间 (§2.1) / Finite probability space
- $(\Omega,\mathbb{P})$:$\Omega$ 非空有限样本空间;$\mathbb{P}:\Omega\to[0,1]$ 且 $\sum_{\omega\in\Omega}\mathbb{P}(\omega)=1$。
- 事件 $A\subseteq\Omega$,$\mathbb{P}(A)=\sum_{\omega\in A}\mathbb{P}(\omega)$;$\mathbb{P}(\Omega)=1$;不相交可加 $\mathbb{P}(A\cup B)=\mathbb{P}(A)+\mathbb{P}(B)$。
- 允许某些 $\omega$ 概率为 0(可放入"必不发生"的结果)。

### 3.2 随机变量、分布、期望 (§2.2) / RV, distribution, expectation
- **随机变量 = $\Omega\to\mathbb{R}$ 的函数**;分布 = 它取各值的概率列表。
- ⚠️ **核心区分:随机变量 ≠ 分布。** 换测度($\mathbb{P}\to\tilde{\mathbb{P}}$)会改变**分布**,但**不改变随机变量本身**——这正是后面真实测度 vs 风险中性测度的根基。
- 期望:$\mathbb{E}X=\sum_\omega X(\omega)\mathbb{P}(\omega)$;风险中性:$\tilde{\mathbb{E}}X=\sum_\omega X(\omega)\tilde{\mathbb{P}}(\omega)$。
- 方差:$\mathrm{Var}(X)=\mathbb{E}\big[(X-\mathbb{E}X)^2\big]$。
- **线性**:$\mathbb{E}(c_1X+c_2Y)=c_1\mathbb{E}X+c_2\mathbb{E}Y$;线性函数 $\mathbb{E}[\ell(X)]=\ell(\mathbb{E}X)$。
- **Jensen 不等式 (Thm 2.2.5)**:$\varphi$ 凸 $\Rightarrow \mathbb{E}[\varphi(X)]\ge\varphi(\mathbb{E}X)$。推论 $\mathbb{E}[X^2]\ge(\mathbb{E}X)^2$。

### 3.3 条件期望 (§2.3)——鞅与马尔可夫共同的地基 / Conditional expectation
**定义 (2.3.6)**:$X$ 依赖前 $N$ 次抛掷,$1\le n\le N$,
$$\tilde{\mathbb{E}}_n[X](\omega_1\cdots\omega_n)=\sum_{\omega_{n+1}\cdots\omega_N}\tilde p^{\,\#H}\,\tilde q^{\,\#T}\,X(\omega_1\cdots\omega_N)$$
即对"剩余抛掷"加权平均;它本身是**依赖前 $n$ 次的随机变量**。
- 两个极端:$\mathbb{E}_0[X]=\mathbb{E}X$(无信息);$\mathbb{E}_N[X]=X$(全信息)。

**Thm 2.3.2 五条基本性质(必背)/ Five fundamental properties**

| # | 名称 | 公式 | 条件 |
|---|---|---|---|
| (i) | 线性 Linearity | $\mathbb{E}_n[c_1X+c_2Y]=c_1\mathbb{E}_n[X]+c_2\mathbb{E}_n[Y]$ | — |
| (ii) | 取出已知 Taking out what is known | $\mathbb{E}_n[XY]=X\cdot\mathbb{E}_n[Y]$ | $X$ 只依赖前 $n$ 次 |
| (iii) | 迭代/塔 Iterated (tower) | $\mathbb{E}_n[\mathbb{E}_m[X]]=\mathbb{E}_n[X]$;特例 $\mathbb{E}[\mathbb{E}_m[X]]=\mathbb{E}X$ | $0\le n\le m\le N$ |
| (iv) | 独立 Independence | $\mathbb{E}_n[X]=\mathbb{E}X$ | $X$ 只依赖第 $n{+}1$ 到 $N$ 次 |
| (v) | 条件 Jensen | $\mathbb{E}_n[\varphi(X)]\ge\varphi(\mathbb{E}_n[X])$ | $\varphi$ 凸 |

### 3.4 注记 (§2.7) / Historical notes
- 样本空间视角:Kolmogorov(可推广到无限空间,见 Vol II)。
- 鞅:Doob 提出,名字源自 Ville 讨论的赌博策略。
- 风险中性定价公式:Harrison–Kreps 与 Harrison–Pliska。

---

# §4 面试速答 / Interview Quick-Fire

> 用法:遮住答案,先自己复述,再核对。中英关键词都给,方便中英双语面试。

**Q1. 什么是鞅?为什么风险中性测度下折现股价是鞅?**
A:鞅即 $M_n=\mathbb{E}_n[M_{n+1}]$,给定当前信息,下一期期望等于当前值,无涨跌倾向。风险中性概率 $\tilde p,\tilde q$ 是被**专门选出来**使 $\tilde p u+\tilde q d=1+r$ 的,代入即得 $\tilde{\mathbb{E}}_n[S_{n+1}]=(1+r)S_n$,折现后期望恒定 → 鞅。

**Q2. 随机变量和分布的区别?为什么换测度重要?**
A:随机变量是 $\Omega\to\mathbb{R}$ 的固定函数(如"正面总数");分布是它取各值的概率表。换测度改变分布与期望,但函数本身不变。定价时同一个 payoff,在真实测度下估计历史统计、在风险中性测度下定价。

**Q3. 风险中性定价公式的直觉?**
A:$V_n=\tilde{\mathbb{E}}_n[V_N/(1+r)^{N-n}]$。因为存在复制组合,衍生品价 = 复制组合财富;而折现财富在 $\tilde{\mathbb{P}}$ 下是鞅,故当前价 = 折现终值的条件期望。

**Q4. 下鞅 vs 上鞅?真实市场里折现股价是哪个?**
A:下鞅 $M_n\le\mathbb{E}_n[M_{n+1}]$(趋升),上鞅反之(趋降)。真实测度下股票回报高于利率以补偿风险,故折现股价是**下鞅**;风险中性测度下被"校准"成鞅。

**Q5. 资产定价第一基本定理?**
A:存在风险中性测度(与真实测度同零测集、且所有基础资产折现价为鞅)⟹ 无套利。证明核心:折现财富期望恒为 $X_0$,无法零成本造出非负且有正概率为正、却无负值可能的终值。

**Q6. 马尔可夫性质?对定价代码意味着什么?**
A:$\mathbb{E}_n[f(X_{n+1})]=g(X_n)$,未来只依赖当前状态。意味着 $V_n=v_n(X_n)$,定价可**逐期逆推、无需存全路径**,把状态空间从 $2^n$ 降到 $O(n)$ 量级。

**Q7. 历史最大值过程为什么不是马尔可夫?怎么修?**
A:单独的 $M_n$ 丢失了当前股价信息,相同 $M_n$ 不同 $S_n$ 会有不同后续。修法:**增加状态变量**,用二维 $(S_n,M_n)$ 恢复马尔可夫性,再用 $v_n(s,m)$ 递归定价。

**Q8. 塔性质 / 迭代条件期望怎么用?**
A:$\mathbb{E}_n[\mathbb{E}_m[X]]=\mathbb{E}_n[X]$($n\le m$),"先粗估再细估 = 直接估"。用来证明多步鞅性质 $M_n=\mathbb{E}_n[M_m]$,以及把多期定价拆成单步逆推。

**Q9. Delta 对冲份额怎么来的?**
A:$\Delta_n=\dfrac{V_{n+1}(H)-V_{n+1}(T)}{S_{n+1}(H)-S_{n+1}(T)}$。由"复制组合在 $H/T$ 两种情形都要复现衍生品价"两个方程联立解出,本质是离散版的 $\partial V/\partial S$。

**Q10. Jensen 不等式在金融里有什么用?**
A:凸函数 $\mathbb{E}[\varphi(X)]\ge\varphi(\mathbb{E}X)$。例:期权 payoff 是凸的 → 波动率越大期权越值钱;$\mathbb{E}[X^2]\ge(\mathbb{E}X)^2$ 即方差非负。

---

### 附:符号对照表 / Notation
| 符号 | 含义 |
|---|---|
| $\Omega,\ \mathbb{P},\ \tilde{\mathbb{P}}$ | 样本空间、真实测度、风险中性测度 |
| $\mathbb{E}_n,\ \tilde{\mathbb{E}}_n$ | 基于前 $n$ 次抛掷的条件期望(真实 / 风险中性) |
| $u,d,r$ | 上涨因子、下跌因子、单期利率 |
| $\tilde p,\tilde q$ | 风险中性上涨/下跌概率 |
| $S_n,\ V_n,\ X_n$ | 股价、衍生品价、组合财富 |
| $\Delta_n$ | 第 $n$ 期持股份额 |
| $M_n$ | 鞅(§1)或历史最大值(§2,按上下文) |
| $#H,\ #T$ | 剩余抛掷中正/反面数 |
