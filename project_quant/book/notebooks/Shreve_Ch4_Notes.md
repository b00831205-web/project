# Shreve《Stochastic Calculus for Finance I》Ch.4 学习笔记
## 美式衍生品 / American Derivative Securities

> **一句话主线**:美式期权可在到期前**任意时刻行权**,于是定价多了一个"何时行权"的维度。两条线:
> 1. **从鞅到上鞅 (Martingale → Supermartingale)**:欧式折现价是鞅;美式折现价在风险中性测度下是**上鞅**(holder 错过最优行权点就会掉价)。定价公式从"逆推取期望"升级成"逆推时与**内在价值**取 max"。
> 2. **停时与最优行权 (Stopping times & optimal exercise)**:行权策略必须是**停时**(只能看过去、不能看未来);最优停时是"价值首次等于内在价值"的时刻。一个反直觉结论:**无分红股票的美式看涨期权永不提前行权**,与欧式同价。
>
> 记号:$g$ 内在价值函数(payoff),$G_n$ 内在价值过程(路径依赖),$V_n$ 期权价,$X_n$ 对冲组合,$C_n\ge0$ 消费,$\tau$ 停时,$n\wedge\tau=\min(n,\tau)$,$\mathcal S_n$ = 取值于 $\{n,\dots,N,\infty\}$ 的停时集。

---

# §0 速查公式表(写项目时直接查)/ Formula Cheat Sheet

### 0.1 欧式 vs 美式逆推算法(只差一个 max)/ European vs American algorithm

| | 终值 | 逆推 $n=N-1,\dots,0$ |
|---|---|---|
| 欧式 European | $v_N(s)=\max\{g(s),0\}$ | $v_n(s)=\frac{1}{1+r}[\tilde p\,v_{n+1}(us)+\tilde q\,v_{n+1}(ds)]$ |
| 美式 American | $v_N(s)=\max\{g(s),0\}$ | $v_n(s)=\max\{\,g(s),\ \frac{1}{1+r}[\tilde p\,v_{n+1}(us)+\tilde q\,v_{n+1}(ds)]\,\}$ |

> **唯一区别**:美式每个节点都和**当前行权的内在价值** $g(s)$ 取 max(continuation value vs intrinsic value)。

### 0.2 带消费的复制对冲 / Replication with consumption(Thm 4.2.2 / 4.4.4)

$$\Delta_n=\frac{V_{n+1}(\cdots H)-V_{n+1}(\cdots T)}{S_{n+1}(\cdots H)-S_{n+1}(\cdots T)}$$
$$C_n=V_n-\frac{1}{1+r}[\tilde p\,V_{n+1}(\cdots H)+\tilde q\,V_{n+1}(\cdots T)]\ \ge 0$$
$$X_{n+1}=\Delta_n S_{n+1}+(1+r)(X_n-C_n-\Delta_n S_n)$$
令 $X_0=V_0$ 向前演化,则所有路径 $X_n=V_n\ge g(S_n)$。$C_n>0$ 恰发生在"该行权而 holder 没行权"的节点——卖方可把多出的价值消费掉,仍维持对冲。

### 0.3 一般(路径依赖)美式理论 / General path-dependent theory(§4.4)

**美式风险中性定价公式 (4.4.1)**:
$$V_n=\max_{\tau\in\mathcal S_n}\tilde{\mathbb{E}}_n\Big[\mathbb{1}_{\{\tau\le N\}}\frac{1}{(1+r)^{\tau-n}}G_\tau\Big]$$

**逆推算法 (4.4.11)**:$V_n=\max\{\,G_n,\ \frac{1}{1+r}[\tilde p\,V_{n+1}(\cdots H)+\tilde q\,V_{n+1}(\cdots T)]\,\}$

**最优停时 (Thm 4.4.5)**:$\tau^*=\min\{n:\ V_n=G_n\}$(价值首次跌到等于内在价值的时刻;若从不相等则 $\tau^*=\infty$,放到期)

**刻画 (Thm 4.4.2)**:$V_n$ 是满足下面两条的**最小**过程——(i) $V_n\ge\max\{G_n,0\}$;(ii) 折现价 $\frac{V_n}{(1+r)^n}$ 是上鞅。

### 0.4 停时与可选抽样 / Stopping times & optional sampling(§4.3)

