import ast
from loopedList import LoopedList


class HaskellASTVisitor(ast.NodeVisitor):
    _globalVariables = {
        'fst': ast.FunctionDef(
            'fst',
            [ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Index(ast.Num(0)), ast.Load()),
            None
        ),
        'snd': ast.FunctionDef(
            'snd',
            [ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Index(ast.Num(1)), ast.Load()),
            None
        ),
        'take': ast.FunctionDef(
            'take',
            [ast.Name('n', ast.Store()), ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(None, ast.Name('n', ast.Load), None), ast.Load()),
            None
        ),
        'drop': ast.FunctionDef(
            'drop',
            [ast.Name('n', ast.Store()), ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(ast.Name('n', ast.Load), None, None), ast.Load()),
            None
        ),
        'reverse': ast.FunctionDef(
            'reverse',
            [ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(None, None, ast.Num(-1)), ast.Load()),
            None
        ),
        'init': ast.FunctionDef(
            'init',
            [ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(None, ast.Num(-1), None), ast.Load()),
            None
        ),
        'tail': ast.FunctionDef(
            'tail',
            [ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Slice(ast.Num(1), None, None), ast.Load()),
            None
        ),
        'last': ast.FunctionDef(
            'last',
            [ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Index(ast.Num(-1)), ast.Load()),
            None
        ),
        'head': ast.FunctionDef(
            'head',
            [ast.Name('l', ast.Store())],
            ast.Subscript(ast.Name('l', ast.Load()), ast.Index(ast.Num(0)), ast.Load()),
            None
        ),
        'length': ast.FunctionDef(
            'length',
            [ast.Name('l', ast.Store())],
            ast.Attribute(ast.Name('l', ast.Load()), '!length', ast.Load()),
            None
        ),
        'null': ast.FunctionDef(
            'null',
            [ast.Name('l', ast.Store())],
            ast.Compare(ast.Name('l', ast.Load()), [ast.Eq], [ast.List([], ast.Store())]),
            None
        ),
        'replicate': ast.FunctionDef(
            'replicate',
            [ast.Name('n', ast.Store()), ast.Name('l', ast.Store())],
            ast.BinOp(ast.List([ast.Name('l', ast.Load())], ast.Store()), ast.Mult, ast.Name('n', ast.Load())),
            None
        ),
        'cycle': ast.FunctionDef(
            'cycle',
            [ast.Name('l', ast.Store())],
            ast.List(LoopedList(ast.Name('l', ast.Load())), ast.Store()),
            None
        ),
        'repeat': ast.FunctionDef(
            'repeat',
            [ast.Name('l', ast.Store())],
            ast.List(LoopedList([ast.Name('l', ast.Load())]), ast.Store()),
            None
        ),
    }
    _funVariablesStack = []


    def generic_visit(self, node):
        return node

    def visit_Assign(self,node):
        result = self.visit(node.value)
        self._globalVariables[node.targets.id] = result
        return result

    def visit_Name(self,node):
        name = None
        try:
            name = self._funVariablesStack[0][node.id]
        except IndexError:
            name = self._globalVariables.get(node.id,None)
        except KeyError:
            name = self._globalVariables.get(node.id,None)

        return name

    def visit_BinOp(self,node):
        operator = node.op
        result = None
        if operator == ast.Add:
            result = self.visit(node.left) + self.visit(node.right)
        elif operator == ast.Sub:
            if isinstance(node.left, str):
                result = ord(self.visit(node.left)) - ord(self.visit(node.right))
            else:
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
        if node.name.id in (self._globalVariables.keys() + self._globalVariables.keys()):
            print "Name already in use"
            return None
        self._globalVariables[node.name.id] = node
        return node.name.id

    def visit_Call(self, node):
        fun = self.visit(node.func)
        parameters = map(lambda x : self.visit(x),node.args)
        args = map(lambda x : x.id,fun.args)
        self._funVariablesStack.insert(0,dict(zip(args,parameters)))
        retval = self.visit(fun.body)
        self._funVariablesStack.pop(0)
        return retval

    def visit_Tuple(self, node):
        return tuple(map(lambda x: self.visit(x), node.elts))

    def visit_List(self, node):
        if isinstance(node.elts, LoopedList):
            return LoopedList([self.visit(x) for x in self.visit(node.elts.l)], [self.visit(x) for x in self.visit(node.elts.h)])
        else:
            return map(lambda x: self.visit(x), node.elts)

    def visit_Subscript(self, node):
        if node.value is None:
            (lower, upper, step) = self.visit(node.slice)
            if isinstance(lower, str):
                lower = ord(lower)
                upper = ord(upper)
                return map(lambda x: chr(x), range(lower, upper + 1, step))
            else:
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
