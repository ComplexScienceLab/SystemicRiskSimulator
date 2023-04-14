"函数区：可视化工具集"

from PySystemicRiskLab import dw, pd, ig, np, plt, reduce
from PySystemicRiskLab.tools.tools import Tools


def get_graph_data_info(data_str: str, r: int, df_BB: pd.DataFrame, df_IB: pd.DataFrame):
    """
    获取网络图数据信息
    Args:
        data_str (str): 数据类型
        r (int): 轮次
        df_BB (pd.DataFrame): 银行数据框
        df_IB (pd.DataFrame): 银行间数据框

    Returns: d 字典格式的数据集

    """
    ## 获取相关的节点与边信息
    d = {}  # 待使用的图数据

    d['banks_name'] = list(df_BB[df_BB['round'] == r]['name'])
    d['bank_id'] = list(df_BB[df_BB['round'] == r]['id_agent'])

    d['vertices'] = list(df_BB[df_BB['round'] == r]['id_agent'] - 1)

    bank_hel = df_BB[df_BB['round'] == r]['hel'].tolist()
    bank_isv = df_BB[df_BB['round'] == r]['isv'].tolist()
    bank_ilq = df_BB[df_BB['round'] == r]['ilq'].tolist()
    # bank_nrr = df_BB[df_BB['round'] == r]['-rr'].tolist()  #TODO 后续添加新状态
    bank_br = df_BB[df_BB['round'] == r]['br'].tolist()
    bank_off = df_BB[df_BB['round'] == r]['off'].tolist()

    d['banks_state'] = []  # 银行状态
    for i in range(len(d['vertices'])):
        d['banks_state'].append(set())
        if bank_hel[i]:
            d['banks_state'][i].add('hel')
        elif bank_off[i]:
            d['banks_state'][i].add('off')
        elif bank_isv[i]:
            d['banks_state'][i].add('isv')
        elif bank_ilq[i]:
            d['banks_state'][i].add('ilq')
        elif bank_br[i]:
            d['banks_state'][i].add('br')
        else:
            print('位于节点' + str(i))
            raise Exception("判断 i 之状态错误".format(str(i)))
            pass  # for
    # for i in range(len(d['vertices'])):
    #     if bank_hel[i] == True and bank_isv[i] == False and bank_ilq[i] == False and bank_br[i] == False:
    #         d['banks_state'].append('hel')
    #     elif bank_hel[i] == False and bank_isv[i] == True and bank_ilq[i] == False and bank_br[i] == False:
    #         d['banks_state'].append('isv')
    #     elif bank_hel[i] == False and bank_isv[i] == False and bank_ilq[i] == True and bank_br[i] == False:
    #         d['banks_state'].append('ilq')
    #     elif bank_hel[i] == False and bank_isv[i] == False and bank_ilq[i] == True and bank_br[i] == False:
    #         d['banks_state'].append('ilq')
    #     elif bank_hel[i] == False and bank_isv[i] == False and bank_ilq[i] == False and bank_br[i] == True:
    #         d['banks_state'].append('br')
    #     else:
    #         print(i)
    #         raise Exception("判断 i 之状态错误".format(str(i)))
    #         pass  # for

    # edge_labels = list(zip(A_IB,Z_IB))  # 边之标签值
    # vertex_labels = A_IB_all  # 点之标签值
    # edge_labels = A_IB  # 边之标签值

    # data['edge_data_idx'] = df_IB[df_IB['round'] == r][df_IB[df_IB['round'] == r]['d['edges_data_value']'] > 0].index.tolist()  # 相关的索引
    d['edges_data_idx'] = (df_IB[(df_IB['round'] == r) & (df_IB[data_str] > 0)]['id_agent'].values - 1).tolist()  # 相关的边索引
    # edges = [list(zip(df_IB[df_IB['round'] == r]['row'] - 1, df_IB[df_IB['round'] == r]['col'] - 1))[j - r * num_items_in_a_round_in_IB] for j in data['edge_data_idx']]  # 相关的边索引（银行编号从1开始计数的）
    d['edges'] = [list(zip(df_IB[df_IB['round'] == r]['row'] - 1, df_IB[df_IB['round'] == r]['col'] - 1))[j] for j in d['edges_data_idx']]  # 相关的边的索引，以两点索引表示（银行编号从1开始计数的）
    d['vertices_data_value'] = df_BB[df_BB['round'] == r][(data_str + '_all')].tolist()  # 相关的点之值
    d['vertices_size'] = list(np.sqrt(np.asarray(Tools.MinMaxScaler(df_BB[df_BB['round'] == r][(data_str + '_all')], (0.1, 1)))))
    d['edges_data_value'] = df_IB[(df_IB['round'] == r) & (df_IB[data_str] > 0)][data_str].values.tolist()  # 相关的边之值
    # Z_IB_all = df_BB[df_BB['round'] == r]['Z_IB_all'].tolist()  # 相关的点之值
    # Z_IB = df_IB[(df_IB['round'] == r)&(df_IB['Z_IB'] > 0)].values.tolist()  # 相关的边之值
    # edge_labels = list(zip(d['edges_data_value'],Z_IB))  # 边之标签值
    # vertex_labels = d['vertices_data_value']  # 点之标签值
    # edge_labels = d['edges_data_value']  # 边之标签值

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
    # for i in d['banks_state']:
    d['vertices_color'] = [state_colors[','.join(s)] for s in d['banks_state']]

    ## 设置各节点之标签
    d['vertices_label'] = [d['banks_name'][i] + '\n' + str(round(d['vertices_data_value'][i])) for i in d['vertices']]

    return d
    pass  # def


