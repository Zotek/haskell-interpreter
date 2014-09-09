import ast

class HaskellASTVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        return node

    def visit_BinOp(self,node):
        operator = node.op.__name__
        result = None
        if operator == "Add":
            result = self.visit(node.left) + self.visit(node.right)
        elif operator == "Sub":
            result = self.visit(node.left) - self.visit(node.right)
        elif operator == "Div":
            result = self.visit(node.left) / self.visit(node.right)
        elif operator == "Mul":
            result = self.visit(node.left) * self.visit(node.right)

        return result

    def visit_Num(self, node):
        return node.n