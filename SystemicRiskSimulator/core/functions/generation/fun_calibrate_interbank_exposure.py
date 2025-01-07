"""
计算双边敞口边权重。

- 使用中心边缘连接算法（Center Peripheral Connection），通过各银行之银行间资产与银行间负债估算银行间双边敞口。
- 使用最大熵值法（Maximum Entropy），通过各银行之银行间资产与银行间负债估算银行间双边敞口。
"""

__all__ = [
    'calculate_bilateral_exposure_by_CP_method',
    'calculate_bilateral_exposure_by_ME_method',
    'calculate_bilateral_exposure_by_ME_method_with_preset_fixed_values',
    'calculate_bilateral_exposure_by_ME_method_with_density',
    'calibrate_bilateral_exposure_by_ME_method_use_R_package'
]

from SystemicRiskSimulator.external_packages import np, pd, Path, time, logging
from SystemicRiskSimulator.core.functions.fun_adjast_bank_balanceSheet import adjust_A_IB_Z_IB_with_virtual_bank, adjust_A_IB_Z_IB_by_resize
from SystemicRiskSimulator.tools.data_tools import check_risk_exposure_matrix_constraints


# from scipy import optimize

def calculate_bilateral_exposure_by_CP_method(
        A_IB_all: np.ndarray,
        Z_IB_all: np.ndarray,
        array_idx_center_bank: np.ndarray = None,
        num_center=20,
        center_agents_networkDensity: float = 1.0,
        algorithm_link_center_banks: str = 'RAS',
        method_link_center_and_peripheral_banks: str = '随机均匀分布',
        df_classify: pd.DataFrame = None,
        method_adjast_bank_balanceSheet: str = 'add_virtual_bank',
        is_maintain_virtual_bank=False,
        is_show_detal: bool = False,
        iteration_threshold: float = 1e-10,
        max_iteration: int = 100000,
        denominator_precition_threshold: float = 1e-10,
        **kwargs,
):
    """
    使用中心边缘连接算法（Center Peripheral Connection），通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    中心银行之间采用 RAS 算法的全连接方法。中心银行与边缘银行之间采用随机选取的方法。

    Args:
        A_IB_all (np.ndarray): 各银行之银行间总资产。注意，在导入之前需要自行将中心银行排在前面。
        Z_IB_all (np.ndarray): 各银行之银行间总负债。注意，在导入之前需要自行将中心银行排在前面。
        array_idx_center_bank (np.ndarray): 中心银行集合之索引。默认值是 None ，按照中心银行排在前面的顺序，选取前 num_center 个银行。 #TODO 目前只能按照默认方法选取中心银行。
        num_center (int): 中心银行数量。默认值 20
        center_agents_networkDensity (float): 中心银行之间的连接密度。默认值 1.0。这个参数只有在 method_link_center_banks 为 'R语言的systemicrisk包之calibrate_ER' 时才有用
        algorithm_link_center_banks (str): 连接中心银行之间的算法。默认值 'RAS'，即使用 RAS 算法。可选值包括：

            - 'RAS'：使用 RAS 算法； #HACK 暂时还没有实现预置值和指定密度的功能。
            - 'R语言的systemicrisk包之calibrate_ER'：调用 R 语言的 systemicrisk 包之 calibrate_ER 算法。该方法允许根据不同的连接密度生成连接矩阵；

        method_link_center_and_peripheral_banks (str): 连接中心银行与边缘银行之间的方法。默认值 '随机均匀分布'，即使用随机均匀分布的方法。可选值包括：

            - '随机均匀分布'：使用随机均匀分布。遍历所有的边缘银行，对于某一个边缘银行，随机选取一个中心银行与制定的边缘银行连接；
            - '按同分类连接'：根据中心银行与边缘银行之间的分类，连接同一分类的银行。对于同分类的中心银行和边缘银行，根据随机均匀分布的方法连接；

        df_classify (pd.DataFrame): 分类数据框。其中要求自行预先排序按照先中心银行，后边缘银行。这个函数不提供排序功能。要求第一列是银行代码，第二列是银行分类。默认值 None，表示不使用分类数据框。
        method_adjast_bank_balanceSheet (str): 调整银行间总资产总负债不一致的方法。默认值 'add_virtual_bank'，即添加虚拟银行。可选值包括：

            - 'none'：不调整；
            - 'add_virtual_bank'：添加虚拟银行；
            - 'resize'：按照多出来的比例，压缩多出来的金额部分，使得二者相等；

        is_maintain_virtual_bank (bool): 是否保留虚拟银行。默认值 False
        is_show_detal (bool): 是否显示迭代过程的热力图。默认值 False
        iteration_threshold (float): 迭代阈值。默认值 1e-10
        max_iteration (int): 最大迭代次数。默认值 100000
        denominator_precition_threshold (float): 分母接近零精度阈值。默认值 1e-10。
        **kwargs: 其他参数
    """

    # 预处理维度
    A_IB_all, Z_IB_all = A_IB_all.flatten(), Z_IB_all.flatten()

    # 调整银行资产负债表使得总资产与总负债相等

    is_added_virtual_bank = None
    match method_adjast_bank_balanceSheet:
        case 'none':
            # NOTE 调整方案〇：无需调整
            A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
        case 'add_virtual_bank':
            # NOTE 调整方案一：添加虚拟银行
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
                is_added_virtual_bank = False
            else:
                A_IB_adjusted, Z_IB_adjusted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB_all, Z_IB_all)
                is_added_virtual_bank = True
                pass  # if
        case 'resize':
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
            else:
                # #NOTE 调整方案二：调整比例。按照多出来的比例，压缩多出来的金额部分，使得二者相等。
                A_IB_adjusted, Z_IB_adjusted = adjust_A_IB_Z_IB_by_resize(A_IB_all, Z_IB_all)
                pass  # if
        case _:
            raise ValueError("不支持的调整方法！")
            pass  # match

    N = A_IB_adjusted.shape[0]  # 获取银行数量

    A_IB_adjusted = np.array(A_IB_adjusted)
    Z_IB_adjusted = np.array(Z_IB_adjusted)

    match algorithm_link_center_banks:
        case 'R语言的systemicrisk包之calibrate_ER':
            A_IB_0 = np.outer(A_IB_adjusted, Z_IB_adjusted)
            # # 归一化到最大值是银行行和约束或者列和约束最大值
            # A_IB_0 = A_IB_0 / max(np.max(A_IB_adjusted), np.max(Z_IB_adjusted))
        case 'RAS':
            # A_IB_0 = np.outer(A_IB_adjusted, Z_IB_adjusted) / denominator_precition_threshold
            A_IB_0 = np.outer(A_IB_adjusted, Z_IB_adjusted)
            pass  # match

    np.fill_diagonal(A_IB_0, 0)  # 对角线为 0
    A_IB_0[num_center:, num_center:] = 0  # 边缘银行连接为 0

    # 连接中心银行和边缘银行，使用均匀分布的随机选取的方法

    match method_link_center_and_peripheral_banks:
        case '随机均匀分布':
            select_center_banks = np.random.choice(np.arange(num_center), N - num_center)  # 随机选取中心银行，用于被边缘银行连接
            select_peripheral_banks = np.random.choice(np.arange(num_center), N - num_center)  # 随机选取中心银行，用于连接到边缘银行
            # A_IB_0[num_center:, :num_center] = np.where(np.arange(num_center) == select_center_banks[:, np.newaxis], A_IB_0[num_center:, :num_center], 0)  # 对于每一个边缘银行，连接到被选取的一个中心银行  #HACK 这个不适用
            A_IB_0[num_center:, :num_center] = np.where(np.arange(num_center) == select_center_banks[:, np.newaxis], A_IB_adjusted[num_center:, np.newaxis], 0)  # 对于每一个边缘银行，连接到被选取的一个中心银行  #BUG 这个只适用于单个边缘银行只连接一个中心银行的情况
            # A_IB_0[:num_center, num_center:] = np.where(np.arange(num_center)[:, np.newaxis] == select_peripheral_banks, A_IB_0[:num_center, num_center:], 0)  # 对于每一个边缘银行，被所选取的中心银行连接  #HACK 这个不适用
            A_IB_0[:num_center, num_center:] = np.where(np.arange(num_center)[:, np.newaxis] == select_peripheral_banks, Z_IB_adjusted[np.newaxis, num_center:], 0)  # 对于每一个边缘银行，被所选取的中心银行连接  #BUG 这个只适用于单个边缘银行只连接一个中心银行的情况
        case '按同分类连接':  # #HACK #BUG 这个似乎不能用
            if df_classify is None:
                raise ValueError("没有导入分类数据框。")
            else:
                # 获取分类信息
                center_banks_class = df_classify.iloc[:num_center, 1].values
                peripheral_banks_class = df_classify.iloc[num_center:, 1].values
                # 遍历边缘银行，对于每一个边缘银行，选取一个中心银行进行连接
                for i in range(num_center, N):
                    peripheral_class = peripheral_banks_class[i - num_center]  # 获取当前边缘银行的分类
                    same_class_center_banks = np.where(center_banks_class == peripheral_class)[0]  # 找到同分类的中心银行
                    if len(same_class_center_banks) > 0:
                        # 随机选取一个同分类的中心银行进行连接，如果是一个中心银行，那么直接连接
                        selected_center_bank = np.random.choice(same_class_center_banks)
                        A_IB_0[i, selected_center_bank] = A_IB_0[i, selected_center_bank]
                        A_IB_0[selected_center_bank, i] = A_IB_0[selected_center_bank, i]
                    else:
                        # 如果没有同分类的中心银行，随机选取一个中心银行进行连接
                        selected_center_bank = np.random.choice(np.arange(num_center))
                        A_IB_0[i, selected_center_bank] = A_IB_0[i, selected_center_bank]
                        A_IB_0[selected_center_bank, i] = A_IB_0[selected_center_bank, i]
                pass  # if
            pass  # match

    if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        cax = ax.matshow(A_IB_0, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title('Iteration: 0')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.25)
        pass  # if

    match algorithm_link_center_banks:
        case 'R语言的systemicrisk包之calibrate_ER':
            A_IB_1, Z_IB_1 = A_IB_0, A_IB_0.T
            A_IB_adjusted_center, Z_IB_adjusted_center = A_IB_adjusted[:num_center], Z_IB_adjusted[:num_center]

            # 需要减掉那些连接值之和，才能抵消行和列和约束多余量
            A_IB_adjusted_center -= A_IB_1[:num_center, num_center:].sum(axis=1)  # 减去中心银行连接边缘银行的值
            Z_IB_adjusted_center -= A_IB_1[num_center:, :num_center].sum(axis=0)  # 减去边缘银行连接中心银行的值

            # 极简版削峰填谷算法：重复以下过程，直到 `A_IB_adjusted_center` 与 `Z_IB_adjusted_center` 不再有负值为止
            iteration = 1
            can_find_valid_adjacency_matrix = True  # 是否有效的邻接矩阵
            while np.any(A_IB_adjusted_center < 0) or np.any(Z_IB_adjusted_center < 0):
                logging.debug(f"第{iteration}次迭代：")

                if iteration > 2 * N * 100:
                    logging.error("改中心银行与边缘连边的迭代次数达到最大值。仍未找到满足`A_IB_adjusted_center` 与 `Z_IB_adjusted_center` 不存在负值的值。改连边失败！程序强制终止！")
                    can_find_valid_adjacency_matrix = False
                    break

                # 分别获取【待去边中心银行】集合、【待加边中心银行】集合
                idxs_vertex_to_remove_edge_in_A_IB = np.where(A_IB_adjusted_center < 0)[0]
                if idxs_vertex_to_remove_edge_in_A_IB.size > 0:
                    idxs_vertex_to_remove_edge_in_A_IB = idxs_vertex_to_remove_edge_in_A_IB[np.argsort(A_IB_adjusted_center[idxs_vertex_to_remove_edge_in_A_IB])]  # 按照 A_IB_adjusted_center 的值从小到大排序
                else:
                    logging.debug("在行和方向找不到可以去边的中心银行！")
                idxs_vertex_to_remove_edge_in_Z_IB = np.where(Z_IB_adjusted_center < 0)[0]
                if idxs_vertex_to_remove_edge_in_Z_IB.size > 0:
                    idxs_vertex_to_remove_edge_in_Z_IB = idxs_vertex_to_remove_edge_in_Z_IB[np.argsort(Z_IB_adjusted_center[idxs_vertex_to_remove_edge_in_Z_IB])]  # 按照 Z_IB_adjusted_center 的值从小到大排序
                else:
                    logging.debug("在列和方向找不到可以去边的中心银行！")
                idxs_vertex_to_add_edge_in_A_IB = np.where(A_IB_adjusted_center >= 0)[0]
                if idxs_vertex_to_add_edge_in_A_IB.size > 0:
                    idxs_vertex_to_add_edge_in_A_IB = idxs_vertex_to_add_edge_in_A_IB[np.argsort(-A_IB_adjusted_center[idxs_vertex_to_add_edge_in_A_IB])]  # 按照 A_IB_adjusted_center 的值从大到小排序
                else:  # 如果没有正值，那么说明找不到可以加边的中心银行
                    can_find_valid_adjacency_matrix = False
                    logging.error("在行和方向找不到可以加边的中心银行！")
                idxs_vertex_to_add_edge_in_Z_IB = np.where(Z_IB_adjusted_center >= 0)[0]
                if idxs_vertex_to_add_edge_in_Z_IB.size > 0:
                    idxs_vertex_to_add_edge_in_Z_IB = idxs_vertex_to_add_edge_in_Z_IB[np.argsort(-Z_IB_adjusted_center[idxs_vertex_to_add_edge_in_Z_IB])]  # 按照 Z_IB_adjusted_center 的值从大到小排序
                else:  # 如果没有正值，那么说明找不到可以加边的中心银行
                    can_find_valid_adjacency_matrix = False
                    logging.error("在列和方向找不到可以加边的中心银行！")

                # idx_vertex_to_remove_edge = min(idxs_vertex_to_remove_edge_in_A_IB[0], idxs_vertex_to_remove_edge_in_Z_IB[0])

                # 判断改连边，选择【待去边中心银行】、【待改连边边缘银行】、【待加边中心银行】，进行改连边，更新 `A_IB_adjusted_center` 或 `Z_IB_adjusted_center`
                if can_find_valid_adjacency_matrix is False:
                    logging.error("改中心银行与边缘连边失败！")
                    break
                elif (len(idxs_vertex_to_remove_edge_in_A_IB) != 0 and len(idxs_vertex_to_remove_edge_in_Z_IB) != 0):
                    what_to_relink_edge = 'A_IB' if idxs_vertex_to_remove_edge_in_A_IB[0] < idxs_vertex_to_remove_edge_in_Z_IB[0] else 'Z_IB'
                elif (len(idxs_vertex_to_remove_edge_in_A_IB) == 0 and len(idxs_vertex_to_remove_edge_in_Z_IB) != 0):
                    what_to_relink_edge = 'Z_IB'
                elif (len(idxs_vertex_to_remove_edge_in_A_IB) != 0 and len(idxs_vertex_to_remove_edge_in_Z_IB) == 0):
                    what_to_relink_edge = 'A_IB'
                    pass  # if

                if what_to_relink_edge == 'A_IB':
                    logging.debug("行和方向：")
                    original_values = A_IB_adjusted_center.copy().tolist()
                    idx_vertex_to_remove_edge = idxs_vertex_to_remove_edge_in_A_IB[0]  # 选择 A_IB_adjusted_center 最大的作为【待去边中心银行】
                    # idx_vertex_to_remove_edge = weighted_random_choice(idxs_vertex_to_remove_edge_in_A_IB, A_IB_adjusted_center[idxs_vertex_to_remove_edge_in_A_IB])  # 选择【待去边中心银行】，A_IB_adjusted_center 越大的选择概率越大
                    idx_vertex_to_relink_edge = np.argmax(A_IB_1[idx_vertex_to_remove_edge, num_center:]) + num_center  # 选择与【待去边中心银行】连接的所有边缘银行当中，对应连接值 A_IB_adjusted 最大的边缘银行，作为【待改连边边缘银行】
                    # idx_vertex_to_relink_edge = weighted_random_choice(np.arange(num_center, N), A_IB_1[idx_vertex_to_remove_edge, num_center:])  # 选择与【待去边中心银行】连接的所有边缘银行当中的一个边缘银行，作为【待改连边边缘银行】。连接值 A_IB_adjusted 越大的选择概率越大
                    idx_vertex_to_add_edge = idxs_vertex_to_add_edge_in_A_IB[0]  # 选择 A_IB_adjusted_center 最大的作为【待加边中心银行】
                    # idx_vertex_to_add_edge = weighted_random_choice(idxs_vertex_to_add_edge_in_A_IB, A_IB_adjusted_center[idxs_vertex_to_add_edge_in_A_IB])  # 选择【待加边中心银行】，A_IB_adjusted_center 越大的选择概率越大
                    logging.debug(f"边缘银行 {idx_vertex_to_relink_edge} 与中心银行 {idx_vertex_to_remove_edge} 去边，与中心银行 {idx_vertex_to_add_edge} 加边")
                    # 【待改连边边缘银行】不与【待去边中心银行】连接，改成与【待加边中心银行】连接。更新 `A_IB_adjusted_center`
                    logging.debug(f"迁移值{A_IB_1[idx_vertex_to_remove_edge, idx_vertex_to_relink_edge]:.2f}")
                    A_IB_adjusted_center[idx_vertex_to_add_edge] -= A_IB_1[idx_vertex_to_remove_edge, idx_vertex_to_relink_edge]
                    A_IB_adjusted_center[idx_vertex_to_remove_edge] += A_IB_1[idx_vertex_to_remove_edge, idx_vertex_to_relink_edge]
                    A_IB_1[idx_vertex_to_add_edge, idx_vertex_to_relink_edge] += A_IB_1[idx_vertex_to_remove_edge, idx_vertex_to_relink_edge]
                    A_IB_1[idx_vertex_to_remove_edge, idx_vertex_to_relink_edge] -= A_IB_1[idx_vertex_to_remove_edge, idx_vertex_to_relink_edge]
                    # A_IB_adjusted_center -= A_IB_1[:num_center, num_center:].sum(axis=1)  # 更新 A_IB_adjusted_center
                    # Z_IB_adjusted_center -= A_IB_1[num_center:, :num_center].sum(axis=0)  # 更新 Z_IB_adjusted_center
                    # #DEBUG 打印出更新后的 A_IB_adjusted_center，只显示变更后的值，没变更的用星号代替
                    logging.debug(f"A_IB_adjusted_center 变更前：{[f'{val:.2f}' for val in original_values]}")
                    changed_values = [A_IB_adjusted_center[i] if A_IB_adjusted_center[i] != original_values[i] else '*' for i in range(len(original_values))]
                    changed_values_str = [f"{val:.2f}" if isinstance(val, (int, float)) else val for val in changed_values]
                    logging.debug(f"A_IB_adjusted_center 变更后：{changed_values_str}")
                elif what_to_relink_edge == 'Z_IB':
                    logging.debug("列和方向：")
                    original_values = Z_IB_adjusted_center.copy().tolist()
                    idx_vertex_to_remove_edge = idxs_vertex_to_remove_edge_in_Z_IB[0]  # 选择 Z_IB_adjusted_center 最大的作为【待去边中心银行】
                    # idx_vertex_to_remove_edge = weighted_random_choice(idxs_vertex_to_remove_edge_in_Z_IB, Z_IB_adjusted_center[idxs_vertex_to_remove_edge_in_Z_IB])  # 选择【待去边中心银行】，Z_IB_adjusted_center 越大的选择概率越大
                    idx_vertex_to_relink_edge = np.argmax(A_IB_1[num_center:, idx_vertex_to_remove_edge]) + num_center  # 选择与【待去边中心银行】连接的所有边缘银行当中，对应连接值 Z_IB_adjusted 最大的边缘银行，作为【待改连边边缘银行】
                    # idx_vertex_to_relink_edge = weighted_random_choice(np.arange(num_center, N), Z_IB_1[num_center:, idx_vertex_to_remove_edge])  # 选择与【待去边中心银行】连接的所有边缘银行当中的一个边缘银行，作为【待改连边边缘银行】。连接值 Z_IB_adjusted 越大的选择概率越大
                    idx_vertex_to_add_edge = idxs_vertex_to_add_edge_in_Z_IB[0]  # 选择 Z_IB_adjusted_center 最大的作为【待加边中心银行】
                    # idx_vertex_to_add_edge = weighted_random_choice(idxs_vertex_to_add_edge_in_Z_IB, Z_IB_adjusted_center[idxs_vertex_to_add_edge_in_Z_IB])  # 选择【待加边中心银行】，Z_IB_adjusted_center 越大的选择概率越大
                    logging.debug(f"边缘银行 {idx_vertex_to_relink_edge} 与中心银行 {idx_vertex_to_remove_edge} 去边，与中心银行 {idx_vertex_to_add_edge} 加边")
                    # 【待改连边边缘银行】不与【待去边中心银行】连接，改成与【待加边中心银行】连接。更新 `Z_IB_adjusted_center`
                    logging.debug(f"迁移值{A_IB_1[idx_vertex_to_relink_edge, idx_vertex_to_remove_edge]:.2f}")
                    Z_IB_adjusted_center[idx_vertex_to_add_edge] -= A_IB_1[idx_vertex_to_relink_edge, idx_vertex_to_remove_edge]
                    Z_IB_adjusted_center[idx_vertex_to_remove_edge] += A_IB_1[idx_vertex_to_relink_edge, idx_vertex_to_remove_edge]
                    A_IB_1[idx_vertex_to_relink_edge, idx_vertex_to_add_edge] += A_IB_1[idx_vertex_to_relink_edge, idx_vertex_to_remove_edge]
                    A_IB_1[idx_vertex_to_relink_edge, idx_vertex_to_remove_edge] -= A_IB_1[idx_vertex_to_relink_edge, idx_vertex_to_remove_edge]
                    # A_IB_adjusted_center -= A_IB_1[:num_center, num_center:].sum(axis=1)  # 更新 A_IB_adjusted_center
                    # Z_IB_adjusted_center -= A_IB_1[num_center:, :num_center].sum(axis=0)  # 更新 Z_IB_adjusted_center
                    # #DEBUG 打印出更新后的 Z_IB_adjusted_center，只显示变更后的值，没变更的用星号代替
                    logging.debug(f"Z_IB_adjusted_center 变更前：{[f'{val:.2f}' for val in original_values]}")
                    changed_values = [Z_IB_adjusted_center[i] if Z_IB_adjusted_center[i] != original_values[i] else '*' for i in range(len(original_values))]
                    changed_values_str = [f"{val:.2f}" if isinstance(val, (int, float)) else val for val in changed_values]
                    logging.debug(f"Z_IB_adjusted_center 变更后：{changed_values_str}")
                    pass  # if

                iteration += 1
                pass  # while

            print(f"更新完之后二者是否保持总和相同：{np.isclose(A_IB_adjusted_center.sum(), Z_IB_adjusted_center.sum())}")

            # 调用 R 语言的 systemicrisk 包之 calibrate_ER 算法 估算中心银行之间的风险敞口矩阵
            A_IB_1_center, Z_IB_1_center = calibrate_bilateral_exposure_by_ME_method_use_R_package(
                A_IB_adjusted_center,
                Z_IB_adjusted_center,
                target_density=center_agents_networkDensity,
                method_adjast_bank_balanceSheet='none',
                year=kwargs['year']
            )

            A_IB_1[:num_center, :num_center], Z_IB_1[:num_center, :num_center] = A_IB_1_center, Z_IB_1_center

            if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
                fig, ax = plt.subplots()
                cax = ax.matshow(A_IB_1, cmap='coolwarm')
                fig.colorbar(cax)
                ax.set_title('Iteration: end')
                ax.set_xlabel('X-axis')
                ax.set_ylabel('Y-axis')
                plt.show()
                time.sleep(0.25)
                print(f"最终迭代。精度：{np.max(np.abs(A_IB_1 - A_IB_0))}")
                pass  # if

        case 'RAS':
            iteration = 1
            while iteration < max_iteration:
                A_IB_1 = RAS_algorithm(A_IB_0, A_IB_adjusted, Z_IB_adjusted, denominator_precition_threshold=denominator_precition_threshold)
                if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
                    fig, ax = plt.subplots()
                    cax = ax.matshow(A_IB_1, cmap='coolwarm')
                    fig.colorbar(cax)
                    ax.set_title('Iteration: {}'.format(iteration))
                    ax.set_xlabel('X-axis')
                    ax.set_ylabel('Y-axis')
                    plt.show()
                    time.sleep(0.25)
                    print(f"第{iteration}次迭代。精度：{np.max(np.abs(A_IB_1 - A_IB_0))}")
                    pass  # if

                if np.allclose(A_IB_1, A_IB_0, atol=iteration_threshold, rtol=iteration_threshold):  # 判断是否达到收敛 #BUG 可能会出现难以收敛到很小的值的情况，可以考虑前后两个 `np.allclose` 的值的差值，如果不降反升，那么就停止迭代
                    break

                iteration += 1
                A_IB_0 = A_IB_1.copy()

                pass  # while

            if iteration >= max_iteration:
                logging.warning(f"迭代次数达到最大值：{max_iteration}。强制终止！")

            Z_IB_1 = A_IB_1.copy().T

            # 检查估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
            diff_of_A_IB_all_and_Z_IB_all, diff_of_row_sum, diff_of_col_sum, diff_of_total_sum = check_risk_exposure_matrix_constraints(A_IB_1, A_IB_adjusted, Z_IB_adjusted)
            logging.info(
                f"""
            \n
            年份: {kwargs['year']}、连接密度: {center_agents_networkDensity}\n
            A_IB_all、Z_IB_all 总和的差别: {diff_of_A_IB_all_and_Z_IB_all}\n
            行和约束的差别: {diff_of_row_sum}\n
            列和约束的差别: {diff_of_col_sum}\n
            总和约束的差别: {diff_of_total_sum}\n
            """
            )

            pass  # match

    logging.info("估算风险敞口矩阵完成。")

    if is_added_virtual_bank is True:  # 如果添加了虚拟银行，则删除虚拟银行
        if is_maintain_virtual_bank:  # 如果保留虚拟银行，则返回虚拟银行
            A_IB = A_IB_1
            Z_IB = Z_IB_1
        else:
            A_IB = A_IB_1[:-1, :-1]
            Z_IB = Z_IB_1[:-1, :-1]
            pass  # if
    else:
        A_IB = A_IB_1
        Z_IB = Z_IB_1
        pass  # if

    return A_IB, Z_IB

    pass  # function