def draw_interbank_flow_graph(d: dict, data_str: str, r: int, df_BB: pd.DataFrame, df_IB: pd.DataFrame):  # TODO绘制的时候要各时期各银行图形尺寸按比例
    """
    绘制单独的银行间资金网络图

    Args:
        d (dict): 网络流数据集
        data_str (str): 数据类型
        r (int): 轮次
        df_BB (pd.DataFrame): 银行数据框
        df_IB (pd.DataFrame): 银行间数据框

    Returns: fig matplotlib格式的图像对象

    """
    ## 创建图对象
    g = ig.Graph(
        directed=True,
    )

    ## 添加节点和边
    g.add_vertices(d['vertices'])
    g.add_edges(d['edges'])

    ## 设置图之顶点与边之数值
    g.vs['name'] = d['banks_name']
    g.vs['health_state'] = d['banks_state']
    g.vs[(data_str + '_all')] = d['vertices_data_value']
    g.es[data_str] = d['edges_data_value']
    # del g.es['A_IB']

    ## 设置图之属性
    g.vs['label'] = d['vertices_label']
    g.vs['color'] = d['vertices_color']
    g.es['color'] = '#CCCCCC'
    g.vs['size'] = d['vertices_size']
    g.es['label'] = [round(i) for i in g.es[data_str]]
    g.es['width'] = Tools.MinMaxScaler(d['edges_data_value'], (0.5, 3))

    ## 生成可视化图
    fig, ax = plt.subplots(
        figsize=(5, 5),
        dpi=400,
    )
    fig.suptitle(data_str + '    round ' + str(r))
    ax.set_title = d['banks_name']
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

    # 显示图像
    # plt.show()

    return fig
    pass  # def


def get_one_bank_accounts_data(df_BB: pd.DataFrame, round: int, id_agent: int):
    """
    生成资产负债表账户数据（嵌套字典形式）
    Args:
        df_BB (pd.DataFrame): 数据框
        round (int): 轮次
        id_agent (int): 银行个体id

    Returns: accounts 资产负债表账户数据（嵌套字典形式）

    """
    accounts = {
        'asset': {
            'level 3': {
                'A_P': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['A_P'].values[0],
                    'color': '#FBE7CF',
                },
                'A_Q': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['A_Q'].values[0],
                    'color': '#DDE8FA',
                },
                'A_R': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['A_R'].values[0],
                    'color': '#DFC942',
                },
                'A_other': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['A_other'].values[0],
                    'color': '#FFFFFF',
                },
                'A_IB_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['A_IB_all'].values[0],
                    'color': '#F1D0CD',
                },
            },
            'level 2': {
                'A_exIB': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['A_exIB'].values[0],
                    'color': '#F9F7EE',
                },
                'A_IB_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['A_IB_all'].values[0],
                    'color': '#F1D0CD',
                },
            },
            'level 1': {
                'A_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['A_all'].values[0],
                    'color': '#EEEEEE',
                },
            },
        },
        'liability': {
            'level 3': {
                'Z_D': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['Z_D'].values[0],
                    'color': '#DFD6E6',
                },
                'Z_IB_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['Z_IB_all'].values[0],
                    'color': '#D9E8D6',
                },
            },
            'level 2': {
                'Z_exIB': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['Z_exIB'].values[0],
                    'color': '#DFD6E6',
                },
                'Z_IB_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['Z_IB_all'].values[0],
                    'color': '#D9E8D6',
                },
            },
            'level 1': {
                'Z_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['Z_all'].values[0],
                    'color': '#EEEEEE',
                },
            },
        },
        'equity': {
            'level 3': {
                'E_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['E_all'].values[0],
                    'color': '#FFFF98',
                },
            },
            'level 2': {
                'E_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['E_all'].values[0],
                    'color': '#FFFF98',
                },
            },
            'level 1': {
                'E_all': {
                    'value': df_BB[(df_BB['round'] == round) & (df_BB['id_agent'] == id_agent)]['E_all'].values[0],
                    'color': '#FFFF98',
                },
            },
        },
    }
    return accounts
    pass  # def


