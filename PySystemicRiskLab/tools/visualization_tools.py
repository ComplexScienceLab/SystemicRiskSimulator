"函数区：可视化工具集"

from PySystemicRiskLab import dw, pd, ig, np, plt, reduce
from PySystemicRiskLab.tools.tools import Tools


def get_graph_data_info(time: int, df_BB: pd.DataFrame, df_IB: pd.DataFrame, env: dict):
    """
    获取网络图数据信息。

    Args:
        time (int): 时间
        df_BB (pd.DataFrame): 银行数据框
        df_IB (pd.DataFrame): 银行间数据框
        env (dict): 环境变量集
        
    Returns:
        data 字典格式的数据集

    """

    ## 获取相关的节点与边信息
    data = {}  # 待使用的图数据

    data['banks_name'] = list(df_BB[df_BB[env['name_time']] == time]['name'])  # 银行名称
    data['bank_id'] = list(df_BB[df_BB[env['name_time']] == time]['id_agent'])  # 银行id
    data['process_name'] = list(df_BB[df_BB[env['name_time']] == time]['process_name'])
    data['round'] = list(df_BB[df_BB[env['name_time']] == time]['round'])
    data['phase'] = list(df_BB[df_BB[env['name_time']] == time]['phase'])

    data['vertices'] = list(df_BB[df_BB[env['name_time']] == time]['id_agent'])  # 节点

    # 银行状态
    bank_hel = df_BB[df_BB[env['name_time']] == time]['hel'].tolist()
    bank_isv = df_BB[df_BB[env['name_time']] == time]['isv'].tolist()
    bank_ilq = df_BB[df_BB[env['name_time']] == time]['ilq'].tolist()
    # bank_nrr = df_BB[df_BB[env['name_time']] == time]['-rr'].tolist()  #TODO 后续添加新状态
    bank_br = df_BB[df_BB[env['name_time']] == time]['br'].tolist()
    bank_off = df_BB[df_BB[env['name_time']] == time]['off'].tolist()

    data['banks_state'] = []  # 银行状态
    for i in range(len(data['vertices'])):
        data['banks_state'].append(set())
        if bank_hel[i]:
            data['banks_state'][i].add('hel')
        elif bank_off[i]:
            data['banks_state'][i].add('off')
        elif bank_isv[i]:
            data['banks_state'][i].add('isv')
        elif bank_ilq[i]:
            data['banks_state'][i].add('ilq')
        elif bank_br[i]:
            data['banks_state'][i].add('br')
        else:
            print('位于节点' + str(i))
            raise Exception("判断 i 之状态错误".format(str(i)))
            pass  # for

    # data['edge_data_idx'] = df_IB[df_IB[env['name_time']] == time][df_IB[df_IB[env['name_time']] == time]['data['edges_data_value']'] > 0].index.tolist()  # 相关的索引
    data['edges_data_idx'] = (df_IB[(df_IB[env['name_time']] == time) & (df_IB[env['data_name']] > 0)]['id_agent'].values).tolist()  # 相关的边索引
    # edges = [list(zip(df_IB[df_IB[env['name_time']] == time]['row'] - 1, df_IB[df_IB[env['name_time']] == time]['col'] - 1))[j - time * num_items_in_a_time_in_IB] for j in data['edge_data_idx']]  # 相关的边索引（银行编号从0开始计数的）
    data['edges'] = [list(zip(df_IB[df_IB[env['name_time']] == time]['row'] - 1, df_IB[df_IB[env['name_time']] == time]['col'] - 1))[j] for j in data['edges_data_idx']]  # 相关的边的索引，以两点索引表示（银行编号从0开始计数的）
    data['vertices_data_value'] = df_BB[df_BB[env['name_time']] == time][(env['data_name'] + '_all')].tolist()  # 相关的点之值
    data['vertices_size'] = list(np.sqrt(np.asarray( #BUG 在Win系统运行警告：RuntimeWarning: invalid value encountered in sqrt
        Tools.MinMaxScaler(
            df_BB[df_BB[env['name_time']] == time][(env['data_name'] + '_all')],
            (
                0.1 * min(df_BB[df_BB[env['name_time']] == time][(env['data_name'] + '_all')]) / env['min_value_BB'],
                1.0 * max(df_BB[df_BB[env['name_time']] == time][(env['data_name'] + '_all')]) / env['max_value_BB']
            )
        )
    )))  # 节点尺寸
    data['edges_data_value'] = df_IB[(df_IB[env['name_time']] == time) & (df_IB[env['data_name']] > 0)][env['data_name']].values.tolist()  # 相关的边之值
    data['edges_width'] = Tools.MinMaxScaler(
        data['edges_data_value'],
        (
            0.5 * (min(df_IB[df_IB[env['name_time']] == time][env['data_name']]) + 0.01) / (env['min_value_IB'] + 0.01),
            5 * (min(df_IB[df_IB[env['name_time']] == time][env['data_name']]) + 0.01) / (env['min_value_IB'] + 0.01)
        )
    )  # 边的宽度

    state_colors = {
        'hel': '#F1D0CB',  # 浅红色
        'isv': '#D9E8D6',  # 浅绿色
        'ilq': '#DDE8FA',  # 浅蓝色
        'ilq,isv': '#DFD6E6',  # 浅紫色
        # '-rr': '#FDF3D0',  # 浅黄色 #TODO 后续添加新状态
        'br': '#CCCCCC',  # 灰色
        'off': '#999999',  # 深灰色
    }

    ## 设置各节点之状态之颜色
    # for i in data['banks_state']:
    data['vertices_color'] = [state_colors[','.join(s)] for s in data['banks_state']]

    ## 设置各节点之标签
    data['vertices_label'] = [data['banks_name'][i] + '\n' + str(round(data['vertices_data_value'][i])) for i in data['vertices']]

    return data
    pass  # def


