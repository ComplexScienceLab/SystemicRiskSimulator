"""
函数区：可视化工具集
"""

from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

if sgv['need_visualization']:
    import matplotlib.pyplot as plt
    import igraph as ig
    import drawsvg as dw

    pass  # if

from SystemicRiskSimulator.external_packages import pd, np, reduce, Any
from SystemicRiskSimulator.tools.tools import Tools


def generate_one_interbank_matrix_heatmaps_data_info(df_BB: pd.DataFrame, df_IB: pd.DataFrame, colormap: tuple, time: int, dataName: tuple, sgv_vis: dict):
    """
    生成矩阵热图相关的数据信息。

    Args:
        df_BB (pd.DataFrame): 银行数据框
        df_IB (pd.DataFrame): 银行间数据框
        colormap (tuple): 颜色映射元组（包括最小数值对应的颜色、最大数值对应的颜色）
        time (int): 时间
        dataName (tuple): 数据类型名称元组（包括竖向的向量1、横向的向量2、矩阵之名称）
        sgv_vis (dict): 模拟器全局变量

    Returns:
        data: 字典格式的可视化数据集。具体为：
        ```
    data = dict(
        vector1_data=vector1,  # 向量1之绘图数据
        vector1_values=data_vector1,  # 向量1之实际数值
        vector1_labels=data_banksName,  # 向量1之标签
        vector2_data=vector2,  # 向量2之绘图数据
        vector2_values=data_vector2,  # 向量2之实际数值
        vector2_labels=data_banksName,  # 向量2之标签
        matrix_data=matrix,  # 矩阵之绘图数据
        matrix_data=matrix.reshape(data_vector1.size, data_vector2.size),  # 矩阵之实际数值
        colormap=(colormap_min_value, colormap_min_color, colormap_max_value, colormap_max_color)  # 颜色映射元组（包括最小数值、最小数值对应的颜色、最大数值、最大数值对应的颜色）
        )
        ```
    """

    dataName_vector1, dataName_vector2, dataName_matrix = dataName[0], dataName[1], dataName[2]

    ## 获取各银行个体之相关的数据
    data_banksName = df_BB[df_BB[sgv_vis['name_time']] == time]['name'].values  # 银行名称
    data_banksId = df_BB[df_BB[sgv_vis['name_time']] == time]['id_agent'].values  # 银行id
    data_vector1 = df_BB[df_BB[sgv_vis['name_time']] == time][dataName_vector1].values  # 向量1之数据
    data_vector2 = df_BB[df_BB[sgv_vis['name_time']] == time][dataName_vector2].values  # 向量2之数据
    data_matrix = df_IB.loc[df_IB[sgv_vis['name_time']] == time, dataName_matrix].values  # 矩阵之数据

    banks_hel = df_BB[df_BB[sgv_vis['name_time']] == time]['hel'].values  # 银行状态数据
    banks_isv = df_BB[df_BB[sgv_vis['name_time']] == time]['isv'].values
    banks_ilq = df_BB[df_BB[sgv_vis['name_time']] == time]['ilq'].values
    # banks_nrr = df_BB[df_BB[sgv_vis['name_time']] == time]['-rr'].values  #TODO 后续添加新状态
    banks_br = df_BB[df_BB[sgv_vis['name_time']] == time]['br'].values
    banks_off = df_BB[df_BB[sgv_vis['name_time']] == time]['off'].values

    ### 银行状态数据
    list_data_banksState = []
    for i in range(len(data_banksId)):
        list_data_banksState.append(set())
        if banks_hel[i]:
            list_data_banksState[i].add('hel')
        elif banks_off[i]:
            list_data_banksState[i].add('off')
        elif banks_isv[i]:
            list_data_banksState[i].add('isv')
        elif banks_ilq[i]:
            list_data_banksState[i].add('ilq')
        elif banks_br[i]:
            list_data_banksState[i].add('br')
        else:
            print('位于节点' + str(i))
            raise Exception("判断 i 之状态错误".format(str(i)))
            pass  # for

    ## 生成相关的数据之可视化信息

    ### 计算向量1、向量2、矩阵之实际可视化数值
    min_value_in_one_heatmap = (data_vector1.min() - sgv_vis['min_BB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_BB_value_in_all_panel'] - sgv_vis['min_BB_value_in_all_panel'] + 0.0001)
    max_value_in_one_heatmap = (data_vector1.max() - sgv_vis['min_BB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_BB_value_in_all_panel'] - sgv_vis['min_BB_value_in_all_panel'] + 0.0001)
    vector1 = 1.0 * Tools.MinMaxScaler(
        data_vector1,
        (
            0.0 + 1.0 * (min_value_in_one_heatmap),
            0.0 + 1.0 * (max_value_in_one_heatmap)
        )
    ).astype(float)
    vector1[np.isclose(vector1, 0.0, atol=1e-4)] = 0.0

    min_value_in_one_heatmap = (data_vector2.min() - sgv_vis['min_BB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_BB_value_in_all_panel'] - sgv_vis['min_BB_value_in_all_panel'] + 0.0001)
    max_value_in_one_heatmap = (data_vector2.max() - sgv_vis['min_BB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_BB_value_in_all_panel'] - sgv_vis['min_BB_value_in_all_panel'] + 0.0001)
    vector2 = 1.0 * Tools.MinMaxScaler(
        data_vector2,
        (
            0.0 + 1.0 * (min_value_in_one_heatmap),
            0.0 + 1.0 * (max_value_in_one_heatmap)
        )
    ).astype(float)
    vector2[np.isclose(vector2, 0.0, atol=1e-4)] = 0.0

    min_value_in_one_heatmap = (data_matrix.min() - sgv_vis['min_BB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_BB_value_in_all_panel'] - sgv_vis['min_BB_value_in_all_panel'] + 0.0001)
    max_value_in_one_heatmap = (data_matrix.max() - sgv_vis['min_BB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_BB_value_in_all_panel'] - sgv_vis['min_BB_value_in_all_panel'] + 0.0001)
    matrix = 1.0 * Tools.MinMaxScaler(
        data_matrix,
        (
            0.0 + 1.0 * (min_value_in_one_heatmap),
            0.0 + 1.0 * (max_value_in_one_heatmap)
        )
    ).astype(float)
    matrix[np.isclose(matrix, 0.0, atol=1e-4)] = 0.0

    ### 获取银行状态数据之颜色
    data_banksState_color = [sgv['vis']['dict_state_colors'][list(list_data_banksState[i])[0]] for i in range(data_vector1.size)]

    ### 计算银行关系矩阵数据（包括债权债务关系）
    data_banksRelation = df_IB.loc[df_IB[sgv_vis['name_time']] == time, 'A_IB'].values.reshape(data_vector1.size, data_vector2.size)
    data_banksRelation_color = np.empty((data_vector1.size, data_vector2.size), dtype=object)
    for i in range(data_banksRelation.shape[0]):
        for j in range(data_banksRelation.shape[1]):
            data_banksRelation_color[i, j] = sgv['vis']['dict_relation_colors']['cre'] if data_banksRelation[i, j] > 0 else sgv['vis']['dict_relation_colors']['deb']  # FIXME
            pass  # for
        pass  # for

    ### 生成颜色映射信息
    colormap_min_value = sgv_vis['min_BB_value_in_all_panel']
    colormap_min_color = colormap[0]
    colormap_max_value = sgv_vis['max_BB_value_in_all_panel']
    colormap_max_color = colormap[1]

    ### 汇总生成的数据
    data = dict(
        vector1_data=vector1,
        vector1_values=data_vector1,
        vector1_labels=data_banksName,
        vector1_labels_color=data_banksState_color,
        vector2_data=vector2,
        vector2_values=data_vector2,
        vector2_labels=data_banksName,
        vector2_labels_color=data_banksState_color,
        matrix_data=matrix.reshape(data_vector1.size, data_vector2.size),
        matrix_values=data_matrix.reshape(data_vector1.size, data_vector2.size),
        matrix_labels_color=data_banksRelation_color,
        colormap=(colormap_min_value, colormap_min_color, colormap_max_value, colormap_max_color),
    )

    return data
    pass  # function


