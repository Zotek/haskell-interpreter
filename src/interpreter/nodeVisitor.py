import ast

class HaskellASTVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        return node

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
        return node.n

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