def calculate_bilateral_exposure_by_ME_method(
        A_IB_all: np.ndarray,
        Z_IB_all: np.ndarray,
        method_adjast_bank_balanceSheet: str = 'add_virtual_bank',
        is_maintain_virtual_bank=False,
        algorithm_link_banks: str = 'RAS',
        iteration_threshold: float = 1e-10,
        is_show_detal: bool = False,
        max_iteration: int = 100000,
        denominator_precition_threshold: float = 1e-10,
        **kwargs,
):
    """
    使用最大熵值法（Maximum Entropy），通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    Args:
        A_IB_all (np.ndarray): 银行间资产邻接矩阵
        Z_IB_all (np.ndarray): 银行间负债邻接矩阵
        method_adjast_bank_balanceSheet (str): 调整银行间总资产总负债不一致的方法。默认值 'add_virtual_bank'，即添加虚拟银行。可选值包括：

            - 'none'：不调整；
            - 'add_virtual_bank'：添加虚拟银行；
            - 'resize'：按照多出来的比例，压缩多出来的金额部分，使得二者相等；

        is_maintain_virtual_bank (bool): 是否保留虚拟银行。默认值 False
        algorithm_link_banks (str): 连接银行之间的方法。默认值 'RAS'，即使用 RAS 算法。可选值包括：

            - 'RAS'：使用 RAS 算法；
            - 'RAS-2'：使用旧的的 RAS 算法；

        is_show_detal (bool): 是否显示迭代过程的热力图。默认值 False
        iteration_threshold (float): 迭代阈值。默认值 1e-10
        max_iteration (int): 最大迭代次数。默认值 100000
        denominator_precition_threshold (float): 分母接近零精度阈值。默认值 1e-10。
        **kwargs: 其他参数

    Returns:
        A_IB_1 (np.ndarray): 银行间资产邻接矩阵
        Z_IB_1 (np.ndarray): 银行间负债邻接矩阵
    """
    import numpy as np

    # 预处理维度
    A_IB_all, Z_IB_all = A_IB_all.flatten(), Z_IB_all.flatten()

    # 调整银行资产负债表使得总资产与总负债相等

    is_added_virtual_bank = None
    match method_adjast_bank_balanceSheet:
        case 'none':
            # NOTE 调整方案〇：无需调整
            A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
        case 'add_virtual_bank':
            # NOTE 调整方案一：添加虚拟银行
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
                is_added_virtual_bank = False
            else:
                A_IB_adjusted, Z_IB_adjusted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB_all, Z_IB_all)
                is_added_virtual_bank = True
                pass  # if
        case 'resize':
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
            else:
                # #NOTE 调整方案二：调整比例。按照多出来的比例，压缩多出来的金额部分，使得二者相等。
                A_IB_adjusted, Z_IB_adjusted = adjust_A_IB_Z_IB_by_resize(A_IB_all, Z_IB_all)
                pass  # if
        case _:
            raise ValueError("不支持的调整方法！")
            pass  # match

    N = A_IB_adjusted.shape[0]  # 获取银行数量

    match algorithm_link_banks:
        case 'RAS':
            # A0 = np.outer(A_IB_adjusted, Z_IB_adjusted) / denominator_precition_threshold
            A_IB_0 = np.outer(A_IB_adjusted, Z_IB_adjusted)
            np.fill_diagonal(A_IB_0, 0)  # 对角线为 0
            if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                cax = ax.matshow(A_IB_0, cmap='coolwarm')
                fig.colorbar(cax)
                ax.set_title('Iteration: 0')
                ax.set_xlabel('X-axis')
                ax.set_ylabel('Y-axis')
                plt.show()
                time.sleep(0.25)
                pass  # if
        case 'RAS-old':
            A_IB_i_star = A_IB_adjusted / np.max([A_IB_adjusted, Z_IB_adjusted])  # 标准化银行间资产负债矩阵
            Z_IB_i_star = Z_IB_adjusted / np.max([A_IB_adjusted, Z_IB_adjusted])
            X_ij_star = np.sqrt(np.outer(A_IB_i_star, Z_IB_i_star))  # 初始化准双边敞口，通过外积计算
            if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                cax = ax.matshow(X_ij_star, cmap='coolwarm')
                fig.colorbar(cax)
                ax.set_title('Iteration: 0')
                ax.set_xlabel('X-axis')
                ax.set_ylabel('Y-axis')
                plt.show()
                time.sleep(0.25)
                pass  # if
            pass  # match

    match algorithm_link_banks:
        case 'RAS':
            iteration = 1
            while iteration < max_iteration:
                A_IB_1 = RAS_algorithm(A_IB_0, A_IB_adjusted, Z_IB_adjusted, denominator_precition_threshold=denominator_precition_threshold)
                if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
                    fig, ax = plt.subplots()
                    cax = ax.matshow(A_IB_1, cmap='coolwarm')
                    fig.colorbar(cax)
                    ax.set_title('Iteration: {}'.format(iteration))
                    ax.set_xlabel('X-axis')
                    ax.set_ylabel('Y-axis')
                    plt.show()
                    time.sleep(0.25)
                    print(f"第{iteration}次迭代。精度：{np.max(np.abs(A_IB_1 - A_IB_0))}")
                    pass  # if

                if np.allclose(A_IB_1, A_IB_0, atol=iteration_threshold, rtol=iteration_threshold):  # 判断是否达到收敛 #BUG 可能会出现难以收敛到很小的值的情况，可以考虑前后两个 `np.allclose` 的值的差值，如果不降反升，那么就停止迭代
                    break

                iteration += 1
                A_IB_0 = A_IB_1.copy()

                pass  # while

            if iteration >= max_iteration:
                logging.warning(f"迭代次数达到最大值：{max_iteration}。强制终止！")

        case 'RAS-old':
            iteration = 1
            while iteration < max_iteration:

                X_ij_prev = X_ij_star.copy()  # 保存上一次迭代的双边敞口矩阵
                for i in range(N):
                    if np.sum(X_ij_prev[:, i]) == 0:  # 行约束迭代
                        X_ij_star[:, i] = 0
                    else:
                        denominator = np.sum(X_ij_prev[:, i]) if np.sum(X_ij_prev[:, i]) > denominator_precition_threshold else denominator_precition_threshold
                        X_ij_star[:, i] = X_ij_prev[:, i] * Z_IB_i_star[i] / denominator

                    if np.sum(X_ij_prev[i, :]) == 0:  # 列约束迭代
                        X_ij_star[i, :] = 0
                    else:
                        denominator = np.sum(X_ij_prev[i, :]) if np.sum(X_ij_prev[i, :]) > denominator_precition_threshold else denominator_precition_threshold
                        X_ij_star[i, :] = X_ij_prev[i, :] * A_IB_i_star[i] / denominator

                if is_show_detal:  # 可视化迭代数据之热力图
                    fig, ax = plt.subplots()
                    cax = ax.matshow(X_ij_star, cmap='coolwarm', vmin=0, vmax=X_ij_star.max())
                    fig.colorbar(cax)
                    ax.set_title('Iteration: {}'.format(iteration))
                    ax.set_xlabel('X-axis')
                    ax.set_ylabel('Y-axis')
                    plt.show()
                    time.sleep(0.25)
                    print(f"第{iteration}次迭代。精度：{np.max(np.abs(X_ij_star - X_ij_prev))}")
                    pass  # if

                if np.allclose(X_ij_star, X_ij_prev, atol=iteration_threshold):  # 判断是否达到收敛
                    break

                iteration += 1
                pass  # while

            if iteration >= max_iteration:
                logging.warning(f"迭代次数达到最大值：{max_iteration}。强制终止！")

            pass  # match

    # NOTE 计算不考虑预置值的最终的银行间资产矩阵
    match algorithm_link_banks:
        case 'RAS':
            Z_IB_1 = A_IB_1.copy().T
        case 'RAS-old':
            A_IB_1 = X_ij_star / X_ij_star.sum() * np.max([A_IB_adjusted.sum(), Z_IB_adjusted.sum()])  # 计算最终的银行间资产矩阵
            Z_IB_1 = A_IB_1.copy().T
            pass  # match

    # # #DEBUG 检测估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
    # logging.debug(f"\n总元素和之误差：{np.round(A_IB_1.sum() - A_IB_all.sum())}")
    # logging.debug(f"\n总元素和之误差占比：{np.abs(A_IB_1.sum() - A_IB_all.sum()) / A_IB_all.sum()}")
    # logging.debug(f"\n行元素和之误差：{np.round(A_IB_1.sum(axis=1) - A_IB_all)}")
    # logging.debug(f"\n行元素和之误差占比：{np.abs(A_IB_1.sum(axis=1) - A_IB_all) / A_IB_all}")
    # logging.debug(f"\n列元素和之误差：{np.round(A_IB_1.sum(axis=0) - Z_IB_all)}")
    # logging.debug(f"\n列元素和之误差占比：{np.abs(A_IB_1.sum(axis=0) - Z_IB_all) / Z_IB_all}")

    logging.info("估算风险敞口矩阵完成。")

    # 检查估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
    diff_of_A_IB_all_and_Z_IB_all, diff_of_row_sum, diff_of_col_sum, diff_of_total_sum = check_risk_exposure_matrix_constraints(A_IB_1, A_IB_adjusted, Z_IB_adjusted)
    logging.info(
        f"""
    \n
    年份: {kwargs['year']}、连接密度: {kwargs['density']}\n
    A_IB_all、Z_IB_all 总和的差别: {diff_of_A_IB_all_and_Z_IB_all}\n
    行和约束的差别: {diff_of_row_sum}\n
    列和约束的差别: {diff_of_col_sum}\n
    总和约束的差别: {diff_of_total_sum}\n
    """
    )

    if is_added_virtual_bank is True:  # 如果添加了虚拟银行，则删除虚拟银行
        if is_maintain_virtual_bank:  # 如果保留虚拟银行，则返回虚拟银行
            A_IB = A_IB_1
            Z_IB = Z_IB_1
        else:
            A_IB = A_IB_1[:-1, :-1]
            Z_IB = Z_IB_1[:-1, :-1]
            pass  # if
    else:
        A_IB = A_IB_1
        Z_IB = Z_IB_1
        pass  # if

    return A_IB, Z_IB

    pass  # function