def draw_one_interbank_matrix_heatmaps(vis_data: dict, sgv_vis: dict, width: float = 10, height: float = 10, dpi=100):
    """
    绘制单独的银行间矩阵热图

    Args:
        vis_data (dict): 网络流数据集
        sgv_vis (dict): 模拟器全局变量
        width (float): 图片宽度（英寸）
        height (float): 图片高度（英寸）
        dpi (int): 图片分辨率

    Returns:
        fig: matplotlib格式的图像对象

    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib.colors import LinearSegmentedColormap
    import matplotlib.colors as colors

    ### 获取、调整该可视化所需要的数据
    vector1_data, vector1_values, vector1_labels, vector1_labels_color, vector2_data, vector2_values, vector2_labels, vector2_labels_color, matrix_data, matrix_values, matrix_labels_color, color_map = np.flipud(vis_data['vector1_data'].astype(float)), np.flipud(vis_data['vector1_values']), np.flipud(vis_data['vector1_labels']), np.flipud(vis_data['vector1_labels_color']), vis_data['vector2_data'], vis_data['vector2_values'], vis_data['vector2_labels'], vis_data['vector2_labels_color'], np.flipud(vis_data['matrix_data'].astype(float)), np.flipud(vis_data['matrix_values']), np.flipud(vis_data['matrix_labels_color']), vis_data['colormap']

    # ## 示例数据  #NOTE 仅在测试该功能期间使用
    # matrix_values = np.random.rand(5, 5)
    # vector1_values = np.random.rand(5)
    # vector2_values = np.random.rand(5)
    # step = 1
    # A_IB = 'A_IB'
    # vector1_labels = ['bank1', 'bank2', 'bank3', 'bank4', 'bank5']
    # vector2_labels = ['bank1', 'bank2', 'bank3', 'bank4', 'bank5']

    ## 创建自定义的颜色映射
    cmap = LinearSegmentedColormap.from_list('custom', [(0, color_map[1]), (1, color_map[3])], N=256)
    norm_color_data = colors.Normalize(vmin=color_map[0], vmax=color_map[2])

    ## 创建 Figure、GridSpec
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    gs = gridspec.GridSpec(2, 2, width_ratios=[1, vector2_data.size], height_ratios=[1, vector1_data.size])

    ## 添加标题与相关的信息
    ax_info = fig.add_subplot(gs[0, 0])
    [spine.set_visible(False) for spine in ax_info.spines.values()]
    if sgv_vis['time_granularity'] == '步进粒度':
        dw_text = f"{sgv_vis['data_name'][2]}\n{sgv_vis['process_name']}\ns={str(sgv_vis['step'])}\nr={str(sgv_vis['round'])}\np={str(sgv_vis['phase'])}"
    elif sgv_vis['time_granularity'] == '轮次粒度':
        dw_text = f"{sgv_vis['data_name'][2]}\n{sgv_vis['process_name']}\nr={str(sgv_vis['round'])}"  # TODO 未测试
    else:
        raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
        pass  # if
    ax_info.text(0, 1, dw_text, ha='left', va='top', color='black', fontsize=20)
    ax_info.set_xticks([])
    ax_info.set_xticklabels([])
    ax_info.set_yticks([])
    ax_info.set_yticklabels([])

    ## 绘制矩阵热图
    ax_matrix = fig.add_subplot(gs[1, 1])
    im_matrix = ax_matrix.pcolormesh(matrix_data.astype(float), cmap=cmap, edgecolors='black', linewidths=0.1, vmin=0, vmax=1)

    ax_matrix.set_title('')
    ax_matrix.set_xticks([])
    ax_matrix.set_xticklabels([])
    ax_matrix.set_yticks([])
    ax_matrix.set_yticklabels([])
    for i in range(matrix_data.shape[0]):  # 在每个方格中添加文本显示值
        for j in range(matrix_data.shape[1]):
            if i == matrix_data.shape[1] - 1 - j:
                continue
            if matrix_values[i, j] == 0:
                ax_matrix.text(j + 0.5, i + 0.5, f'{matrix_values[i, j]:.0f}', ha='center', va='center', color=matrix_labels_color[i, j], fontsize=20, bbox=dict(facecolor=matrix_labels_color[i, j], edgecolor=matrix_labels_color[i, j], boxstyle='round,pad=0.3'))
            else:
                ax_matrix.text(j + 0.5, i + 0.5, f'{matrix_values[i, j]:.0f}', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor=matrix_labels_color[i, j], edgecolor='black', boxstyle='round,pad=0.3'))
                pass  # if
            pass  # for
        pass  # for

    ## 绘制向量1的热图
    ax_vector1 = fig.add_subplot(gs[1, 0])
    ax_vector1.pcolormesh(vector1_data[:, np.newaxis].astype(float), cmap=cmap, edgecolors='black', linewidths=0.1, vmin=0, vmax=1)

    ax_vector1.set_title('')
    ax_vector1.set_xticks([])
    ax_vector1.set_xticklabels([])
    ax_vector1.set_yticks(np.arange(len(vector1_labels)) + 0.5)
    ax_vector1.set_yticklabels(vector1_labels, rotation='vertical', fontsize=16)
    for i in range(vector1_data.shape[0]):  # 在每个方格中添加文本显示值
        if vector1_values[i] == 0:
            # continue
            ax_vector1.text(0.5, i + 0.5, f'{vector1_values[i]:.0f}', ha='center', va='center', color='white', fontsize=20, bbox=dict(facecolor=vector1_labels_color[i], edgecolor='black', boxstyle='round,pad=0.3'))
        else:
            ax_vector1.text(0.5, i + 0.5, f'{vector1_values[i]:.0f}', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor=vector1_labels_color[i], edgecolor='black', boxstyle='round,pad=0.3'))
            pass  # if
        pass  # for

    ## 绘制向量2的热图
    ax_vector2 = fig.add_subplot(gs[0, 1])
    ax_vector2.pcolormesh(vector2_data[np.newaxis, :].astype(float), cmap=cmap, edgecolors='black', linewidths=0.1, vmin=0, vmax=1)

    ax_vector2.set_title('')
    ax_vector2.set_xticks(np.arange(len(vector2_labels)) + 0.5)
    ax_vector2.set_xticklabels(vector2_labels, fontsize=16)
    ax_vector2.xaxis.tick_top()
    ax_vector2.set_yticks([])
    ax_vector2.set_yticklabels([])
    for i in range(vector2_data.shape[0]):  # 在每个方格中添加文本显示值
        if vector2_values[i] == 0:
            # continue
            ax_vector2.text(i + 0.5, 0.5, f'{vector2_values[i]:.0f}', ha='center', va='center', color='white', fontsize=20, bbox=dict(facecolor=vector2_labels_color[i], edgecolor='black', boxstyle='round,pad=0.3'))
        else:
            ax_vector2.text(i + 0.5, 0.5, f'{vector2_values[i]:.0f}', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor=vector2_labels_color[i], edgecolor='black', boxstyle='round,pad=0.3'))
            pass  # if
        pass  # for

    ## 在热图的右侧手动添加颜色条
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(im_matrix, cax=cbar_ax)
    ticks_cbar = Tools.MinMaxScaler(np.linspace(color_map[0], color_map[2], 10), (0, 1))
    labels_cbar = [f'{tick:.0f}' for tick in np.linspace(color_map[0], color_map[2], 10)]
    cbar.set_ticks(ticks_cbar)
    cbar.set_ticklabels(labels_cbar)

    ## 调整子图之间的间距
    plt.subplots_adjust(wspace=0.05, hspace=0.05)

    # plt.show()  # 显示图像  #NOTE 仅在测试该功能期间使用
    plt.close()  # 关闭图像

    return fig
    pass  # function


def generate_one_interbank_graph_data_info(df_BB: pd.DataFrame, df_IB: pd.DataFrame, dict_vis_data: dict, time: int, data_name: str, sgv_vis: dict):
    """
    生成网络图数据信息。

    Args:
        df_BB (pd.DataFrame): 银行数据框
        df_IB (pd.DataFrame): 银行间数据框
        dict_vis_data (dict): 单个时间单个数据类型相关的可视化数据（数据框字典形式）
        time (int): 时间
        data_name (str): 数据名称
        sgv_vis (dict): 模拟器全局变量
        
    Returns:
        data 字典格式的数据集

    """

    df_data_edgeTypes = dict_vis_data['edge_types']

    ### 获取银行间数据种类之名称
    list_edgeTypes_name = df_data_edgeTypes['edge_type'].tolist()

    ## 获取各银行个体之相关的数据
    list_data_banksName = df_BB[df_BB[sgv_vis['name_time']] == time]['name'].tolist()  # 银行名称
    list_data_banksId = df_BB[df_BB[sgv_vis['name_time']] == time]['id_agent'].tolist()  # 银行id
    list_data_processName = df_BB[df_BB[sgv_vis['name_time']] == time]['process_name'].tolist()  # 模型过程名称
    list_data_steps = df_BB[df_BB[sgv_vis['name_time']] == time]['step'].tolist()  # 模型步长
    list_data_rounds = df_BB[df_BB[sgv_vis['name_time']] == time]['round'].tolist()  # 模型轮次
    list_data_phases = df_BB[df_BB[sgv_vis['name_time']] == time]['phase'].tolist()  # 模型相步
    list_data_dataName = df_BB[df_BB[sgv_vis['name_time']] == time][list_edgeTypes_name[0] + '_all'].tolist()  # 节点数据名称
    list_data_A_Q = df_BB[df_BB[sgv_vis['name_time']] == time]['A_Q'].tolist()  # A_Q
    list_data_Shock_run_ilq_t = df_BB[df_BB[sgv_vis['name_time']] == time][list_edgeTypes_name[1] + '_t'].tolist()  # Shock_run_ilq_t
    list_data_Shock_run_ilq_s = df_BB[df_BB[sgv_vis['name_time']] == time][list_edgeTypes_name[1] + '_s'].tolist()  # Shock_run_ilq_s
    # list_vertices_data = [list_data_vertices.extend(list_bank) for list_bank in [list_data_A_Q, list_data_Shock_run_ilq_t, data['Shock_run_ilq_s']]]  # 拼接总的节点索引

    banks_hel = df_BB[df_BB[sgv_vis['name_time']] == time]['hel'].tolist()  # 银行状态数据
    banks_isv = df_BB[df_BB[sgv_vis['name_time']] == time]['isv'].tolist()
    banks_ilq = df_BB[df_BB[sgv_vis['name_time']] == time]['ilq'].tolist()
    # banks_nrr = df_BB[df_BB[sgv_vis['name_time']] == time]['-rr'].tolist()  #TODO 后续添加新状态
    banks_br = df_BB[df_BB[sgv_vis['name_time']] == time]['br'].tolist()
    banks_off = df_BB[df_BB[sgv_vis['name_time']] == time]['off'].tolist()

    list_data_banksState = []  # 银行状态数据
    for i in range(len(list_data_banksId)):
        list_data_banksState.append(set())
        if banks_hel[i]:
            list_data_banksState[i].add('hel')
        elif banks_off[i]:
            list_data_banksState[i].add('off')
        elif banks_isv[i]:
            list_data_banksState[i].add('isv')
        elif banks_ilq[i]:
            list_data_banksState[i].add('ilq')
        elif banks_br[i]:
            list_data_banksState[i].add('br')
        else:
            raise Exception(f"位于节点 {i} 判断 {i} 之状态错误！")
            pass  # for

    ### 获取银行间数据之索引
    list_data_idx_AIBorZIB = (df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[0]] > 0)]['id_agent'].values).tolist()  # 银行间借贷数据之索引
    list_data_idx_ShockIBRunIlq = (df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[1]] > 0)]['id_agent'].values).tolist()  # 银行间之流动性短缺挤兑冲击数据之索引
    list_data_idx_BoIB = (df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[2]] > 0)]['id_agent'].values).tolist()  # 银行间之还款流量数据之索引

    ### 获取银行间数据之类型
    list_dataType_AIBorZIB = [list_edgeTypes_name[0]] * len(list_data_idx_AIBorZIB)
    list_dataType_ShockIBRunIlq = [list_edgeTypes_name[1]] * len(list_data_idx_ShockIBRunIlq)
    list_dataType_BoIB = [list_edgeTypes_name[2]] * len(list_data_idx_BoIB)

    ### 获取银行间数据之边集。边集数据结构是元组列表。元素是元组。元组是边的两个顶点 id 值。
    edges_all = list(zip(df_IB[df_IB[sgv_vis['name_time']] == time]['row'], df_IB[df_IB[sgv_vis['name_time']] == time]['col']))  # 全连接数据之边集，以两点索引表示（银行编号从0开始计数的）
    list_edges_AIBorZIB = [edges_all[i] for i in list_data_idx_AIBorZIB]  # 银行间借贷数据之边集
    list_edges_ShockIBRunIlq = [edges_all[i] for i in list_data_idx_ShockIBRunIlq]  # 银行间之流动性短缺挤兑冲击数据之边集
    list_edges_BoIB = [edges_all[i] for i in list_data_idx_BoIB]  # 银行间之还款流量数据之边集

    ### 获取银行间数据之内容
    list_data_values_AIBorZIB = df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[0]] > 0)][list_edgeTypes_name[0]].values.tolist()  # 银行间借贷数据之值
    list_data_values_ShockIBRunIlq = df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[1]] > 0)][list_edgeTypes_name[1]].values.tolist()  # 银行间之流动性短缺挤兑冲击数据之值
    list_data_values_BoIB = df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[2]] > 0)][list_edgeTypes_name[2]].values.tolist()  # 银行间之还款流量数据之值

    ## 生成相关的数据之可视化信息

    ### 生成各节点之信息
    list_vertices = list_data_banksId  # 节点索引
    list_vertices_value = list_data_dataName  # 节点数据值

    ### 初始化各节点之标签、尺寸、颜色
    list_vertices_label = [''] * len(list_vertices)
    list_vertices_size = [0] * len(list_vertices)
    list_vertices_color = ['#000000'] * len(list_vertices)

    ### 节点数据框
    df_vertices_data = pd.DataFrame(
        dict(
            vertices=list_vertices,
            vertices_label=list_vertices_label,
            vertices_value=list_vertices_value,
            vertices_size=list_vertices_size,
            vertices_color=list_vertices_color,
        )
    )

    ### 设置各节点之尺寸、颜色、标签
    min_vertices_size_in_one_graph = (min(df_vertices_data['vertices_value']) - sgv_vis['min_BB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_BB_value_in_all_panel'] - sgv_vis['min_BB_value_in_all_panel'] + 0.0001)  # 计算单个资金流量网络图之节点尺寸之最小值
    max_vertices_size_in_one_graph = (max(df_vertices_data['vertices_value']) - sgv_vis['min_BB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_BB_value_in_all_panel'] - sgv_vis['min_BB_value_in_all_panel'] + 0.0001)  # 计算单个资金流量网络图之节点尺寸之最大值
    df_vertices_data['vertices_size'] = 40.0 * np.sqrt(np.abs(np.asarray(
        Tools.MinMaxScaler(
            df_vertices_data['vertices_value'].values,
            (
                0.1 + 1.0 * (min_vertices_size_in_one_graph),
                1.0 + 1.0 * (max_vertices_size_in_one_graph)
            )
        )  # 计算各节点之尺寸
    )))  # 设置各节点之尺寸
    df_vertices_data['vertices_color'] = [sgv_vis['dict_state_colors'][','.join(s)] if v >= 0 else '#000000' for s, v in zip(list_data_banksState, df_vertices_data['vertices_value'].values)]  # 设置各节点之颜色，如果是节点值是负数那么是黑色
    df_vertices_data['vertices_label'] = [list_data_banksName[i] + '\n' + str(round(list_vertices_value[i])) for i in range(len(list_vertices_value))]  # 设置各节点之标签

    ### 生成各边集之信息
    list_edges_idx = []
    for list_idx in [list_data_idx_AIBorZIB, list_data_idx_ShockIBRunIlq, list_data_idx_BoIB]:  # 拼接总的边集索引
        list_edges_idx.extend(list_idx)
    list_edges_type = []
    for list_idx in [list_dataType_AIBorZIB, list_dataType_ShockIBRunIlq, list_dataType_BoIB]:  # 拼接总的边集类型
        list_edges_type.extend(list_idx)
    list_edges_value = []
    for list_idx in [list_data_values_AIBorZIB, list_data_values_ShockIBRunIlq, list_data_values_BoIB]:  # 拼接总的边集值
        list_edges_value.extend(list_idx)
    list_edges = []
    for list_idx in [list_edges_AIBorZIB, list_edges_ShockIBRunIlq, list_edges_BoIB]:  # 拼接总的边集列表
        list_edges.extend(list_idx)

    ### 初始化各边之标签、宽度、颜色
    list_edges_label = [''] * len(list_edges_idx)
    list_edges_width = [0] * len(list_edges_idx)
    list_edges_color = ['#000000'] * len(list_edges_idx)

    ### 边数据框
    df_edges_data = pd.DataFrame(
        dict(
            edges=list_edges,
            edges_idx=list_edges_idx,
            edges_type=list_edges_type,
            edges_label=list_edges_label,
            edges_value=list_edges_value,
            edges_width=list_edges_width,
            edges_color=list_edges_color,
        )
    )

    ### 设置各边之宽度、颜色、标签
    for edgeType in df_data_edgeTypes.itertuples():
        min_edges_size_in_one_graph = (min(df_edges_data['edges_value']) - sgv_vis['min_IB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_IB_value_in_all_panel'] - sgv_vis['min_IB_value_in_all_panel'] + 0.0001)  # 计算单个资金流量网络图之边宽度之最小值
        max_edges_size_in_one_graph = (max(df_edges_data['edges_value']) - sgv_vis['min_IB_value_in_all_panel'] + 0.0001) / (sgv_vis['max_IB_value_in_all_panel'] - sgv_vis['min_IB_value_in_all_panel'] + 0.0001)  # 计算单个资金流量网络图之边宽度之最大值
        if ~(df_edges_data['edges_type'] == edgeType.edge_type).any():  # 如果指定类型的边集是空集的话则略过处理
            continue
            pass  # if
        df_edges_data.loc[(df_edges_data['edges_type'] == edgeType.edge_type), 'edges_width'] = 5.0 * np.sqrt(np.asarray(  # BUG 警告：【FutureWarning: Setting an item of incompatible dtype is deprecated and will raise in a future error of pandas. Value 'XXXX.XX' has dtype incompatible with int64, please explicitly cast to a compatible dtype first.】
            Tools.MinMaxScaler(
                df_edges_data.loc[(df_edges_data['edges_type'] == edgeType.edge_type), 'edges_value'].values,
                (
                    0.1 + 1.0 * (min_edges_size_in_one_graph),
                    1.0 + 1.0 * (max_edges_size_in_one_graph),
                )
            )  # 计算各边之宽度
        ))  # 设置各边之宽度
        df_edges_data.loc[df_edges_data['edges_type'] == edgeType.edge_type, 'edges_color'] = edgeType.edge_color  # 设置各边之颜色
        df_edges_data.loc[(df_edges_data['edges_type'] == edgeType.edge_type), 'edges_label'] = [f'{round(v)}' for i, v in enumerate(df_edges_data.loc[(df_edges_data['edges_type'] == edgeType.edge_type), 'edges_value'])]  # 设置各边之标签
        pass  # for

    data = {}  # 待使用的图数据
    data['edge_types'] = df_data_edgeTypes
    data['vertices'] = df_vertices_data
    data['edges'] = df_edges_data
    return data
    pass  # function


def draw_one_interbank_flow_graph(vis_data: dict, sgv_vis: dict, width: float = 5, height: float = 5, dpi: int = 72):
    """
    绘制单独的银行间资金网络图

    Args:
        vis_data (dict): 网络流数据集
        sgv_vis (dict): 模拟器全局变量
        width (float): 图片宽度（英寸）
        height (float): 图片高度（英寸）
        dpi (int): DPI


    Returns:
        fig: matplotlib格式的图像对象

    """
    vertices_data, edges_data = vis_data['vertices'], vis_data['edges']

    ## 创建图对象
    g = ig.Graph(
        directed=True,
    )

    ## 绘制标题
    if sgv_vis['time_granularity'] == '步进粒度':
        dw_text = rf"{sgv_vis['data_name']}    {sgv_vis['process_name']}    s={str(sgv_vis['step'])}    r={str(sgv_vis['round'])}    p={str(sgv_vis['phase'])}"
    elif sgv_vis['time_granularity'] == '轮次粒度':
        dw_text = rf"{sgv_vis['data_name']}    {sgv_vis['process_name']}    r={str(sgv_vis['round'])}"  # DEBUG 未测试
    else:
        raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
        pass  # if

    ## 添加节点和边
    g.add_vertices(vertices_data['vertices'])
    g.add_edges(edges_data['edges'])

    # ## 设置图之顶点与边之数值
    # g.vs['name'] = vertices_data['banks_name']
    # g.vs['health_state'] = vertices_data['data_banksState']
    # g.vs[(sgv_vis['data_name'] + '_all')] = vis_data['vertices_data_value']
    # g.es[sgv_vis['data_name']] = vis_data['edges_data_value']
    # g.es['type']
    # # del g.es['A_IB']

    ## 设置图之属性
    g.vs['label'] = vertices_data['vertices_label']
    g.vs['color'] = vertices_data['vertices_color']
    g.vs['size'] = vertices_data['vertices_size']
    g.es['color'] = edges_data['edges_color']
    g.es['label'] = edges_data['edges_label']
    g.es['width'] = edges_data['edges_width']

    ## 生成可视化图
    fig, ax = plt.subplots(  # BUG 运行警告：RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`). Consider using `matplotlib.pyplot.close()`.
        figsize=(width, height),
        dpi=dpi,
    )
    fig.suptitle(dw_text)
    # ax.set_title = vis_data['banks_name']
    layout = g.layout(layout='auto')
    # layout = g.layout(layout='circle')
    ig.plot(
        g,
        target=ax,
        title='a',
        # bbox= (600,600),
        layout=layout,
        edge_width=g.es['width'],
        vertex_label=g.vs['label'],
        vertex_label_size=8,
        # vertex_frame_color='red',
        vertex_frame_width=0.1,
        edge_label=g.es['label'],
        edge_align_label=True,
        edge_label_dist=100,
        edge_color=g.es['color'],
        edge_background=None,
        edge_font=1,
        edge_label_size=8,
    )

    # plt.show()  # 显示图像  #NOTE 仅在测试该功能期间使用
    plt.close()  # 关闭图像

    return fig
    pass  # function


def generate_one_bank_accounts_data(df_BB: pd.DataFrame, dict_vis_data: dict, time: int, id_agent: int, sgv_vis: dict):
    """
    生成单个银行某一时期之资产负债表账户数据（数据框形式）
    Args:
        df_BB (pd.DataFrame): 银行相关数据
        dict_vis_data (dict): 单个银行单个时间相关的可视化数据（数据框字典形式）
        time (int): 时间
        id_agent (int): 银行个体id
        sgv_vis (dict): 模拟器全局变量

    Returns:
        data: 单个银行单个时间相关的可视化数据（字典列表形式，列表每个元素是数据框形式）

    """

    df_accounts_data, df_shocks_data = dict_vis_data['accounts'], dict_vis_data['shocks']

    # sgv_vis['max_value_BB'] = 0  # 获取资产负债数据之最大值
    # for i in range(sgv_vis['num_items_in_a_time_in_BB']):  # 计算资产负债数据最值
    #     for t in range(sgv_vis['num_time']):
    #         if df_BB[(df_BB[sgv_vis['name_time']] == t) & (df_BB['id_agent'] == i)]['A_all'].values[0] > sgv_vis['max_value_BB']:
    #             sgv_vis['max_value_BB'] = df_BB[(df_BB[sgv_vis['name_time']] == t) & (df_BB['id_agent'] == i)]['A_all'].values[0]
    #         if df_BB[(df_BB[sgv_vis['name_time']] == t) & (df_BB['id_agent'] == i)]['Z_all'].values[0] > sgv_vis['max_value_BB']:
    #             sgv_vis['max_value_BB'] = df_BB[(df_BB[sgv_vis['name_time']] == t) & (df_BB['id_agent'] == i)]['Z_all'].values[0]
    #             pass  # if
    #         pass  # for
    #     pass  # for

    ## 计算资产负债表各列各项数据之值、变动值对应的矩形之高亮框
    for account_data in df_accounts_data.itertuples():
        df_accounts_data.loc[account_data.Index, 'value'] = df_BB.loc[(df_BB[sgv_vis['name_time']] == time) & (df_BB['id_agent'] == id_agent), account_data.subject].values[0]  # BUG 警告：【FutureWarning: Setting an item of incompatible dtype is deprecated and will raise in a future error of pandas. Value 'XXXX.XX' has dtype incompatible with int64, please explicitly cast to a compatible dtype first.】
        value_last = df_BB.loc[(df_BB[sgv_vis['name_time']] == (time - 1 if time != 0 else 0)) & (df_BB['id_agent'] == id_agent), account_data.subject].values[0]
        is_value_changed = False if np.isclose(df_accounts_data.loc[account_data.Index, 'value'], value_last, atol=1e0) else True
        if is_value_changed:
            df_accounts_data.loc[account_data.Index, 'stroke_color'] = '#B7B700'
            df_accounts_data.loc[account_data.Index, 'stroke_width'] = 4
            pass  # if
        pass  # for

    ## 计算资产负债表各资产负债科目之各项数据对应的矩形之绘制位置、绘制尺寸
    boxs_width = [sgv_vis['one_bank_BalanceSheet_width'] * 5 / 24, sgv_vis['one_bank_BalanceSheet_width'] * 4 / 24, sgv_vis['one_bank_BalanceSheet_width'] * 3 / 24, sgv_vis['one_bank_BalanceSheet_width'] * 3 / 24, sgv_vis['one_bank_BalanceSheet_width'] * 4 / 24, sgv_vis['one_bank_BalanceSheet_width'] * 5 / 24]  # 设置资产负债表之账户之各侧边柱子之宽度
    nibs_x = [reduce(lambda x, y: x + y, boxs_width[0:i + 1]) - boxs_width[i] for i in range(len(boxs_width))]  # 设置笔尖之x方向的位置之资产负债表之账户之各侧边柱子之起点
    o = [2, 1, 0, 3, 4, 5]  # 设置资产负债表之账户之各侧边柱子之绘制次序
    count_subject_values_is_zero = 0
    items_subject_values_is_zero = []
    nibs_y = [0, 0, 0, 0, 0, 0]  # 列表之笔尖起始坐标之开始位置之y坐标
    p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
    grouped_by_dataType = df_accounts_data.groupby('data_type')
    for data_type, dataType_values in grouped_by_dataType:
        if data_type == 'equity':
            continue
        grouped_by_level = dataType_values.groupby('level')
        for level, level_values in grouped_by_level:
            nib = (
                sgv_vis['one_bank_BalanceSheet_border'] + int(nibs_x[o[p]]),
                sgv_vis['one_bank_BalanceSheet_border'] + sgv_vis['one_bank_BalanceSheet_title_height']
            )  # 笔尖起始坐标之新柱子之开始位置
            count_balance_is_zero = 0
            items_balance_is_zero = []
            grouped_by_subject = level_values.groupby('subject')
            for subject, subject_values in grouped_by_subject:
                account_idx = df_accounts_data.loc[(df_accounts_data['data_type'] == data_type) & (df_accounts_data['level'] == level) & (df_accounts_data['subject'] == subject), 'subject'].idxmax()
                df_accounts_data.at[account_idx, 'position'] = nib
                df_accounts_data.at[account_idx, 'size'] = (
                    int(boxs_width[o[p]]),
                    int(sgv_vis['one_bank_BalanceSheet_height'] * (subject_values['value'].iloc[0] / sgv_vis['max_BB_value_in_all_panel']))
                )

                # if subject_values['value'].iloc[0]  != 0:
                if subject_values['value'].iloc[0] != 0 or subject_values['value'].iloc[0] == 0:
                    nib = (
                        sgv_vis['one_bank_BalanceSheet_border'] + int(nibs_x[o[p]]),
                        int(nib[1] + sgv_vis['one_bank_BalanceSheet_height'] * (subject_values['value'].iloc[0] / sgv_vis['max_BB_value_in_all_panel']))
                    )  # 笔尖起始坐标之该柱子之下一个项目之柱节之开始位置
                else:  # 如果柱节高度为0...
                    count_subject_values_is_zero += 1
                    items_subject_values_is_zero.append((subject, subject_values['value'].iloc[0], nib[1]))
                    pass  # if
                # for (subject, subject_values['value'].iloc[0], nib_y) in items_subject_values_is_zero:  # HACK 如果有必要的话尝试标记那些柱节高度为0的值
                #     pass  # for
                pass  # for
            nibs_y[o[p]] = nib[1]
            p += 1
            pass  # for
        pass  # for

    ## 计算资产负债表之 equity 科目之对应的矩形之绘制位置、绘制尺寸
    o = [3, 4, 5] if df_accounts_data.loc[(df_accounts_data['data_type'] == 'equity') & (df_accounts_data['level'] == 'level 1') & (df_accounts_data['subject'] == 'E_all'), 'value'].iloc[0] >= 0 else [2, 1, 0]  # 设置资产负债表之账户之各侧边柱子之绘制次序
    p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
    grouped_by_dataType = df_accounts_data.groupby('data_type')
    for data_type, dataType_values in grouped_by_dataType:
        if data_type != 'equity':
            continue
        grouped_by_level = dataType_values.groupby('level')
        for level, level_values in grouped_by_level:
            nib = (
                sgv_vis['one_bank_BalanceSheet_border'] + int(nibs_x[o[p]]),
                int(nibs_y[o[p]])
            )  # 笔尖起始坐标之新柱子之开始位置
            count_balance_is_zero = 0
            items_balance_is_zero = []
            s = 1  # 资产负债表值账户之各侧边柱子之各柱节之绘制索引
            grouped_by_subject = level_values.groupby('subject')
            for subject, subject_values in grouped_by_subject:
                account_idx = df_accounts_data.loc[(df_accounts_data['data_type'] == data_type) & (df_accounts_data['level'] == level) & (df_accounts_data['subject'] == subject), 'subject'].idxmax()
                df_accounts_data.at[account_idx, 'size'] = (
                    int(boxs_width[o[p]]),
                    int(sgv_vis['one_bank_BalanceSheet_height'] * (abs(subject_values['value'].iloc[0]) / sgv_vis['max_BB_value_in_all_panel']))
                )
                df_accounts_data.at[account_idx, 'position'] = nib
                df_accounts_data.at[account_idx, 'fill_color'] = subject_values['fill_color'].iloc[0] if subject_values['value'].iloc[0] >= 0 else '#FFFFFF'  # 如果 equity 是负数则更改其柱子之填充颜色

                # if subject_values['value'].iloc[0]  != 0:
                if subject_values['value'].iloc[0] != 0 or subject_values['value'].iloc[0] == 0:
                    pass  # if
                pass  # for
            p += 1
            pass  # for
        pass  # for

    ## 计算各冲击变量之数据之值、变动值对应的矩形之高亮框、绘制位置、绘制尺寸
    for shock_data in df_shocks_data.itertuples():
        df_shocks_data.loc[shock_data.Index, 'value'] = df_BB.loc[(df_BB[sgv_vis['name_time']] == time) & (df_BB['id_agent'] == id_agent), shock_data.subject].values[0]  # BUG 警告：【FutureWarning: Setting an item of incompatible dtype is deprecated and will raise in a future error of pandas. Value 'XXXX.XX' has dtype incompatible with int64, please explicitly cast to a compatible dtype first.】
        value_last = df_BB.loc[(df_BB[sgv_vis['name_time']] == (time - 1 if time != 0 else 0)) & (df_BB['id_agent'] == id_agent), shock_data.subject].values[0]
        is_value_changed = False if np.isclose(df_shocks_data.loc[shock_data.Index, 'value'], value_last, atol=1e0) else True
        if is_value_changed:
            df_shocks_data.loc[shock_data.Index, 'stroke_color'] = '#B7B700'
            df_shocks_data.loc[shock_data.Index, 'stroke_width'] = 3
            pass  # if

        account_idx = df_accounts_data.loc[(df_accounts_data['data_type'] == shock_data.side) & (df_accounts_data['level'] == shock_data.level) & (df_accounts_data['subject'] == shock_data.align), 'subject'].idxmax()
        account_position = df_accounts_data.loc[account_idx, 'position']
        account_size = df_accounts_data.loc[account_idx, 'size']
        df_shocks_data.at[shock_data.Index, 'size'] = (
            int(account_size[0] * 0.4),
            int(sgv_vis['one_bank_BalanceSheet_height'] * (df_shocks_data.loc[shock_data.Index, 'value'] / sgv_vis['max_BB_value_in_all_panel']))
        )
        if shock_data.data_type[-2:] == '_t':
            offsetScale_by_dataType = 1 / 11
        elif shock_data.data_type[-2:] == '_s':
            offsetScale_by_dataType = 6 / 11
            pass  # if
        df_shocks_data.at[shock_data.Index, 'position'] = (
            account_position[0] + int(account_size[0] * offsetScale_by_dataType),
            account_position[1] + int(account_size[1] - df_shocks_data.loc[shock_data.Index, 'size'][1])
        )  # 笔尖起始坐标之新柱子之开始位置。该坐标值应该与资产负债表之关联的科目之 y 坐标值下对齐。
        pass  # for

    data = {}
    data['accounts'] = df_accounts_data
    data['shocks'] = df_shocks_data
    return data
    pass  # function


def draw_one_bank_BalanceSheet(vis_data: dict, sgv_vis: dict, width: int = 600, height: int = 600, title_height: int = 15, border: int = 5):
    """
    绘制单个银行资产负债表。
    Args:
        vis_data (dict): 可视化数据
        sgv_vis (dict): 相关的一些参数数据（不含资产项目相关的数据）
        width (int): 资产负债表宽度（像素值）
        height (int): 资产负债表高度（像素值）
        title_height (int): 标题高度（像素值）
        border (int): 边框边距（像素值）

    Returns:
        svg_balanceSheet: 单个银行的资产负债表svg格式数据

    """
    accounts_data, shocks_data = vis_data['accounts'], vis_data['shocks']

    svg_balanceSheet = dw.Drawing(border + width + border, border + title_height + height + border, id_prefix='Balance Sheet')

    ## 绘制画布方框
    svg_balanceSheet.append(
        dw.Rectangle(
            x=0,
            y=0,
            width=border + width + border,
            height=border + title_height + height + border,
            fill='none',
            stroke='gray',
            # stroke_opacity=0.5,
            stroke_width=1,
        )
    )

    # ## 绘制有效方框  #NOTE 仅在测试该功能期间使用
    # svg_balanceSheet.append(
    #     dw.Rectangle(
    #         x=border,
    #         y=border + title_height,
    #         width=width,
    #         height=height,
    #         fill='none',
    #         stroke='grey',
    #         stroke_width=1,
    #     )
    # )

    ## 绘制标题
    if sgv_vis['time_granularity'] == '步进粒度':
        dw_text = rf"{sgv_vis['bank_name']}    {sgv_vis['process_name']}    s={str(sgv_vis['step'])}    r={str(sgv_vis['round'])}    p={str(sgv_vis['phase'])}"
    elif sgv_vis['time_granularity'] == '轮次粒度':
        dw_text = rf"{sgv_vis['bank_name']}    {sgv_vis['process_name']}    r={str(sgv_vis['round'])}"  # DEBUG 未测试
    else:
        raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
        pass  # if

    svg_balanceSheet.append(
        dw.Text(
            dw_text,
            font_size=18,
            x=width // 2,
            y=border + title_height // 2,
            text_anchor='middle',
            dominant_baseline='middle',
            font_family=sgv_vis['zh_font_family'],
        )
    )

    ## 绘制资产负债表各列各项之矩形
    for account_data in accounts_data.itertuples():
        svg_balanceSheet.append(
            dw.Rectangle(
                x=account_data.position[0],
                y=account_data.position[1],
                width=account_data.size[0],
                height=account_data.size[1],
                fill=account_data.fill_color,
                fill_opacity=1.0,
                stroke=account_data.stroke_color,
                stroke_width=account_data.stroke_width,
            )
        )
        pass  # for

    ## 绘制各冲击变量之各列各项之矩形
    for shock_data in shocks_data.itertuples():
        if shock_data.size[1] != 0:  # 如果矩形高度为0，则不绘制
            svg_balanceSheet.append(
                dw.Rectangle(
                    x=shock_data.position[0],
                    y=shock_data.position[1],
                    width=shock_data.size[0],
                    height=shock_data.size[1],
                    fill=shock_data.fill_color,
                    fill_opacity=1.0,
                    stroke=shock_data.stroke_color,
                    stroke_width=shock_data.stroke_width
                )
            )
            pass  # if
        pass  # for

    ## 绘制资产负债表各列各项之文本
    for account_data in accounts_data.itertuples():
        svg_balanceSheet.append(
            dw.Text(
                account_data.subject + '\n' + str(round(account_data.value)),
                font_size=18,
                x=account_data.position[0] + account_data.size[0] // 2,
                y=account_data.position[1] + account_data.size[1] // 2,
                text_anchor='middle',
                dominant_baseline='middle',
                font_family=sgv_vis['en_font_family'],
            )
        )
        pass  # for

    ## 绘制各冲击变量之各列各项之文本
    for shock_data in shocks_data.itertuples():
        if shock_data.size[1] != 0:  # 如果矩形高度为0，则不绘制
            svg_balanceSheet.append(
                dw.Text(
                    shock_data.subject + '\n' + str(round(shock_data.value)),
                    font_size=18,
                    x=shock_data.position[0] + shock_data.size[0] // 3,
                    y=shock_data.position[1] + shock_data.size[1] // 3,
                    fill='blue',
                    background='white',
                    text_anchor='middle',
                    dominant_baseline='middle',
                    font_family=sgv_vis['en_font_family'],
                )
            )
            pass  # if
        pass  # for

    return svg_balanceSheet
    pass  # function
