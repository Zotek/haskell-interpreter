import ast

class HaskellASTVisitor(ast.NodeVisitor):
    _globalVariables = {}
    _functions = {}
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
        return self.visit(node.n)

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
        self._funVariablesStack.insert(0,dict(zip(fun.args,node.args)))
        retval = self.visit(fun.body)
        self._funVariablesStack.pop(0)
        return retval