def calculate_bilateral_exposure_by_ME_method_with_preset_fixed_values(
        A_IB_all: np.ndarray,
        Z_IB_all: np.ndarray,
        A_preset_values: np.ndarray,
        mask: np.ndarray,
        method_adjast_bank_balanceSheet: str = 'add_virtual_bank',
        is_maintain_virtual_bank=False,
        is_show_detal: bool = False,
        iteration_threshold: float = 1e-10,
        max_iteration: int = 100000,
        denominator_precition_threshold: float = 1e-10,
        **kwargs,
):
    """
    # 通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    使用最大熵值法（Maximum Entropy）。

    估算银行间双边敞口矩阵，允许使用手动预置的元素值。

    Args:
        A_IB_all (np.ndarray): 银行间资产邻接矩阵
        Z_IB_all (np.ndarray): 银行间负债邻接矩阵
        A_preset_values (np.ndarray): 预置的银行间资产邻接矩阵
        mask (np.ndarray): 预置的银行间资产邻接矩阵的掩码。值为 True 表示预置值，值为 False 表示非预置值。
        method_adjast_bank_balanceSheet (str): 调整银行间总资产总负债不一致的方法。默认值 'add_virtual_bank'，即添加虚拟银行。可选值包括：

            - 'none'：不调整；
            - 'add_virtual_bank'：添加虚拟银行；
            - 'resize'：按照多出来的比例，压缩多出来的金额部分，使得二者相等；

        is_maintain_virtual_bank (bool): 是否保留虚拟银行。默认值 False
        method_link_center_banks (str): 连接中心银行之间的方法。默认值 'RAS'，即使用 RAS 算法。可选值包括：

            - 'RAS'：使用 RAS 算法；
            - 'RAS-2'：使用旧的的 RAS 算法；

        is_show_detal (bool): 是否显示迭代过程的热力图。默认值 False
        iteration_threshold (float): 迭代阈值。默认值 1e-10
        max_iteration (int): 最大迭代次数。默认值 100000
        denominator_precition_threshold (float): 分母接近零精度阈值。默认值 1e-10。
        **kwargs: 其他参数

    Returns:
        A_IB_1 (np.ndarray): 银行间资产邻接矩阵
        Z_IB_1 (np.ndarray): 银行间负债邻接矩阵
    """
    import numpy as np

    # 预处理维度
    A_IB_all, Z_IB_all = A_IB_all.flatten(), Z_IB_all.flatten()

    # 调整银行资产负债表使得总资产与总负债相等

    is_added_virtual_bank = None
    match method_adjast_bank_balanceSheet:
        case 'none':
            # NOTE 调整方案〇：无需调整
            A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
        case 'add_virtual_bank':
            # NOTE 调整方案一：添加虚拟银行
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
                is_added_virtual_bank = False
            else:
                A_IB_adjusted, Z_IB_adjusted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB_all, Z_IB_all)
                is_added_virtual_bank = True
                pass  # if
        case 'resize':
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
            else:
                # #NOTE 调整方案二：调整比例。按照多出来的比例，压缩多出来的金额部分，使得二者相等。
                A_IB_adjusted, Z_IB_adjusted = adjust_A_IB_Z_IB_by_resize(A_IB_all, Z_IB_all)
                pass  # if
        case _:
            raise ValueError("不支持的调整方法！")
            pass  # match

    N = A_IB_adjusted.shape[0]  # 获取银行数量

    # 预置一些先验的元素值

    # 预置规则 1：对角线为 0
    np.fill_diagonal(A_preset_values, 0)
    mask |= np.eye(N, dtype=bool)

    # 根据预置的元素值，重新计算银行间资产负债矩阵之行和、列和
    A_IB_adjusted_prior = A_IB_adjusted - np.sum(np.where(mask, A_preset_values, 0), axis=1)
    Z_IB_adjusted_prior = Z_IB_adjusted - np.sum(np.where(mask, A_preset_values, 0), axis=0)

    A_IB_0 = np.outer(A_IB_adjusted_prior, Z_IB_adjusted_prior)
    if is_show_detal:  # 可视化双边敞口矩阵为热力图
        import matplotlib.pyplot as plt
        A_IB_0_prev_masked = np.ma.masked_where(mask, A_IB_0)
        fig, ax = plt.subplots()
        cax = ax.matshow(A_IB_0_prev_masked, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title('Iteration: 0')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.25)
        pass  # if

    iteration = 1
    while iteration < max_iteration:
        A_IB_0_prev_masked = np.ma.masked_where(mask, A_IB_0)
        A_IB_adjusted_prior_masked = np.ma.masked_where(np.all(mask, 1), A_IB_adjusted_prior)
        Z_IB_adjusted_prior_masked = np.ma.masked_where(np.all(mask, 0), Z_IB_adjusted_prior)
        A_IB_1_masked = RAS_algorithm(A_IB_0_prev_masked, A_IB_adjusted_prior_masked, Z_IB_adjusted_prior_masked, denominator_precition_threshold=denominator_precition_threshold)  # 调用 RAS 算法
        A_IB_1 = np.ma.filled(A_IB_1_masked, A_preset_values)
        # A_IB_1 = RAS_algorithm_with_preset_values(A_IB_0, A_IB_adjusted_prior, Z_IB_adjusted_prior, A_preset_values, mask, denominator_precition_threshold=denominator_precition_threshold)  # 调用 RAS 算法
        if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
            fig, ax = plt.subplots()
            cax = ax.matshow(A_IB_1_masked, cmap='coolwarm')
            fig.colorbar(cax)
            ax.set_title('Iteration: {}'.format(iteration))
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            plt.show()
            time.sleep(0.25)
            print(f"第{iteration}次迭代。精度：{np.max(np.abs(A_IB_1 - A_IB_0))}")
            pass  # if

        if np.allclose(A_IB_1, A_IB_0, atol=iteration_threshold, rtol=iteration_threshold):  # 判断是否达到收敛 #BUG 可能会出现难以收敛到很小的值的情况，可以考虑前后两个 `np.allclose` 的值的差值，如果不降反升，那么就停止迭代
            break

        iteration += 1
        A_IB_0 = A_IB_1.copy()

        pass  # while

    if iteration >= max_iteration:
        logging.warning(f"迭代次数达到最大值：{max_iteration}。强制终止！")

    if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
        fig, ax = plt.subplots()
        cax = ax.matshow(A_IB_1, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title('Iteration: {}'.format(iteration))
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.25)
        print(f"最终精度：{np.max(np.abs(A_IB_1 - A_IB_0))}")
        pass  # if

    Z_IB_1 = A_IB_1.copy().T

    # # #DEBUG 检测估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
    # logging.debug(f"\n总元素和之误差：{np.round(A_IB_1.sum() - A_IB_all.sum())}")
    # logging.debug(f"\n总元素和之误差占比：{np.abs(A_IB_1.sum() - A_IB_all.sum()) / A_IB_all.sum()}")
    # logging.debug(f"\n行元素和之误差：{np.round(A_IB_1.sum(axis=1) - A_IB_all)}")
    # logging.debug(f"\n行元素和之误差占比：{np.abs(A_IB_1.sum(axis=1) - A_IB_all) / A_IB_all}")
    # logging.debug(f"\n列元素和之误差：{np.round(A_IB_1.sum(axis=0) - Z_IB_all)}")
    # logging.debug(f"\n列元素和之误差占比：{np.abs(A_IB_1.sum(axis=0) - Z_IB_all) / Z_IB_all}")

    logging.info("估算风险敞口矩阵完成。")

    # 检查估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
    diff_of_A_IB_all_and_Z_IB_all, diff_of_row_sum, diff_of_col_sum, diff_of_total_sum = check_risk_exposure_matrix_constraints(A_IB_1, A_IB_adjusted, Z_IB_adjusted)
    logging.info(
        f"""
    \n
    年份: {kwargs['year']}、连接密度: {kwargs['density']}\n
    A_IB_all、Z_IB_all 总和的差别: {diff_of_A_IB_all_and_Z_IB_all}\n
    行和约束的差别: {diff_of_row_sum}\n
    列和约束的差别: {diff_of_col_sum}\n
    总和约束的差别: {diff_of_total_sum}\n
    """
    )

    if is_added_virtual_bank is True:  # 如果添加了虚拟银行，则删除虚拟银行
        if is_maintain_virtual_bank:  # 如果保留虚拟银行，则返回虚拟银行
            A_IB = A_IB_1
            Z_IB = Z_IB_1
        else:
            A_IB = A_IB_1[:-1, :-1]
            Z_IB = Z_IB_1[:-1, :-1]
            pass  # if
    else:
        A_IB = A_IB_1
        Z_IB = Z_IB_1
        pass  # if

    return A_IB, Z_IB

    pass  # function