- **停时定义**:$\tau$ 取值 $\{0,\dots,N,\infty\}$,且若 $\tau(\omega_1\cdots\omega_n\cdots)=n$,则对所有后续 $\omega'$ 也有 $\tau(\omega_1\cdots\omega_n\omega'\cdots)=n$——**只看前 $n$ 次,不能预知未来**。
- **停止过程** $Y_{n\wedge\tau}$:时间继续走,但**值在 $\tau$ 时刻冻结**($n\wedge\tau=\min$)。
- **Optional Sampling I (Thm 4.3.2)**:鞅/上鞅/下鞅在停时处停止,仍是鞅/上鞅/下鞅。
- **Optional Sampling II (Thm 4.3.3)**:下鞅 $\Rightarrow\mathbb{E}[X_{n\wedge\tau}]\le\mathbb{E}[X_n]$;上鞅 $\Rightarrow\ge$;鞅 $\Rightarrow=$。

### 0.5 美式看涨 = 欧式看涨 / American call = European call(Thm 4.5.1)

凸 payoff $g$ 且 $g(0)=0$(如 call $(s-K)^+$)、$r\ge0$:美式价 $=$ 欧式价,**提前行权毫无价值**。
> 原因:折现内在价值 $\frac{g^+(S_n)}{(1+r)^n}$ 在风险中性下是**下鞅**(有上升趋势),由 optional sampling,任何停时都不优于等到 $N$。put 的折现内在价值不是下鞅,故可能提前行权。

### 0.6 教材数值算例(写单元测试时拿来对答案)/ Canonical test case

两期 $S_0=4,u=2,d=\tfrac12,r=\tfrac14\Rightarrow\tilde p=\tilde q=\tfrac12$,美式 put $K=5$,$g(s)=5-s$。$\frac{1}{1+r}=\tfrac45$,单步 $=\tfrac45\cdot\tfrac12(\cdot+\cdot)=\tfrac25(\cdot+\cdot)$:

| 节点 | 计算 | 价 |
|---|---|---|
| $v_2(16),v_2(4),v_2(1)$ | $\max\{5-s,0\}$ | $0,\ 1,\ 4$ |
| $v_1(8)$ | $\max\{-3,\ \tfrac25(0{+}1)\}$ | $0.40$(等待) |
| $v_1(2)$ | $\max\{3,\ \tfrac25(1{+}4)=2\}$ | $\mathbf{3}$(**行权**) |
| $v_0(4)$ | $\max\{1,\ \tfrac25(0.40{+}3)\}$ | $\mathbf{1.36}$ |

对比欧式 put 同参数 $v_0(4)=0.864$(见 Ch1 笔记):美式 $1.36>0.864$,差额即**提前行权溢价**。
折现价 $Y_n=(\tfrac45)^n v_n$:$Y_0=1.36,Y_1(H)=0.32,Y_1(T)=2.40,Y_2=0,0.64,2.56$。在 $T$ 节点 $2.40>\tfrac12(0.64)+\tfrac12(2.56)=1.60$ → **严格上鞅**;停在 $\tau$ 后变鞅。

---

# §1 非路径依赖的美式期权 / Non-Path-Dependent American Derivatives(§4.2)

### 1.1 美式算法 / The American algorithm
美式期权在任意 $n$ 可行权拿 $g(S_n)$,故对冲组合须**时时** $X_n\ge g(S_n)$。把欧式逆推 (4.2.2) 改成每步与内在价值取 max:
$$v_N(s)=\max\{g(s),0\},\qquad v_n(s)=\max\Big\{g(s),\ \tfrac{1}{1+r}[\tilde p\,v_{n+1}(us)+\tilde q\,v_{n+1}(ds)]\Big\}$$
则 $V_n=v_n(S_n)$ 即美式价(payoff 只依赖当前 $S_n$,故 Markov 化简成立)。

### 1.2 例 4.2.1:两期美式 put / Worked example
见 §0.6。关键节点 $v_1(2)=\max\{3,2\}=3$:**内在价值 3 严格大于等待价值 2**,所以这里应立即行权。正是这一个节点让美式价 $1.36$ 高于欧式。

### 1.3 带消费的复制 / Replication with consumption(Thm 4.2.2)
卖方从 $X_0=v_0(S_0)$ 出发,用 $\Delta_n$(同欧式 1.2.17)对冲。但因 holder 可能**不在最优时刻行权**,卖方在"该行权未行权"的节点会有**多余价值**,可消费 $C_n\ge0$(4.2.8)。财富方程加入消费项 (4.2.9):
$$X_{n+1}=\Delta_n S_{n+1}+(1+r)(X_n-C_n-\Delta_n S_n)$$
结论:$X_n=v_n(S_n)\ge g(S_n)$ 对所有路径成立——**无论 holder 何时行权,卖方都对冲得住**。
> 例 4.2.1 中第一次为 $T$、holder 在 $t{=}1$ 没行权:卖方组合值 $v_1(2)=3$,而继续对冲只需 $2$,于是**消费 \$1**,用剩下的 \$2 继续对冲。