def draw_interbank_flow_graph(data: dict, env: dict):
    """
    绘制单独的银行间资金网络图

    Args:
        data (dict): 网络流数据集
        env (dict): 环境变量集

    Returns:
        fig matplotlib格式的图像对象

    """
    ## 创建图对象
    g = ig.Graph(
        directed=True,
    )

    ## 绘制标题
    if env['time_granularity'] == '步进粒度':
        dw_text = rf"{env['data_name']}    {env['process_name']}    s = {str(env['step'])}    r = {str(env['round'])}    p = {str(env['phase'])}"
    elif env['time_granularity'] == '轮次粒度':
        dw_text = rf"{env['data_name']}    {env['process_name']}    r = {str(env['round'])}"  # TODO 未测试
    else:
        raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
        pass  # if

    ## 添加节点和边
    g.add_vertices(data['vertices'])
    g.add_edges(data['edges'])

    ## 设置图之顶点与边之数值
    g.vs['name'] = data['banks_name']
    g.vs['health_state'] = data['banks_state']
    g.vs[(env['data_name'] + '_all')] = data['vertices_data_value']
    g.es[env['data_name']] = data['edges_data_value']
    # del g.es['A_IB']

    ## 设置图之属性
    g.vs['label'] = data['vertices_label']
    g.vs['color'] = data['vertices_color']
    g.es['color'] = '#CCCCCC'
    g.vs['size'] = data['vertices_size']
    g.es['label'] = [round(i) for i in g.es[env['data_name']]]
    g.es['width'] = data['edges_width']

    ## 生成可视化图
    fig, ax = plt.subplots(
        figsize=(5, 5),
        dpi=400,
    )
    fig.suptitle(dw_text)
    ax.set_title = data['banks_name']
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
        vertex_label_size=4,
        # vertex_frame_color='red',
        vertex_frame_width=0.0,
        edge_label=g.es['label'],
        edge_align_label=True,
        edge_label_dist=100,
        # edge_color='#7F7F7F',
        edge_background=None,
        edge_font=1,
        edge_label_size=4,
    )

    # plt.show()  # 显示图像
    # plt.close()  # 关闭图像

    return fig
    pass  # def