def calculate_bilateral_exposure_by_ME_method_with_density(
        A_IB_all: np.ndarray,
        Z_IB_all: np.ndarray,
        target_density: float = 0.25,
        method_adjast_bank_balanceSheet: str = 'add_virtual_bank',
        is_maintain_virtual_bank=False,
        is_show_detal: bool = False,
        iteration_threshold: float = 1e-10,
        max_iteration: int = 100000,
        denominator_precition_threshold: float = 1e-10,
        **kwargs,
):
    """
    通过各银行之银行间资产与银行间负债估算银行间双边敞口。 #BUG 存在行和难以拟合到约束的问题。

    使用最大熵值法（Maximum Entropy）。

    估算银行间双边敞口矩阵，允许使用手动预置的元素值。

    Args:
        A_IB_all (np.ndarray): 银行间资产邻接矩阵
        Z_IB_all (np.ndarray): 银行间负债邻接矩阵
        target_density (float): 邻接矩阵指定的密度。默认值 0.25
        method_adjast_bank_balanceSheet (str): 调整银行间总资产总负债不一致的方法。默认值 'add_virtual_bank'，即添加虚拟银行。可选值包括：

            - 'none'：不调整；
            - 'add_virtual_bank'：添加虚拟银行；
            - 'resize'：按照多出来的比例，压缩多出来的金额部分，使得二者相等；

        is_maintain_virtual_bank (bool): 是否保留虚拟银行。默认值 False
        method_link_center_banks (str): 连接中心银行之间的方法。默认值 'RAS'，即使用 RAS 算法。可选值包括：

            - 'RAS'：使用 RAS 算法；
            - 'RAS-2'：使用旧的的 RAS 算法；

        is_show_detal (bool): 是否显示迭代过程的热力图。默认值 False
        iteration_threshold (float): 迭代阈值。默认值 1e-10
        max_iteration (int): 最大迭代次数。默认值 100000
        denominator_precition_threshold (float): 分母接近零精度阈值。默认值 1e-10。
        **kwargs: 其他参数

    Returns:
        A_IB_4 (np.ndarray): 银行间资产邻接矩阵
        Z_IB_4 (np.ndarray): 银行间负债邻接矩阵
        density (float): 最终的连接密度
        is_the_target_density (bool): 是否达到目标密度
    """
    import numpy as np

    # 预处理维度
    A_IB_all, Z_IB_all = A_IB_all.flatten(), Z_IB_all.flatten()

    # 调整银行资产负债表使得总资产与总负债相等

    is_added_virtual_bank = None
    match method_adjast_bank_balanceSheet:
        case 'none':
            # NOTE 调整方案〇：无需调整
            A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
        case 'add_virtual_bank':
            # NOTE 调整方案一：添加虚拟银行
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
                is_added_virtual_bank = False
            else:
                A_IB_adjusted, Z_IB_adjusted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB_all, Z_IB_all)
                is_added_virtual_bank = True
                pass  # if
        case 'resize':
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
            else:
                # #NOTE 调整方案二：调整比例。按照多出来的比例，压缩多出来的金额部分，使得二者相等。
                A_IB_adjusted, Z_IB_adjusted = adjust_A_IB_Z_IB_by_resize(A_IB_all, Z_IB_all)
                pass  # if
        case _:
            raise ValueError("不支持的调整方法！")
            pass  # match

    N = A_IB_adjusted.shape[0]  # 获取银行数量（包括虚拟银行）

    A_IB_0 = np.outer(A_IB_adjusted, Z_IB_adjusted)
    np.fill_diagonal(A_IB_0, 0)  # 对角线为 0

    if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        cax = ax.matshow(A_IB_0, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title('Iteration: 0')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.25)
        pass  # if

    iteration = 1
    while iteration < max_iteration:
        A_IB_1 = RAS_algorithm(A_IB_0, A_IB_adjusted, Z_IB_adjusted, denominator_precition_threshold=denominator_precition_threshold)
        if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
            fig, ax = plt.subplots()
            cax = ax.matshow(A_IB_1, cmap='coolwarm')
            fig.colorbar(cax)
            ax.set_title('Iteration: {}'.format(iteration))
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            plt.show()
            time.sleep(0.25)
            print(f"第{iteration}次迭代。精度：{np.max(np.abs(A_IB_1 - A_IB_0))}")
            pass  # if

        if np.allclose(A_IB_1, A_IB_0, atol=iteration_threshold, rtol=iteration_threshold):  # 判断是否达到收敛 #BUG 可能会出现难以收敛到很小的值的情况，可以考虑前后两个 `np.allclose` 的值的差值，如果不降反升，那么就停止迭代
            break

        iteration += 1
        A_IB_0 = A_IB_1.copy()

        pass  # while

    if iteration >= max_iteration:
        logging.warning(f"迭代次数达到最大值：{max_iteration}。强制终止！")

    # 调整连接密度 #BUG 这个方案可能不一定会达到目标密度，因为可能有一些更优的解没有被发现

    # 检查是否是除了对角线之外的全连接邻接矩阵
    if not is_valid_adjacency_matrix(A_IB_1):
        raise ValueError("银行间资产邻接矩阵不是对角线元素为 0 的全连接邻接矩阵！")

    iteration += 1
    A_IB_2 = A_IB_1.copy()
    num_edges_no_zeros = np.count_nonzero(A_IB_2)  # 计算非零元素的个数
    num_edges_to_delete = int(np.ceil(num_edges_no_zeros * (1 - target_density)))  # 计算指定的连接密度所需要去掉的连边数
    A_IB_2_flatten = A_IB_2.flatten()  # 给 A_IB_4 按照元素值从小到大排序，获取排序的值和索引信息
    A_IB_2_sorted_idx = np.unravel_index(np.argsort(A_IB_2_flatten), A_IB_2.shape)
    A_IB_2_sorted_val = np.sort(A_IB_2_flatten)
    A_IB_2_sorted_idx = (A_IB_2_sorted_idx[0][A_IB_2_sorted_val != 0], A_IB_2_sorted_idx[1][A_IB_2_sorted_val != 0])  # 去掉0元素的索引和对应的值
    A_IB_2_sorted_val = A_IB_2_sorted_val[A_IB_2_sorted_val != 0]
    # 逐步去掉非零的最小值的元素，直到达到目标密度
    i = 0  # 记录判断的元素索引
    j = 0  # 记录已经去掉的连接个数
    while (j != num_edges_to_delete) and (i < num_edges_no_zeros):
        k = A_IB_2_sorted_idx[0][i], A_IB_2_sorted_idx[1][i]  # 获取最小元素索引
        # 判断是否满足行列值约束最低条件
        # 如果去掉该元素之后，导致行和向量或者列和向量出现0值，并且约束条件对应元素没有0值，则不允许去掉该元素
        temp_r = A_IB_2[k[0], :].sum()
        temp_c = A_IB_2[:, k[1]].sum()
        if ~((temp_r - A_IB_2[k] == 0) ^ (A_IB_adjusted[k[0]] == 0)) and ~((temp_c - A_IB_2[k] == 0) ^ (Z_IB_adjusted[k[1]] == 0)):
            A_IB_2[k] = 0  # 去掉该连接
            # A_IB_2_sorted_idx = (np.delete(A_IB_2_sorted_idx[0], i), np.delete(A_IB_2_sorted_idx[1], i))  # 去掉索引和对应的值
            j += 1
            # if is_show_detal:  # 可视化双边敞口矩阵为热力图 #DEBUG 测试用
            #     mask = np.where(A_IB_2 == 0, True, False)
            #     A_IB_2_masked = np.ma.masked_where(mask, A_IB_2)
            #     fig, ax = plt.subplots()
            #     cax = ax.matshow(A_IB_2_masked, cmap='coolwarm')
            #     fig.colorbar(cax)
            #     ax.set_title(f'Iteration: {iteration} - {i}')
            #     ax.set_xlabel('X-axis')
            #     ax.set_ylabel('Y-axis')
            #     plt.show()
            #     time.sleep(0.1)
            #     pass  # if
        else:
            logging.warning(f"不允许去掉元素：{k}，对应的值为：{A_IB_2[k]}。")
            pass  # if
        i += 1
        pass  # while

    # 总结调整后的的连接密度
    num_edges_adjusted = np.count_nonzero(A_IB_2)  # 计算非零元素的个数
    density = num_edges_adjusted / num_edges_no_zeros
    # 完成率
    density / target_density
    logging.info(f"调整后的的连接密度：{density}")
    if density > target_density:
        is_the_target_density = False
        logging.warning(f"调整后的的连接密度未达到目标密度：{target_density}")
    else:
        is_the_target_density = True
        logging.info(f"调整后的的连接密度已达到目标密度：{target_density}")
        pass

    # 根据预置的元素值，重新计算银行间资产负债矩阵之行和、列和
    mask = np.where(A_IB_2 == 0, True, False)
    # A_IB_adjusted_prior = A_IB_adjusted - np.sum(np.where(mask, A_preset_values, 0), axis=1)
    # Z_IB_adjusted_prior = Z_IB_adjusted - np.sum(np.where(mask, A_preset_values, 0), axis=0)

    # A_IB_ij_prev = np.outer(A_IB_adjusted, Z_IB_adjusted)
    if is_show_detal:  # 可视化双边敞口矩阵为热力图
        A_IB_2_masked = np.ma.masked_where(mask, A_IB_2)
        fig, ax = plt.subplots()
        cax = ax.matshow(A_IB_2_masked, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title(f'Iteration: {iteration} - adjusted density masked')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.25)
        pass  # if

    if is_show_detal:  # 可视化双边敞口矩阵为热力图
        fig, ax = plt.subplots()
        cax = ax.matshow(A_IB_1, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title(f'Iteration: {iteration} - not adjusted density')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.25)
        pass  # if

    A_IB_3 = A_IB_2.copy()
    iteration += 1
    while iteration < max_iteration:
        A_IB_3_masked = np.ma.masked_where(mask, A_IB_3)
        # A_IB_adjusted_prior_masked = np.ma.masked_where(np.all(mask, 1), A_IB_adjusted_prior)
        # Z_IB_adjusted_prior_masked = np.ma.masked_where(np.all(mask, 0), Z_IB_adjusted_prior)
        # A_IB_4_masked = RAS_algorithm_with_preset_values(A_IB_3_masked, A_IB_adjusted, Z_IB_adjusted, denominator_precition_threshold=denominator_precition_threshold)  # 调用 RAS 算法
        A_IB_4_masked = RAS_algorithm(A_IB_3_masked, A_IB_adjusted, Z_IB_adjusted, denominator_precition_threshold=denominator_precition_threshold)  # 调用 RAS 算法
        A_IB_4 = np.ma.filled(A_IB_4_masked, A_IB_3)
        # A_IB_4 = RAS_algorithm_with_preset_values(A_IB_ij_prev, A_IB_adjusted_prior, Z_IB_adjusted_prior, A_preset_values, mask, denominator_precition_threshold=denominator_precition_threshold)  # 调用 RAS 算法
        if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
            fig, ax = plt.subplots()
            cax = ax.matshow(A_IB_4_masked, cmap='coolwarm')
            fig.colorbar(cax)
            ax.set_title('Iteration: {}'.format(iteration))
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            plt.show()
            time.sleep(0.25)
            print(f"第{iteration}次迭代。精度：{np.max(np.abs(A_IB_4 - A_IB_3))}")
            pass  # if

        if np.allclose(A_IB_4, A_IB_3, atol=iteration_threshold, rtol=iteration_threshold):  # 判断是否达到收敛 #BUG 可能会出现难以收敛到很小的值的情况，可以考虑前后两个 `np.allclose` 的值的差值，如果不降反升，那么就停止迭代
            break

        iteration += 1
        A_IB_3 = A_IB_4.copy()

        pass  # while

    if iteration >= max_iteration:
        logging.warning(f"迭代次数达到最大值：{max_iteration}。强制终止！")

    if is_show_detal:  # 可视化标准双边敞口矩阵为热力图
        fig, ax = plt.subplots()
        cax = ax.matshow(A_IB_4, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title('Iteration: {}'.format(iteration))
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.25)
        print(f"最终精度：{np.max(np.abs(A_IB_4 - A_IB_3))}")
        pass  # if

    Z_IB_4 = A_IB_4.copy().T

    # # #DEBUG 检测估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
    # logging.debug(f"\n总元素和之误差：{np.round(A_IB_4.sum() - A_IB_all.sum())}")
    # logging.debug(f"\n总元素和之误差占比：{np.abs(A_IB_4.sum() - A_IB_all.sum()) / A_IB_all.sum()}")
    # logging.debug(f"\n行元素和之误差：{np.round(A_IB_4.sum(axis=1) - A_IB_all)}")
    # logging.debug(f"\n行元素和之误差占比：{np.abs(A_IB_4.sum(axis=1) - A_IB_all) / A_IB_all}")
    # logging.debug(f"\n列元素和之误差：{np.round(A_IB_4.sum(axis=0) - Z_IB_all)}")
    # logging.debug(f"\n列元素和之误差占比：{np.abs(A_IB_4.sum(axis=0) - Z_IB_all) / Z_IB_all}")

    logging.info("估算风险敞口矩阵完成。")

    # 检查估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
    diff_of_A_IB_all_and_Z_IB_all, diff_of_row_sum, diff_of_col_sum, diff_of_total_sum = check_risk_exposure_matrix_constraints(A_IB_1, A_IB_adjusted, Z_IB_adjusted)
    logging.info(
        f"""
    \n
    年份: {kwargs['year']}、连接密度: {target_density}\n
    A_IB_all、Z_IB_all 总和的差别: {diff_of_A_IB_all_and_Z_IB_all}\n
    行和约束的差别: {diff_of_row_sum}\n
    列和约束的差别: {diff_of_col_sum}\n
    总和约束的差别: {diff_of_total_sum}\n
    """
    )

    if is_added_virtual_bank is True:  # 如果添加了虚拟银行，则删除虚拟银行
        if is_maintain_virtual_bank:  # 如果保留虚拟银行，则返回虚拟银行
            A_IB = A_IB_4
            Z_IB = Z_IB_4
        else:
            A_IB = A_IB_4[:-1, :-1]
            Z_IB = Z_IB_4[:-1, :-1]
            pass  # if
    else:
        A_IB = A_IB_4
        Z_IB = Z_IB_4
        pass  # if

    return A_IB, Z_IB, density, is_the_target_density

    pass  # function