## 绘制单个银行资产负债表
def draw_one_bank_BalanceSheet(accounts, bank_name, r, max_money: float, width: int = 600, height: int = 600, title_height: int = 15, border: int = 5):
    """
    绘制单个银行资产负债表
    Args:
        accounts (): 资产项目信息
        bank_name (str): 银行名称
        r (int): 轮次
        max_money (float): 总资金
        width (int): 资产负债表宽度
        height (int): 资产负债表高度
        title_height (int): 标题高度
        border (int): 边框边距

    Returns: balanceSheet_svg 单个银行的资产负债表svg格式数据

    """

    balanceSheet_svg = dw.Drawing(border + width + border, border + title_height + height + border, id_prefix='Balance Sheet')

    ## 绘制画布方框 #NOTE建议仅在调试使用
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
    balanceSheet_svg.append(
        dw.Text(
            bank_name + '    round ' + str(r),
            font_size=12,
            x=width // 2,
            y=border + title_height // 2,
            text_anchor='middle',
            dominant_baseline='middle',
            font_family='Times',
        )
    )

    ## 资产负债表各列各项
    # boxs_width = [width / 6, width / 6, width / 6, width / 6, width / 6, width / 6]  # 设置资产负债表之账户之各侧边柱子之宽度
    boxs_width = [width * 5 / 24, width * 4 / 24, width * 3 / 24, width * 3 / 24, width * 4 / 24, width * 5 / 24]  # 设置资产负债表之账户之各侧边柱子之宽度
    nibs_x = [reduce(lambda x, y: x + y, boxs_width[0:i + 1]) - boxs_width[i] for i in range(len(boxs_width))]  # 设置笔尖之x方向的位置之资产负债表之账户之各侧边柱子之起点
    o = [0, 1, 2, 5, 4, 3]  # 设置资产负债表之账户之各侧边柱子之绘制次序
    # a = 0  # 资产负债表之账户之绘制索引
    # nib_equity_x = width // 2 if accounts['equity']['E_all']['value'] >= 0 else 0  # 笔尖起始坐标之equity之开始位置之x坐标
    nibs_y = [0,0,0,0,0,0]  # 列表之笔尖起始坐标之开始位置之y坐标
    p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
    for accounts_type in list(accounts.keys())[:-1]:
        for level in accounts[accounts_type]:
            nib = (border + nibs_x[o[p]], border + title_height)  # 笔尖起始坐标之新柱子之开始位置
            count_balance_is_zero = 0
            items_balance_is_zero = []
            # s = 1  # 资产负债表值账户之各侧边柱子之各柱节之绘制索引
            for name, balance in accounts[accounts_type][level].items():
                if balance['value'] != 0:
                    ## 绘制单个项目对应的矩形
                    balanceSheet_svg.append(
                        dw.Rectangle(
                            x=nib[0],
                            y=nib[1],
                            width=boxs_width[o[p]],
                            height=int(height * (balance['value'] / max_money)),
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
                            y=nib[1] + int(height * (balance['value'] / max_money)) // 2,
                            text_anchor='middle',
                            dominant_baseline='middle',
                            font_family='Times New Roman',
                        )
                    )
                    nib = (border + nibs_x[o[p]], int(nib[1] + height * (balance['value'] / max_money)))  # 笔尖起始坐标之该柱子之下一个项目之柱节之开始位置
                    # if s < len(accounts[accounts_type][level]):
                    #     nib = (border + nibs_x[o[p]], int(nib[1] + height * (balance['value'] / max_money)))  # 笔尖起始坐标之该柱子之下一个项目之柱节之开始位置
                    #     s += 1
                    # else:
                    #     nibs_y = nib[1]
                else:  # 如果柱节高度为0...
                    count_balance_is_zero += 1
                    items_balance_is_zero.append((name, balance['value'], nib[1]))
                    pass  # if
                for (name, balance['value'], nib_y) in items_balance_is_zero:  # TODO尝试标记那些柱节高度为0的值
                    pass  # for
                pass  # for
            nibs_y[o[p]]=nib[1]
            p += 1
            pass  # for
        # nib_equity = nibs_y if nibs_y < nib_equity else nib_equity
        # a += 1
        pass  # for

    ## 绘制项目equity对应的矩形
    o = [5, 4, 3] if accounts['equity']['level 1']['E_all']['value'] >= 0 else [0, 1, 2]  # 设置资产负债表之账户之各侧边柱子之绘制次序
    p = 0  # 资产负债表之账户之各侧边柱子之绘制索引
    for accounts_type in list(accounts.keys())[-1:]:
        for level in accounts[accounts_type]:
            nib = (border + nibs_x[o[p]], border + nibs_y[o[p]])  # 笔尖起始坐标之新柱子之开始位置
            count_balance_is_zero = 0
            items_balance_is_zero = []
            s = 1  # 资产负债表值账户之各侧边柱子之各柱节之绘制索引
            for name, balance in accounts[accounts_type][level].items():
                # nib = (border + nib_equity_x, border + nib_equity)  # 笔尖起始坐标之equity之开始位置
                balance['color'] = balance['color'] if balance['value'] >= 0 else '#FFFFFF'  # 设置资产负债表之账户之各侧边柱子之绘制次序
                balanceSheet_svg.append(
                    dw.Rectangle(
                        x=nib[0],
                        y=nib[1],
                        width=boxs_width[o[p]],
                        height=int(height * (balance['value'] / max_money)),
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
                        y=nib[1] + int(height * (balance['value'] / max_money)) // 2,
                        text_anchor='middle',
                        dominant_baseline='middle',
                        font_family='Times New Roman',
                    )
                )
                pass  # for
            p += 1
            pass  # for
        # nib_equity = nibs_y if nibs_y < nib_equity else nib_equity
        # a += 1
        pass  # for

    return balanceSheet_svg
    pass  # def