def get_one_bank_accounts_data(df_BB: pd.DataFrame, time: int, id_agent: int, env: dict):
    """
    生成资产负债表账户数据（嵌套字典形式）
    Args:
        df_BB (pd.DataFrame): 数据框
        time (int): 时间
        id_agent (int): 银行个体id
        env (dict): 环境变量集

    Returns:
         accounts_data 资产负债表账户数据（嵌套字典形式）

    """

    accounts = {
        'asset': {
            'level 3': {
                'A_P': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['A_P'].values[0],
                    'color': '#FBE7CF',
                },
                'A_Q': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['A_Q'].values[0],
                    'color': '#DDE8FA',
                },
                'A_R': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['A_R'].values[0],
                    'color': '#DFC942',
                },
                'A_other': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['A_other'].values[0],
                    'color': '#FFFFFF',
                },
                'A_IB_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['A_IB_all'].values[0],
                    'color': '#F1D0CD',
                },
            },
            'level 2': {
                'A_exIB': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['A_exIB'].values[0],
                    'color': '#F9F7EE',
                },
                'A_IB_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['A_IB_all'].values[0],
                    'color': '#F1D0CD',
                },
            },
            'level 1': {
                'A_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['A_all'].values[0],
                    'color': '#EEEEEE',
                },
            },
        },
        'liability': {
            'level 3': {
                'Z_D': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['Z_D'].values[0],
                    'color': '#DFD6E6',
                },
                'Z_IB_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['Z_IB_all'].values[0],
                    'color': '#D9E8D6',
                },
            },
            'level 2': {
                'Z_exIB': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['Z_exIB'].values[0],
                    'color': '#DFD6E6',
                },
                'Z_IB_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['Z_IB_all'].values[0],
                    'color': '#D9E8D6',
                },
            },
            'level 1': {
                'Z_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['Z_all'].values[0],
                    'color': '#EEEEEE',
                },
            },
        },
        'equity': {
            'level 3': {
                'E_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['E_all'].values[0],
                    'color': '#FFFF98',
                },
            },
            'level 2': {
                'E_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['E_all'].values[0],
                    'color': '#FFFF98',
                },
            },
            'level 1': {
                'E_all': {
                    'value': df_BB[(df_BB[env['name_time']] == time) & (df_BB['id_agent'] == id_agent)]['E_all'].values[0],
                    'color': '#FFFF98',
                },
            },
        },
    }
    return accounts
    pass  # def


