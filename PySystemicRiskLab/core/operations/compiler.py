"""
编译机。用于编译过程组件之内容。

#HACK 没有做覆盖性的单元测试。目前只要求能够在主程序中正确运行就好。
"""

from PySystemicRiskLab import logging

from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.operations.tree_structure import Tree
from PySystemicRiskLab.core.operations.stack_structure import Stack


class Compiler:
    """
    编译机

    编译后的指令列表有几种形式的元组：

    - `node XXX`。3元组。元素1是指令行号；元素2是指令`node`；元素3是指令内容是算法实体之节点实体；

    - `execute XXX`。3元组。元素1是指令行号；元素2是指令`execute`；元素3是指令内容是算法实体之内容变量；

    - `if XXX goto XXX`。6元组。元素1是指令行号；元素2是指令`if`；元素3是指令内容是算法实体之条件实体，呈现以字符串形式的内容；元素4是指令`goto`；元素5是指令内容是算法实体之节点实体；元素6是标记元素5对应的节点所在的指令行号；

    """

    # #HACK 以下无用
    # def __init__(self):
    #     self.instructions = []
    #
    # # @classmethod
    # def execute(self, node):
    #     self.instructions.append((self.line_number, 'execute', node))
    #
    # # @classmethod
    # def discriminate(self, condition, conditions):
    #     self.instructions.append(('discriminate', condition, conditions))
    #
    # # @classmethod
    # def goto(self, position):
    #     self.instructions.append(('goto', position))

    @classmethod
    def compile(cls, model_nodeEntity: Entity):
        """
        编译。

        编译过程分为三步：

        1. 构建编译树；

                遍历所有节点实体过程，生成编译树用于生成编译序列。

        2. 生成编译序列；

            该功能是生成一个编译序列，以记录编制整个程序代码段完整的编译路径。

        3. 编译；

            该功能是根据编译序列，执行编译过程，生成编译指令列表。

        Args:
            model_nodeEntity (Entity): 待编译的模型实体（模型节点实体）。

        Returns:

        """

        ## 预编译阶段

        ## 生成一棵编译树。
        logging.debug(f"\n\n\n开始生成编译树。\n")
        compile_tree = Tree()  # 创建一棵编译树
        build_tree_stack = Stack()  # 【生成树栈】，栈之元素是编译树节点实体之id。
        compile_tree.root_node.content = model_nodeEntity  # 设置编译树之根节点之内容
        build_tree_stack.push(compile_tree.root_node)  # 将根节点压入栈
        ## 生成编译树
        while not build_tree_stack.is_empty():  # 当栈不为空时
            compile_tree_node = build_tree_stack.pop()  # 弹出节点，进行处理。
            logging.debug(f"栈弹出节点{compile_tree_node.attribute.entity_name}，变成{build_tree_stack.print_stack(mode='return')}。")
            compile_nodeEntity = compile_tree_node.content  # 获取编译树节点之对应的节点实体
            compile_algorithmEntity = compile_nodeEntity.content  # 获取编译树节点之对应的节点实体
            if compile_algorithmEntity.process is not None:
                compile_tree_node.attribute.other = {'is_terminal': False}
            else:
                compile_tree_node.attribute.other = {'is_terminal': True}
                pass  # if
            code_process_content = compile_algorithmEntity.process  # 获取算法实体之过程，其内容是代码段
            code_lines = code_process_content.split('\n')  # 将代码分割成很多行
            compile_tree_node.attribute.other['start_line_number'] = 1  # 设置编译树节点之起始行号
            compile_tree_node.attribute.other['end_line_number'] = len(code_lines)  # 设置编译树节点之结束行号
            sub_node_list = []  # 当前节点之子节点列表
            ## 逐行扫描代码段，生成子节点
            for line_number, line in enumerate(code_lines):
                ## 判断是否是有效指令行
                if line.strip() == '' or line.strip().startswith('#'):  # 忽略空行和注释行
                    continue
                tokens = line.strip().split(' ')  # 分割代码行为关键字和参数
                ## 如果指令是`execute process xxx`，则说明需要进入该子过程编译。添加编译树子节点实体到编译树中。
                if tokens[0] == 'execute' and (tokens[1] == 'process'):
                    sub_process_name = tokens[2]  # 获取子过程名称
                    compile_tree_sub_node = compile_tree.create_and_add_node(entity_name=sub_process_name, parent_item=compile_tree_node)  # 创建编译树子节点实体
                    compile_tree_sub_node.content = compile_algorithmEntity.container[sub_process_name]  # 设置编译树子节点之内容为该算法实体之子节点实体
                    sub_node_list.append(compile_tree_sub_node)  # 暂存编译树子节点实体。等待遍历完当前节点实体的所有子节点实体后，再压入栈。
                    pass  # if
                ## 如果指令是`end define`，则标记位置，表示该过程编译结束
                if tokens[0] == 'end' and tokens[1] == 'define':
                    break
                    pass  # if
                pass  # for
            if len(sub_node_list) == 0:  # 如果当前算法节点没有子节点，则标记该编译树节点为终端节点，否则标记为非终端节点
                compile_tree_node.attribute.other['is_terminal'] = True
                continue
            else:
                compile_tree_node.attribute.other['is_terminal'] = False
                sub_node_list.reverse()  # 将编译树子节点实体倒序压入栈。这样做的目的是为了保证栈中的节点顺序和编译序列中的节点顺序一致。
                build_tree_stack.push(sub_node_list)
                logging.debug(f"栈压入节点{'[' + ', '.join([node.attribute.entity_name for node in sub_node_list]) + ']'}，变成{build_tree_stack.print_stack(mode='return')}。")
                pass  # if
            pass  # while
        ## 打印编译树
        logging.debug(f"编译树：")
        compile_tree.print_tree()

        ## 遍历编译树生成编译序列。
        ## NOTE：从树的遍历算法上看，本质上是中序遍历。从应用上来比喻，相当于实现从头到尾的跳步阅读行为。
        logging.debug(f"\n\n\n开始遍历编译树生成编译序列：\n")
        compile_order_list = []  # 编译序列列表。每个元素是一个5元组。元素1是编译树节点实体，元素2是待编译的节点实体，元素3是待编译的算法实体，元素4是待编译的节点之过程之代码段之开始编译的行号，元素5是待编译的节点之过程之代码段之停止编译的行号。
        precompile_stack = Stack()  # 预编译栈。，栈之元素是待编译的节点之id。
        precompile_stack.push(compile_tree.root_node)  # 将根节点压入栈
        ## 遍历编译树，生成编译序列
        while not precompile_stack.is_empty():  # 当栈不为空时
            compile_tree_node = precompile_stack.pop()  # 弹出节点，进行处理。
            logging.debug(f"栈弹出节点{compile_tree_node.attribute.entity_name}，变成{precompile_stack.print_stack(mode='return')}。")
            if (compile_tree_node.attribute.other['is_terminal'] is False and compile_tree_node.attribute.other['start_line_number'] == 1):  # 如果该节点是非终端节点，且还没有预编译过，则将该节点再压入编译序列
                compile_tree_node_children = compile_tree.get_children(compile_tree_node)  # 获取该编译树节点之所有子节点
                ## 倒序、遍历该编译树节点之所有子节点，然后间隔插入父节点，再压入栈。
                if len(compile_tree_node_children) is not 0:
                    compile_tree_node_children.reverse()
                    for compile_tree_node_child in compile_tree_node_children:
                        precompile_stack.push(compile_tree_node)  # 将该编译树节点压入栈
                        logging.debug(f"栈压入节点{compile_tree_node.attribute.entity_name}，变成{precompile_stack.print_stack(mode='return')}。")
                        precompile_stack.push(compile_tree_node_child)  # 将子节点压入栈
                        logging.debug(f"栈压入节点{compile_tree_node_child.attribute.entity_name}，变成{precompile_stack.print_stack(mode='return')}。")
                        pass  # for
                    pass  # if
                pass  # if
            compile_nodeEntity = compile_tree_node.content  # 获取编译树节点之对应的节点实体
            compile_algorithmEntity = compile_nodeEntity.content  # 获取编译树节点之对应的节点实体
            logging.debug(f'编译树节点{compile_tree_node.attribute.entity_name}，对应的算法实体之节点实体{compile_nodeEntity.attribute.entity_name}，对应的算法实体{compile_algorithmEntity.attribute.entity_name}')
            code_process_content = compile_algorithmEntity.process  # 获取算法实体之过程，其内容是代码段
            code_lines = code_process_content.split('\n')  # 将代码分割成很多行
            ## 逐行扫描代码段，生成编译序列
            line_number = compile_tree_node.attribute.other['start_line_number']  # 记录当前行号
            for line in code_lines[compile_tree_node.attribute.other['start_line_number']:]:
                ## 判断是否是有效指令行
                if line.strip() == '' or line.strip().startswith('#'):  # 忽略空行和注释行
                    line_number += 1  # 继续扫描下一行
                    continue
                    pass  # if
                logging.debug(f"当前行号：{line_number}，当前行内容：{line}。")
                tokens = line.strip().split(' ')  # 分割代码行为关键字和参数
                ## 如果指令是`execute process xxx`，则说明需要进入该子过程编译。添加编译树子节点实体到编译树中。
                if tokens[0] == 'execute' and (tokens[1] == 'process'):
                    compile_tree_node.attribute.other['end_line_number'] = line_number  # 标记需要编译的当前算法实体之过程代码段之结束行号到当前编译树节点实体之特征。
                    compile_order_list.append((compile_tree_node, compile_nodeEntity, compile_algorithmEntity, compile_tree_node.attribute.other['start_line_number'], compile_tree_node.attribute.other['end_line_number']))  # 添加当前编译节点、编译起止行号、特征之是否终端节点到编译序列中
                    compile_tree_node.attribute.other['start_line_number'] = line_number + 1  # 更新当前编译节点之过程代码段之初始位置
                    break  # 停止扫描当前编译节点之过程，转而扫描子节点。
                    pass  # if
                ## 如果是指令`define process`，则说明是编译该过程的起点
                if tokens[0] == 'define' and tokens[1] == 'process':
                    ## 标记当前编译节点之过程代码段之初始位置
                    compile_tree_node.attribute.other['start_line_number'] = line_number  # 标记当前编译节点之过程代码段之初始位置
                    line_number += 1  # 继续扫描下一行
                    continue
                    pass  # if
                ## 如果指令是`end define`，则标记位置，表示该过程编译结束
                if tokens[0] == 'end' and tokens[1] == 'define':
                    compile_tree_node.attribute.other['end_line_number'] = line_number  # 标记需要编译的当前算法实体之过程代码段之结束行号到当前编译树节点实体之特征。
                    compile_order_list.append((compile_tree_node, compile_nodeEntity, compile_algorithmEntity, compile_tree_node.attribute.other['start_line_number'], compile_tree_node.attribute.other['end_line_number']))  # 添加当前编译节点、编译起止行号到编译序列中。
                    break  # 停止扫描当前编译节点之过程，转而扫描父节点。
                ## 如果是其他指令
                else:
                    line_number += 1  # 继续扫描下一行
                    pass  # if
                pass  # for

            pass  # while
        ## 打印编译序列
        logging.debug(f"\n\n编译序列：\n")
        for i in range(len(compile_order_list)):
            logging.debug(f"树节点：{compile_order_list[i][0].attribute.entity_name}、节点：{compile_order_list[i][1].attribute.entity_name}、算法：{compile_order_list[i][2].attribute.entity_name}、起止行({str(compile_order_list[i][3])}, {str(compile_order_list[i][4])})")

        ## 编译阶段

        ## 编译。遍历编译序列依次编译每一段代码段。最后拼接起来，形成指令列表。
        logging.debug("\n\n\n开始编译：\n")
        instructions = []  # 编译后的指令列表。
        instructions_line_number = 1  # 指令行号
        for compile_item in compile_order_list:
            compile_tree_node, compile_nodeEntity, compile_algorithmEntity, start_line_number, end_line_number = compile_item[0], compile_item[1], compile_item[2], compile_item[3], compile_item[4]  # 获取编译节点实体、编译起止行号
            code_process_content = compile_algorithmEntity.process  # 获取算法实体之过程，其内容是代码段
            code_lines = code_process_content.split('\n')  # 将代码分割成很多行
            ## 逐行扫描代码段，生成编译序列
            for line in code_lines[start_line_number:end_line_number + 1]:
                ## 判断是否是有效指令行
                if line.strip() == '' or line.strip().startswith('#'):  # 忽略空行和注释行
                    continue
                    pass  # if
                tokens = line.strip().split(' ')  # 分割代码行为关键字和参数
                ## 判断指令类型做相应的编译处理
                if tokens[0] == 'execute' and tokens[1] == 'content':  # 如果指令是`execute content`，则需要编译算法内容
                    instructions.append((instructions_line_number, 'node', compile_algorithmEntity.container[tokens[2]]))  # 生成指令`node <nodeEntity>`
                    logging.debug(f"{instructions_line_number}\t{instructions[instructions_line_number - 1][1]}\t\t{compile_algorithmEntity.container[tokens[2]].attribute.entity_name} {compile_algorithmEntity.container[tokens[2]].attribute.id}")
                    instructions_line_number += 1  # 下一指令行号
                    instructions.append((instructions_line_number, tokens[0], compile_algorithmEntity.container[tokens[2]]))  # 生成指令`execute <nodeEntity之algorithmContent>`。
                    logging.debug(f"{instructions_line_number}\t{instructions[instructions_line_number - 1][1]}\t\t{compile_algorithmEntity.container[tokens[2]].attribute.entity_name} {compile_algorithmEntity.container[tokens[2]].attribute.id}")
                    instructions_line_number += 1  # 下一指令行号
                elif tokens[0] == 'if' and tokens[2] == 'goto':  # 如果是连续的指令`if XXX goto XXX`，则编译判别条件
                    instructions.append((instructions_line_number, tokens[0], compile_algorithmEntity.condition[tokens[1]].content, tokens[2], compile_algorithmEntity.container[tokens[3]], None))  # 生成指令。但是该指令之内容是文本形式的判别条件，需要在执行过程时再解析。
                    logging.debug(f"{instructions_line_number}\t{tokens[0]}\t\t{compile_algorithmEntity.condition[tokens[1]].content}\t\t{tokens[2]}\t\t{compile_algorithmEntity.container[tokens[3]].attribute.entity_name} {compile_algorithmEntity.container[tokens[3]].attribute.id}")
                    instructions_line_number += 1  # 下一指令行号
                elif tokens[0] == 'define' and tokens[1] == 'process':  # 如果是根节点之指令`define process xxx`，则编译成`node xxx`
                    instructions.append((instructions_line_number, 'node', compile_nodeEntity))
                    logging.debug(f"{instructions_line_number}\t{instructions[instructions_line_number - 1][1]}\t\t{compile_nodeEntity.attribute.entity_name} {compile_nodeEntity.attribute.id}")
                    instructions_line_number += 1  # 下一指令行号
                    pass  # if
                # ## 如果是根节点之指令`end define xxx`，则编译成`end process xxx`
                # if tokens[0] == 'end' and tokens[1] == 'define':
                #     instructions.append((instructions_line_number, 'end process', compile_nodeEntity.attribute.id))
                #     logging.debug(f"{instructions[instructions_line_number - 1][0]}\t{instructions[instructions_line_number - 1][1]}\t\t{compile_nodeEntity.attribute.entity_name} {compile_nodeEntity.attribute.id}")
                #     instructions_line_number += 1  # 下一指令行号
                #     continue
                #     pass  # if
                ## TODO 旧版本，后续考虑是否删除
                # if tokens[0] == 'execute' and tokens[1] == 'content':  # 如果指令是`execute content`，则需要编译算法内容
                #     instructions.append((instructions_line_number, 'node', compile_algorithmEntity.container[tokens[2]]))  # 生成指令`node <nodeEntity之id>`
                #     logging.debug(f"{instructions[instructions_line_number - 1][0]}\t{instructions[instructions_line_number - 1][1]}\t\t{compile_algorithmEntity.container[tokens[2]].attribute.entity_name} {compile_algorithmEntity.container[tokens[2]].attribute.id}")
                #     instructions_line_number += 1  # 下一指令行号
                #     instructions.append((instructions_line_number, tokens[0], compile_algorithmEntity.container[tokens[2]]))  # 生成指令`execute <nodeEntity之algorithmContent>`。但是该指令之内容是文本形式的算法内容，需要在执行过程时再解析。
                #     logging.debug(f"{instructions[instructions_line_number - 1][0]}\t{instructions[instructions_line_number - 1][1]}\t\t{compile_algorithmEntity.container[tokens[2]].attribute.entity_name} {compile_algorithmEntity.container[tokens[2]].attribute.id}")
                #     instructions_line_number += 1  # 下一指令行号
                #     continue
                #     pass  # if
                # ## 如果是连续的指令`if XXX goto XXX`，则编译判别条件
                # if tokens[0] == 'if' and tokens[2] == 'goto':
                #     instructions.append((instructions_line_number, tokens[0], compile_algorithmEntity.condition[tokens[1]], tokens[2], compile_algorithmEntity.container[tokens[3]].attribute.id))  # 生成指令。但是该指令之内容是文本形式的判别条件，需要在执行过程时再解析。
                #     logging.debug(f"{instructions[instructions_line_number - 1][0]}\t{instructions[instructions_line_number - 1][1]}\t\t{tokens[1]}\t\t{instructions[instructions_line_number - 1][3]}\t\t{compile_nodeEntity.attribute.entity_name} {compile_nodeEntity.attribute.id}")
                #     instructions_line_number += 1  # 下一指令行号
                #     continue
                #     pass  # if
                # ## 如果是根节点之指令`define process xxx`，则编译成`start process xxx`
                # if tokens[0] == 'define' and tokens[1] == 'process':
                #     instructions.append((instructions_line_number, 'start process', compile_nodeEntity.attribute.id))
                #     logging.debug(f"{instructions[instructions_line_number - 1][0]}\t{instructions[instructions_line_number - 1][1]}\t\t{compile_nodeEntity.attribute.entity_name} {compile_nodeEntity.attribute.id}")
                #     instructions_line_number += 1  # 下一指令行号
                #     continue
                #     pass  # if
                # ## 如果是根节点之指令`end define xxx`，则编译成`end process xxx`
                # if tokens[0] == 'end' and tokens[1] == 'define':
                #     instructions.append((instructions_line_number, 'end process', compile_nodeEntity.attribute.id))
                #     logging.debug(f"{instructions[instructions_line_number - 1][0]}\t{instructions[instructions_line_number - 1][1]}\t\t{compile_nodeEntity.attribute.entity_name} {compile_nodeEntity.attribute.id}")
                #     instructions_line_number += 1  # 下一指令行号
                #     continue
                #     pass  # if
                pass  # for
            pass  # for

        ## 装配编译指令之行号。遍历编译指令，将指令 if-goto 之待跳转的节点之行号，替换成该节点之行号
        for i, instruction_i in enumerate(instructions):
            if instruction_i[1] == 'if':
                node_id = instruction_i[4]
                for instruction_j in instructions:
                    if instruction_j[1] == 'node' and instruction_j[2] == node_id:
                        new_line_number = instruction_j[0]  # 获取指令 if-goto 之待跳转的节点之行号
                        pass  # if
                    pass  # for
                instructions[i] = (instruction_i[0], instruction_i[1], instruction_i[2], instruction_i[3], instruction_i[4], new_line_number)  # 重新装配编译指令之行号
                pass  # if
            pass  # for

        ## 打印编译指令
        logging.info("\n\n\n编译指令：\n")
        for instruction in instructions:
            if instruction[1] == 'node':
                logging.info(f"{instruction[0]}\t{instruction[1]}\t\t{instruction[2].attribute.entity_name} {instruction[2].attribute.id}")
            elif instruction[1] == 'execute':
                logging.info(f"{instruction[0]}\t{instruction[1]}\t\t{instruction[2].attribute.entity_name} {instruction[2].attribute.id}")
            elif instruction[1] == 'if' and instruction[3] == 'goto':
                logging.info(f"{instruction[0]}\t{instruction[1]}\t\t{instruction[2]}\t\t{instruction[3]}\t\t{instruction[4].attribute.entity_name} {instruction[4].attribute.id}\t{instruction[5]}")
                pass  # if
            pass  # for

        return instructions
        pass  # def

    pass  # class
