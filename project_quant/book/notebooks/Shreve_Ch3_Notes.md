# Shreve《Stochastic Calculus for Finance I》Ch.3 学习笔记
## 状态价格 / State Prices

> **一句话主线**:前两章里有真实测度 $\mathbb{P}$ 和风险中性测度 $\tilde{\mathbb{P}}$ 两套权重;本章引入**第三个对象**把它们连起来,再应用到最优投资。两条线:
> 1. **变更测度的机器 (Change-of-measure machinery)**:Radon-Nikodým 导数 $Z=\tilde{\mathbb{P}}/\mathbb{P}$ 在两个测度间换算期望;它的"过程版" $Z_n=\mathbb{E}_n[Z]$ 是鞅;把折现与风险打包成**状态价格密度** $\zeta=Z/(1+r)^N$,于是定价可以**完全在真实测度下**做。
> 2. **应用:最优投资 (Optimal investment / CAPM)**:用状态价格密度把"选交易策略"的难题(Problem 3.3.1)拆成"先选终值财富 $X_N$、再复制"两步,Lagrange 乘子一步解出。
>
> **核心反直觉**:某条路径的时刻 0 价值 ≠ 它的(真实)概率。还要乘一个**风险修正因子** $Z$——它压低"终值高于 $S_0$"的路径权重、抬高"终值低于 $S_0$"的路径权重。这就是状态价格里的风险。
>
> 记号:$\mathbb{P}$ 真实测度(概率 $p,q$),$\tilde{\mathbb{P}}$ 风险中性测度(概率 $\tilde p,\tilde q$),$r$ 利率,$N$ 期数,$\#H,\#T$ 序列里正/反面数。

---

# §0 速查公式表(写项目时直接查)/ Formula Cheat Sheet

### 0.1 Radon-Nikodým 导数 / R-N derivative

