class Compiler:
    def __init__(self):
        self.instructions = []

    def execute(self, node):
        self.instructions.append(('execute', node))

    def discriminate(self, condition, conditions):
        self.instructions.append(('discriminate', condition, conditions))

    def goto(self, position):
        self.instructions.append(('goto', position))

    def mark(self, position):
        self.instructions.append(('mark', position))

    def compile(self, code):
        for line in code.strip().split("\n"):
            line = line.strip()
            if line.startswith("mark"):
                position = line.split()[1]
                self.mark(position)
            elif line.startswith("execute"):
                node = line.split()[1]
                self.execute(node)
            elif line.startswith("discriminate"):
                condition, conditions = line.split()[1:]
                self.discriminate(condition, conditions.split(","))
            elif line.startswith("goto"):
                position = line.split()[1]
                self.goto(position)
            else:
                raise ValueError(f"Invalid line: {line}")

class Interpreter:
    def __init__(self):
        self.state = State()

    def execute(self, node):
        self.state.node = node
        node()

    def discriminate(self, condition, conditions):
        self.state.condition = condition
        return eval(condition) in [eval(c) for c in conditions]

    def run(self, code):
        compiler = Compiler()
        compiler.compile(code)
        instructions = compiler.instructions

        position = 0
        while position < len(instructions):
            instruction = instructions[position]
            if instruction[0] == "mark":
                pass
            elif instruction[0] == "execute":
                node = instruction[1]
                self.execute(node)
            elif instruction[0] == "discriminate":
                condition, conditions = instruction[1], instruction[2]
                if self.discriminate(condition, conditions):
                    pass
                else:
                    position += 1
                    continue
            elif instruction[0] == "goto":
                position = instructions.index(('mark', instruction[1]))
                continue
            else:
                raise ValueError(f"Invalid instruction: {instruction}")

            position += 1

class State:
    def __init__(self):
        self.node = None
        self.condition = None
        self.positions = {}

    def mark_position(self, name, line):
        self.positions[name] = line


class Compiler:
    def __init__(self):
        self.instructions = []

    def execute(self, node):
        self.instructions.append(('execute', node))

    def discriminate(self, condition, conditions):
        self.instructions.append(('discriminate', condition, conditions))

    def goto(self, position):
        self.instructions.append(('goto', position))

    def compile(self, code):
        for line in code.strip().split('\n'):
            # 忽略空行和注释行
            if line.strip() == '' or line.strip().startswith('#'):
                continue
            # 分割代码行为关键字和参数
            parts = line.strip().split(' ')
            # 根据关键字和参数生成指令
            if parts[0] == 'execute':
                node = parts[1]
                self.execute(node)


def compile_dsl(dsl_code):
    """
    编译DSL代码，返回指令列表
    """
    # 将DSL代码分割成多行
    lines = dsl_code.split('\n')

    # 初始化指令列表
    instructions = []

    # 初始化节点函数字典
    node_functions = {}

    # 遍历每行代码，进行编译
    i = 0
    while i < len(lines):
        line = lines[i]
        # 忽略空行和注释行
        if line.strip() == '' or line.strip().startswith('#'):
            i += 1
            continue

        # 分割代码行为关键字和参数
        parts = line.strip().split(' ')

        # 根据关键字和参数生成指令
        if parts[0] == 'execute':
            # 判断是否为最终节点
            if len(parts) == 2:
                # 生成"执行函数"指令
                instructions.append(('execute', parts[1]))
            else:
                # 生成"进入子流程"指令
                sub_process_name = parts[1]
                sub_process_code = ''
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('end'):
                    sub_process_code += lines[i] + '\n'
                    i += 1
                # 编译子流程代码
                sub_process_instructions = compile_dsl(sub_process_code)
                # 将子流程指令添加到主指令列表中
                instructions.append(('start_sub_process', sub_process_name, sub_process_instructions))
        elif parts[0] == 'function':
            # 判断是否为函数定义
            func_name = parts[1]
            func_code = ''
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('end'):
                func_code += lines[i] + '\n'
                i += 1
            # 将函数代码添加到函数字典中
            node_functions[func_name] = func_code
        i += 1

    # 返回指令列表和节点函数字典
    return instructions, node_functions


def execute_dsl(instructions, node_functions):
    """
    执行DSL代码，根据指令列表和节点函数字典执行代码
    """
    # 初始化变量
    current_node = 0
    current_variables = {}

    # 循环执行指令
    while current_node < len(instructions):
        instruction = instructions[current_node]
        if instruction[0] == 'execute':
            # 执行"执行函数"指令
            func_name = instruction[1]
            if func_name in node_functions:
                # 如果函数在函数字典中，执行函数代码
                func_code = node_functions[func_name]
                exec(func_code, current_variables)
            else:
                # 如果函数不在函数字典中，抛出异常
                raise Exception('Function not found: {}'.format(func_name))
            current_node += 1
        elif instruction[0] == 'start_sub_process':
            # 执行"进入子流程"指令
            sub_process_name = instruction[1]
            sub_process_instructions = instruction[2]
            # 将子流程指令列表添加到当前指令列表中
            instructions[current_node:current_node + 1] = sub_process_instructions
            # 将子流程变量和当前变量合并
            current_variables = {**current_variables, **{'sub_process_name': sub_process_name}}
        else:
            # 如果指令不是"执行函数"或"进入子流程"，抛出异常
            raise Exception('Invalid instruction: {}'.format(instruction))

    # 返回最终变量值
    return current_variables