---

# §2 停时 / Stopping Times(§4.3)

### 2.1 停时定义(不能预知未来)/ Definition 4.3.1
$\tau$ 取值于 $\{0,1,\dots,N,\infty\}$,且**在 $n$ 停止的决定只能依赖前 $n$ 次抛掷**。
- **合法停时**(例 4.3.1):$\tau(HH)=\infty,\tau(HT)=2,\tau(TH)=\tau(TT)=1$。
- **非法**(例 4.3.2):$\rho(HH)=0,\rho(HT)=0,\rho(TH)=1,\rho(TT)=2$——要求 $t{=}0$ 就根据第一次抛掷结果决定,等于"内幕信息",不是停时。

### 2.2 停止过程 / Stopped process
$Y_{n\wedge\tau}$:时间不停,**值在 $\tau$ 冻结**。例:$Y_{2\wedge\tau}(TH)=Y_1(T)=2.40$(因 $\tau(TH)=1$,值停在 $t{=}1$)。

### 2.3 可选抽样定理 / Optional Sampling
- **Part I (Thm 4.3.2)**:鞅(上/下鞅)停在停时处,仍是鞅(上/下鞅)。
  - 折现 American put 价是上鞅,停在最优停时 $\tau$ 后变**鞅**:$2.40=Y_{1\wedge\tau}(T)=\tfrac12(2.40)+\tfrac12(2.40)$。
  - 折现股价 $M_n=(\tfrac45)^nS_n$ 是鞅,停在合法 $\tau$ 后仍是鞅;但停在**非停时** $\rho$(向前看)会破坏鞅性、引入向下偏差。
- **Part II (Thm 4.3.3)**:$\mathbb{E}[X_{n\wedge\tau}]$ 与 $\mathbb{E}[X_n]$ 的大小关系随鞅类型而定(下鞅 $\le$,上鞅 $\ge$,鞅 $=$)。

---

# §3 一般美式期权理论 / General American Derivatives(§4.4)

### 3.1 路径依赖定价公式 / Path-dependent pricing formula
内在价值过程 $G_n$(依赖前 $n$ 次)。**美式风险中性定价 (4.4.1)**:
$$V_n=\max_{\tau\in\mathcal S_n}\tilde{\mathbb{E}}_n\Big[\mathbb{1}_{\{\tau\le N\}}\tfrac{1}{(1+r)^{\tau-n}}G_\tau\Big]$$
即"在所有合法停时里,选折现期望 payoff 最大的那个"。特例 $V_N=\max\{G_N,0\}$ (4.4.2)。

### 3.2 三条核心定理 / Three theorems
- **Thm 4.4.2(刻画)**:$V_n$ 是满足 (i) $V_n\ge\max\{G_n,0\}$ 且 (ii) 折现价为上鞅 的**最小**过程。
  - (i)+(ii) ⟹ 卖方报价**够用**(能对冲);(iii) 最小 ⟹ 报价**不虚高**,对买方公平。
- **Thm 4.4.3(算法)**:$V_n=\max\{G_n,\ \tfrac{1}{1+r}[\tilde p\,V_{n+1}(\cdots H)+\tilde q\,V_{n+1}(\cdots T)]\}$,即 §0.1 美式逆推的路径依赖版。
- **Thm 4.4.4(复制)**:$\Delta_n,C_n,X_{n+1}$ 同 §0.2,$X_n=V_n$。证明 $X_{n+1}(H)=V_{n+1}(H)$ 的代数关键:$\tfrac{u-1-r}{u-d}=\tilde q$,$\tilde p+\tilde q=1$。