| 量 | 公式 |
|---|---|
| R-N 导数(随机变量) | $Z(\omega)=\dfrac{\tilde{\mathbb{P}}(\omega)}{\mathbb{P}(\omega)}$ |
| 二叉树显式 (3.1.8) | $Z(\omega_1\cdots\omega_N)=\Big(\dfrac{\tilde p}{p}\Big)^{\#H}\Big(\dfrac{\tilde q}{q}\Big)^{\#T}$ |
| 三条性质 (Thm 3.1.1) | $\mathbb{P}(Z>0)=1,\quad \mathbb{E}Z=1,\quad \tilde{\mathbb{E}}Y=\mathbb{E}[ZY]$ |
| 反向换算 (Ex 3.1) | $\mathbb{E}Y=\tilde{\mathbb{E}}\!\big[\tfrac1Z\,Y\big]$ |

### 0.2 状态价格密度与定价 / State price density & pricing

| 量 | 公式 |
|---|---|
| 状态价格密度(随机变量)(3.1.9) | $\zeta(\omega)=\dfrac{Z(\omega)}{(1+r)^N}$ |
| 状态价格 (state price) | $\zeta(\omega)\mathbb{P}(\omega)$ = 时刻 0 买"$\omega$ 发生则付 1"合约的价 |
| 真实测度下定价 (3.1.10) | $V_0=\mathbb{E}[\zeta V_N]=\displaystyle\sum_\omega V_N(\omega)\zeta(\omega)\mathbb{P}(\omega)$ |

> 与第 2 章对照:$V_0=\tilde{\mathbb{E}}\big[\tfrac{V_N}{(1+r)^N}\big]$(风险中性) $=\mathbb{E}[\zeta V_N]$(真实测度)。两者相等,$\zeta$ 把折现 $\tfrac1{(1+r)^N}$ 与风险修正 $Z$ 合二为一。

### 0.3 R-N 导数过程(鞅)/ R-N derivative process

$$Z_n=\mathbb{E}_n[Z],\quad n=0,\dots,N;\qquad Z_0=1,\ Z_N=Z$$
- **是 $\mathbb{P}$ 下的鞅**(Thm 3.2.1):$\mathbb{E}_n[Z_{n+1}]=Z_n$(在 $\tilde{\mathbb{P}}$ 下同样成立)。
- 部分路径显式 (3.2.4):$Z_n(\omega_1\cdots\omega_n)=\Big(\dfrac{\tilde p}{p}\Big)^{\#H}\Big(\dfrac{\tilde q}{q}\Big)^{\#T}$(只数前 $n$ 次)。
- **简化期望** (Lemma 3.2.5):$Y$ 只依赖前 $n$ 次 $\Rightarrow\ \tilde{\mathbb{E}}Y=\mathbb{E}[Z_n Y]$。
- **简化条件期望(抽象 Bayes)** (Lemma 3.2.6):$Y$ 只依赖前 $m$ 次,$n\le m$:
$$\tilde{\mathbb{E}}_n[Y]=\frac{1}{Z_n}\,\mathbb{E}_n[Z_m Y]$$
- 状态价格密度过程 (3.2.7):$\zeta_n=\dfrac{Z_n}{(1+r)^n}$,定价 (3.2.6):$V_n=\tilde{\mathbb{E}}_n\big[\tfrac{V_N}{(1+r)^{N-n}}\big]=\dfrac{1}{\zeta_n}\mathbb{E}_n[\zeta_N V_N]$。

### 0.4 最优投资(状态价格密度法)/ Optimal investment recipe

目标:max $\mathbb{E}\,U(X_N)$ s.t. 自融资财富方程(真实测度下取期望)。三步走 (Thm 3.3.6):

| 步 | 操作 |
|---|---|
| ① 解乘子 $\lambda$ | $\mathbb{E}\!\Big[\dfrac{Z}{(1+r)^N}\,I\!\Big(\dfrac{\lambda Z}{(1+r)^N}\Big)\Big]=X_0$,其中 $I=(U')^{-1}$ |
| ② 算最优终值 | $X_N^*=I\!\Big(\dfrac{\lambda Z}{(1+r)^N}\Big)$ |
| ③ 复制 | 把 $X_N^*$ 当 payoff,用第 1 章定理 1.2.2 算 $\Delta_0,\dots,\Delta_{N-1}$ |

**对数效用闭式解**($U=\ln x,\ U'(x)=\tfrac1x,\ I(y)=\tfrac1y$):
$$\boxed{X_N^*=\frac{X_0\,(1+r)^N}{Z}}\qquad(\lambda=\tfrac1{X_0})$$
直觉:$Z$ 大(真实概率被风险中性"高估")的路径,最优投资就少分配财富。

### 0.5 教材数值算例(写单元测试时拿来对答案)/ Canonical test cases

**三期模型** $S_0=4,u=2,d=\tfrac12,r=\tfrac14$,真实 $p=\tfrac23,q=\tfrac13\Rightarrow\tilde p=\tilde q=\tfrac12$:

| 量 | 值 |
|---|---|
| $Z$(终点) | $Z(HHH)=\tfrac{27}{64},\ Z(\cdot,2H)=\tfrac{27}{32},\ Z(\cdot,1H)=\tfrac{27}{16},\ Z(TTT)=\tfrac{27}{8}$ |
| $Z_2$ | $Z_2(HH)=\tfrac{9}{16},\ Z_2(HT)=Z_2(TH)=\tfrac98,\ Z_2(TT)=\tfrac94$ |
| $Z_1$ | $Z_1(H)=\tfrac34,\ Z_1(T)=\tfrac32$ ;$Z_0=1$ |
| 回望期权 | $V_3=\max_n S_n-S_3$,$V_0=\mathbb{E}[\zeta V_3]=1.376$(与 §Ch1/Ch2 一致) |

**两期最优投资** $r=\tfrac14$,真实 $\mathbb{P}(HH)=\tfrac49,\mathbb{P}(HT)=\mathbb{P}(TH)=\tfrac29,\mathbb{P}(TT)=\tfrac19$,$X_0=4$,对数效用:
$$X_2(HH)=\tfrac{100}{9},\ X_2(HT)=X_2(TH)=\tfrac{50}{9},\ X_2(TT)=\tfrac{25}{9};\quad
\Delta_0=\tfrac59,\ \Delta_1(H)=\tfrac{25}{54},\ \Delta_1(T)=\tfrac{25}{27}$$

---

# §1 变更测度 / Change of Measure(§3.1)

### 1.1 两个测度与 R-N 导数 / Two measures & the R-N derivative
真实测度 $\mathbb{P}$(经验估计参数得到,是"对的")与风险中性测度 $\tilde{\mathbb{P}}$(折现资产价为鞅,是"虚构但有用的")**对哪些路径可能发生意见一致**(都赋正概率),只在概率大小上不同。设两者对每个 $\omega$ 都 $>0$,定义
$$Z(\omega)=\frac{\tilde{\mathbb{P}}(\omega)}{\mathbb{P}(\omega)}$$
称为 $\tilde{\mathbb{P}}$ 关于 $\mathbb{P}$ 的 **Radon-Nikodým 导数**(有限空间里其实是个商)。

**定理 3.1.1**(三条性质):
1. $\mathbb{P}(Z>0)=1$(由 $\tilde{\mathbb{P}}(\omega)>0$);
2. $\mathbb{E}Z=\sum_\omega \tfrac{\tilde{\mathbb{P}}(\omega)}{\mathbb{P}(\omega)}\mathbb{P}(\omega)=\sum_\omega\tilde{\mathbb{P}}(\omega)=1$;
3. 对任意随机变量 $Y$:$\tilde{\mathbb{E}}Y=\mathbb{E}[ZY]$(换测度算期望的核心公式)。

### 1.2 例 3.1.2:三期模型 / Worked example
$p=\tfrac23,q=\tfrac13$ → $\mathbb{P}(HHH)=\tfrac{8}{27}$ 等;$\tilde p=\tilde q=\tfrac12$ → $\tilde{\mathbb{P}}(\text{每点})=\tfrac18$。
故 $Z=\tilde{\mathbb{P}}/\mathbb{P}$:$Z(HHH)=\tfrac{8^{-1}}{8/27}=\tfrac{27}{64}$,…,$Z(TTT)=\tfrac{27}{8}$(见 §0.5)。

回望期权两种等价算法,都得 $V_0=1.376$:
- 风险中性 (3.1.6):$V_0=\big(\tfrac45\big)^3\sum_\omega V_3(\omega)\tilde{\mathbb{P}}(\omega)$
- 真实测度 (3.1.7):$V_0=\big(\tfrac45\big)^3\sum_\omega V_3(\omega)Z(\omega)\mathbb{P}(\omega)$ ← **不提风险中性测度**,但先用 $Z$ 给 payoff 重新加权。

### 1.3 状态价格 / State prices(定义 3.1.3)
**状态价格密度**:$\zeta(\omega)=\dfrac{Z(\omega)}{(1+r)^N}$;**状态价格** = $\zeta(\omega)\mathbb{P}(\omega)$。
> 含义:$\zeta(\omega)\mathbb{P}(\omega)$ 是时刻 0 买入"若且唯若 $\omega$ 发生、时刻 $N$ 付 1"这份合约(Arrow-Debreu 证券)的价格。

**为什么需要 $Z$ 这一项?** 价格须反映两件事:① 货币时间价值 → $\tfrac1{(1+r)^N}$;② $\omega$ 发生的概率 → $\mathbb{P}(\omega)$。但仅靠这两项会让价格**只依赖真实期望收益**,忽略风险。$Z(\omega)$ 正是**风险修正**:由 §0.5 可见,有 2~3 个正面(终值 $>S_0$)的路径 $Z<1$,其权重被压低;终值 $<S_0$ 的路径 $Z>1$,权重被抬高——效果是让持有股票显得不如单看 $\mathbb{E}[(\tfrac45)^3 S_3]$ 那么诱人。

**一般合约定价 (3.1.10)**:任意 payoff 看成"诸 Arrow-Debreu 证券的组合":
$$V_0=\mathbb{E}[\zeta V_N]=\sum_\omega V_N(\omega)\zeta(\omega)\mathbb{P}(\omega)$$
"density(密度)"之名:$\zeta=$ **单位真实概率上的** 时刻 0 价格。

---

# §2 Radon-Nikodým 导数过程 / R-N Derivative Process(§3.2)

### 2.1 定义与鞅性 / Definition & martingale property
$Z$ 依赖全部 $N$ 次抛掷;若只想用前 $n$ 次的信息,就取条件期望估计:
$$Z_n=\mathbb{E}_n[Z],\quad n=0,\dots,N\quad(Z_0=1,\ Z_N=Z)\tag{Def 3.2.4}$$
**定理 3.2.1**:$Z_n$ 是 $\mathbb{P}$ 下的鞅。
> 证明(迭代条件期望):$\mathbb{E}_n[Z_{n+1}]=\mathbb{E}_n[\mathbb{E}_{n+1}[Z]]=\mathbb{E}_n[Z]=Z_n$。Remark 3.2.2:在 $\tilde{\mathbb{P}}$ 下同样是鞅。

> **直觉**:随时间推移对 $Z$ 的估计越来越精确,但**没有上升或下降的倾向**——若后续估计平均偏高,这一倾向早该体现在当前估计里(类比有效市场:已知能跑赢的信息早被计入价格)。

### 2.2 部分路径显式公式 / Partial-path formula
$$Z_n(\omega_1\cdots\omega_n)=\Big(\frac{\tilde p}{p}\Big)^{\#H(\omega_1\cdots\omega_n)}\Big(\frac{\tilde q}{q}\Big)^{\#T(\omega_1\cdots\omega_n)}\tag{3.2.4}$$
即**前 $n$ 次** 这段部分路径的"风险中性概率 ÷ 真实概率"。验证:$Z_2(HH)=(\tfrac{1/2}{2/3})^2=(\tfrac34)^2=\tfrac9{16}$ ✓。

### 2.3 两条换算引理 / Two conversion lemmas
- **Lemma 3.2.5**($Y$ 只依赖前 $n$ 次):$\tilde{\mathbb{E}}Y=\mathbb{E}[Z_n Y]$。即可用 $Z_n$ 当 $Z$ 的"替身",不必管 $n$ 之后的抛掷。
  > 证:$\tilde{\mathbb{E}}Y=\mathbb{E}[ZY]=\mathbb{E}[\mathbb{E}_n[ZY]]=\mathbb{E}[Y\mathbb{E}_n[Z]]=\mathbb{E}[YZ_n]$(用塔性质 + 取出已知)。
- **Lemma 3.2.6**(条件期望换测度,**离散版抽象 Bayes / Girsanov 雏形**;$Y$ 只依赖前 $m$ 次,$n\le m$):
$$\tilde{\mathbb{E}}_n[Y]=\frac{1}{Z_n}\,\mathbb{E}_n[Z_m Y]\tag{3.2.5}$$

### 2.4 状态价格密度过程与定价 / SPD process & pricing(定理 3.2.7)
$$\zeta_n=\frac{Z_n}{(1+r)^n};\qquad
V_n=\underbrace{\tilde{\mathbb{E}}_n\Big[\frac{V_N}{(1+r)^{N-n}}\Big]}_{\text{第2章}}=\frac{1}{\zeta_n}\,\mathbb{E}_n[\zeta_N V_N]\tag{3.2.6}$$
> 三个等号:第一个是第 2 章 (2.4.11);第二个由 Lemma 3.2.6;第三个是 $\zeta_n$ 的定义。意义:风险中性定价可以**整套搬到真实测度下**用状态价格密度做。

---

# §3 资本资产定价模型:最优投资 / CAPM: Optimal Investment(§3.3)

> 标题虽叫 CAPM,实质是**期望效用最大化**(在完备市场下用无套利机器求解),这是本章把前面工具落地的应用。

### 3.1 效用函数 / Utility functions
**效用函数** = 不减、凹函数(可取 $-\infty$,不可取 $+\infty$),如 $\ln x$(约定 $x\le0$ 时 $\ln x=-\infty$)。
凹性 (3.3.1):$U(\alpha x+(1-\alpha)y)\ge\alpha U(x)+(1-\alpha)U(y)$。
**HARA 类**:$U_p(x)=\tfrac1p(x-c)^p$($x>c$),绝对风险厌恶指数 $-\dfrac{U''(x)}{U'(x)}=\dfrac{1-p}{x-c}$(双曲型);$p=0$ 对应 $U_0(x)=\ln(x-c)$。
凹性捕捉**风险-收益权衡**:由 Jensen"反向"用(Thm 2.2.5),$\mathbb{E}U(X)\le U(\mathbb{E}X)$ → 风险厌恶者宁要确定的 $\mathbb{E}X$ 也不要随机的 $X$。

### 3.2 最优投资问题 / The optimal-investment problem
**Problem 3.3.1**:给定 $X_0$,选适应组合过程 $\Delta_0,\dots,\Delta_{N-1}$ 最大化 $\mathbb{E}\,U(X_N)$,受自融资财富方程约束。
> 注意:期望在**真实测度** $\mathbb{P}$ 下。**不能在风险中性测度下做**——因为 $\tilde{\mathbb{P}}$ 下股票与货币市场收益率都是 $r$,理性人会只投货币市场,风险偏好无从体现。

### 3.3 关键技巧:用 $\tilde{\mathbb{E}}[X_N/(1+r)^N]=X_0$ 解耦 / Decoupling via the budget constraint
直接解 Problem 3.3.1 很痛苦($\Delta_n$ 数目随期数指数增长)。突破口是推论 2.4.6:
$$\tilde{\mathbb{E}}\Big[\frac{X_N}{(1+r)^N}\Big]=X_0\tag{3.3.17}$$
任何从 $X_0$ 出发的自融资策略,终值财富的折现风险中性期望恒为 $X_0$。这把"选策略"换成"选终值":

**Problem 3.3.3**:选随机变量 $X_N$(不管组合)最大化 $\mathbb{E}U(X_N)$,s.t. $\tilde{\mathbb{E}}[X_N/(1+r)^N]=X_0$。
**Lemma 3.3.4**:两问题等价。完备市场里任一满足预算约束的 $X_N$ 都能被复制(定理 1.2.2),反之最优策略的终值也满足约束 → **先求最优 $X_N^*$,再复制**。

### 3.4 拉格朗日求解 / Lagrange solution
用 $Z,\zeta$ 把约束写成纯真实测度形式:$\mathbb{E}[\zeta X_N]=X_0$。离散化为 $M=2^N$ 个状态:
**Problem 3.3.5**:max $\sum_m p_m U(x_m)$ s.t. $\sum_m p_m x_m \zeta_m=X_0$。
拉格朗日一阶条件:
$$U'(x_m)=\lambda\zeta_m\ \Longrightarrow\ U'(X_N)=\frac{\lambda Z}{(1+r)^N}\tag{3.3.23/24}$$
设 $I=(U')^{-1}$(因 $U$ 严格凹,$U'$ 严格减、可逆):
$$X_N^*=I\!\Big(\frac{\lambda Z}{(1+r)^N}\Big)\tag{3.3.25},\qquad
\mathbb{E}\!\Big[\frac{Z}{(1+r)^N}I\!\Big(\frac{\lambda Z}{(1+r)^N}\Big)\Big]=X_0\ \text{解出}\ \lambda\tag{3.3.26}$$

**定理 3.3.6**(求解流程):解 (3.3.26) 得 $\lambda$ → 代 (3.3.25) 得 $X_N^*$ → 用定理 1.2.2 算最优组合 $\Delta_0,\dots,\Delta_{N-1}$。

### 3.5 例 3.3.2:对数效用 / Log-utility example
两期,$X_0=4$,$\mathbb{P}(HH)=\tfrac49$ 等。$U=\ln x\Rightarrow I(y)=\tfrac1y$,代入得 $X_N^*=\dfrac{X_0(1+r)^N}{Z}$,$\lambda=\tfrac1{X_0}$。
算出 $X_2=\tfrac{100}9,\tfrac{50}9,\tfrac{50}9,\tfrac{25}9$,再用 $\Delta_n=\dfrac{X_{n+1}(H)-X_{n+1}(T)}{S_{n+1}(H)-S_{n+1}(T)}$ 反推 $\Delta_0=\tfrac59,\Delta_1(H)=\tfrac{25}{54},\Delta_1(T)=\tfrac{25}{27}$(见 §0.5)。
> 对照:直接对 $\Delta$ 求导的"暴力法"也能得同样答案,但变量数随期数指数膨胀;状态价格密度法把它降成一个含乘子 $\lambda$ 的标量方程。

---

# §4 面试速答 / Interview Quick-Fire

> 用法:遮住答案先复述,再核对。

**Q1. 什么是 Radon-Nikodým 导数?它有哪三条性质?**
A:$Z=\tilde{\mathbb{P}}/\mathbb{P}$(有限空间是两测度之商)。性质:$\mathbb{P}(Z>0)=1$、$\mathbb{E}Z=1$、$\tilde{\mathbb{E}}Y=\mathbb{E}[ZY]$。它是连续时间 Girsanov 定理换测度的离散原型。

**Q2. 怎么在两个测度间换算期望 / 条件期望?**
A:无条件:$\tilde{\mathbb{E}}Y=\mathbb{E}[ZY]$,反向 $\mathbb{E}Y=\tilde{\mathbb{E}}[Y/Z]$。条件(抽象 Bayes):$\tilde{\mathbb{E}}_n[Y]=\tfrac1{Z_n}\mathbb{E}_n[Z_mY]$,其中 $Z_n=\mathbb{E}_n[Z]$。

**Q3. 什么是状态价格 / 状态价格密度?Arrow-Debreu 含义?**
A:状态价格 $\zeta(\omega)\mathbb{P}(\omega)$ = 时刻 0 买"$\omega$ 发生则时刻 $N$ 付 1"合约(Arrow-Debreu 证券)的价。密度 $\zeta=Z/(1+r)^N$ 是单位真实概率的价格。任意 payoff 定价 $V_0=\mathbb{E}[\zeta V_N]$。

**Q4. 价格为什么不能只用"折现 × 真实概率"?$Z$ 起什么作用?**
A:那样价格只反映期望收益、忽略风险。$Z$ 是风险修正:压低终值高于 $S_0$ 的路径权重、抬高终值低于 $S_0$ 的路径权重,使资产价同时反映期望收益**与风险**。

**Q5. 为什么 $Z_n=\mathbb{E}_n[Z]$ 是鞅?有什么直觉?**
A:由迭代条件期望 $\mathbb{E}_n[Z_{n+1}]=\mathbb{E}_n[\mathbb{E}_{n+1}[Z]]=Z_n$。直觉:对同一随机变量的逐次估计越来越准,但无系统性升降倾向(类比有效市场——可预期的超额表现早被计入)。

**Q6. 为什么不能在风险中性测度下做效用最大化?**
A:$\tilde{\mathbb{P}}$ 下股票与货币市场期望收益率都是 $r$,无风险溢价可言,风险厌恶者会只投货币市场。风险-收益权衡必须在真实测度下刻画;但预算约束 $\tilde{\mathbb{E}}[X_N/(1+r)^N]=X_0$ 又把 $\tilde{\mathbb{P}}$ 引了回来。

**Q7. 状态价格密度法(鞅方法)怎么解最优投资?为什么比动态规划好?**
A:两步——① 把"选策略"换成"选终值 $X_N$",一阶条件 $U'(X_N)=\lambda\zeta$ 给出 $X_N^*=I(\lambda Z/(1+r)^N)$,由预算约束定 $\lambda$;② 把 $X_N^*$ 当 payoff 用定理 1.2.2 复制。优点:变量从 $2^N$ 个 $\Delta$ 降到一个标量 $\lambda$,避免随期数指数膨胀。

**Q8. 对数效用的最优终值财富闭式?**
A:$U=\ln x\Rightarrow I(y)=1/y$,$X_N^*=\dfrac{X_0(1+r)^N}{Z}$,即 $Z$ 越大(风险中性相对高估)的路径分配越少财富;$\lambda=1/X_0$。

**Q9. 真实测度与风险中性测度各在什么场景用?**
A:**定价衍生品**只需 $\tilde{\mathbb{P}}$;**资产管理**(权衡真实风险与真实收益)和**风险管理**(灾难事件的真实概率)需 $\mathbb{P}$。但风险管理里组合含衍生品,其情景价仍要用 $\tilde{\mathbb{P}}$ 算。

**Q10. 完备市场 vs 不完备市场下,无套利定价还成立吗?**
A:本书的无套利定价以**完备市场**为前提(任何 payoff 可复制 → 价格唯一)。不完备市场里价格不能仅由无套利确定,需效用基础模型;实务中仍广泛(不严格地)套用风险中性定价。

---

### 附:小结 / Summary(§3.4)
变更测度的核心是 $Z=\tilde{\mathbb{P}}/\mathbb{P}$:严格正、$\mathbb{E}Z=1$、$\tilde{\mathbb{E}}Y=\mathbb{E}[ZY]$;过程版 $Z_n=\mathbb{E}_n[Z]$ 是鞅且 $=(\tfrac{\tilde p}p)^{\#H}(\tfrac{\tilde q}q)^{\#T}$;状态价格密度 $\zeta=Z/(1+r)^N$ 把折现与风险打包,$V_0=\mathbb{E}[\zeta V_N]$。最优投资经 Problem 3.3.1→3.3.3→3.3.5 化为 Lagrange 问题,$X_N^*=I(\lambda Z/(1+r)^N)$,再复制。

### 附:文献注记 / Notes(§3.5)
状态价格思想溯源 **Arrow–Debreu**;最优投资/消费:离散 **Hakansson**、连续 **Merton**;状态价格密度解法 **Pliska**,后由 **Cox–Huang**、**Karatzas–Lehoczky–Shreve** 发展。

### 附:符号对照表 / Notation
| 符号 | 含义 |
|---|---|
| $\mathbb{P},\ \tilde{\mathbb{P}}$ | 真实测度、风险中性测度 |
| $Z=\tilde{\mathbb{P}}/\mathbb{P}$ | Radon-Nikodým 导数(随机变量) |
| $Z_n=\mathbb{E}_n[Z]$ | R-N 导数过程($\mathbb{P}$ 下鞅,$Z_0=1,Z_N=Z$) |
| $\zeta=Z/(1+r)^N,\ \zeta_n=Z_n/(1+r)^n$ | 状态价格密度(及其过程) |
| $\zeta(\omega)\mathbb{P}(\omega)$ | 状态价格(Arrow-Debreu 证券价) |
| $U,\ U',\ I=(U')^{-1}$ | 效用函数、其导数、导数的反函数 |
| $\lambda$ | 拉格朗日乘子 |
| $X_N^*$ | 最优终值财富 |
| $\#H,\#T$ | 序列中正/反面数 |

---

**一句话本章精髓**:Radon-Nikodým 导数 $Z$ 是连接真实测度与风险中性测度的"换轨器",状态价格密度 $\zeta=Z/(1+r)^N$ 把**折现与风险**一并打包;有了它,定价能完全在真实测度下做,最优投资也能用一个标量乘子 $\lambda$ 解出——这正是连续时间里 **Girsanov 定理 + 鞅方法** 的离散预演。