def calibrate_bilateral_exposure_by_ME_method_use_R_package(
        A_IB_all: np.ndarray,
        Z_IB_all: np.ndarray,
        target_density,
        n_samples_calib=10,
        thin=100,
        method_adjast_bank_balanceSheet='add_virtual_bank',
        is_maintain_virtual_bank=False,
        **kwargs,
):
    """
    调用 R 语言之工具包 systemicrisk 之函数 calibrate_ER，校准银行间资产负债矩阵，到指定的密度。
    中的 calibrate_bilateral_exposure_by_ME_method_use_R_package 函数,并将结果转换为 NumPy 数组。

    Args:
        A_IB_all (np.ndarray): 银行间资产
        Z_IB_all (np.ndarray): 银行间负债
        target_density (float): 目标密度
        n_samples_calib (int, optional): 校准时生成的矩阵样本数量。默认为 10。这个参数决定了在校准过程中生成的矩阵样本数量。它影响最终模型的精度和计算的成本。增加样本数通常会提供更精确的校准结果，但也会显著增加计算量。
        thin (int, optional): 校准时的稀疏化参数。默认为 100。用于控制从采样过程中选择的样本数量，从生成的所有样本中只选择每隔 thin 次的一个样本，这有助于减少计算量并避免自相关。稀疏性较高的矩阵可能需要更大的 thin 值，以减少过多的采样。反之，稠密矩阵可能需要较小的 thin 值。
        method_adjast_bank_balanceSheet (str): 调整银行间总资产总负债不一致的方法。默认值 'add_virtual_bank'，即添加虚拟银行。可选值包括：

            - 'none'：不调整；
            - 'add_virtual_bank'：添加虚拟银行；
            - 'resize'：按照多出来的比例，压缩多出来的金额部分，使得二者相等；

        is_maintain_virtual_bank (bool): 是否保留虚拟银行。默认值 False。
        folderpath_result (Path, optional): 结果文件夹路径。默认为 None。
        **kwargs: 其他参数

    Returns:
        Tuple[np.array, np.array]: 重构后的银行间资产负债矩阵
    """

    # NOTE 调用 R 函数方案一：使用 rpy2 直接调用
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    from rpy2.robjects import numpy2ri

    ro.conversion.py2rpy = numpy2ri.py2rpy

    # 导入 R 中的 systemicrisk 包
    systemicrisk = importr('systemicrisk')

    is_added_virtual_bank = None
    match method_adjast_bank_balanceSheet:
        case 'none':
            # NOTE 调整方案〇：无需调整
            A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
        case 'add_virtual_bank':
            # NOTE 调整方案一：添加虚拟银行
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
                is_added_virtual_bank = False
            else:
                A_IB_adjusted, Z_IB_adjusted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB_all, Z_IB_all)
                is_added_virtual_bank = True
                pass  # if
        case 'resize':
            if np.abs(A_IB_all.sum() - Z_IB_all.sum()) < 1e-10:
                A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
                logging.warning("银行间总资产与银行间总负债相等，无需调整。")
            else:
                # #NOTE 调整方案二：调整比例。按照多出来的比例，压缩多出来的金额部分，使得二者相等。
                A_IB_adjusted, Z_IB_adjusted = adjust_A_IB_Z_IB_by_resize(A_IB_all, Z_IB_all)
                pass  # if
        case _:
            raise ValueError("不支持的调整方法！")
            pass  # match

    # 将 NumPy 数组转换为 R 对象
    A_IB_r = numpy2ri.py2rpy(A_IB_adjusted)
    Z_IB_r = numpy2ri.py2rpy(Z_IB_adjusted)

    # 调用 R 中的 calibrate_bilateral_exposure_by_ME_method_use_R_package 函数
    if A_IB_adjusted.size != Z_IB_adjusted.size:  # 如果 A_IB 不是方阵，则使用 nonsquare 模型
        model = systemicrisk.calibrate_ER_nonsquare(A_IB_r, Z_IB_r, float(target_density), n_samples_calib, thin)
    else:
        model = systemicrisk.calibrate_ER(A_IB_r, Z_IB_r, float(target_density), n_samples_calib, thin)
        pass  # if

    # 使用重构的模型生成样本
    reconstructed_L_r = systemicrisk.sample_HierarchicalModel(l=A_IB_r, a=Z_IB_r, model=model, nsamples=1, thin=thin)

    # 将 R 对象转换为 NumPy 数组
    reconstructed_L = np.array(reconstructed_L_r)

    # 最终的银行间负债矩阵
    A_IB_ij = reconstructed_L[0][0]
    Z_IB_ij = A_IB_ij.copy().T

    # # #DEBUG 检测估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
    # logging.debug(f"\n总元素和之误差：{np.round(A_IB_ij.sum() - A_IB_all.sum())}")
    # logging.debug(f"\n总元素和之误差占比：{np.abs(A_IB_ij.sum() - A_IB_all.sum()) / A_IB_all.sum()}")
    # logging.debug(f"\n行元素和之误差：{np.round(A_IB_ij.sum(axis=1) - A_IB_all)}")
    # logging.debug(f"\n行元素和之误差占比：{np.abs(A_IB_ij.sum(axis=1) - A_IB_all) / A_IB_all}")
    # logging.debug(f"\n列元素和之误差：{np.round(A_IB_ij.sum(axis=0) - Z_IB_all)}")
    # logging.debug(f"\n列元素和之误差占比：{np.abs(A_IB_ij.sum(axis=0) - Z_IB_all) / Z_IB_all}")

    logging.info("估算风险敞口矩阵完成。")

    # 检查估算之后的最终的银行间负债矩阵对比原始的银行间负债矩阵
    diff_of_A_IB_all_and_Z_IB_all, diff_of_row_sum, diff_of_col_sum, diff_of_total_sum = check_risk_exposure_matrix_constraints(A_IB_ij, A_IB_adjusted, Z_IB_adjusted)
    logging.info(
        f"""
    \n
    年份: {kwargs['year']}、连接密度: {target_density}\n
    A_IB_all、Z_IB_all 总和的差别: {diff_of_A_IB_all_and_Z_IB_all}\n
    行和约束的差别: {diff_of_row_sum}\n
    列和约束的差别: {diff_of_col_sum}\n
    总和约束的差别: {diff_of_total_sum}\n
    """
    )

    if is_added_virtual_bank is True:  # 如果添加了虚拟银行，则删除虚拟银行
        if is_maintain_virtual_bank:  # 如果保留虚拟银行，则返回虚拟银行
            A_IB = A_IB_ij
            Z_IB = Z_IB_ij
        else:
            A_IB = A_IB_ij[:-1, :-1]
            Z_IB = Z_IB_ij[:-1, :-1]
            pass  # if
    else:
        A_IB = A_IB_ij
        Z_IB = Z_IB_ij
        pass  # if

    return A_IB, Z_IB

    # HACK 调用 R 函数方案二：导出 csv 文件再通过命令行运行 R 函数，最后导入生成的 csv 文件  BUG 这个方案暂时无法运行成功。原因是传入数值失败。

    # match method_adjast_bank_balanceSheet:
    #     case 'none':
    #         ## #NOTE 调整方案〇：无需调整
    #         A_IB_adjusted, Z_IB_adjusted = A_IB_all, Z_IB_all
    #     case 'add_virtual_bank':
    #         ## #NOTE 调整方案一：添加虚拟银行
    #         A_IB_adjusted, Z_IB_adjusted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB_all, Z_IB_all)
    #     case 'resize':
    #         # #NOTE 调整方案二：调整比例。按照多出来的比例，压缩多出来的金额部分，使得二者相等。
    #         A_IB_adjusted, Z_IB_adjusted = adjust_A_IB_Z_IB_by_resize(A_IB_all, Z_IB_all)
    #         pass  # match
    #
    # # 保存 A_IB 和 Z_IB 到 CSV 文件
    # np.savetxt("A_IB_all.csv", A_IB_adjusted, delimiter=",")
    # np.savetxt("Z_IB_all.csv", Z_IB_adjusted, delimiter=",")
    #
    # # 运行 R 脚本
    # # os.system(f"Rscript fun_calibrate_interbank_exposure.R -t {target_density} -i {folderpath_result} -o {Path(folderpath_result, 'reconstructed_L.csv')} -n {n_samples_calib} -l {thin}")
    # os.system(rf'Rscript {Path(Path(__file__).parent.resolve(), "fun_calibrate_interbank_exposure.R")} -d {target_density} -i "{str(folderpath_result)}" -o "{Path(folderpath_result, "reconstructed_L.csv")}" -n {n_samples_calib} -l {thin}')
    #
    # # 读取生成的 CSV 文件
    # reconstructed_L = pd.read_csv("reconstructed_L.csv", header=None).to_numpy()
    #
    # return reconstructed_L

    pass  # function


