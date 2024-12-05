"""
函数区：可视化工具集。

#NOTE 注意，如果在绘制网络图时，感觉速度慢，可以自行手动修改代码切换到 igraph 工具包代替 NetworkX 工具包。
"""

import matplotlib.pyplot as plt
# import igraph as ig
import networkx as nx
import drawsvg as dw
import fitz
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

from SystemicRiskSimulator.external_packages import pd, np, reduce, Optional, re, Path, deepcopy
from SystemicRiskSimulator.tools.tools import Tools


def generate_one_interbank_matrix_heatmaps_data_info(df_1D_row: pd.DataFrame, df_1D_col: pd.DataFrame, df_2D: pd.DataFrame, colormap: tuple, relations: str, time: int, dataName: tuple, sgv_vis: dict):
    """
    生成矩阵热图相关的数据信息。

    Args:
        df_1D_row (pd.DataFrame): 1D 个体数据框，用于绘制矩阵热图之行信息（对应向量1）
        df_1D_col (pd.DataFrame): 1D 个体数据框，用于绘制矩阵热图之列信息（对应向量2）
        df_2D (pd.DataFrame): 2D 个体间数据框，用于绘制矩阵热图之矩阵信息（对应矩阵）
        colormap (tuple): 颜色映射元组（包括最小数值对应的颜色、最大数值对应的颜色）
        relations (str): 需要绘制的个体间关系
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

    ## 获取各个体之相关的数据
    data_agentsName_row = df_1D_row[df_1D_row[sgv_vis['name_time']] == time]['fullName'].values  # 向量1之个体名称
    data_agentsName_col = df_1D_col[df_1D_col[sgv_vis['name_time']] == time]['fullName'].values  # 向量2之个体名称
    data_agentsId_row = df_1D_row[df_1D_row[sgv_vis['name_time']] == time]['id_agent'].values  # 向量1之个体id
    data_agentsId_col = df_1D_col[df_1D_col[sgv_vis['name_time']] == time]['id_agent'].values  # 向量2之个体id
    data_vector1 = df_1D_row[df_1D_row[sgv_vis['name_time']] == time][dataName_vector1].values  # 向量1之数据
    data_vector2 = df_1D_col[df_1D_col[sgv_vis['name_time']] == time][dataName_vector2].values  # 向量2之数据
    data_matrix = df_2D.loc[df_2D[sgv_vis['name_time']] == time, dataName_matrix].values  # 矩阵之数据

    ### 个体状态数据
    agents_state_row = {}  # 向量1之个体状态数据
    for agentsState_dataType in sgv_vis['set_dataTypes_for_agentsState']:
        if agentsState_dataType in df_1D_row.columns:
            agents_state_row[agentsState_dataType] = df_1D_row[df_1D_row[sgv_vis['name_time']] == time][agentsState_dataType].values
            pass  # if
        pass  # for
    list_data_agentsState_row = []  # 向量1之个体状态数据
    for i in range(len(data_agentsId_row)):
        list_data_agentsState_row.append(set())
        for k, v in agents_state_row.items():
            if v[i]:
                list_data_agentsState_row[i].add(k)
                pass  # if
            if k not in sgv_vis['set_dataTypes_for_agentsState']:
                raise Exception(f"位于节点 {i} 判断 {k} 之状态错误！")
                pass  # if
            pass  # for
        pass  # for

    agents_state_col = {}  # 向量2之个体状态数据
    for agentsState_dataType in sgv_vis['set_dataTypes_for_agentsState']:
        if agentsState_dataType in df_1D_col.columns:
            agents_state_col[agentsState_dataType] = df_1D_col[df_1D_col[sgv_vis['name_time']] == time][agentsState_dataType].values
            pass  # if
        pass  # for
    list_data_agentsState_col = []  # 向量2之个体状态数据
    for i in range(len(data_agentsId_col)):
        list_data_agentsState_col.append(set())
        for k, v in agents_state_col.items():
            if v[i]:
                list_data_agentsState_col[i].add(k)
                pass  # if
            if k not in sgv_vis['set_dataTypes_for_agentsState']:
                raise Exception(f"位于节点 {i} 判断 {k} 之状态错误！")
                pass  # if
            pass  # for
        pass  # for

    ## 生成相关的数据之可视化信息

    ### 计算向量1、向量2、矩阵之实际可视化数值
    min_value_in_one_heatmap = (data_vector1.min() - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001) / (sgv_vis['max_1D_agent_value_in_all_panel'] - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001)  # #BUG 这里很小的正数 0.0001 是为了避免除数为0，但是在一些情景下，可能依然不够小。后同。
    max_value_in_one_heatmap = (data_vector1.max() - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001) / (sgv_vis['max_1D_agent_value_in_all_panel'] - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001)
    vector1 = 1.0 * Tools.MinMaxScaler(
        data_vector1,
        (
            0.0 + 1.0 * (min_value_in_one_heatmap),
            0.0 + 1.0 * (max_value_in_one_heatmap)
        )
    ).astype(float)
    vector1[np.isclose(vector1, 0.0, atol=1e-4)] = 0.0

    min_value_in_one_heatmap = (data_vector2.min() - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001) / (sgv_vis['max_1D_agent_value_in_all_panel'] - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001)
    max_value_in_one_heatmap = (data_vector2.max() - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001) / (sgv_vis['max_1D_agent_value_in_all_panel'] - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001)
    vector2 = 1.0 * Tools.MinMaxScaler(
        data_vector2,
        (
            0.0 + 1.0 * (min_value_in_one_heatmap),
            0.0 + 1.0 * (max_value_in_one_heatmap)
        )
    ).astype(float)
    vector2[np.isclose(vector2, 0.0, atol=1e-4)] = 0.0

    min_value_in_one_heatmap = (data_matrix.min() - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001) / (sgv_vis['max_1D_agent_value_in_all_panel'] - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001)
    max_value_in_one_heatmap = (data_matrix.max() - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001) / (sgv_vis['max_1D_agent_value_in_all_panel'] - sgv_vis['min_1D_agent_value_in_all_panel'] + 0.0001)
    matrix = 1.0 * Tools.MinMaxScaler(
        data_matrix,
        (
            0.0 + 1.0 * (min_value_in_one_heatmap),
            0.0 + 1.0 * (max_value_in_one_heatmap)
        )
    ).astype(float)
    matrix[np.isclose(matrix, 0.0, atol=1e-4)] = 0.0

    ### 获取个体状态数据之颜色
    data_agentsState_color_row = [None] * data_vector1.size
    for i, bank_states in enumerate(list_data_agentsState_row):
        for state in sgv_vis['set_dataTypes_for_agentsState']:  # 顺序遍历 set_dataTypes_for_agentsState 中的每一个状态，如果该状态能够与 bank_states 中的状态匹配，那么就将该状态的颜色添加到个体颜色列表
            if state in bank_states:
                data_agentsState_color_row[i] = sgv_vis['dict_state_colors'][state]
                break
            else:
                data_agentsState_color_row[i] = '#FFFFFF'  # 如果没有个体状态数据，那么就将个体状态数据之颜色设置为白色
                pass  # if
            pass  # for
        pass  # for

    data_agentsState_color_col = [None] * data_vector2.size
    for i, bank_states in enumerate(list_data_agentsState_col):
        for state in sgv_vis['set_dataTypes_for_agentsState']:  # 顺序遍历 set_dataTypes_for_agentsState 中的每一个状态，如果该状态能够与 bank_states 中的状态匹配，那么就将该状态的颜色添加到个体颜色列表
            if state in bank_states:
                data_agentsState_color_col[i] = sgv_vis['dict_state_colors'][state]
                break
            else:
                data_agentsState_color_col[i] = '#FFFFFF'  # 如果没有个体状态数据，那么就将个体状态数据之颜色设置为白色
                pass  # if
            pass  # for
        pass  # for

    ### 计算个体关系矩阵数据（包括债权债务关系），并且设置颜色  #BUG 如果代入的变量不存在字段名称为 'A_IB' 或者 'Z_IB'，那么会报错
    data_agentsRelation_color = np.full((data_vector1.size, data_vector2.size), '#FFFFFF', dtype=object)
    if 'A_IB' in df_2D.columns and 'Z_IB' in df_2D.columns:
        data_A_IB = df_2D.loc[df_2D[sgv_vis['name_time']] == time, 'A_IB'].values.reshape(data_vector1.size, data_vector2.size)
        data_debtors = data_A_IB > 0.0
        data_Z_IB = df_2D.loc[df_2D[sgv_vis['name_time']] == time, 'Z_IB'].values.reshape(data_vector1.size, data_vector2.size)
        data_creditors = data_Z_IB > 0.0
        data_banksRelation = None
        relation_color = '#FFFFFF'  # 如果没有债权债务关系，那么就将关系状态数据之颜色设置为白色
        if relations == 'cre':
            data_banksRelation = data_creditors
            relation_color = sgv_vis['dict_relation_colors']['cre']
        elif relations == 'deb':
            data_banksRelation = data_debtors
            relation_color = sgv_vis['dict_relation_colors']['deb']
            pass  # if
        for i in range(data_agentsRelation_color.shape[0]):
            for j in range(data_agentsRelation_color.shape[1]):
                if data_banksRelation[i, j] > 0:
                    data_agentsRelation_color[i, j] = relation_color
                    pass  # if
                pass  # for
            pass  # for
        pass  # if

    ### 生成值数据颜色映射信息
    colormap_min_value = sgv_vis['min_1D_agent_value_in_all_panel']
    colormap_min_color = colormap[0]
    colormap_max_value = sgv_vis['max_1D_agent_value_in_all_panel']
    colormap_max_color = colormap[1]

    ### 生成其他信息
    others = dict(
        color_map=(colormap_min_value, colormap_min_color, colormap_max_value, colormap_max_color),
        time_granularity=sgv_vis['time_granularity'],
        data_name=[dataName_vector1, dataName_vector2, dataName_matrix],
        process_name=df_1D_row[df_1D_row[sgv_vis['name_time']] == time]['process_name'].values[0],
        step=df_1D_row[df_1D_row[sgv_vis['name_time']] == time]['step'].values[0],
        turn=df_1D_row[df_1D_row[sgv_vis['name_time']] == time]['turn'].values[0],
        phase=df_1D_row[df_1D_row[sgv_vis['name_time']] == time]['phase'].values[0],
    )

    ### 汇总生成的数据
    data = dict(
        vector1_data=vector1,
        vector1_values=data_vector1,
        vector1_labels=data_agentsName_row,
        vector1_labels_color=data_agentsState_color_row,
        vector2_data=vector2,
        vector2_values=data_vector2,
        vector2_labels=data_agentsName_col,
        vector2_labels_color=data_agentsState_color_col,
        matrix_data=matrix.reshape(data_vector1.size, data_vector2.size),
        matrix_values=data_matrix.reshape(data_vector1.size, data_vector2.size),
        matrix_labels_color=data_agentsRelation_color,
        others=others,
    )

    return data
    pass  # function


def draw_one_interbank_matrix_heatmaps(vis_data: dict, sgv_vis: dict, width: float = 10, height: float = 10, dpi: int = 72):
    """
    绘制单独的个体间矩阵热图

    Args:
        vis_data (dict): 网络流数据集
        sgv_vis (dict): 模拟器全局变量
        width (float): 图片宽度（英寸）
        height (float): 图片高度（英寸）
        dpi (int): 图片分辨率

    Returns:
        fig: matplotlib格式的图像对象

    """

    ### 获取、调整该可视化所需要的数据
    (
        vector1_data,
        vector1_values,
        vector1_labels,
        vector1_labels_color,
        vector2_data,
        vector2_values,
        vector2_labels,
        vector2_labels_color,
        matrix_data,
        matrix_values,
        matrix_labels_color,
        others
    ) = (
        np.flipud(vis_data['vector1_data'].astype(float)),
        np.flipud(vis_data['vector1_values']),
        np.flipud(vis_data['vector1_labels']),
        np.flipud(vis_data['vector1_labels_color']),
        vis_data['vector2_data'],
        vis_data['vector2_values'],
        vis_data['vector2_labels'],
        vis_data['vector2_labels_color'],
        np.flipud(vis_data['matrix_data'].astype(float)),
        np.flipud(vis_data['matrix_values']),
        np.flipud(vis_data['matrix_labels_color']),
        vis_data['others']
    )

    # ## 示例数据  #NOTE 仅在测试该功能期间使用
    # matrix_values = np.random.rand(5, 5)
    # vector1_values = np.random.rand(5)
    # vector2_values = np.random.rand(4)
    # step = 1
    # A_IB = 'A_IB'
    # vector1_labels = ['bank1', 'bank2', 'bank3', 'bank4', 'bank5']
    # vector2_labels = ['asset1', 'asset2', 'asset3', 'asset4']

    ## 创建自定义的颜色映射
    cmap = LinearSegmentedColormap.from_list('custom', [(0, others['color_map'][1]), (1, others['color_map'][3])], N=256)
    norm_color_data = colors.Normalize(vmin=others['color_map'][0], vmax=others['color_map'][2])

    ## 创建 Figure、GridSpec
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    gs = gridspec.GridSpec(3, 3, width_ratios=[1, vector2_data.size, 0.75], height_ratios=[0.75, 1, vector1_data.size])

    ## 添加标题与相关的信息
    ax_info = fig.add_subplot(gs[0, :])  # 创建一个新的子图，覆盖整个图像的顶部
    ax_info.axis('off')
    if others['time_granularity'] == '步进粒度':
        # dw_text = f"{others['data_name'][2]}    {others['process_name']}    r={str(others['turn'])}    s={str(others['step'])}    p={str(others['phase'])}"
        dw_text = f"{others['process_name']}    r={str(others['turn'])}    s={str(others['step'])}    p={str(others['phase'])}"
    elif others['time_granularity'] == '轮次粒度':
        # dw_text = f"{others['data_name'][2]}    {others['process_name']}    r={str(others['turn'])}"  # TODO 未测试
        dw_text = f"{others['process_name']}    r={str(others['turn'])}"  # TODO 未测试
    else:
        raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
    ax_info.text(0.5, 1.0, dw_text, ha='center', va='center', color='black', fontsize=16)  # 在子图的中心添加文本

    ## 绘制矩阵热图
    ax_matrix = fig.add_subplot(gs[2, 1], aspect='equal')
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
            if np.isnan(matrix_values[i, j]):
                ax_matrix.text(j + 0.5, i + 0.5, 'NaN', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
            elif matrix_values[i, j] == 0:
                ax_matrix.text(j + 0.5, i + 0.5, f'{matrix_values[i, j]:.0f}', ha='center', va='center', color=matrix_labels_color[i, j], fontsize=20, bbox=dict(facecolor=matrix_labels_color[i, j], edgecolor=matrix_labels_color[i, j], boxstyle='round,pad=0.3'))
            else:
                ax_matrix.text(j + 0.5, i + 0.5, f'{matrix_values[i, j]:.0f}', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor=matrix_labels_color[i, j], edgecolor='black', boxstyle='round,pad=0.3'))
                pass  # if
            pass  # for
        pass  # for

    ## 绘制向量1的热图
    ax_vector1 = fig.add_subplot(gs[2, 0], aspect='equal')
    ax_vector1.pcolormesh(vector1_data[:, np.newaxis].astype(float), cmap=cmap, edgecolors='black', linewidths=0.1, vmin=0, vmax=1)

    ax_vector1.set_title('')
    ax_vector1.set_xticks([])
    ax_vector1.set_xticklabels([])
    ax_vector1.set_yticks(np.arange(len(vector1_labels)) + 0.5)
    ax_vector1.set_yticklabels(vector1_labels, rotation='vertical', fontsize=16)
    ax_vector1.set_ylabel(f"{others['data_name'][0]}", fontsize=16)
    for i in range(vector1_data.shape[0]):  # 在每个方格中添加文本显示值
        if np.isnan(vector1_values[i]):
            ax_vector1.text(0.5, i + 0.5, 'NaN', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
        elif vector1_values[i] == 0:
            ax_vector1.text(0.5, i + 0.5, f'{vector1_values[i]:.0f}', ha='center', va='center', color=vector1_labels_color[i], fontsize=20, bbox=dict(facecolor=vector1_labels_color[i], edgecolor=vector1_labels_color[i], boxstyle='round,pad=0.3'))
        else:
            ax_vector1.text(0.5, i + 0.5, f'{vector1_values[i]:.0f}', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor=vector1_labels_color[i], edgecolor='black', boxstyle='round,pad=0.3'))
            pass  # if
        pass  # for

    ## 绘制向量2的热图
    ax_vector2 = fig.add_subplot(gs[1, 1], aspect='equal')
    ax_vector2.pcolormesh(vector2_data[np.newaxis, :].astype(float), cmap=cmap, edgecolors='black', linewidths=0.1, vmin=0, vmax=1)

    ax_vector2.set_title('')
    ax_vector2.set_xticks(np.arange(len(vector2_labels)) + 0.5)
    ax_vector2.set_xticklabels(vector2_labels, fontsize=16)
    ax_vector2.xaxis.tick_top()
    ax_vector2.set_xlabel(f"{others['data_name'][1]}", fontsize=16)
    ax_vector2.xaxis.set_label_position('top')
    ax_vector2.set_yticks([])
    ax_vector2.set_yticklabels([])
    for i in range(vector2_data.shape[0]):  # 在每个方格中添加文本显示值
        if np.isnan(vector2_values[i]):
            ax_vector2.text(i + 0.5, 0.5, 'NaN', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
        elif vector2_values[i] == 0:
            ax_vector2.text(i + 0.5, 0.5, f'{vector2_values[i]:.0f}', ha='center', va='center', color=vector2_labels_color[i], fontsize=20, bbox=dict(facecolor=vector2_labels_color[i], edgecolor=vector2_labels_color[i], boxstyle='round,pad=0.3'))
        else:
            ax_vector2.text(i + 0.5, 0.5, f'{vector2_values[i]:.0f}', ha='center', va='center', color='black', fontsize=20, bbox=dict(facecolor=vector2_labels_color[i], edgecolor='black', boxstyle='round,pad=0.3'))
            pass  # if
        pass  # for

    ## 在热图的右侧手动添加颜色条
    cbar_ax = fig.add_axes([0.875, 0.1, 0.03, 0.7])
    cbar = fig.colorbar(im_matrix, cax=cbar_ax)
    ticks_cbar = Tools.MinMaxScaler(np.linspace(others['color_map'][0], others['color_map'][2], 10), (0, 1))
    labels_cbar = [f'{tick:.0f}' for tick in np.linspace(others['color_map'][0], others['color_map'][2], 10)]
    cbar.set_ticks(ticks_cbar)
    cbar.set_ticklabels(labels_cbar)

    ## 添加向量1之变量名、向量2之变量名、矩阵之变量名
    ax_title = fig.add_subplot(gs[1, 0])  # 创建一个新的子图，实现向量1之变量名、向量2之变量名、矩阵之变量名的显示
    ax_title.axis('off')
    # ax_title.text(0.5, 0.25, f"{others['data_name'][0]}", ha='center', va='center', color='black', fontsize=16)
    # ax_title.text(0.5, 1.25, f"{others['data_name'][1]}", ha='center', va='center', color='black', fontsize=16)
    ax_title.text(0.25, 0.75, f"{others['data_name'][2]}", ha='center', va='center', color='black', fontsize=16)

    ## 调整子图之间的间距
    plt.subplots_adjust(wspace=0.05, hspace=0.05)

    # plt.show()  # 显示图像  #NOTE 仅在测试该功能期间使用
    plt.close()  # 关闭图像

    return fig
    pass  # function


def generate_one_interbank_graph_data_info(df_BB: pd.DataFrame, df_IB: pd.DataFrame, dict_vis_data: dict, time: int, data_name: str, sgv_vis: dict):
    """
    生成网络图数据信息。 #TODO 需要重构

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
    list_data_banksName = df_BB[df_BB[sgv_vis['name_time']] == time]['fullName'].tolist()  # 银行名称
    list_data_banksId = df_BB[df_BB[sgv_vis['name_time']] == time]['id_agent'].tolist()  # 银行id
    list_data_processName = df_BB[df_BB[sgv_vis['name_time']] == time]['process_name'].tolist()  # 模型过程名称
    list_data_steps = df_BB[df_BB[sgv_vis['name_time']] == time]['step'].tolist()  # 模型步长
    list_data_turns = df_BB[df_BB[sgv_vis['name_time']] == time]['turn'].tolist()  # 模型轮次
    list_data_phases = df_BB[df_BB[sgv_vis['name_time']] == time]['phase'].tolist()  # 模型相步
    list_data_dataName = df_BB[df_BB[sgv_vis['name_time']] == time][list_edgeTypes_name[0] + '_all'].tolist()  # 节点数据名称
    list_data_A_Q = df_BB[df_BB[sgv_vis['name_time']] == time]['A_Q'].tolist()  # A_Q
    list_data_Shock_run_ilq_t = df_BB[df_BB[sgv_vis['name_time']] == time][list_edgeTypes_name[1] + '_t'].tolist()  # Shock_run_ilq_t
    list_data_Shock_run_ilq_s = df_BB[df_BB[sgv_vis['name_time']] == time][list_edgeTypes_name[1] + '_s'].tolist()  # Shock_run_ilq_s
    # list_vertices_data = [list_data_vertices.extend(list_bank) for list_bank in [list_data_A_Q, list_data_Shock_run_ilq_t, data['Shock_run_ilq_s']]]  # 拼接总的节点索引

    data_banksId = df_BB[df_BB[sgv_vis['name_time']] == time]['id_agent'].values  # 银行id

    ### 银行状态数据
    banks_state = {}
    for banksState_dataType in sgv_vis['set_dataTypes_for_agentsState']:
        banks_state[banksState_dataType] = df_BB[df_BB[sgv_vis['name_time']] == time][banksState_dataType].values
        pass  # for
    list_data_banksState = []
    for i in range(len(list_data_banksId)):
        list_data_banksState.append(set())
        for k, v in banks_state.items():
            if v[i]:
                list_data_banksState[i].add(k)
                pass  # if
            if k not in sgv_vis['set_dataTypes_for_agentsState']:
                raise Exception(f"位于节点 {i} 判断 {k} 之状态错误！")
                pass  # if
            pass  # for
        pass  # for

    ### 获取银行间数据之索引
    if len(list_edgeTypes_name) <= 2:
        list_data_idx_AIBorZIB = (df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[0]] > 0)]['id_agent'].values).tolist()  # 银行间借贷数据之索引
        list_data_idx_ShockIBRunIlq = (df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[1]] > 0)]['id_agent'].values).tolist()  # 银行间之流动性短缺挤兑冲击数据之索引
    else:
        list_data_idx_BoIB = (df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[2]] > 0)]['id_agent'].values).tolist()  # 银行间之还款流量数据之索引

    ### 获取银行间数据之类型
    if len(list_edgeTypes_name) <= 2:
        list_dataType_AIBorZIB = [list_edgeTypes_name[0]] * len(list_data_idx_AIBorZIB)
        list_dataType_ShockIBRunIlq = [list_edgeTypes_name[1]] * len(list_data_idx_ShockIBRunIlq)
    else:
        list_dataType_BoIB = [list_edgeTypes_name[2]] * len(list_data_idx_BoIB)

    ### 获取银行间数据之边集。边集数据结构是元组列表。元素是元组。元组是边的两个顶点 id 值。
    edges_all = list(zip(df_IB[df_IB[sgv_vis['name_time']] == time]['row'], df_IB[df_IB[sgv_vis['name_time']] == time]['col']))  # 全连接数据之边集，以两点索引表示（银行编号从0开始计数的）
    if len(list_edgeTypes_name) <= 2:
        list_edges_AIBorZIB = [edges_all[i] for i in list_data_idx_AIBorZIB]  # 银行间借贷数据之边集
        list_edges_ShockIBRunIlq = [edges_all[i] for i in list_data_idx_ShockIBRunIlq]  # 银行间之流动性短缺挤兑冲击数据之边集
    else:
        list_edges_BoIB = [edges_all[i] for i in list_data_idx_BoIB]  # 银行间之还款流量数据之边集

    ### 获取银行间数据之内容
    if len(list_edgeTypes_name) <= 2:
        list_data_values_AIBorZIB = df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[0]] > 0)][list_edgeTypes_name[0]].values.tolist()  # 银行间借贷数据之值
        list_data_values_ShockIBRunIlq = df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[1]] > 0)][list_edgeTypes_name[1]].values.tolist()  # 银行间之流动性短缺挤兑冲击数据之值
    else:
        list_data_values_BoIB = df_IB[(df_IB[sgv_vis['name_time']] == time) & (df_IB[list_edgeTypes_name[2]] > 0)][list_edgeTypes_name[2]].values.tolist()  # 银行间之还款流量数据之值

    ## 生成相关的数据之可视化信息

    ### 生成各节点之信息
    list_vertices = list_data_banksId  # 节点索引
    list_vertices_value = list_data_dataName  # 节点数据值

    ### 初始化各节点之标签、尺寸、颜色
    list_vertices_label = [''] * len(list_vertices)
    list_vertices_size = [0.0] * len(list_vertices)
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
    df_vertices_data['vertices_size'] = 80.0 * np.sqrt(np.abs(np.asarray(
        Tools.MinMaxScaler(
            df_vertices_data['vertices_value'].values,
            (
                0.1 + 1.0 * (min_vertices_size_in_one_graph),
                1.0 + 1.0 * (max_vertices_size_in_one_graph)
            )
        )  # 计算各节点之尺寸
    )))  # 设置各节点之尺寸
    df_vertices_data['vertices_color'] = [None] * len(list_vertices_value)
    for i, bank_states in enumerate(list_data_banksState):
        for state in sgv_vis['set_dataTypes_for_agentsState']:  # 顺序遍历 set_dataTypes_for_agentsState 中的每一个状态，如果该状态能够与 bank_states 中的状态匹配，那么就将该状态的颜色添加到个体颜色列表
            if state in bank_states:
                df_vertices_data['vertices_color'][i] = sgv_vis['dict_state_colors'][state] if (not np.isnan(list_vertices_value[i]) and list_vertices_value[i] >= 0) else '#000000'
                break

    df_vertices_data['vertices_label'] = [list_data_banksName[i] + '\n' + str(round(list_vertices_value[i]) if not np.isnan(list_vertices_value[i]) else 'NaN') for i in range(len(list_vertices_value))]  # 设置各节点之标签

    ### 生成各边集之信息
    list_edges_idx = []
    if len(list_edgeTypes_name) <= 2:
        for list_idx in [list_data_idx_AIBorZIB, list_data_idx_ShockIBRunIlq]:  # 拼接总的边集索引
            list_edges_idx.extend(list_idx)
        list_edges_type = []
        for list_idx in [list_dataType_AIBorZIB, list_dataType_ShockIBRunIlq]:  # 拼接总的边集类型
            list_edges_type.extend(list_idx)
        list_edges_value = []
        for list_idx in [list_data_values_AIBorZIB, list_data_values_ShockIBRunIlq]:  # 拼接总的边集值
            list_edges_value.extend(list_idx)
        list_edges = []
        for list_idx in [list_edges_AIBorZIB, list_edges_ShockIBRunIlq]:  # 拼接总的边集列表
            list_edges.extend(list_idx)
    else:
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
        pass  # if

    ### 初始化各边之标签、宽度、颜色
    list_edges_label = [''] * len(list_edges_idx)
    list_edges_width = [0.0] * len(list_edges_idx)
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
        df_edges_data.loc[(df_edges_data['edges_type'] == edgeType.edge_type), 'edges_width'] = 10.0 * np.sqrt(np.asarray(
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

    ## 生成其他信息
    others = dict(
        time_granularity=sgv_vis['time_granularity'],
        data_name=data_name,
        process_name=df_BB[df_BB[sgv_vis['name_time']] == time]['process_name'].values[0],
        step=df_BB[df_BB[sgv_vis['name_time']] == time]['step'].values[0],
        turn=df_BB[df_BB[sgv_vis['name_time']] == time]['turn'].values[0],
        phase=df_BB[df_BB[sgv_vis['name_time']] == time]['phase'].values[0],
    )

    # 待使用的图数据
    data = dict(
        edge_types=df_data_edgeTypes,
        vertices=df_vertices_data,
        edges=df_edges_data,
        others=others,
    )

    return data
    pass  # function


def draw_one_interbank_flow_graph(vis_data: dict, width: float = 10, height: float = 10, dpi: int = 72):
    """
    绘制单独的银行间资金网络图（NetworkX 版本）

    Args:
        vis_data (dict): 网络流数据集
        width (float): 图片宽度（英寸）
        height (float): 图片高度（英寸）
        dpi (int): DPI

    Returns:
        fig: matplotlib格式的图像对象

    """
    edge_types, vertices_data, edges_data, others = vis_data['edge_types'], vis_data['vertices'], vis_data['edges'], vis_data['others']

    ## 创建图对象
    G = nx.DiGraph()

    ## 添加节点和边
    for vertex in vertices_data['vertices']:
        G.add_node(vertex, label=vertices_data['vertices_label'][vertex], color=vertices_data['vertices_color'][vertex], size=vertices_data['vertices_size'][vertex])

    for i, edge in enumerate(edges_data['edges']):
        G.add_edge(edge[0], edge[1], label=edges_data['edges_label'][i], color=edges_data['edges_color'][i], width=edges_data['edges_width'][i])

    ## 绘制标题
    if others['time_granularity'] == '步进粒度':
        dw_text = rf"{others['data_name']}   {others['process_name']}   r={str(others['turn'])}   s={str(others['step'])}   p={str(others['phase'])}"
    elif others['time_granularity'] == '轮次粒度':
        dw_text = rf"{others['data_name']}   {others['process_name']}   r={str(others['turn'])}"
    else:
        raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")

    ## 生成可视化图
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    fig.suptitle(dw_text, fontsize=16)

    pos = nx.spring_layout(G)  # 使用 spring 布局
    node_colors = [G.nodes[node]['color'] for node in G.nodes]
    node_sizes = [G.nodes[node]['size'] * 100 for node in G.nodes]  # 调整节点大小
    edge_colors = [G.edges[edge]['color'] for edge in G.edges]
    edge_widths = [G.edges[edge]['width'] for edge in G.edges]
    edge_labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, ax=ax, labels=nx.get_node_attributes(G, 'label'), node_color=node_colors, node_size=node_sizes, edge_color=edge_colors, width=edge_widths, with_labels=True, font_size=16)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=16)

    plt.close()  # 关闭图像

    return fig