### 3.3 最优行权时刻 / Optimal exercise(Thm 4.4.5)
$$\tau^*=\min\{n:\ V_n=G_n\}$$
即**价值首次等于内在价值**的时刻。证明用到:折现停止过程 $\tfrac{1}{(1+r)^{n\wedge\tau^*}}V_{n\wedge\tau^*}$ 是鞅,于是 $V_0=\tilde{\mathbb{E}}[\mathbb{1}_{\{\tau^*\le N\}}\tfrac{1}{(1+r)^{\tau^*}}G_{\tau^*}]$。
> 直觉:$V_n>G_n$ 时,折现价严格上鞅(还有等待价值),不该行权;一旦 $V_n=G_n$,继续持有会掉价,应立即行权。若期权始终价外($V_n>G_n$ 恒成立),则 $\tau^*=\infty$,放到期。
> 与第 2 章 Thm 2.4.8 衔接:按 $\tau^*$ 行权等价于一个在 $\tau^*$ 付 $G_{\tau^*}$ 的现金流,其时刻 0 价正是 $V_0$。

---

# §4 美式看涨期权 / American Call Options(§4.5)

### 4.1 主结论 / Main result(Thm 4.5.1)
凸 payoff $g$ 且 $g(0)=0$、利率 $r\ge0$ ⟹ 美式价 $V_0^A=$ 欧式价 $V_0^E$。**无分红股票的美式 call 提前行权零价值**。

### 4.2 证明骨架 / Proof sketch
令 $g^+=\max\{g,0\}$(仍凸、$g^+(0)=0$)。
1. 凸 + $g^+(0)=0$ ⟹ $g^+(\lambda s)\le\lambda g^+(s)$,$\lambda\in[0,1]$ (4.5.4)。
2. 股价鞅性:$S_n=\tilde{\mathbb{E}}_n[\tfrac{1}{1+r}S_{n+1}]$。
3. 条件 Jensen(Thm 2.3.2(v)):$g^+(\tilde{\mathbb{E}}_n[\tfrac{S_{n+1}}{1+r}])\le\tilde{\mathbb{E}}_n[g^+(\tfrac{S_{n+1}}{1+r})]$ (4.5.5)。
4. 取 $\lambda=\tfrac{1}{1+r}$ 代入第 1 步:$g^+(\tfrac{S_{n+1}}{1+r})\le\tfrac{1}{1+r}g^+(S_{n+1})$ (4.5.6)。
5. 合并 ⟹ $\tfrac{1}{(1+r)^n}g^+(S_n)\le\tilde{\mathbb{E}}_n[\tfrac{1}{(1+r)^{n+1}}g^+(S_{n+1})]$,即折现内在价值是**下鞅**。
6. 下鞅 + optional sampling (Thm 4.3.3) ⟹ 任何停时 $\tau$:$\tilde{\mathbb{E}}[\tfrac{g^+(S_{N\wedge\tau})}{(1+r)^{N\wedge\tau}}]\le\tilde{\mathbb{E}}[\tfrac{g^+(S_N)}{(1+r)^N}]=V_0^E$,故 $V_0^A\le V_0^E$;又显然 $V_0^A\ge V_0^E$,得等号。

### 4.3 call vs put 的不对称(高频面试点)/ The call–put asymmetry
- **Call**:行权要**付出** $K$。delay 行权 ⟹ 让 $K$ 被折现"贬值"是**好事**,强化凸性效应 ⟹ 永不提前行权。
- **Put**:行权能**收到** $K$。早行权可在 $K$ 被折现贬值前锁定它;对深度价内(低股价)的 put,这一效应压过凸性 ⟹ **提前行权变优**。
- **分红改变 call 故事**:若股票分红,股价会因分红下跌,持有 call 的人可能想在分红前提前行权——此时美式 call 提前行权可能有价值。

---

# §5 面试速答 / Interview Quick-Fire

> 用法:遮住答案先复述,再核对。这一章几条是买方/做市面试的高频题。

**Q1. 欧式 vs 美式,折现价的鞅性质有何区别?**
A:欧式折现价在风险中性下是**鞅**;美式是**上鞅**——holder 若错过最优行权点,期权有掉价倾向。在"不该行权"的时段,美式折现价表现得像鞅。

**Q2. 为什么无分红股票的美式看涨期权永不提前行权?(经典题)**
A:折现内在价值 $(s-K)^+/(1+r)^n$ 在风险中性下是**下鞅**(凸 payoff + 股价鞅性 + 条件 Jensen),有上升趋势,等到到期最优。直觉:行权要付 $K$,延迟行权让 $K$ 被折现贬值是好事,与凸性同向 ⟹ 不提前。故美式 call 价 = 欧式 call 价。

**Q3. 那为什么美式 put 可能提前行权?**
A:put 行权能**收到** $K$;早行权锁定 $K$、避免其被折现贬值。对深度价内的 put,这一效应超过凸性带来的"等待溢价",提前行权变优。其折现内在价值不是下鞅。