def calibrate_bilateral_exposure_by_ME_method_with_density_use_Other_algorithm():
    pass  # function


# import numpy as np
# from scipy.optimize import fsolve
#
# def calibrate_ER(l, a, target_density, L_fixed=None, n_samples_calib=100, thin_calib=100):
#     """
#     根据给定的行和列总和,以及目标密度,校准 Erdos-Renyi (ER) 模型。
#
#     参数:
#     l (np.ndarray): 待重构矩阵的行总和
#     a (np.ndarray): 待重构矩阵的列总和
#     target_density (float): 期望的网络密度
#     L_fixed (np.ndarray, optional): 包含已知值的矩阵,NA表示未知。默认为None,表示没有已知值。
#     n_samples_calib (int, optional): 校准过程中生成的矩阵样本数量。默认为100。
#     thin_calib (int, optional): 校准过程中的稀疏化参数。默认为100。
#
#     返回:
#     Model: 校准后的ER模型,可用于生成样本。
#     """
#     n = len(l)
#     if L_fixed is not None:
#         n_free = np.sum(np.isnan(L_fixed))
#     else:
#         n_free = n * n
#     lambda_ = 1 / (np.sum(l) / (target_density * n_free))
#
#     def f(p):
#         print(f"p={p}")
#         model = Model_Indep_p_lambda(Model_p_constant(n, p), Model_lambda_constant(lambda_, n))
#         L_samples = sample_HierarchicalModel(l, a, L_fixed=L_fixed, model=model, n_samples=n_samples_calib, thin=100)
#         return np.mean([np.mean(x > 0) for x in L_samples["L"]] if L_fixed is None else
#                       [np.mean(np.where(~np.isnan(L_fixed), x > 0, np.nan), skipna=True) for x in L_samples["L"]]) - target_density
#
#     res = fsolve(f, 0.5, xtol=0.01, maxfev=20)
#     p = res[0]
#     print(f"p={p}")
#     return Model_Indep_p_lambda(Model_p_constant(n, p), Model_lambda_constant(lambda_, n))
#
# import numpy as np
#
# def sample_HierarchicalModel(l, a, L_fixed=None, model=None, n_samples=10000, thin=100, burn_in=None, matr_per_theta=None, silent=False, tol=np.sqrt(np.finfo(float).eps)):
#     """
#     从给定的行和列总和以及模型中采样矩阵。
#
#     参数:
#     l (np.ndarray): 每个节点的出度之和
#     a (np.ndarray): 每个节点的入度之和
#     L_fixed (np.ndarray, optional): 包含已知值的矩阵,NA表示未知。默认为None,表示没有已知值。
#     model (Model): 校准后的ER模型
#     n_samples (int): 要生成的样本数量
#     thin (int): 采样过程中的稀疏化参数
#     burn_in (int, optional): burn-in的迭代次数,默认为5%的采样次数
#     matr_per_theta (int, optional): 每次更新θ时更新矩阵的次数
#     silent (bool, optional): 是否抑制输出
#     tol (float, optional): 用于检查相等的容差
#
#     返回:
#     dict: 包含生成的样本矩阵和模型参数的字典
#     """
#     # 实现采样过程
#     pass
#
# if __name__ == '__main__':
#     import numpy as np
#
#     # 首先生成一个真实的网络
#     n = 10
#     p = 0.45
#     lam = 0.1
#     L = np.random.binomial(1, p, (n, n)) * np.random.exponential(1/lam, (n, n))
#
#     # 然后使用目标密度0.55重构网络
#     model = calibrate_ER(rowsum(L), colsum(L), 0.55, n_samples_calib=10)
#     L_samples = sample_HierarchicalModel(rowsum(L), colsum(L), model=model, n_samples=10, thin=100)
#
#     # 检查行总和
#     print(rowsum(L))
#     print(rowsum(L_samples["L"][-1]))
#
#     # 检查校准结果
#     print(np.mean(L_samples["L"][-1] > 0))
#
#     # 现在有一些固定的条目
#     L_fixed = L.copy()
#     L_fixed[:n//2, :] = np.nan
#     # 然后使用目标密度0.9重构网络
#     model = calibrate_ER(rowsum(L), colsum(L), 0.9, L_fixed=L_fixed, n_samples_calib=10)
#     L_samples = sample_HierarchicalModel(rowsum(L), colsum(L), L_fixed=L_fixed, model=model, n_samples=10, thin=100)
#     print(np.mean(L_samples["L"][-1][n//2:, :] > 0))  # 已知条目
#     print(np.mean(L_samples["L"][-1][:n//2, :] > 0))  # 重构的条目