# def draw_one_interbank_flow_graph(vis_data: dict, width: float = 10, height: float = 10, dpi: int = 72):
#     """
#     绘制单独的银行间资金网络图（igraph 版本）
#
#     Args:
#         vis_data (dict): 网络流数据集
#         width (float): 图片宽度（英寸）
#         height (float): 图片高度（英寸）
#         dpi (int): DPI
#
#
#     Returns:
#         fig: matplotlib格式的图像对象
#
#     """
#     edge_types, vertices_data, edges_data, others = vis_data['edge_types'], vis_data['vertices'], vis_data['edges'], vis_data['others']
#
#     ## 创建图对象
#     g = ig.Graph(
#         directed=True,
#     )
#
#     ## 绘制标题
#     if others['time_granularity'] == '步进粒度':
#         dw_text = rf"{others['data_name']}   {others['process_name']}   r={str(others['turn'])}   s={str(others['step'])}   p={str(others['phase'])}"
#     elif others['time_granularity'] == '轮次粒度':
#         dw_text = rf"{others['data_name']}   {others['process_name']}   r={str(others['turn'])}"  # DEBUG 未测试
#     else:
#         raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
#         pass  # if
#
#     ## 添加节点和边
#     g.add_vertices(vertices_data['vertices'])
#     g.add_edges(edges_data['edges'])
#
#     # ## 设置图之顶点与边之数值
#     # g.vs['name'] = vertices_data['banks_name']
#     # g.vs['health_state'] = vertices_data['data_banksState']
#     # g.vs[(others['data_name'] + '_all')] = vis_data['vertices_data_value']
#     # g.es[sgv_vis['data_name']] = vis_data['edges_data_value']
#     # g.es['type']
#     # # del g.es['A_IB']
#
#     ## 设置图之属性
#     g.vs['label'] = vertices_data['vertices_label']
#     # g.vs['label'] = vertices_data['vertices_label'] if not np.isnan(vertices_data['vertices_label']) else 'NaN'
#     g.vs['color'] = vertices_data['vertices_color']
#     # g.vs['size'] = vertices_data['vertices_size']
#     g.vs['size'] = [vertices_size if not np.isnan(vertices_size) else 0.0 for vertices_size in vertices_data['vertices_size']]
#     g.es['color'] = edges_data['edges_color']
#     g.es['label'] = edges_data['edges_label']
#     # g.es['width'] = edges_data['edges_width']
#     g.es['width'] = [edges_width if not np.isnan(edges_width) else 0.0 for edges_width in edges_data['edges_width']]
#
#     ## 生成可视化图
#     fig, ax = plt.subplots(
#         figsize=(width, height),
#         dpi=dpi,
#     )
#     fig.suptitle(dw_text, fontsize=16)
#     # ax.set_title = vis_data['banks_name']
#     layout = g.layout(layout='auto')
#     # layout = g.layout(layout='circle')
#     ig.plot(
#         g,
#         target=ax,
#         title='a',
#         # bbox= (600,600),
#         layout=layout,
#         edge_width=g.es['width'],
#         vertex_label=g.vs['label'],
#         vertex_label_size=16,
#         # vertex_frame_color='red',
#         vertex_frame_width=0.1,
#         edge_label=g.es['label'],
#         edge_align_label=True,
#         edge_label_dist=100,
#         edge_color=g.es['color'],
#         edge_background=None,
#         edge_font=1,
#         edge_label_size=16,
#     )
#
#     # plt.show()  # 显示图像  #NOTE 仅在测试该功能期间使用
#     plt.close()  # 关闭图像
#
#     return fig
#     pass  # function


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

    # #TODO 可视化资产负债表图标题移到下面位置

    # 判断资产负债表单侧有几列。如果找不到 level='level 3'，则是单侧 2 列的资产负债表
    for k1, v1 in dict_vis_data.items():
        for v2 in v1.itertuples():
            if v2.level == 'level 3':
                num_column_one_side = 3
                break
            else:
                num_column_one_side = 2
                pass  # if
            pass  # for
        pass  # for

    # 如果是单侧 3 列的资产负债表
    if num_column_one_side == 3:
        ## 计算资产负债表各列各项数据之值、变动值对应的矩形之高亮框
        for account_data in dict_vis_data['accounts'].itertuples():
            dict_vis_data['accounts'].loc[account_data.Index, 'value'] = df_BB.loc[(df_BB[sgv_vis['name_time']] == time) & (df_BB['id_agent'] == id_agent), account_data.subject].values[0]
            value_last = df_BB.loc[(df_BB[sgv_vis['name_time']] == (time - 1 if time != 0 else 0)) & (df_BB['id_agent'] == id_agent), account_data.subject].values[0]
            is_value_changed = False if np.isclose(dict_vis_data['accounts'].loc[account_data.Index, 'value'], value_last, atol=1e0) else True
            if is_value_changed:
                dict_vis_data['accounts'].loc[account_data.Index, 'stroke_color'] = '#000000'
                dict_vis_data['accounts'].loc[account_data.Index, 'stroke_width'] = 2
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
        grouped_by_dataType = dict_vis_data['accounts'].groupby('data_type')
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
                    account_idx = dict_vis_data['accounts'].loc[(dict_vis_data['accounts']['data_type'] == data_type) & (dict_vis_data['accounts']['level'] == level) & (dict_vis_data['accounts']['subject'] == subject), 'subject'].idxmax()
                    dict_vis_data['accounts'].at[account_idx, 'position'] = nib
                    # 判断如果有一个数值出现 NaN 则设置其高度为一个很大的数，以便于在绘制时显示异常，从而提示这里有错误
                    if not (np.isnan(subject_values['value'].iloc[0]) or np.isnan(sgv_vis['max_BB_value_in_all_panel'])):
                        height_size = int(sgv_vis['one_bank_BalanceSheet_height'] * (subject_values['value'].iloc[0] / (sgv_vis['max_BB_value_in_all_panel'] if not np.isnan(sgv_vis['max_BB_value_in_all_panel']) else 'NaN')))
                    else:
                        height_size = int(1e6)  # #BUG 最好抛出异常
                        pass  # if
                    dict_vis_data['accounts'].at[account_idx, 'size'] = (
                        int(boxs_width[o[p]]),
                        height_size
                    )

                    # if subject_values['value'].iloc[0]  != 0:
                    if subject_values['value'].iloc[0] != 0 or subject_values['value'].iloc[0] == 0:
                        nib = (
                            sgv_vis['one_bank_BalanceSheet_border'] + int(nibs_x[o[p]]),
                            int(nib[1] + height_size)
                        )  # 笔尖起始坐标之该柱子之下一个项目之柱节之开始位置
                    else:  # 如果柱节高度为0... #HACK #TODO 这个以后再处理
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
        o = [3, 4, 5] if dict_vis_data['accounts'].loc[(dict_vis_data['accounts']['data_type'] == 'equity') & (dict_vis_data['accounts']['level'] == 'level 1') & (dict_vis_data['accounts']['subject'] == 'E_all'), 'value'].iloc[0] >= 0 else [2, 1, 0]  # 设置资产负债表之账户之各侧边柱子之绘制次序
        p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
        grouped_by_dataType = dict_vis_data['accounts'].groupby('data_type')
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
                    account_idx = dict_vis_data['accounts'].loc[(dict_vis_data['accounts']['data_type'] == data_type) & (dict_vis_data['accounts']['level'] == level) & (dict_vis_data['accounts']['subject'] == subject), 'subject'].idxmax()
                    # 判断如果有一个数值出现 NaN 则设置其高度为一个很大的数，以便于在绘制时显示异常，从而提示这里有错误
                    if not (np.isnan(subject_values['value'].iloc[0]) or np.isnan(sgv_vis['max_BB_value_in_all_panel'])):
                        height_size = int(sgv_vis['one_bank_BalanceSheet_height'] * (subject_values['value'].iloc[0] / (sgv_vis['max_BB_value_in_all_panel'] if not np.isnan(sgv_vis['max_BB_value_in_all_panel']) else 'NaN')))
                    else:
                        height_size = int(1e6)
                        pass  # if
                    dict_vis_data['accounts'].at[account_idx, 'size'] = (
                        int(boxs_width[o[p]]),
                        height_size
                    )
                    dict_vis_data['accounts'].at[account_idx, 'position'] = nib
                    dict_vis_data['accounts'].at[account_idx, 'fill_color'] = subject_values['fill_color'].iloc[0] if subject_values['value'].iloc[0] >= 0 else '#FFFFFF'  # 如果 equity 是负数则更改其柱子之填充颜色

                    # if subject_values['value'].iloc[0]  != 0:
                    if subject_values['value'].iloc[0] != 0 or subject_values['value'].iloc[0] == 0:
                        pass  # if
                    pass  # for
                p += 1
                pass  # for
            pass  # for

        ## 计算除了资产负债表各科目之外的其他变量之数据之值、变动值对应的矩形之高亮框、绘制位置、绘制尺寸
        df_data_to_vis_other_variables_for_one_bank_accounts = pd.DataFrame(sgv_vis['config_data_to_vis_other_variables_for_one_bank_accounts'])
        for index, row in df_data_to_vis_other_variables_for_one_bank_accounts.iterrows():
            for a_data in dict_vis_data[row['df_dataName']].itertuples():
                a_data_value = df_BB.loc[(df_BB[sgv_vis['name_time']] == time) & (df_BB['id_agent'] == id_agent), a_data.subject].values[0]
                dict_vis_data[row['df_dataName']].loc[a_data.Index, 'value'] = a_data_value
                value_last = df_BB.loc[(df_BB[sgv_vis['name_time']] == (time - 1 if time != 0 else 0)) & (df_BB['id_agent'] == id_agent), a_data.subject].values[0]
                is_value_changed = False if np.isclose(a_data_value, value_last, atol=1e0) else True
                if is_value_changed:
                    dict_vis_data[row['df_dataName']].loc[a_data.Index, 'stroke_color'] = '#000000'
                    dict_vis_data[row['df_dataName']].loc[a_data.Index, 'stroke_width'] = 2
                    pass  # if

                account_idx = dict_vis_data['accounts'].loc[(dict_vis_data['accounts']['data_type'] == a_data.side) & (dict_vis_data['accounts']['level'] == a_data.level) & (dict_vis_data['accounts']['subject'] == a_data.align), 'subject'].idxmax()
                account_position = dict_vis_data['accounts'].loc[account_idx, 'position']
                account_size = dict_vis_data['accounts'].loc[account_idx, 'size']
                dict_vis_data[row['df_dataName']].at[a_data.Index, 'size'] = (
                    int(account_size[0] * (3 / 13)),
                    int(sgv_vis['one_bank_BalanceSheet_height'] * ((a_data_value if not np.isnan(a_data_value) else 0) / sgv_vis['max_BB_value_in_all_panel']))
                )
                if a_data.data_type[-2:] == '_t':
                    row['offsetScale_by_dataType'] = 1 / 13
                elif a_data.data_type[-2:] == '_s':
                    row['offsetScale_by_dataType'] = 9 / 13
                    pass  # if
                dict_vis_data[row['df_dataName']].at[a_data.Index, 'position'] = (
                    account_position[0] + int(account_size[0] * row['offsetScale_by_dataType']),
                    account_position[1] + int(account_size[1] - dict_vis_data[row['df_dataName']].loc[a_data.Index, 'size'][1])
                )  # 笔尖起始坐标之新柱子之开始位置。该坐标值应该与资产负债表之关联的科目之 y 坐标值下对齐。
                pass  # for
            pass  # for
        pass  # if

    # 如果是单侧 2 列的资产负债表
    if num_column_one_side == 2:
        ## 计算资产负债表各列各项数据之值、变动值对应的矩形之高亮框
        for account_data in dict_vis_data['accounts'].itertuples():
            dict_vis_data['accounts'].loc[account_data.Index, 'value'] = df_BB.loc[(df_BB[sgv_vis['name_time']] == time) & (df_BB['id_agent'] == id_agent), account_data.subject].values[0]
            value_last = df_BB.loc[(df_BB[sgv_vis['name_time']] == (time - 1 if time != 0 else 0)) & (df_BB['id_agent'] == id_agent), account_data.subject].values[0]
            is_value_changed = False if np.isclose(dict_vis_data['accounts'].loc[account_data.Index, 'value'], value_last, atol=1e0) else True
            if is_value_changed:
                dict_vis_data['accounts'].loc[account_data.Index, 'stroke_color'] = '#000000'
                dict_vis_data['accounts'].loc[account_data.Index, 'stroke_width'] = 2
                pass  # if
            pass  # for

        ## 计算资产负债表各资产负债科目之各项数据对应的矩形之绘制位置、绘制尺寸
        boxs_width = [sgv_vis['one_bank_BalanceSheet_width'] * 8 / 24, sgv_vis['one_bank_BalanceSheet_width'] * 4 / 24, sgv_vis['one_bank_BalanceSheet_width'] * 4 / 24, sgv_vis['one_bank_BalanceSheet_width'] * 8 / 24]  # 设置资产负债表之账户之各侧边柱子之宽度
        nibs_x = [reduce(lambda x, y: x + y, boxs_width[0:i + 1]) - boxs_width[i] for i in range(len(boxs_width))]  # 设置笔尖之x方向的位置之资产负债表之账户之各侧边柱子之起点
        o = [1, 0, 2, 3]  # 设置资产负债表之账户之各侧边柱子之绘制次序
        count_subject_values_is_zero = 0
        items_subject_values_is_zero = []
        nibs_y = [0, 0, 0, 0]  # 列表之笔尖起始坐标之开始位置之y坐标
        p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
        grouped_by_dataType = dict_vis_data['accounts'].groupby('data_type')
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
                    account_idx = dict_vis_data['accounts'].loc[(dict_vis_data['accounts']['data_type'] == data_type) & (dict_vis_data['accounts']['level'] == level) & (dict_vis_data['accounts']['subject'] == subject), 'subject'].idxmax()
                    dict_vis_data['accounts'].at[account_idx, 'position'] = nib
                    # 判断如果有一个数值出现 NaN 则设置其高度为一个很大的数，以便于在绘制时显示异常，从而提示这里有错误
                    if not (np.isnan(subject_values['value'].iloc[0]) or np.isnan(sgv_vis['max_BB_value_in_all_panel'])):
                        height_size = int(sgv_vis['one_bank_BalanceSheet_height'] * (subject_values['value'].iloc[0] / (sgv_vis['max_BB_value_in_all_panel'] if not np.isnan(sgv_vis['max_BB_value_in_all_panel']) else 'NaN')))
                    else:
                        height_size = int(1e6)  # #BUG 最好抛出异常
                        pass  # if
                    dict_vis_data['accounts'].at[account_idx, 'size'] = (
                        int(boxs_width[o[p]]),
                        height_size
                    )

                    # if subject_values['value'].iloc[0]  != 0:
                    if subject_values['value'].iloc[0] != 0 or subject_values['value'].iloc[0] == 0:
                        nib = (
                            sgv_vis['one_bank_BalanceSheet_border'] + int(nibs_x[o[p]]),
                            int(nib[1] + height_size)
                        )  # 笔尖起始坐标之该柱子之下一个项目之柱节之开始位置
                    else:  # 如果柱节高度为0... #HACK #TODO 这个以后再处理
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
        o = [2, 3] if dict_vis_data['accounts'].loc[(dict_vis_data['accounts']['data_type'] == 'equity') & (dict_vis_data['accounts']['level'] == 'level 1') & (dict_vis_data['accounts']['subject'] == 'E_all'), 'value'].iloc[0] >= 0 else [1, 0]  # 设置资产负债表之账户之各侧边柱子之绘制次序
        p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
        grouped_by_dataType = dict_vis_data['accounts'].groupby('data_type')
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
                    account_idx = dict_vis_data['accounts'].loc[(dict_vis_data['accounts']['data_type'] == data_type) & (dict_vis_data['accounts']['level'] == level) & (dict_vis_data['accounts']['subject'] == subject), 'subject'].idxmax()
                    # 判断如果有一个数值出现 NaN 则设置其高度为一个很大的数，以便于在绘制时显示异常，从而提示这里有错误
                    if not (np.isnan(subject_values['value'].iloc[0]) or np.isnan(sgv_vis['max_BB_value_in_all_panel'])):
                        height_size = int(sgv_vis['one_bank_BalanceSheet_height'] * (subject_values['value'].iloc[0] / (sgv_vis['max_BB_value_in_all_panel'] if not np.isnan(sgv_vis['max_BB_value_in_all_panel']) else 'NaN')))
                    else:
                        height_size = int(1e6)
                        pass  # if
                    dict_vis_data['accounts'].at[account_idx, 'size'] = (
                        int(boxs_width[o[p]]),
                        height_size
                    )
                    dict_vis_data['accounts'].at[account_idx, 'position'] = nib
                    dict_vis_data['accounts'].at[account_idx, 'fill_color'] = subject_values['fill_color'].iloc[0] if subject_values['value'].iloc[0] >= 0 else '#FFFFFF'  # 如果 equity 是负数则更改其柱子之填充颜色

                    # if subject_values['value'].iloc[0]  != 0:
                    if subject_values['value'].iloc[0] != 0 or subject_values['value'].iloc[0] == 0:
                        pass  # if
                    pass  # for
                p += 1
                pass  # for
            pass  # for

        ## 计算除了资产负债表各科目之外的其他变量之数据之值、变动值对应的矩形之高亮框、绘制位置、绘制尺寸
        df_data_to_vis_other_variables_for_one_bank_accounts = pd.DataFrame(sgv_vis['config_data_to_vis_other_variables_for_one_bank_accounts'])
        for index, row in df_data_to_vis_other_variables_for_one_bank_accounts.iterrows():
            for a_data in dict_vis_data[row['df_dataName']].itertuples():
                a_data_value = df_BB.loc[(df_BB[sgv_vis['name_time']] == time) & (df_BB['id_agent'] == id_agent), a_data.subject].values[0]
                dict_vis_data[row['df_dataName']].loc[a_data.Index, 'value'] = a_data_value
                value_last = df_BB.loc[(df_BB[sgv_vis['name_time']] == (time - 1 if time != 0 else 0)) & (df_BB['id_agent'] == id_agent), a_data.subject].values[0]
                is_value_changed = False if np.isclose(a_data_value, value_last, atol=1e0) else True
                if is_value_changed:
                    dict_vis_data[row['df_dataName']].loc[a_data.Index, 'stroke_color'] = '#000000'
                    dict_vis_data[row['df_dataName']].loc[a_data.Index, 'stroke_width'] = 2
                    pass  # if

                account_idx = dict_vis_data['accounts'].loc[(dict_vis_data['accounts']['data_type'] == a_data.side) & (dict_vis_data['accounts']['level'] == a_data.level) & (dict_vis_data['accounts']['subject'] == a_data.align), 'subject'].idxmax()
                account_position = dict_vis_data['accounts'].loc[account_idx, 'position']
                account_size = dict_vis_data['accounts'].loc[account_idx, 'size']
                dict_vis_data[row['df_dataName']].at[a_data.Index, 'size'] = (
                    int(account_size[0] * (3 / 13)),
                    int(sgv_vis['one_bank_BalanceSheet_height'] * ((a_data_value if not np.isnan(a_data_value) else 0) / sgv_vis['max_BB_value_in_all_panel']))
                )
                if a_data.data_type[-2:] == '_t':
                    row['offsetScale_by_dataType'] = 1 / 13
                elif a_data.data_type[-2:] == '_s':
                    row['offsetScale_by_dataType'] = 9 / 13
                    pass  # if
                dict_vis_data[row['df_dataName']].at[a_data.Index, 'position'] = (
                    account_position[0] + int(account_size[0] * row['offsetScale_by_dataType']),
                    account_position[1] + int(account_size[1] - dict_vis_data[row['df_dataName']].loc[a_data.Index, 'size'][1])
                )  # 笔尖起始坐标之新柱子之开始位置。该坐标值应该与资产负债表之关联的科目之 y 坐标值下对齐。
                pass  # for
            pass  # for
        pass  # if

    ### 银行状态数据
    for state in sgv_vis['set_dataTypes_for_agentsState']:  # 顺序遍历 set_dataTypes_for_agentsState 中的每一个状态，如果该状态能够与 bank_states 中的状态匹配，那么就将该状态的颜色添加到个体颜色列表
        if df_BB[(df_BB[sgv_vis['name_time']] == time) & (df_BB['id_agent'] == id_agent)][state].values[0]:
            bankState_color = sgv_vis['dict_state_colors'][state]
            break

    ## 生成其他信息
    others = dict(
        time_granularity=sgv_vis['time_granularity'],
        bank_name=df_BB[(df_BB[sgv_vis['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['fullName'].values[0],
        process_name=df_BB[df_BB[sgv_vis['name_time']] == time]['process_name'].values[0],
        step=df_BB[df_BB[sgv_vis['name_time']] == time]['step'].values[0],
        turn=df_BB[df_BB[sgv_vis['name_time']] == time]['turn'].values[0],
        phase=df_BB[df_BB[sgv_vis['name_time']] == time]['phase'].values[0],
        bank_sate_color=bankState_color
    )

    data = dict(
        others=others,
    )
    data.update({k: dict_vis_data[k] for k in dict_vis_data.keys()})

    return data
    pass  # function


def draw_one_bank_BalanceSheet(vis_data: dict, sgv_vis: dict, width: int = 600, height: int = 600, title_height: int = 21, border: int = 5):
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
    if vis_data['others']['time_granularity'] == '步进粒度':
        dw_text = rf"{vis_data['others']['bank_name']}   {vis_data['others']['process_name']}   r={str(vis_data['others']['turn'])}   s={str(vis_data['others']['step'])}   p={str(vis_data['others']['phase'])}"
    elif vis_data['others']['time_granularity'] == '轮次粒度':
        dw_text = rf"{vis_data['others']['bank_name']}   {vis_data['others']['process_name']}   r={str(vis_data['others']['turn'])}"  # DEBUG 未测试
    else:
        raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
        pass  # if

    # 计算文本的宽度和高度
    text_width = len(dw_text) * 8  # 假设每个字符的宽度为16
    text_height = 16  # 字体大小为16

    # 绘制文字背景颜色矩形
    svg_balanceSheet.append(
        dw.Rectangle(
            x=width // 2 - text_width // 2,
            y=border + title_height // 2 - text_height,
            width=text_width,
            height=text_height,
            fill=vis_data['others']['bank_sate_color'],
        )
    )
    svg_balanceSheet.append(
        dw.Text(
            dw_text,
            font_size=text_height,
            x=width // 2,
            y=border + title_height // 2,
            text_anchor='middle',
            dominant_baseline='middle',
            font_family=sgv_vis['zh_font_family'],
            # fill=vis_data['others']['bank_sate_color'],  # 添加文本颜色
        )
    )

    ## 绘制资产负债表各列各项之矩形
    for account_data in vis_data['accounts'].itertuples():
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

    ## 绘制资产负债表其它各变量之各列各项之矩形
    df_data_to_vis_other_variables_for_one_bank_accounts = pd.DataFrame(sgv_vis['config_data_to_vis_other_variables_for_one_bank_accounts'])
    for bank_BalanceSheet_other_data in [vis_data[name] for name in sgv_vis['config_data_to_vis_other_variables_for_one_bank_accounts']['df_dataName']]:
        for one_rect_data in bank_BalanceSheet_other_data.itertuples():
            if np.isnan(one_rect_data.value) or one_rect_data.value != 0:  # 如果值为 NaN 或者 0，则不绘制
                svg_balanceSheet.append(
                    dw.Rectangle(
                        x=one_rect_data.position[0],
                        y=one_rect_data.position[1],
                        width=one_rect_data.size[0],
                        height=one_rect_data.size[1],
                        fill=one_rect_data.fill_color,
                        fill_opacity=1.0,
                        stroke=one_rect_data.stroke_color,
                        stroke_width=one_rect_data.stroke_width,
                    )
                )
                pass  # if
            pass  # for
        pass  # for

    ## 绘制资产负债表各列各项之文本
    for account_data in vis_data['accounts'].itertuples():
        if np.isnan(account_data.value):  # 如果值为 NaN ，则标记 NaN，字颜色黑色，底色红色
            svg_balanceSheet.append(
                dw.Text(
                    account_data.subject + '\n' + 'NaN',
                    font_size=18,
                    x=account_data.position[0] + account_data.size[0] // 2,
                    y=account_data.position[1] + account_data.size[1] // 2,
                    fill='red',
                    stroke='black',
                    stroke_width=0.5,
                    background='red',
                    text_anchor='middle',
                    dominant_baseline='middle',
                    font_family=sgv_vis['en_font_family'],
                )
            )
        elif account_data.value != 0:  # 如果值不为0，则绘制
            svg_balanceSheet.append(
                dw.Text(
                    account_data.subject + '\n' + str(round(account_data.value)),
                    font_size=18,
                    x=account_data.position[0] + account_data.size[0] // 2,
                    y=account_data.position[1] + account_data.size[1] // 2,
                    stroke='none',
                    stroke_width=0.0,
                    text_anchor='middle',
                    dominant_baseline='middle',
                    font_family=sgv_vis['en_font_family'],
                )
            )
            pass  # if
        pass  # for

    for i, bank_BalanceSheet_other_data in enumerate([vis_data[name] for name in sgv_vis['config_data_to_vis_other_variables_for_one_bank_accounts']['df_dataName']]):
        for one_text_data in bank_BalanceSheet_other_data.itertuples():
            if np.isnan(one_text_data.value):  # 如果值为 NaN ，则标记 NaN，字颜色黑色，底色红色
                svg_balanceSheet.append(
                    dw.Text(
                        one_text_data.subject + '\n' + 'NaN',
                        font_size=18,
                        x=one_text_data.position[0] + one_text_data.size[0] // 2,
                        y=one_text_data.position[1] + one_text_data.size[1] // 2,
                        fill='red',
                        stroke='black',
                        stroke_width=0.5,
                        background='red',
                        text_anchor='middle',
                        dominant_baseline='middle',
                        font_family=sgv_vis['en_font_family'],
                    )
                )
            elif one_text_data.value != 0:  # 如果值不为0，则绘制
                svg_balanceSheet.append(
                    dw.Text(
                        one_text_data.subject + '\n' + str(round(one_text_data.value)),
                        font_size=18,
                        x=one_text_data.position[0] + one_text_data.size[0] // sgv_vis['config_data_to_vis_other_variables_for_one_bank_accounts']['text_offsetScale_x'][i],
                        y=one_text_data.position[1] + one_text_data.size[1] // sgv_vis['config_data_to_vis_other_variables_for_one_bank_accounts']['text_offsetScale_y'][i],
                        fill=sgv_vis['config_data_to_vis_other_variables_for_one_bank_accounts']['text_fill'][i],
                        stroke='black',
                        stroke_width=0.5,
                        # background='white',
                        text_anchor='middle',
                        dominant_baseline='middle',
                        font_family=sgv_vis['en_font_family'],
                    )
                )
                pass  # if
            pass  # for
        pass  # for

    return svg_balanceSheet
    pass  # function


def merged_and_bind_figs_to_a_pdf_file(order_of_variable_mean_in_horizontal_and_vertical_direction: tuple, order_of_paging_in_horizontal_and_vertical_direction: tuple, order_of_match_pattern_in_horizontal_and_vertical_direction: tuple, list_fig_files: list, i_exp: int):
    """
    将多个图像拼接、分页到一个 PDF 文件中。

    Args:
        order_of_variable_mean_in_horizontal_and_vertical_direction (tuple): 横向与纵向的变量含义之顺序
        order_of_paging_in_horizontal_and_vertical_direction (tuple): 横向与纵向的分页顺序
        order_of_match_pattern_in_horizontal_and_vertical_direction (tuple): 横向与纵向的匹配文本之顺序
        list_fig_files (list): 图像文件列表
        i_exp (int): 实验索引

    Returns:
        merged_pdf_file: 合并之后的 PDF 文件

    """

    ## 声明与定义变量
    num_figure_in_horizontal_direction: Optional[int] = None  # 横向的图片数量
    num_figure_in_vertical_direction: Optional[int] = None  # 纵向的图片数量
    max_num_of_figures_in_horizontal_direction_per_page: Optional[int] = None  # 每页横向的最大图片数量
    max_num_of_figures_in_vertical_direction_per_page: Optional[int] = None  # 每页纵向的最大图片数量
    match_pattern_in_vertical_direction: Optional[str] = None  # 纵向需要匹配的文本
    match_pattern_in_horizontal_direction: Optional[str] = None  # 横向需要匹配的文本
    num_figure_in_horizontal_direction_per_page: Optional[int] = None  # 每页之横向之图片数量
    num_figure_in_vertical_direction_per_page: Optional[int] = None  # 每页之纵向之图片数量
    num_figure_in_paging_direction: Optional[int] = None  # 分页方向之图片数量
    num_figure_in_no_paging_direction: Optional[int] = None  # 不分页方向之图片数量
    max_num_of_figures_in_paging_direction_per_page: Optional[int] = None  # 每页之分页方向之最大图片数量
    max_num_of_figures_in_no_paging_direction_per_page: Optional[int] = None  # 每页之不分页方向之最大图片数量
    match_pattern_in_paging_direction: Optional[str] = None  # 分页方向需要匹配的文本
    match_pattern_in_no_paging_direction: Optional[str] = None  # 不分页方向需要匹配的文本
    num_figure_in_paging_direction_per_page: Optional[int] = None  # 每页之分页方向之图片数量
    num_figure_in_no_paging_direction_per_page: Optional[int] = None  # 每页之不分页方向之图片数量
    single_plot_size_width: Optional[float] = None  # 单个图之宽度
    single_plot_size_height: Optional[float] = None  # 单个图之高度
    single_plot_size_in_paging_direction: Optional[float] = None  # 单个图之在分页方向之尺寸
    single_plot_size_in_no_paging_direction: Optional[float] = None  # 单个图之在不分页方向之尺寸

    ## 赋值设置项
    num_figure_in_horizontal_direction, num_figure_in_vertical_direction = order_of_variable_mean_in_horizontal_and_vertical_direction[0], order_of_variable_mean_in_horizontal_and_vertical_direction[1]
    max_num_of_figures_in_horizontal_direction_per_page, max_num_of_figures_in_vertical_direction_per_page = order_of_paging_in_horizontal_and_vertical_direction[0], order_of_paging_in_horizontal_and_vertical_direction[1]  # `None`表示不限制。
    match_pattern_in_horizontal_direction, match_pattern_in_vertical_direction = order_of_match_pattern_in_horizontal_and_vertical_direction[0], order_of_match_pattern_in_horizontal_and_vertical_direction[1]

    ## 计算相关的变量
    # 根据文件类型，获取相关的变量
    if Path(list_fig_files[0]).suffix == '.pdf':
        original_file_suffix = 'pdf'
    elif Path(list_fig_files[0]).suffix == '.svg':
        original_file_suffix = 'svg'
    else:
        raise ValueError('不支持的文件类型！')
        pass  # if

    if original_file_suffix == 'pdf':
        single_plot_pdf = fitz.open(list_fig_files[0])
        single_plot_size_width = single_plot_pdf.load_page(0).rect[2]  # 获取单个图的尺寸（这里所有图的尺寸都是一样的）
        single_plot_size_height = single_plot_pdf.load_page(0).rect[3]
        single_plot_pdf.close()
    elif original_file_suffix == 'svg':
        single_plot_size_width = svg2rlg(list_fig_files[0]).width  # 获取单个图的尺寸（这里所有图的尺寸都是一样的）
        single_plot_size_height = svg2rlg(list_fig_files[0]).height
        pass  # if

    ## 判断分页的方向
    if max_num_of_figures_in_horizontal_direction_per_page is not None and max_num_of_figures_in_vertical_direction_per_page is None:
        paging_direction = 'horizontal'
    elif max_num_of_figures_in_vertical_direction_per_page is not None and max_num_of_figures_in_horizontal_direction_per_page is None:
        paging_direction = 'vertical'
    elif max_num_of_figures_in_vertical_direction_per_page is not None and max_num_of_figures_in_horizontal_direction_per_page is not None:
        paging_direction = 'none'
    else:
        raise ValueError('不可以双向都分页！')
        pass  # if

    ## 根据分页的方向，赋值分页与不分页方向之相关变量
    if paging_direction == 'horizontal':
        num_figure_in_paging_direction = num_figure_in_horizontal_direction
        num_figure_in_no_paging_direction = num_figure_in_vertical_direction
        max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
        max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
        match_pattern_in_paging_direction = match_pattern_in_horizontal_direction
        match_pattern_in_no_paging_direction = match_pattern_in_vertical_direction
        single_plot_size_in_paging_direction = single_plot_size_width
        single_plot_size_in_no_paging_direction = single_plot_size_height
        num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
        num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
        num_figure_in_horizontal_direction_per_page = num_figure_in_paging_direction_per_page
        num_figure_in_vertical_direction_per_page = num_figure_in_no_paging_direction_per_page
    elif paging_direction == 'vertical':
        num_figure_in_paging_direction = num_figure_in_vertical_direction
        num_figure_in_no_paging_direction = num_figure_in_horizontal_direction
        max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
        max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
        match_pattern_in_paging_direction = match_pattern_in_vertical_direction
        match_pattern_in_no_paging_direction = match_pattern_in_horizontal_direction
        single_plot_size_in_paging_direction = single_plot_size_height
        single_plot_size_in_no_paging_direction = single_plot_size_width
        num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
        num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
        num_figure_in_horizontal_direction_per_page = num_figure_in_no_paging_direction_per_page
        num_figure_in_vertical_direction_per_page = num_figure_in_paging_direction_per_page
    elif paging_direction == 'none':  # 如果不分页，那么默认按照纵向分页的情况处理
        num_figure_in_paging_direction = num_figure_in_vertical_direction
        num_figure_in_no_paging_direction = num_figure_in_horizontal_direction
        max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
        max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
        match_pattern_in_paging_direction = match_pattern_in_vertical_direction
        match_pattern_in_no_paging_direction = match_pattern_in_horizontal_direction
        single_plot_size_in_paging_direction = single_plot_size_height
        single_plot_size_in_no_paging_direction = single_plot_size_width
        num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
        num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
        num_figure_in_horizontal_direction_per_page = num_figure_in_no_paging_direction_per_page
        num_figure_in_vertical_direction_per_page = num_figure_in_paging_direction_per_page
        pass  # if

    total_figures_per_page = num_figure_in_horizontal_direction_per_page * num_figure_in_vertical_direction_per_page  # 每页最大总图数
    num_pages = int(np.ceil(len(list_fig_files) / total_figures_per_page))  # 最大总页数

    ## 排序，优先按照需要分页的方向，其次按照不需要分页的方向。 #BUG 按照 data 排序的时候有时候可能出现个别乱序现象
    sorted_pkl_panel_file_list = sorted(list_fig_files, key=lambda name: (
        re.search(match_pattern_in_paging_direction, name)[0] if not re.search(match_pattern_in_paging_direction, name)[0].isdigit() else int(re.search(match_pattern_in_paging_direction, name)[0]),
        re.search(match_pattern_in_no_paging_direction, name)[0] if not re.search(match_pattern_in_no_paging_direction, name)[0].isdigit() else int(re.search(match_pattern_in_no_paging_direction, name)[0]),
    ))

    ## 分页处理
    merged_pdf = fitz.open()  # 新建需要合并的pdf
    for page_idx in range(num_pages):

        ## 创建一个新的分页
        merged_pdf_page = merged_pdf.new_page(
            # -1, # 这里不需要指定页码，fitz会自动分配
            width=single_plot_size_width * num_figure_in_horizontal_direction_per_page,
            height=single_plot_size_height * num_figure_in_vertical_direction_per_page,
        )

        ## 对于该新的分页，逐个导入单幅pdf，临时装订pdf
        binded_pdf = fitz.open()  # 创建一个空白pdf用于装订单幅pdf
        for i in range(total_figures_per_page):
            idx = page_idx * total_figures_per_page + i
            if idx >= len(list_fig_files):
                break
            filepath = sorted_pkl_panel_file_list[idx]
            if original_file_suffix == 'svg':
                svg_file = svg2rlg(filepath)
                renderPDF.drawToFile(svg_file, filepath.split('.')[0] + '.pdf')
                single_pdf_file = fitz.open(filepath.split('.')[0] + '.pdf')
            elif original_file_suffix == 'pdf':
                single_pdf_file = fitz.open(filepath)
                pass  # if
            binded_pdf.insert_pdf(single_pdf_file)
            single_pdf_file.close()
            pass  # for

        ## 设置装订的pdf之每个图在该新的分页之位置
        adjasted_page_content_positions = []
        for i in range(num_figure_in_paging_direction_per_page):
            if (
                    paging_direction != 'none'  # 如果是存在分页的情况
                    and page_idx == num_pages - 1  # 如果是最后一页
                    and num_figure_in_paging_direction % num_figure_in_paging_direction_per_page != 0  # 如果最后一页不是满页的情况
                    and i >= num_figure_in_paging_direction % num_figure_in_paging_direction_per_page  # 如果该索引处于空行或者空列
            ):
                break  # 需要分页方向跳过最后一页的空行或者空列
                pass  # if
            for j in range(num_figure_in_no_paging_direction_per_page):
                if paging_direction == 'horizontal':
                    adjasted_page_content_positions.append(
                        fitz.Rect(single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * (i + 1), single_plot_size_in_no_paging_direction * (j + 1))
                    )
                elif paging_direction == 'vertical':
                    adjasted_page_content_positions.append(
                        fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                    )
                elif paging_direction == 'none':
                    adjasted_page_content_positions.append(
                        fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                    )
                    pass  # if
                pass  # for
            pass  # for

        ## 将装订的pdf之每个图放到该新的分页之对应的位置
        for i_fig, page in enumerate(binded_pdf):
            merged_pdf_page.show_pdf_page(adjasted_page_content_positions[i_fig], binded_pdf, page.number)
            pass  # for

        pass  # for

    binded_pdf.close()

    ## 自适应换行
    ## 如果分页的方向是分为每页仅仅是 1 行的情况下，考虑将每一页仅有一行的所有图像自适应换行，此时设定每一行 3 个图像。这样做的目的是防止拼接的每一页的图像显得过于狭长。
    if num_figure_in_paging_direction_per_page == 1:
        is_adjast_horizontal_direction = True
        ### 获取当前显示器长宽比。根据总的图片数，分配与长宽比最接近的每行、每列图片数
        from screeninfo import get_monitors
        import math
        monitor = get_monitors()[0]
        width = monitor.width
        height = monitor.height
        aspect_ratio = width / height
        max_num_figure_for_adjast_in_vertical_direction_per_page = max_num_figure_for_adjast_in_horizontal_direction_per_page = math.floor(math.sqrt(total_figures_per_page))
        while max_num_figure_for_adjast_in_horizontal_direction_per_page * max_num_figure_for_adjast_in_vertical_direction_per_page < total_figures_per_page:
            if max_num_figure_for_adjast_in_horizontal_direction_per_page / max_num_figure_for_adjast_in_vertical_direction_per_page > aspect_ratio:
                max_num_figure_for_adjast_in_vertical_direction_per_page += 1
            else:
                max_num_figure_for_adjast_in_horizontal_direction_per_page += 1
                pass  # if
            pass  # while

        num_figure_for_adjast_in_horizontal_direction_per_page = min(max_num_figure_for_adjast_in_horizontal_direction_per_page, num_figure_in_no_paging_direction_per_page)  # 计算自适应调整之后分页的那一个方向的图片数
        num_figure_for_adjast_in_vertical_direction_per_page = int(np.ceil(total_figures_per_page / num_figure_for_adjast_in_horizontal_direction_per_page))  # 计算自适应调整之后不分页的那一个方向的一个页面的图片数
    else:
        is_adjast_horizontal_direction = False
        pass  # if

    if is_adjast_horizontal_direction:  # 创建一个新的自适应分行的 adjasted_pdf
        adjasted_pdf = fitz.open()
        adjasted_page_content_positions = []  # 设置自适应分行的pdf之每个图在该新的分页之位置
        for i in range(num_figure_for_adjast_in_vertical_direction_per_page):
            for j in range(num_figure_for_adjast_in_horizontal_direction_per_page):
                adjasted_page_content_positions.append(
                    fitz.Rect(single_plot_size_width * j, single_plot_size_height * i, single_plot_size_width * (j + 1), single_plot_size_height * (i + 1))
                )
                pass  # for
            pass  # for
        merged_page_content_positions = []  # 设置对应的源pdf之每个图在该新的分页之位置
        for i in range(num_figure_in_paging_direction_per_page):
            for j in range(num_figure_in_no_paging_direction_per_page):
                merged_page_content_positions.append(
                    fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                )
                pass  # for
            pass  # for
        for i_page, page in enumerate(merged_pdf):  # 遍历merged_pdf中的每一页
            adjasted_pdf_page = adjasted_pdf.new_page(
                # -1, # 这里不需要指定页码，fitz会自动分配
                width=single_plot_size_width * num_figure_for_adjast_in_horizontal_direction_per_page,
                height=single_plot_size_height * num_figure_for_adjast_in_vertical_direction_per_page,
            )

            for i_fig in range(total_figures_per_page):  # 将装订的pdf之每个图放到该新的分页之对应的位置
                adjasted_pdf_page.show_pdf_page(adjasted_page_content_positions[i_fig], merged_pdf, i_page, clip=merged_page_content_positions[i_fig])
                pass  # for

            pass  # for

        return adjasted_pdf
        pass  # if

    return merged_pdf

    pass  # function