# TODO 以下无用可以删除

class Scene:
    """
    绘制一个画布
    """

    def __init__(self, name="svg", height=400, width=400):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self, item):
        """
        添加项

        Args:
            item (): 项

        Returns:

        """
        self.items.append(item)

    def strarray(self):
        """
        XML形式的文本序列

        Returns:

        """
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"%d\" width=\"%d\" >\n" % (
                   self.height, self.width),
               " <g style=\"fill-opacity:1.0; stroke:black;\n",
               "  stroke-width:1;\">\n"]
        for item in self.items:
            var += item.strarray()
        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self, filename=None):
        """
        写出SVG文件

        Args:
            filename ():

        Returns:

        """
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname, 'w')
        file.writelines(self.strarray())
        file.close()
        return self.strarray()


class Line:
    """直线对象"""

    def __init__(self, start, end):
        self.start = start  # xy tuple
        self.end = end  # xy tuple
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %
                (self.start[0], self.start[1], self.end[0], self.end[1])]


class Rectangle:
    """矩形对象"""

    def __init__(self, origin, height, width, color=(255, 255, 255)):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %
                (self.origin[0], self.origin[1], self.height),
                "    width=\"%d\" style=\"fill:%s;\" />\n" %
                (self.width, colorstr(self.color))]


class Text:
    """文本对象"""

    def __init__(self, origin, text, size=18, align_horizontal="middle", align_vertical="auto"):
        self.origin = origin
        self.text = text
        self.size = size
        self.align_horizontal = align_horizontal
        self.align_vertical = align_vertical
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\"" %
                (self.origin[0], self.origin[1],
                 self.size), " text-anchor=\"", self.align_horizontal, "\"",
                " dominant-baseline=\"", self.align_vertical, "\">\n",
                "   %s\n" % self.text,
                "  </text>\n"]


class Textbox:
    """文本框对象"""

    def __init__(self, origin, height, width, text, color=(255, 255, 255), text_size=16):
        self.Outer = Rectangle(origin, height, width, color)
        self.Inner = Text((origin[0] + width // 2, origin[1] + height // 2),
                          text, text_size, align_horizontal="middle", align_vertical="middle")
        return

    def strarray(self):
        return self.Outer.strarray() + self.Inner.strarray()


"""XML形式的颜色字符串"""


def colorstr(rgb): return "rgb({}, {}, {})".format(rgb[0], rgb[1], rgb[2])
