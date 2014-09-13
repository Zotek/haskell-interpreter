import ast

class HaskellASTVisitor(ast.NodeVisitor):
    _globalVariables = {}
    _functions = {
        'fst': ast.FunctionDef(
            'fst',
            ['l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Index(ast.Num(0)), ast.Load()),
            None
        ),
        'snd': ast.FunctionDef(
            'snd',
            ['l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Index(ast.Num(1)), ast.Load()),
            None
        ),
        'take': ast.FunctionDef(
            'take',
            ['n', 'l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(None, ast.Name('n', ast.Load), None), ast.Load()),
            None
        ),
        'drop': ast.FunctionDef(
            'drop',
            ['n', 'l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(ast.Name('n', ast.Load), None, None), ast.Load()),
            None
        ),
        'reverse': ast.FunctionDef(
            'reverse',
            ['l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(None, None, ast.Num(-1)), ast.Load()),
            None
        ),
        'init': ast.FunctionDef(
            'init',
            ['l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(None, ast.Num(-1), None), ast.Load()),
            None
        ),
        'tail': ast.FunctionDef(
            'tail',
            ['l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(ast.Num(1), None, None), ast.Load()),
            None
        ),
        'last': ast.FunctionDef(
            'last',
            ['l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Index(ast.Num(-1)), ast.Load()),
            None
        ),
        'head': ast.FunctionDef(
            'head',
            ['l'],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Index(ast.Num(0)), ast.Load()),
            None
        ),
        'length': ast.FunctionDef(
            'length',
            ['l'],
            ast.Attribute(ast.Name('l', ast.Load()), '!length', ast.Load()),
            None
        ),
        'null': ast.FunctionDef(
            'null',
            ['l'],
            ast.Compare(ast.Name('l', ast.Load()), [ast.Eq], [ast.List([], ast.Store())]),
            None
        ),
    }
    _funVariablesStack = []


    def generic_visit(self, node):
        return node

    def visit_Assign(self,node):
        self._globalVariables[node.targets[0]]=node.value
        return self.visit(node.value)

    def visit_Name(self,node):
        name = None
        if len(self._funVariablesStack) == 0: name = self._globalVariables.get(node.id,None)
        else: name = self._funVariablesStack[0][node.id]

        return self.visit(name)

    def visit_BinOp(self,node):
        operator = node.op
        result = None
        if operator == ast.Add:
            result = self.visit(node.left) + self.visit(node.right)
        elif operator == ast.Sub:
            result = self.visit(node.left) - self.visit(node.right)
        elif operator == ast.Div:
            result = self.visit(node.left) / self.visit(node.right)
        elif operator == ast.Mult:
            result = self.visit(node.left) * self.visit(node.right)

        return result

    def visit_Num(self, node):
        return self.visit(node.n) if not isinstance(node.n,int) else node.n

    def visit_BoolOp(self,node):
        if len(node.values)<1:
            return None
        if node.op == None:
            return node.values[0]
        elif node.op == ast.And:
            return self.visit(node.values[0]) and self.visit(node.values[1])
        elif node.op == ast.Or:
            return self.visit(node.values[0]) or self.visit(node.values[1])
        elif node.op == ast.Not:
            return not self.visit(node.values[0])

    def visit_Compare(self, node):
        operator = node.ops[0]
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        if operator == ast.Gt : return left > right
        elif operator == ast.GtE : return left >= right
        elif operator == ast.Lt : return  left < right
        elif operator == ast.LtE : return  left <= right
        elif operator == ast.Eq : return left == right
        elif operator == ast.NotEq : return left != right

    def visit_FunctionDef(self, node):
        if node.name in (self._globalVariables.keys() + self._functions.keys()):
            print "Name already in use"
            return None
        self._functions[node.name] = node
        return node.name

    def visit_Call(self, node):
        fun = self._functions[node.func]
        parameters = map(lambda x : self.visit(x),node.args)
        self._funVariablesStack.insert(0,dict(zip(fun.args,parameters)))
        retval = self.visit(fun.body)
        self._funVariablesStack.pop(0)
        return retval

    def visit_Tuple(self, node):
        return tuple(map(lambda x: self.visit(x), node.elts))

    def visit_List(self, node):
        return map(lambda x: self.visit(x), node.elts)

    def visit_Subscript(self, node):
        if node.value is None:
            (lower, upper, step) = self.visit(node.slice)
            return range(lower, upper + 1, step)

        if isinstance(node.slice, ast.Index):
            return self.visit(node.value)[self.visit(node.slice)]
        if isinstance(node.slice, ast.Slice):
            (lower, upper, step) = self.visit(node.slice)
            return self.visit(node.value)[lower:upper:step]

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_If(self, node):
        if self.visit(node.test):
            return self.visit(node.body)
        else:
            return self.visit(node.orelse)

    def visit_Slice(self, node):
        lower = self.visit(node.lower)
        upper = self.visit(node.upper)
        step = self.visit(node.step)
        return [lower, upper, step]

    def visit_Attribute(self, node):
        if node.attr == '!length':
            return len(self.visit(node.value))
