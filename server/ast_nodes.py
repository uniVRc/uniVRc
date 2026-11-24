"""anti_hls.frontend.ast_nodes — Strongly-typed AST node hierarchy for uniVRc and pseudo-uniVRc."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Union


@dataclass
class SourceLocation:
    line: int = 1
    col: int = 1
    end_line: Optional[int] = None
    end_col: Optional[int] = None


@dataclass
class ASTNode:
    loc: SourceLocation = field(default_factory=SourceLocation)
    annotations: Dict[str, Any] = field(default_factory=dict)


# --- Types ---
@dataclass
class TypeNode(ASTNode):
    pass


@dataclass
class PrimitiveType(TypeNode):
    name: str = ""  # 'int', 'float', 'bool', 'reg'


@dataclass
class SizedIntType(TypeNode):
    is_signed: bool = False
    width: Any = None  # AST Expr (NumberLit or Expr)


@dataclass
class FxpType(TypeNode):
    width: Any = None  # AST Expr
    frac: Any = None   # AST Expr


@dataclass
class StructRefType(TypeNode):
    name: str = ""


@dataclass
class StreamType(TypeNode):
    elem_type: TypeNode = field(default_factory=TypeNode)
    depth: Optional[Any] = None
    is_fifo: bool = False


@dataclass
class WireType(TypeNode):
    width: Optional[Any] = None  # None for 1-bit, or Expr for sized wire


# --- Synthesis Attributes / Pragmas ---
@dataclass
class Attribute(ASTNode):
    name: str = ""  # e.g., 'PIPE', 'UNROLL', 'REG', 'MEM', 'MODULE', 'FUNC', 'THREAD', 'PARAM'
    args: Dict[str, Any] = field(default_factory=dict)  # e.g., {'II': 1, 'FACTOR': 4}
    positional_args: List[Any] = field(default_factory=list)


# --- Expressions ---
@dataclass
class Expr(ASTNode):
    pass


@dataclass
class Identifier(Expr):
    name: str = ""


@dataclass
class NumberLit(Expr):
    value: Union[int, float] = 0
    raw: str = ""


@dataclass
class BoolLit(Expr):
    value: bool = False


@dataclass
class SizedLit(Expr):
    width: int = 0
    base: str = "d"  # 'b', 'h', 'd'
    raw: str = ""
    value: int = 0


@dataclass
class StringLit(Expr):
    value: str = ""
    raw: str = ""


@dataclass
class EdgeExpr(Expr):
    edge: str = "posedge"  # 'posedge', 'negedge', 'level'
    signal: str = ""


@dataclass
class SimTimeLit(Expr):
    kind: str = "time"  # 'time', 'realtime'


@dataclass
class BinaryOp(Expr):
    op: str = ""  # '+', '-', '*', '/', '%', '**', '<<', '>>', '<<<', '>>>', '<<o', '>>o', '&', '|', '^', '~^', '==', '!=', '<', '<=', '>', '>=', 'and', 'or', 'xor'
    left: Expr = field(default_factory=Expr)
    right: Expr = field(default_factory=Expr)


@dataclass
class UnaryOp(Expr):
    op: str = ""  # '-', '+', '~', '!', 'not'
    operand: Expr = field(default_factory=Expr)


@dataclass
class ReductionOp(Expr):
    op: str = ""  # '<&', '<|', '<^', '<!', '<~|', '<~^'
    operand: Expr = field(default_factory=Expr)


@dataclass
class TernaryOp(Expr):
    cond: Expr = field(default_factory=Expr)
    true_expr: Expr = field(default_factory=Expr)
    false_expr: Expr = field(default_factory=Expr)


@dataclass
class MemberAccess(Expr):
    base: Expr = field(default_factory=Expr)
    member: str = ""


@dataclass
class IndexExpr(Expr):
    base: Expr = field(default_factory=Expr)
    index: Expr = field(default_factory=Expr)


@dataclass
class SliceExpr(Expr):
    base: Expr = field(default_factory=Expr)
    msb: Expr = field(default_factory=Expr)
    lsb: Expr = field(default_factory=Expr)
    step: Optional[Expr] = None


@dataclass
class SliceIndexed(Expr):
    base: Expr = field(default_factory=Expr)
    index: Expr = field(default_factory=Expr)
    width: Expr = field(default_factory=Expr)
    is_plus: bool = True  # True for +:, False for -:


@dataclass
class ConcatExpr(Expr):
    elements: List[Expr] = field(default_factory=list)


@dataclass
class ReplicationExpr(Expr):
    count: Expr = field(default_factory=Expr)
    value: Expr = field(default_factory=Expr)


@dataclass
class CallExpr(Expr):
    func: Expr = field(default_factory=Expr)
    args: List[Expr] = field(default_factory=list)


@dataclass
class BuiltinCall(Expr):
    name: str = ""  # 'min', 'max', 'abs'
    args: List[Expr] = field(default_factory=list)


@dataclass
class CastExpr(Expr):
    target_type: TypeNode = field(default_factory=TypeNode)
    expr: Expr = field(default_factory=Expr)


@dataclass
class InitList(Expr):
    elements: List[Any] = field(default_factory=list)


# --- Statements ---
@dataclass
class Statement(ASTNode):
    pass


@dataclass
class Block(Statement):
    statements: List[Statement] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class VarDecl(Statement):
    name: str = ""
    type_desc: Optional[TypeNode] = None
    array_dims: List[Expr] = field(default_factory=list)
    initializer: Optional[Expr] = None
    is_const: bool = False
    is_var: bool = False
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class AssignStmt(Statement):
    target: Expr = field(default_factory=Expr)
    value: Expr = field(default_factory=Expr)
    is_register: bool = False  # False for '=', True for ':='
    is_continuous: bool = False  # True for continuous 'assign target = value'


@dataclass
class AugAssignStmt(Statement):
    target: Expr = field(default_factory=Expr)
    op: str = ""  # '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', ':+=', etc.
    value: Expr = field(default_factory=Expr)
    is_register: bool = False


@dataclass
class IncDecStmt(Statement):
    target: Expr = field(default_factory=Expr)
    op: str = "++"  # '++' or '--'
    is_prefix: bool = True  # True for ++x, False for x++


@dataclass
class CallStmt(Statement):
    call: CallExpr = field(default_factory=CallExpr)


@dataclass
class BreakStmt(Statement):
    pass


@dataclass
class ContinueStmt(Statement):
    pass


@dataclass
class ReturnStmt(Statement):
    value: Optional[Expr] = None


@dataclass
class AssertStmt(Statement):
    cond: Expr = field(default_factory=Expr)
    message: Optional[Expr] = None


@dataclass
class DelayStmt(Statement):
    cycles: Expr = field(default_factory=Expr)


@dataclass
class IfStmt(Statement):
    cond: Expr = field(default_factory=Expr)
    then_block: Block = field(default_factory=Block)
    elifs: List[Tuple[Expr, Block]] = field(default_factory=list)
    else_block: Optional[Block] = None
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class SwitchCase(ASTNode):
    values: List[Expr] = field(default_factory=list)
    body: Block = field(default_factory=Block)


@dataclass
class SwitchStmt(Statement):
    expr: Expr = field(default_factory=Expr)
    cases: List[SwitchCase] = field(default_factory=list)
    default_block: Optional[Block] = None
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class ForStmt(Statement):
    kind: str = "cstyle"  # 'cstyle', 'standard_c', 'iter_range', 'iter_set'
    iterator: Optional[str] = None
    start: Optional[Expr] = None
    end: Optional[Expr] = None
    step: Optional[Expr] = None
    set_items: Optional[List[Expr]] = None
    body: Block = field(default_factory=Block)
    init_stmt: Optional[Statement] = None
    cond_expr: Optional[Expr] = None
    step_stmt: Optional[Statement] = None
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class WhileStmt(Statement):
    cond: Expr = field(default_factory=Expr)
    body: Block = field(default_factory=Block)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class DoWhileStmt(Statement):
    cond: Expr = field(default_factory=Expr)
    body: Block = field(default_factory=Block)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class RepeatStmt(Statement):
    count: Expr = field(default_factory=Expr)
    body: Block = field(default_factory=Block)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class SensitivityItem(ASTNode):
    edge: Optional[str] = None  # 'posedge', 'negedge', or None
    signal: str = ""


@dataclass
class AlwaysStmt(Statement):
    sensitivity: List[SensitivityItem] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)


@dataclass
class ThreadStmt(Statement):
    body: List[Statement] = field(default_factory=list)


# --- Hardware Module and Functions ---
@dataclass
class PortConn(ASTNode):
    port_name: Optional[str] = None  # None for positional port connection
    expr: Expr = field(default_factory=Expr)


@dataclass
class InstStmt(Statement):
    module_name: str = ""
    inst_name: str = ""
    connections: List[PortConn] = field(default_factory=list)


@dataclass
class PortDef(ASTNode):
    direction: str = "in"  # 'in', 'out', 'inout'
    type_desc: TypeNode = field(default_factory=TypeNode)
    name: str = ""
    array_dims: List[Expr] = field(default_factory=list)
    default_val: Optional[Expr] = None


@dataclass
class ParamDef(ASTNode):
    name: str = ""
    value: Optional[Expr] = None


@dataclass
class ModuleDef(Statement):
    name: str = ""
    ports: List[PortDef] = field(default_factory=list)
    params: List[ParamDef] = field(default_factory=list)
    body: Block = field(default_factory=Block)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class FuncParamDef(ASTNode):
    type_desc: TypeNode = field(default_factory=TypeNode)
    name: str = ""
    array_dims: List[Expr] = field(default_factory=list)
    default_val: Optional[Expr] = None


@dataclass
class FuncDef(Statement):
    name: str = ""
    params: List[FuncParamDef] = field(default_factory=list)
    return_type: Optional[TypeNode] = None
    body: Block = field(default_factory=Block)
    params_section: List[ParamDef] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class TestbenchDef(Statement):
    __test__ = False
    name: str = ""
    params: List[FuncParamDef] = field(default_factory=list)
    body: Block = field(default_factory=Block)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class StructField(ASTNode):
    type_desc: TypeNode = field(default_factory=TypeNode)
    name: str = ""
    array_dims: List[Expr] = field(default_factory=list)


@dataclass
class StructDef(Statement):
    name: str = ""
    fields: List[StructField] = field(default_factory=list)


@dataclass
class EnumEntry(ASTNode):
    name: str = ""
    value: Optional[Expr] = None


@dataclass
class EnumDef(Statement):
    name: str = ""
    width: Optional[Expr] = None
    entries: List[EnumEntry] = field(default_factory=list)


@dataclass
class TypedefDef(Statement):
    type_desc: TypeNode = field(default_factory=TypeNode)
    name: str = ""
    array_dims: List[Expr] = field(default_factory=list)


@dataclass
class InterfaceItem(ASTNode):
    direction: str = "in"
    type_desc: Optional[TypeNode] = None
    name: str = ""
    array_dims: List[Expr] = field(default_factory=list)
    default_val: Optional[Expr] = None
    var_decl: Optional[Statement] = None


@dataclass
class InterfaceDef(Statement):
    name: str = ""
    generics: List[ParamDef] = field(default_factory=list)
    items: List[InterfaceItem] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class StaticStmt(Statement):
    body: Any = None


# Backward compatibility alias
GenerateStmt = StaticStmt


@dataclass
class Program(ASTNode):
    statements: List[Statement] = field(default_factory=list)

    @property
    def modules(self) -> List[ModuleDef]:
        return [s for s in self.statements if isinstance(s, ModuleDef)]

    @property
    def functions(self) -> List[FuncDef]:
        return [s for s in self.statements if isinstance(s, FuncDef)]

    @property
    def structs(self) -> List[StructDef]:
        return [s for s in self.statements if isinstance(s, StructDef)]

    @property
    def enums(self) -> List[EnumDef]:
        return [s for s in self.statements if isinstance(s, EnumDef)]

    @property
    def testbenches(self) -> List[TestbenchDef]:
        return [s for s in self.statements if isinstance(s, TestbenchDef)]

    @property
    def typedefs(self) -> List[TypedefDef]:
        return [s for s in self.statements if isinstance(s, TypedefDef)]


# --- Serialization & Visitor ---
def ast_to_dict(node: Any) -> Any:
    """Recursively converts an AST node hierarchy to a nested dictionary for JSON serialization."""
    if hasattr(node, '__dataclass_fields__'):
        d = {'_type': node.__class__.__name__}
        for f in node.__dataclass_fields__:
            d[f] = ast_to_dict(getattr(node, f))
        return d
    elif isinstance(node, (list, tuple)):
        return [ast_to_dict(x) for x in node]
    elif isinstance(node, dict):
        return {k: ast_to_dict(v) for k, v in node.items()}
    return node


class ASTVisitor:
    """Base visitor class for traversing the pseudoVR AST."""

    def visit(self, node: ASTNode) -> Any:
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode) -> Any:
        for field_name in getattr(node, '__dataclass_fields__', {}):
            val = getattr(node, field_name)
            if isinstance(val, ASTNode):
                self.visit(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, ASTNode):
                        self.visit(item)