**Q4. 什么是停时?为什么行权策略必须是停时?**
A:停时 $\tau$ 在 $n$ 停止的决定只依赖前 $n$ 次信息、不能预知未来。行权必须是停时,否则等于用"内幕信息"(如 $\rho$:$t{=}0$ 就按第一次抛掷决定),现实中无法实施。

**Q5. 美式期权的最优行权规则?**
A:$\tau^*=\min\{n:V_n=G_n\}$,即**价值首次等于内在价值**的时刻。此前 $V_n>G_n$(有等待价值,折现价严格上鞅);此刻起继续持有会掉价,应行权。

**Q6. 什么是可选抽样定理(Optional Sampling)?**
A:鞅/上鞅/下鞅在停时处停止,仍保持各自类型(Part I);且 $\mathbb{E}[X_{n\wedge\tau}]$ 与 $\mathbb{E}[X_n]$ 的不等方向随类型而定(Part II)。它是把"美式折现价上鞅、停在 $\tau^*$ 后变鞅"严格化的工具。

**Q7. 怎么对冲一个美式期权空头?和欧式有何不同?**
A:用同样的 $\Delta_n=\Delta V/\Delta S$,但财富方程**加入消费项** $C_n\ge0$。在"holder 该行权却没行权"的节点,卖方组合值高于继续对冲所需,可消费多余部分,仍保证 $X_n=V_n\ge g(S_n)$,无论何时被行权都赔得起。

**Q8. 什么是提前行权溢价(early exercise premium)?**
A:美式价减去同条件欧式价。call(无分红)为 0;put 可观。例 4.2.1:美式 put $1.36$ vs 欧式 $0.864$,溢价来自 $v_1(2)$ 那个该行权的节点。

**Q9. 为什么美式 straddle 价 < 美式 put 价 + 美式 call 价?(Ex 4.1)**
A:跨式可看成 put+call,但**只能选一个停时**;而分开持有 put、call 各自用**最优停时**(通常不同时刻)。约束更紧 ⟹ 跨式价严格小于两者之和。

**Q10. 什么是 Bermudan 期权?**
A:介于欧式与美式之间——只能在合约指定的**有限个日期**行权。定价用美式逆推算法,但只在允许的日期与内在价值取 max。

---

### 附:小结 / Summary(§4.6）
美式期权价 $\ge$ 内在价值;折现价是风险中性**上鞅**,在该行权时刻有掉价倾向。$V_n$ 是支配内在价值的**最小非负上鞅**(Thm 4.4.2),由逆推算法 (4.4.10/4.4.11) 计算;空头可用 (4.4.14) 对冲并在下行时段消费 (4.4.15);最优行权是"价值首次等于内在价值"(Thm 4.4.5)。停时 + optional sampling 证明了无分红美式 call = 欧式 call(Thm 4.5.1)。

### 附:文献注记 / Notes(§4.7）
基于停时的美式期权严格分析始于 **Bensoussan**,由 **Karatzas** 继续,系统处理见 **Karatzas–Shreve**;原始理论为连续时间,本书特化到二叉树。

### 附:符号对照表 / Notation
| 符号 | 含义 |
|---|---|
| $g(s),\ g^+(s)=\max\{g,0\}$ | 内在价值函数(payoff)及其非负部分 |
| $G_n$ | 内在价值过程(路径依赖,依赖前 $n$ 次) |
| $V_n,\ v_n(s)$ | 美式期权价(随机变量 / Markov 函数形式) |
| $X_n$ | 对冲组合价值 |
| $\Delta_n$ | 持股份额;$C_n\ge0$ 消费 |
| $\tau,\ \tau^*$ | 停时;最优停时 $\min\{n:V_n=G_n\}$ |
| $n\wedge\tau$ | $\min(n,\tau)$ |
| $\mathcal S_n$ | 取值 $\{n,\dots,N,\infty\}$ 的停时集 |
| $Y_{n\wedge\tau}$ | 停止过程(值在 $\tau$ 冻结) |

---

**一句话本章精髓**:美式期权 = 欧式期权 + "何时行权"的最优停时问题;折现价从鞅退化为**上鞅**,定价是"逆推时与内在价值取 max",最优行权是"价值首次触及内在价值";由凸性 + Jensen 可证**无分红美式 call 永不提前行权、与欧式同价**,而 put 因能提前锁定行权金 $K$ 而存在提前行权溢价。