# ## 基于以下程序之 Stata 版本翻译成的 Python 版本： #HACK 感觉这个版本不太合适于自己的情况
# # 熵值法通用程序 *********
# #
# # *          设计者：周晶
# #
# # *          单  位：中南财经政法大学工商管理学院农业经济系
# # *          电  邮：zhoucejing@126.com
#
# import numpy as np
#
# def szf(m, n, *args):
#     A = np.zeros((n, 3))
#
#     for i in range(n):
#         j = i + 1
#         b = args[i]
#         b_mean = np.mean(b)
#         b_std = np.std(b)
#         bss = (b - b_mean) / b_std
#         bss = bss + np.min(bss) + 1
#         bs = bss / np.sum(bss)
#         e = np.sum(-1/np.log(m) * bs * np.log(bs))
#         d = 1 - e
#         w = d / np.sum(d)
#         f = np.sum(np.array([w[j-1] * bs[i] for j in range(n)]))
#         A[i, :] = [f, d, w]
#
#     return A
#
# m = 100  # 样本个数
# n = 5  # 指标个数
# x1 = np.random.rand(m)
# x2 = np.random.rand(m)
# x3 = np.random.rand(m)
# x4 = np.random.rand(m)
# x5 = np.random.rand(m)
#
# result = szf(m, n, x1, x2, x3, x4, x5)
# print(result)
# print("This program was developed by Zhou Jing, Zhongnan University of Economics & Law, Wuhan, China")
# print("Email: zhoucejing@126.com")


def RAS_algorithm(A_0: np.ndarray, A_row_sum: np.ndarray, A_col_sum: np.ndarray, denominator_precition_threshold=1e-10) -> np.ndarray:
    """
    RAS 算法

    RAS 算法是一种矩阵调整技术，适用于已知行列总和约束的情境，通常用于平衡矩阵中的行、列总和以达到指定的边际值。在网络生成中，比如借贷矩阵生成时，我们可以使用 RAS 方法确保生成的矩阵符合银行的借入、借出总额约束。

    Args:
        A_0 (np.ndarray): 输入矩阵。
        A_row_sum (np.ndarray): 行约束条件（行和）
        A_col_sum (np.ndarray): 列约束条件（列和）
        denominator_precition_threshold (float): 分母接近零精度阈值。默认值 1e-10。

    Returns:
        np.ndarray: 调整后的矩阵。
    """
    A = np.zeros_like(A_0)
    A1 = np.zeros_like(A_0)
    temp_x = A_0.sum(axis=1)  # 计算每行的和
    temp_x_safe = np.where(temp_x == 0, denominator_precition_threshold, temp_x)  # 将 temp_x 中的零值替换为一个非常小的数值
    r_x = A_row_sum / temp_x_safe  # 计算 r_x
    A1 = A_0 * r_x[:, np.newaxis]
    temp_y = A1.sum(axis=0)  # 计算每列的和
    temp_y_safe = np.where(temp_y == 0, denominator_precition_threshold, temp_y)  # 将 temp_y 中的零值替换为一个非常小的数值
    r_y = A_col_sum / temp_y_safe  # 计算 r_y
    A = A1 * r_y[np.newaxis, :]
    return A
    pass  # function


# def RAS_algorithm_with_preset_values(A_0: np.ndarray, A_row_sum: np.ndarray, A_col_sum: np.ndarray, A_preset_values: np.ndarray, mask: np.ndarray, denominator_precition_threshold=1e-10) -> np.ndarray:
#     """
#     # RAS 算法，带有预置值。
#
#     RAS 算法是一种矩阵调整技术，适用于已知行列总和约束的情境，通常用于平衡矩阵中的行、列总和以达到指定的边际值。在网络生成中，比如借贷矩阵生成时，我们可以使用 RAS 方法确保生成的矩阵符合银行的借入、借出总额约束。
#
#     Args:
#         A_0 (np.ndarray): 输入矩阵。
#         A_row_sum (np.ndarray): 行约束条件（行和，列向量）
#         A_col_sum (np.ndarray): 列约束条件（列和，行向量）
#         A_preset_values (np.ndarray): 预置值的矩阵。
#         mask (np.ndarray): 预置的矩阵掩码。值为 True 表示预置值，值为 False 表示非预置值。
#         denominator_precition_threshold (float): 分母接近零精度阈值。默认值 1e-10。
#
#     Returns:
#         np.ndarray: 调整后的矩阵。
#     """
#     A_0_masked = np.ma.masked_where(mask, A_0)
#     A_row_sum_masked = np.ma.masked_where(np.all(mask, 1), A_row_sum)
#     A_col_sum_masked = np.ma.masked_where(np.all(mask, 0), A_col_sum)
#     A_1 = np.zeros_like(A_0_masked)
#     A_2 = np.zeros_like(A_0_masked)
#     temp_x = np.sum(A_0_masked, axis=1)  # 计算每行的和
#     # temp_x = np.sum(A0 * ~mask, axis=1)  # 计算每行的和
#     temp_x_safe = np.where(temp_x == 0, denominator_precition_threshold, temp_x)  # 将 temp_x 中的零值替换为一个非常小的数值
#     r_x = A_row_sum_masked / temp_x_safe  # 计算 r_x
#     A_1 = A_0_masked * r_x[:, np.newaxis]
#     temp_y = A_1.sum(axis=0)  # 计算每列的和
#     temp_y_safe = np.where(temp_y == 0, denominator_precition_threshold, temp_y)  # 将 temp_y 中的零值替换为一个非常小的数值
#     r_y = A_col_sum_masked / temp_y_safe  # 计算 r_y
#     A_2 = A_1 * r_y[np.newaxis, :]
#     A = np.ma.filled(A_2, fill_value=A_0)
#     return A
#     pass  # function


def is_valid_adjacency_matrix(A: np.ndarray) -> bool:
    """
    检查邻接矩阵是否是对角线元素为 0 的全连接邻接矩阵

    Args:
        A (np.ndarray): 邻接矩阵

    Returns:
        is_valid (bool): 是否是有效的邻接矩阵
    """
    is_valid = True
    if np.any(np.diag(A) != 0):
        logging.error("对角线元素不为 0")
        is_valid = False

    # 检查非对角线元素是否全为非零
    mask = np.ones_like(A, dtype=bool)  # 非对角线元素掩码
    np.fill_diagonal(mask, 0)  # 将对角线元素置为0，保持非对角线为1
    if np.any(A[mask] == 0):  # 如果非对角线元素中有零值，返回False
        logging.error("非对角线元素中有零值")
        is_valid = False

    return is_valid
    pass  # function


def calibrate_with_speed_optimization_for_ME_algorithm_by_R_package(A_IB_all, Z_IB_all, target_density=1.0, n_samples_calib=1000, thin=10):
    """
    #HACK 未适配未使用。通过自适应调整采样数量数量 （n_samples_calib） 来优化校准过程和 thinning factor （thin） 以平衡速度和精度。

    Args:
        A_IB_all (np.ndarray): 银行间资产邻接矩阵
        Z_IB_all (np.ndarray): 银行间负债邻接矩阵
        target_density (float): 邻接矩阵指定的密度。默认值 1.0
        n_samples_calib (int): 校准时生成的矩阵样本数量。默认值 1000
        thin (int): 校准时的稀疏化参数。默认值 10

    Returns:
        Tuple[np.array, np.array]: 重构后的银行间资产负债矩阵
    """
    try:
        # 调整采样数量和薄化因子
        logging.info(f"校准：采用 n_samples_calib={n_samples_calib}, thin={thin}")

        # 调用估算函数
        A_IB_ij, Z_IB_ij = calibrate_bilateral_exposure_by_ME_method_use_R_package(
            A_IB_all,
            Z_IB_all,
            target_density=target_density,
            n_samples_calib=n_samples_calib,
            thin=thin
        )

        # 根据校准结果
        A_IB_all = A_IB_ij.sum(axis=1)
        Z_IB_all = Z_IB_ij.sum(axis=1)

        logging.info("校准完成")
        return A_IB_ij, Z_IB_ij
    except Exception as e:
        logging.error(f"校准失败 {e}")
        return None, None


