"""
@File   ：cascading_failure_single_mechanism_algorithm.py
@Desc   :  单层单机制级联失效算法层封装

该模块对上提供通用的 Python 函数接口，
并在模块内部提供 `CascadeFailuresModel_SingleMechanism` 的实现。

约定：
- 机制层只关注 state/load/capacity 三个量以及负载重分配规则；
- 业务模型（例如银行系统性风险模型）负责把自己的状态
  （资产负债表、资本缓冲、违约状态等）映射为 load/capacity 等，
  再调用本算法层。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np


STATE_NORMAL = 0
STATE_FAILED = 1


class CascadeFailuresModel_SingleMechanism:
    """单层单机制级联失效模型（SRS 内置实现）。"""

    def __init__(
        self,
        adjacency: np.ndarray,
        N: int,
        steps: int = 200,
        seed: Optional[int] = None,
        load_redundancy: float = 0.0,
        early_stop_patience: int = 10,
        redistribution_mode: str = "average",
        redistribution_weights: Optional[np.ndarray] = None,
        random_dirichlet_alpha: float = 1.0,
    ):
        self.adjacency = np.asarray(adjacency, dtype=float)
        self.N = int(N)
        self.steps = int(steps)
        self.seed = seed
        self.load_redundancy = float(load_redundancy)
        self.early_stop_patience = int(early_stop_patience)
        self.redistribution_mode = redistribution_mode
        self.redistribution_weights = (
            None if redistribution_weights is None else np.asarray(redistribution_weights, dtype=float)
        )
        self.random_dirichlet_alpha = float(random_dirichlet_alpha)

        self.load = np.zeros(self.N, dtype=float)
        self.capacity = np.zeros(self.N, dtype=float)
        self.state = np.full(self.N, STATE_NORMAL, dtype=int)
        self.current_failed = np.full(self.N, False, dtype=bool)
        self._rng = np.random.default_rng(self.seed)

    def initialize(self, load_init_max: float = 0.0, use_degree: bool = True):
        """兼容接口：初始化由业务侧覆盖的 load/capacity 容器。"""
        self.load[:] = 0.0
        self.capacity[:] = 0.0
        self.state[:] = STATE_NORMAL
        self.current_failed[:] = False

    def _calc_probs(self, weights: np.ndarray) -> np.ndarray:
        positive = weights > 0.0
        if not positive.any():
            return np.zeros_like(weights)

        mode = (self.redistribution_mode or "average").lower()
        probs = np.zeros_like(weights)

        if mode == "average":
            probs[positive] = 1.0 / positive.sum()
            return probs

        if mode == "random":
            alpha = max(self.random_dirichlet_alpha, 1e-12)
            vec = self._rng.dirichlet(np.full(positive.sum(), alpha, dtype=float))
            probs[positive] = vec
            return probs

        # default proportional
        s = weights[positive].sum()
        if s <= 0.0:
            probs[positive] = 1.0 / positive.sum()
        else:
            probs[positive] = weights[positive] / s
        return probs

    def run(self, is_record_history: bool = True) -> Dict[str, Any]:
        history = {"states": [], "loads": [], "capacities": []} if is_record_history else None
        no_change_rounds = 0

        for _ in range(self.steps):
            if is_record_history:
                history["states"].append(self.state.copy())
                history["loads"].append(self.load.copy())
                history["capacities"].append(self.capacity.copy())

            overloaded = self.load > (self.capacity * (1.0 + self.load_redundancy))
            newly_failed = overloaded & (~self.current_failed)

            if not newly_failed.any():
                no_change_rounds += 1
                if no_change_rounds >= self.early_stop_patience:
                    break
                continue

            no_change_rounds = 0
            added = np.zeros_like(self.load)

            for i in np.where(newly_failed)[0]:
                outflow = max(self.load[i], 0.0)
                if outflow <= 0.0:
                    self.load[i] = 0.0
                    continue

                weights = self.adjacency[i].astype(float, copy=True)

                # 失效节点不接收再分配负载
                alive_mask = ~self.current_failed
                alive_mask[i] = False
                weights[~alive_mask] = 0.0

                if self.redistribution_weights is not None:
                    weights = weights * self.redistribution_weights

                probs = self._calc_probs(weights)
                if probs.sum() > 0.0:
                    added += outflow * probs

                self.load[i] = 0.0

            self.load += added
            self.current_failed[newly_failed] = True
            self.state[self.current_failed] = STATE_FAILED

        result: Dict[str, Any] = {"final_state": self.state.copy()}
        if is_record_history:
            result["history"] = {
                "states": np.asarray(history["states"]),
                "loads": np.asarray(history["loads"]),
                "capacities": np.asarray(history["capacities"]),
            }
        return result


def _ensure_numpy_1d(arr, name: str) -> np.ndarray:
    """将输入转换为 1D numpy 数组，便于内部统一处理。"""
    if arr is None:
        raise ValueError(f"`{name}` 不能为空。")
    a = np.asarray(arr)
    if a.ndim != 1:
        raise ValueError(f"`{name}` 必须是一维数组，当前 ndim={a.ndim}。")
    return a.astype(float, copy=False)


def run_single_mechanism_cascade(
    adjacency: np.ndarray,
    load: np.ndarray,
    capacity: np.ndarray,
    initial_failed_mask: Optional[np.ndarray] = None,
    *,
    steps: int = 200,
    seed: Optional[int] = None,
    load_redundancy: float = 0.0,
    early_stop_patience: int = 10,
    redistribution_mode: str = "average",
    redistribution_weights: Optional[np.ndarray] = None,
    random_dirichlet_alpha: float = 1.0,
    record_history: bool = True,
) -> Dict[str, Any]:
    """
    运行单层单机制级联失效过程的通用入口函数。

    该函数对外暴露给各类业务模型使用：
    - 业务层提供网络结构 `adjacency`、当前负载 `load` 与容量阈值
      `capacity`，以及外生给定的初始失效集合 `initial_failed_mask`；
    - 算法层内部构造并运行 `CascadeFailuresModel_SingleMechanism`，
      返回最终状态与（可选）演化历史。

    Args:
        adjacency: np.ndarray 邻接矩阵 (N, N)，表示节点间负载重分配的权重结构。
        load: np.ndarray 初始负载数组 (N,)，表示每个节点的初始负载值。
        capacity: np.ndarray 容量阈值数组 (N,)，表示每个节点的容量上限。
        initial_failed_mask: Optional[np.ndarray] 可选的一维布尔数组 (N,)，
            指示初始失效节点的位置。若为 None，则假设所有节点初始均为正常状态。
        steps: int 最大迭代步数。
        seed: Optional[int] 随机种子，用于可重复的随机过程。
        load_redundancy: float 负载冗余比例，用于调整节点容量。
        early_stop_patience: int 早停耐心值，连续多少步无新失效则提前终止。
        redistribution_mode: str 负载重分配模式，支持 "average"、"proportional" 等。
        redistribution_weights: Optional[np.ndarray] 可选的重分配权重数组 (N,)，
            用于自定义节点间负载分配比例。
        random_dirichlet_alpha: float 随机Dirichlet分布的alpha参数，用于引入随机性。
        record_history: bool 是否记录演化历史，若为 True 则返回每步的状态快照。

    Returns:
        Dict[str, Any] 包含以下键值对：
            - "final_state": np.ndarray 最终节点状态数组 (N,)，0=正常，1=失效。
            - "history": Optional[Dict[str, np.ndarray]] 可选的演化历史字典，
              包含 "states"、"loads"、"capacities" 等键。
            - "final_failed_mask": np.ndarray 最终失效节点的布尔数组 (N,)。


    Examples:
        >>> adjacency = np.array([[0, 1], [1, 0]])
        >>> load = np.array([5.0, 3.0])
        >>> capacity = np.array([4.0, 4.0])
        >>> initial_failed_mask = np.array([True, False])
        >>> result = run_single_mechanism_cascade(
        ...     adjacency=adjacency,
        ...     load=load,
        ...     capacity=capacity,
        ...     initial_failed_mask=initial_failed_mask,
        ...     steps=100,
        ...     seed=42,
        ...     load_redundancy=0.1,
        ...     early_stop_patience=5,
        ...     redistribution_mode="average",
        ...     record_history=True
        ... )
        >>> print(result["final_failed_mask"])
        [ True  True]

    """

    A = np.asarray(adjacency, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("`adjacency` 必须是方阵 (N, N)。")

    N = A.shape[0]
    load_arr = _ensure_numpy_1d(load, "load")
    capacity_arr = _ensure_numpy_1d(capacity, "capacity")
    if load_arr.shape[0] != N or capacity_arr.shape[0] != N:
        raise ValueError("`load` 与 `capacity` 的长度必须与 adjacency 的规模一致。")

    if initial_failed_mask is not None:
        init_fail = np.asarray(initial_failed_mask, dtype=bool)
        if init_fail.ndim != 1 or init_fail.shape[0] != N:
            raise ValueError("`initial_failed_mask` 必须是一维布尔数组，长度为 N。")
    else:
        init_fail = np.zeros(N, dtype=bool)

    model = CascadeFailuresModel_SingleMechanism(
        adjacency=A,
        N=N,
        steps=steps,
        seed=seed,
        load_redundancy=load_redundancy,
        early_stop_patience=early_stop_patience,
        redistribution_mode=redistribution_mode,
        redistribution_weights=redistribution_weights,
        random_dirichlet_alpha=random_dirichlet_alpha,
    )

    # 使用机制层的 initialize 以设置好基本结构，然后用业务侧给定值覆盖
    model.initialize(load_init_max=0.0, use_degree=True)
    model.load[:] = load_arr
    model.capacity[:] = capacity_arr

    # 初始化失效状态
    if init_fail.any():
        model.state[init_fail] = STATE_FAILED
        model.current_failed[init_fail] = True

    result_core = model.run(is_record_history=record_history)

    final_state = result_core["final_state"]
    final_failed_mask = final_state == STATE_FAILED

# 补充机制层运行后对业务有用的原始量：最终负载与最终容量
    result: Dict[str, Any] = {
        **result_core,
        "final_failed_mask": final_failed_mask,
        "load_final": model.load.copy(),
        "capacity": model.capacity.copy(),
    }
    return result


def run_bank_interbank_cascade(
    *,
    Z_IB: np.ndarray,
    E_all: np.ndarray,
    Z_IB_all: np.ndarray,
    Loss_exIB_init: np.ndarray,
    Loss_IB_init: Optional[np.ndarray] = None,
    initial_failed_mask: Optional[np.ndarray] = None,
    steps: int = 200,
    seed: Optional[int] = None,
    load_redundancy: float = 0.0,
    early_stop_patience: int = 10,
    redistribution_mode: str = "average",
    redistribution_weights: Optional[np.ndarray] = None,
    random_dirichlet_alpha: float = 1.0,
    record_history: bool = True,
) -> Dict[str, Any]:
    """基于银行间资产负债表变量的单机制级联失效封装。

    该函数专门服务于 SystemicRiskSimulator 中的银行网络模型，
    根据给定的 interbank 资产矩阵和资产负债变量，构造：

    - adjacency: 从 `Z_IB` 归一化得到的邻接矩阵（行归一化为权重）；
    - load: 初始负载 = 外部资产损失 + 已有银行间损失；
    - capacity: 节点容量 = 资本 + interbank 资产总额；
    - initial_failed_mask: 初始失效集合，可显式给定；若为 None，
      则根据 `load > capacity` 自动判断初始失效节点。

    返回值在 `run_single_mechanism_cascade` 的基础上补充：
    - "adjacency"、"load_init"、"capacity"，便于业务侧后处理。
    """

    Z = np.asarray(Z_IB, dtype=float)
    if Z.ndim != 2 or Z.shape[0] != Z.shape[1]:
        raise ValueError("`Z_IB` 必须是方阵 (N, N)。")
    N = Z.shape[0]

    E = _ensure_numpy_1d(E_all, "E_all")
    Z_total = _ensure_numpy_1d(Z_IB_all, "Z_IB_all")
    Loss_ex = _ensure_numpy_1d(Loss_exIB_init, "Loss_exIB_init")
    if Loss_IB_init is None:
        Loss_IB = np.zeros_like(Loss_ex)
    else:
        Loss_IB = _ensure_numpy_1d(Loss_IB_init, "Loss_IB_init")

    if not (E.shape[0] == Z_total.shape[0] == Loss_ex.shape[0] == Loss_IB.shape[0] == N):
        raise ValueError("E_all / Z_IB_all / Loss_exIB_init / Loss_IB_init 长度必须与 Z_IB 规模一致。")

    # 邻接矩阵：按行归一化的权重，表示从 i 向 j 的负载分配比例
    row_sum = Z.sum(axis=1, keepdims=True)
    adjacency = np.divide(Z, row_sum, out=np.zeros_like(Z), where=row_sum > 0.0)

    # 节点容量：资本 + interbank 资产总额（可视为一阶近似）
    capacity = E + Z_total

    # 初始负载：外部资产损失 + 已有 interbank 损失
    load = Loss_ex + Loss_IB

    if initial_failed_mask is None:
        init_failed_mask = load > (capacity * (1.0 + load_redundancy))
    else:
        init_failed_mask = np.asarray(initial_failed_mask, dtype=bool)
        if init_failed_mask.ndim != 1 or init_failed_mask.shape[0] != N:
            raise ValueError("`initial_failed_mask` 必须是一维布尔数组，长度为 N。")

    result = run_single_mechanism_cascade(
        adjacency=adjacency,
        load=load,
        capacity=capacity,
        initial_failed_mask=init_failed_mask,
        steps=steps,
        seed=seed,
        load_redundancy=load_redundancy,
        early_stop_patience=early_stop_patience,
        redistribution_mode=redistribution_mode,
        redistribution_weights=redistribution_weights,
        random_dirichlet_alpha=random_dirichlet_alpha,
        record_history=record_history,
    )

    # 补充一些对业务模型有用的原始量
    result.update(
        {
            "adjacency": adjacency,
            "load_init": load,
            "capacity": capacity,
        }
    )
    return result


__all__ = ["run_single_mechanism_cascade", "run_bank_interbank_cascade"]