class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def __repr__(self):
        return f'Node(name={self.name}, children={self.children})'

    def compile_node(node, node_functions):
        """
        编译多叉树节点，返回指令列表
        """
        instructions = []

        # 遍历节点的子节点，递归编译
        for child in node.children:
            child_instructions = compile_node(child, node_functions)
            instructions.extend(child_instructions)

        # 根据节点名称生成指令
        if node.name == 'execute':
            # 生成"执行函数"指令
            instructions.append(('execute', node.children[0].name))
        elif node.name == 'sub_process':
            # 生成"进入子流程"指令
            sub_process_name = node.children[0].name
            sub_process_instructions = []
            # 遍历子节点，递归编译
            for child in node.children[1:]:
                child_instructions = compile_node(child, node_functions)
                sub_process_instructions.extend(child_instructions)
            # 将子流程指令列表添加到主指令列表中
            instructions.append(('start_sub_process', sub_process_name, sub_process_instructions))

        return instructions

    def execute_node(node, node_functions, current_variables):
        """
        执行多叉树节点，根据指令列表和节点函数字典执行代码
        """
        # 遍历节点的子节点，递归执行
        for child in node.children:
            execute_node(child, node_functions, current_variables)

        # 根据节点名称执行指令
        if node.name == 'execute':
            # 执行"执行函数"指令
            func_name = node.children[0].name
            if func_name in node_functions:
                # 如果函数在函数字典中，执行函数代码
                func_code = node_functions[func_name]
                exec(func_code, current_variables)
            else:
                # 如果函数不在函数字典中，抛出异常
                raise Exception('Function not found: {}'.format(func_name))
        elif node.name == 'sub_process':
            # 执行"进入子流程"指令
            sub_process_name = node.children[0].name
            sub_process_instructions = []
            # 遍历子节点，递归执行
            for child in node.children[1:]:
                execute_node(child, node_functions, current_variables)
            # 在当前变量中添加子流程变量
            current_variables['sub_process_name'] = sub_process_name
            # 获取子流程指令列表并执行
            for instruction in node.instructions:
                execute_instruction(instruction, node_functions, current_variables)

    def compile_dsl(dsl_code):
        """
        编译DSL代码，返回多叉树根节点
        """
        # 将DSL代码分割成多行
        lines = dsl_code.split('\n')

        # 初始化根节点
        root = Node('root')

        # 初始化节点和函数字典
        node_dict = {}
        node_functions = {}

        # 初始化当前节点和当前父节点
        current_node = root
        current_parent = root

        # 遍历每行代码，进行编译
        for line in lines:
            # 忽略空行和注释行
            if line.strip() == '' or line.strip().startswith('#'):
                continue

            # 分割代码行为关键字和参数
            parts = line.strip().split(' ')

            # 根据关键字和参数生成节点
            if parts[0] == 'execute':
                # 创建"执行函数"节点
                node = Node('execute')
                # 创建函数名称子节点
                node.add_child(Node(parts[1]))
                # 将节点添加到当前父节点的子节点列表中
                current_parent.add_child(node)
            elif parts[0] == 'sub_process':
                # 创建"进入子流程"节点
                node = Node('sub_process')
                # 创建子流程名称子节点
                node.add_child(Node(parts[1]))
                # 将当前节点设置为子流程节点
                current_parent = node
                # 将节点添加到当前父节点的子节点列表中
                current_node.add_child(node)
                # 将子流程节点添加到节点字典中，以便在执行时使用
                node_dict[parts[1]] = node
            elif parts[0] == 'end':
                # 结束子流程，将当前节点设置为当前父节点
                current_parent = current_node.parent
            elif parts[0] == 'function':
                # 将函数代码添加到函数字典中
                func_name = parts[1]
                func_code = ''
                for line in lines(continued)

                # 忽略空行和注释行
                if line.strip() == '' or line.strip().startswith('#'):
                    continue
                # 如果代码行以“end function”开头，表示函数定义结束
                elif line.strip().startswith('end function'):
                    break
                else:
                    func_code += line + '\n'
                node_functions[func_name] = func_code
            else:
                # 如果关键字不是上述三种情况之一，抛出异常
                raise Exception('Invalid keyword: {}'.format(parts[0]))

        # 返回多叉树根节点
        return root


# 在主程序中使用编译器和解释器
if __name__ == '__main__':
    # 示例DSL代码
    dsl_code = """
    execute print_hello
    sub_process my_sub_process
        execute print_world
    end
    function print_hello
        print('Hello')
    end function
    function print_world
        print('World')
    end function
    """

    # 编译DSL代码为多叉树节点
    root_node = compile_dsl(dsl_code)

    # 执行多叉树节点
    execute_node(root_node, node_functions={}, current_variables={})