def weighted_random_choice(choices, weights):
    return np.random.choice(choices, p=np.abs(weights) / np.sum(np.abs(weights)))


# def select_vertices(idxs_vertex_to_remove_edge_in_A_IB, A_IB_adjusted_center, A_IB_1, num_center, N, idxs_vertex_to_add_edge_in_A_IB):
#     idx_vertex_to_remove_edge = weighted_random_choice(idxs_vertex_to_remove_edge_in_A_IB, A_IB_adjusted_center[idxs_vertex_to_remove_edge_in_A_IB])
#     idx_vertex_to_relink_edge = weighted_random_choice(np.arange(num_center, N), A_IB_1[idx_vertex_to_remove_edge, num_center:])
#     idx_vertex_to_add_edge = weighted_random_choice(idxs_vertex_to_add_edge_in_A_IB, A_IB_adjusted_center[idxs_vertex_to_add_edge_in_A_IB])
#     return idx_vertex_to_remove_edge, idx_vertex_to_relink_edge, idx_vertex_to_add_edge


if __name__ == "__main__":
    ## 测试用
    logging.basicConfig(level=logging.DEBUG)

    # ## #DEBUG 测试 calculate_bilateral_exposure_by_CP_method
    #
    # # 假设有 8 个中心银行和 24 个边缘银行
    # num_center = 8
    # num_peripheral = 24
    # num_banks = num_center + num_peripheral
    #
    # # 随机生成银行间总资产和总负债矩阵
    # np.random.seed(42)  # 固定随机种子以便复现结果
    # A_IB_all = (np.random.rand(num_banks) + 1) * 10
    # A_IB_all[:num_center] = (np.random.rand(num_center) + 1) * 500
    # Z_IB_all = (np.random.rand(num_banks) + 1) * 10
    # Z_IB_all[:num_center] = (np.random.rand(num_center) + 1) * 500
    # Z_IB_all = A_IB_all.sum() / Z_IB_all.sum() * Z_IB_all  # A_IB_all 与 Z_IB_all 之和相等
    # print(f"银行间总资产总和与银行间总负债总和差异：{A_IB_all.sum() - Z_IB_all.sum()}")
    #
    # # 中心银行的索引
    # array_idx_center_bank = np.arange(num_center)
    #
    # # 调用函数计算双边敞口
    # A_IB_ij, Z_IB_ij = calculate_bilateral_exposure_by_CP_method(
    #     A_IB_all=A_IB_all,
    #     Z_IB_all=Z_IB_all,
    #     array_idx_center_bank=array_idx_center_bank,
    #     center_agents_networkDensity=0.75,
    #     algorithm_link_center_banks='R语言的systemicrisk包之calibrate_ER',
    #     method_adjast_bank_balanceSheet='resize',
    #     num_center=num_center,
    #     is_show_detal=True,
    #     iteration_threshold=1e-10,
    #     max_iteration=1000,
    #     denominator_precition_threshold=1e-10,
    #     year=2021,
    # )
    #
    # # 打印结果
    # print("银行间资产矩阵 A_IB_ij:")
    # print(A_IB_ij)
    # print(f"\n总元素和之误差：{np.round(A_IB_ij.sum() - A_IB_all.sum())}")
    # print(f"\n总元素和之误差占比：{np.abs(A_IB_ij.sum() - A_IB_all.sum()) / A_IB_all.sum()}")
    # print(f"\n行元素和之误差：{np.round(A_IB_ij.sum(axis=1) - A_IB_all)}")
    # print(f"\n行元素和之误差占比：{np.abs(A_IB_ij.sum(axis=1) - A_IB_all) / A_IB_all}")
    # print(f"\n列元素和之误差：{np.round(A_IB_ij.sum(axis=0) - Z_IB_all)}")
    # print(f"\n列元素和之误差占比：{np.abs(A_IB_ij.sum(axis=0) - Z_IB_all) / Z_IB_all}")
    #
    # print("\n测试 calculate_bilateral_exposure_by_CP_method 完成。\n\n\n")
    #
    # ## #DEBUG 测试 calculate_bilateral_exposure_by_ME_method
    #
    # import numpy as np
    #
    # # 假设有 10 个银行
    # num_banks = 10
    #
    # # 随机生成银行间总资产和总负债矩阵
    # np.random.seed(42)  # 固定随机种子以便复现结果
    # A_IB_all = np.random.rand(num_banks) * 100
    # Z_IB_all = np.random.rand(num_banks) * 100
    # Z_IB_all = A_IB_all.sum() / Z_IB_all.sum() * Z_IB_all  # A_IB_all 与 Z_IB_all 之和相等
    #
    # # 调用函数计算双边敞口
    # A_IB_ij, Z_IB_ij = calculate_bilateral_exposure_by_ME_method(A_IB_all=A_IB_all, Z_IB_all=Z_IB_all, iteration_threshold=1e-10, is_show_detal=True, max_iteration=100, denominator_precition_threshold=1e-10)
    #
    # # 打印结果
    # print("银行间资产矩阵 A_IB_ij:")
    # print(A_IB_ij)
    # print(f"\n总元素和之误差：{np.round(A_IB_ij.sum() - A_IB_all.sum())}")
    # print(f"\n总元素和之误差占比：{np.abs(A_IB_ij.sum() - A_IB_all.sum()) / A_IB_all.sum()}")
    # print(f"\n行元素和之误差：{np.round(A_IB_ij.sum(axis=1) - A_IB_all)}")
    # print(f"\n行元素和之误差占比：{np.abs(A_IB_ij.sum(axis=1) - A_IB_all) / A_IB_all}")
    # print(f"\n列元素和之误差：{np.round(A_IB_ij.sum(axis=0) - Z_IB_all)}")
    # print(f"\n列元素和之误差占比：{np.abs(A_IB_ij.sum(axis=0) - Z_IB_all) / Z_IB_all}")
    #
    # print("\n测试 calculate_bilateral_exposure_by_ME_method 完成。\n\n\n")
    #
    ## #DEBUG 测试 calculate_bilateral_exposure_by_ME_method_with_preset_fixed_values
    #
    # import numpy as np
    #
    # # 假设有 10 个银行
    # num_banks = 10
    #
    # # 随机生成银行间总资产和总负债矩阵
    # np.random.seed(42)  # 固定随机种子以便复现结果
    # A_IB_all = np.random.rand(num_banks) * 100 + 100
    # Z_IB_all = np.random.rand(num_banks) * 100 + 100
    # Z_IB_all = A_IB_all.sum() / Z_IB_all.sum() * Z_IB_all  # A_IB_all 与 Z_IB_all 之和相等
    #
    # # 随机生成预置值的矩阵
    # A_preset_values = np.random.rand(num_banks, num_banks)
    #
    # # 预置规则1：随机选取 25% 的值设为 50，其余的值设为 0
    # set_1 = 10
    # A_preset_values[A_preset_values < 0.75] = 0
    # A_preset_values[A_preset_values >= 0.25] = set_1
    # A_mask = np.where(A_preset_values == set_1, True, False)
    #
    # # 预置规则2：对角线上的值设为 0
    # A_preset_values = A_preset_values - np.diag(np.diag(A_preset_values))
    # A_mask |= np.eye(num_banks, dtype=bool)
    #
    # # A_IB_all += A_preset_values.sum(axis=1)
    # # Z_IB_all += A_preset_values.sum(axis=0)
    #
    # # 调用函数计算双边敞口
    # A_IB_ij, Z_IB_ij = calculate_bilateral_exposure_by_ME_method_with_preset_fixed_values(A_IB_all=A_IB_all, Z_IB_all=Z_IB_all, A_preset_values=A_preset_values, mask=A_mask, iteration_threshold=1e-3, is_show_detal=True, max_iteration=100, denominator_precition_threshold=1e-3)
    #
    # # 打印结果
    # print("银行间资产矩阵 A_IB_ij:")
    # print(A_IB_ij)
    # print(f"\n总元素和之误差：{np.round(A_IB_ij.sum() - A_IB_all.sum())}")
    # print(f"\n总元素和之误差占比：{np.abs(A_IB_ij.sum() - A_IB_all.sum()) / A_IB_all.sum()}")
    # print(f"\n行元素和之误差：{np.round(A_IB_ij.sum(axis=1) - A_IB_all)}")
    # print(f"\n行元素和之误差占比：{np.abs(A_IB_ij.sum(axis=1) - A_IB_all) / A_IB_all}")
    # print(f"\n列元素和之误差：{np.round(A_IB_ij.sum(axis=0) - Z_IB_all)}")
    # print(f"\n列元素和之误差占比：{np.abs(A_IB_ij.sum(axis=0) - Z_IB_all) / Z_IB_all}")
    #
    # print("\n测试 calculate_bilateral_exposure_by_ME_method_with_preset_fixed_values 完成。\n\n\n")
    #
    # ## #DEBUG 测试 calculate_bilateral_exposure_by_ME_method_with_density
    #
    # import numpy as np
    #
    # for i in range(1):
    #     # 假设有 5 个银行
    #     num_banks = 30
    #     target_density = 0.75
    #
    #     # 随机生成银行间总资产和总负债矩阵
    #     np.random.seed(i)  # 固定随机种子以便复现结果
    #     A_IB_all = np.random.rand(num_banks) * 100 + 100
    #     Z_IB_all = np.random.rand(num_banks) * 100 + 100
    #     Z_IB_all = A_IB_all.sum() / Z_IB_all.sum() * Z_IB_all  # A_IB_all 与 Z_IB_all 之和相等
    #
    #     # 调用函数计算双边敞口
    #     A_IB_ij, Z_IB_ij, density, is_the_target_density = calculate_bilateral_exposure_by_ME_method_with_density(
    #         A_IB_all=A_IB_all,
    #         Z_IB_all=Z_IB_all,
    #         target_density=target_density,
    #         iteration_threshold=1e-3,
    #         is_show_detal=True,
    #         max_iteration=100,
    #         denominator_precition_threshold=1e-3,
    #         year=2021,
    #     )
    #
    #     # 打印结果
    #     print(f"\n\n第 {i + 1} 次测试结果：")
    #     print("银行间资产矩阵 A_IB_ij:")
    #     print(A_IB_ij)
    #     print("银行间资产矩阵 A_IB_ij:")
    #     print(A_IB_ij)
    #     print(f"\n总元素和之误差：{np.round(A_IB_ij.sum() - A_IB_all.sum())}")
    #     print(f"\n总元素和之误差占比：{np.abs(A_IB_ij.sum() - A_IB_all.sum()) / A_IB_all.sum()}")
    #     print(f"\n行元素和之误差：{np.round(A_IB_ij.sum(axis=1) - A_IB_all)}")
    #     print(f"\n行元素和之误差占比：{np.abs(A_IB_ij.sum(axis=1) - A_IB_all) / A_IB_all}")
    #     print(f"\n列元素和之误差：{np.round(A_IB_ij.sum(axis=0) - Z_IB_all)}")
    #     print(f"\n列元素和之误差占比：{np.abs(A_IB_ij.sum(axis=0) - Z_IB_all) / Z_IB_all}")
    #     print(f"\n实际密度：{density}")
    #     print(f"\n目标密度：{target_density}")
    #     print(f"\n是否达到目标密度：{is_the_target_density}")
    #
    #     print(f"\n测试 calculate_bilateral_exposure_by_ME_method_with_density 第 {i + 1} 次 完成。\n\n\n")

    pass