## 绘制单个银行资产负债表
def draw_one_bank_BalanceSheet(accounts_data: dict, env: dict, width: int = 600, height: int = 600, title_height: int = 15, border: int = 5):
    """
    绘制单个银行资产负债表
    Args:
        accounts_data (dict): 资产项目相关的数据
        env (dict): 相关的一些参数数据（不含资产项目相关的数据）
        width (int): 资产负债表宽度
        height (int): 资产负债表高度
        title_height (int): 标题高度
        border (int): 边框边距

    Returns:
        balanceSheet_svg 单个银行的资产负债表svg格式数据

    """

    balanceSheet_svg = dw.Drawing(border + width + border, border + title_height + height + border, id_prefix='Balance Sheet')

    ## 绘制画布方框
    balanceSheet_svg.append(
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

    # ## 绘制有效方框 #NOTE建议仅在调试使用
    # balanceSheet_svg.append(
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
    if env['time_granularity'] == '步进粒度':
        dw_text = rf"{env['bank_name']}    {env['process_name']}    s = {str(env['step'])}    r = {str(env['round'])}    p = {str(env['phase'])}"
    elif env['time_granularity'] == '轮次粒度':
        dw_text = rf"{env['bank_name']}    {env['process_name']}    r = {str(env['round'])}"  # TODO 未测试
    else:
        raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
        pass  # if

    balanceSheet_svg.append(
        dw.Text(
            dw_text,
            font_size=12,
            x=width // 2,
            y=border + title_height // 2,
            text_anchor='middle',
            dominant_baseline='middle',
            font_family=env['en_font_family'],
        )
    )

    ## 资产负债表各列各项
    boxs_width = [width * 5 / 24, width * 4 / 24, width * 3 / 24, width * 3 / 24, width * 4 / 24, width * 5 / 24]  # 设置资产负债表之账户之各侧边柱子之宽度
    nibs_x = [reduce(lambda x, y: x + y, boxs_width[0:i + 1]) - boxs_width[i] for i in range(len(boxs_width))]  # 设置笔尖之x方向的位置之资产负债表之账户之各侧边柱子之起点
    o = [0, 1, 2, 5, 4, 3]  # 设置资产负债表之账户之各侧边柱子之绘制次序
    nibs_y = [0, 0, 0, 0, 0, 0]  # 列表之笔尖起始坐标之开始位置之y坐标
    p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
    for accounts_type in list(accounts_data.keys())[:-1]:
        for level in accounts_data[accounts_type]:
            nib = (border + nibs_x[o[p]], border + title_height)  # 笔尖起始坐标之新柱子之开始位置
            count_balance_is_zero = 0
            items_balance_is_zero = []
            for name, balance in accounts_data[accounts_type][level].items():
                if balance['value'] != 0:
                    ## 绘制单个项目对应的矩形
                    balanceSheet_svg.append(
                        dw.Rectangle(
                            x=nib[0],
                            y=nib[1],
                            width=boxs_width[o[p]],
                            height=int(height * (balance['value'] / env['max_value_BB'])),
                            fill=balance['color'],
                            fill_opacity=1.0,
                            stroke='rgb(50%,50%,50%)',
                            stroke_width=2,
                        )
                    )
                    ## 绘制单个项目对应的文本标签
                    balanceSheet_svg.append(
                        dw.Text(
                            name + '\n' + str(round(balance['value'])),
                            font_size=6,
                            x=nib[0] + boxs_width[o[p]] // 2,
                            y=nib[1] + int(height * (balance['value'] / env['max_value_BB'])) // 2,
                            text_anchor='middle',
                            dominant_baseline='middle',
                            font_family=env['en_font_family'],
                        )
                    )
                    nib = (border + nibs_x[o[p]], int(nib[1] + height * (balance['value'] / env['max_value_BB'])))  # 笔尖起始坐标之该柱子之下一个项目之柱节之开始位置
                else:  # 如果柱节高度为0...
                    count_balance_is_zero += 1
                    items_balance_is_zero.append((name, balance['value'], nib[1]))
                    pass  # if
                for (name, balance['value'], nib_y) in items_balance_is_zero:  # TODO尝试标记那些柱节高度为0的值
                    pass  # for
                pass  # for
            nibs_y[o[p]] = nib[1]
            p += 1
            pass  # for
        pass  # for

    ## 绘制项目equity对应的矩形
    o = [5, 4, 3] if accounts_data['equity']['level 1']['E_all']['value'] >= 0 else [0, 1, 2]  # 设置资产负债表之账户之各侧边柱子之绘制次序
    p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
    for accounts_type in list(accounts_data.keys())[-1:]:
        for level in accounts_data[accounts_type]:
            nib = (border + nibs_x[o[p]], nibs_y[o[p]])  # 笔尖起始坐标之新柱子之开始位置
            count_balance_is_zero = 0
            items_balance_is_zero = []
            s = 1  # 资产负债表值账户之各侧边柱子之各柱节之绘制索引
            for name, balance in accounts_data[accounts_type][level].items():
                balance['color'] = balance['color'] if balance['value'] >= 0 else '#FFFFFF'  # 设置资产负债表之账户之各侧边柱子之绘制次序
                balanceSheet_svg.append(
                    dw.Rectangle(
                        x=nib[0],
                        y=nib[1],
                        width=boxs_width[o[p]],
                        height=int(height * (abs(balance['value']) / env['max_value_BB'])),
                        fill=balance['color'],
                        fill_opacity=1.0,
                        stroke='rgb(50%,50%,50%)',
                        stroke_width=2,
                    )
                )
                ## 绘制项目equity对应的文本标签
                balanceSheet_svg.append(
                    dw.Text(
                        name + '\n' + str(round(balance['value'])),
                        font_size=6,
                        x=nib[0] + boxs_width[o[p]] // 2,
                        y=nib[1] + int(height * (abs(balance['value']) / env['max_value_BB'])) // 2,
                        text_anchor='middle',
                        dominant_baseline='middle',
                        font_family=env['en_font_family'],
                    )
                )
                pass  # for
            p += 1
            pass  # for
        pass  # for

    return balanceSheet_svg
    pass  # def
