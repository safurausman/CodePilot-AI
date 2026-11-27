import ast, math, operator

_ALLOWED_BIN = {ast.Add:operator.add, ast.Sub:operator.sub, ast.Mult:operator.mul,
                ast.Div:operator.truediv, ast.FloorDiv:operator.floordiv,
                ast.Mod:operator.mod, ast.Pow:operator.pow}
_ALLOWED_UNARY = {ast.UAdd:operator.pos, ast.USub:operator.neg, ast.Not:operator.not_}
_ALLOWED_CMP = {ast.Eq:operator.eq, ast.NotEq:operator.ne, ast.Lt:operator.lt,
                ast.LtE:operator.le, ast.Gt:operator.gt, ast.GtE:operator.ge}
_SAFE_FUNCS = {"abs":abs,"round":round,"min":min,"max":max,"sum":sum,"len":len,
               "sorted":sorted,"sqrt":math.sqrt,"floor":math.floor,"ceil":math.ceil}

def _eval(node, env):
    if isinstance(node, ast.Constant): return node.value
    if isinstance(node, ast.Name):
        if node.id in env: return env[node.id]
        if node.id in _SAFE_FUNCS: return _SAFE_FUNCS[node.id]
        raise ValueError(f"Name not allowed: {node.id}")
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        vals=[_eval(x,env) for x in node.elts]
        return vals if isinstance(node,ast.List) else tuple(vals) if isinstance(node,ast.Tuple) else set(vals)
    if isinstance(node, ast.Dict): return {_eval(k,env):_eval(v,env) for k,v in zip(node.keys,node.values)}
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BIN:
        a,b=_eval(node.left,env),_eval(node.right,env)
        if isinstance(node.op,ast.Pow) and abs(b)>100: raise ValueError("Exponent too large.")
        return _ALLOWED_BIN[type(node.op)](a,b)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
        return _ALLOWED_UNARY[type(node.op)](_eval(node.operand,env))
    if isinstance(node, ast.Compare):
        left=_eval(node.left,env)
        for op, comp in zip(node.ops,node.comparators):
            right=_eval(comp,env)
            if type(op) not in _ALLOWED_CMP or not _ALLOWED_CMP[type(op)](left,right): return False
            left=right
        return True
    if isinstance(node, ast.BoolOp):
        vals=[bool(_eval(v,env)) for v in node.values]
        return all(vals) if isinstance(node.op,ast.And) else any(vals)
    if isinstance(node, ast.IfExp): return _eval(node.body if _eval(node.test,env) else node.orelse,env)
    if isinstance(node, ast.Call) and isinstance(node.func,ast.Name) and node.func.id in _SAFE_FUNCS:
        return _SAFE_FUNCS[node.func.id](*[_eval(a,env) for a in node.args])
    raise ValueError(f"Python construct not permitted: {type(node).__name__}")

def execute_safe_python(source: str):
    """Evaluate a restricted expression (not arbitrary Python code)."""
    if len(source)>5000: raise ValueError("Input is limited to 5,000 characters.")
    tree=ast.parse(source,mode="eval")
    return repr(_eval(tree.body,{}))
