"""uniVRc ANTLR4 AST Visitor — Converts ANTLR4 parse tree into typed AST nodes."""

import re
from typing import List, Dict, Any, Optional, Tuple, Union

try:
    from .antlr_gen.UniVRcVisitor import UniVRcVisitor
    from .antlr_gen.UniVRcParser import UniVRcParser
    from .ast_nodes import (
        ASTNode, SourceLocation, Program, Statement, Expr, TypeNode,
        PrimitiveType, SizedIntType, FxpType, StructRefType,
        Attribute, Identifier, NumberLit, BoolLit, SizedLit,
        BinaryOp, UnaryOp, ReductionOp, TernaryOp, MemberAccess,
        IndexExpr, SliceExpr, SliceIndexed, ConcatExpr, ReplicationExpr,
        CallExpr, BuiltinCall, CastExpr, InitList,
        Block, VarDecl, AssignStmt, AugAssignStmt, IncDecStmt, CallStmt,
        BreakStmt, ContinueStmt, ReturnStmt, IfStmt, SwitchStmt, SwitchCase,
        ForStmt, WhileStmt, DoWhileStmt, RepeatStmt, AlwaysStmt, SensitivityItem,
        ThreadStmt, InstStmt, PortConn, PortDef, ParamDef, ModuleDef,
        FuncParamDef, FuncDef, StructField, StructDef, EnumEntry, EnumDef,
        TypedefDef, StreamType, StringLit, AssertStmt, DelayStmt, TestbenchDef,
        InterfaceDef, InterfaceItem, StaticStmt, GenerateStmt
    )
except (ImportError, ValueError):
    from antlr_gen.UniVRcVisitor import UniVRcVisitor
    from antlr_gen.UniVRcParser import UniVRcParser
    from ast_nodes import (
        ASTNode, SourceLocation, Program, Statement, Expr, TypeNode,
        PrimitiveType, SizedIntType, FxpType, StructRefType,
        Attribute, Identifier, NumberLit, BoolLit, SizedLit,
        BinaryOp, UnaryOp, ReductionOp, TernaryOp, MemberAccess,
        IndexExpr, SliceExpr, SliceIndexed, ConcatExpr, ReplicationExpr,
        CallExpr, BuiltinCall, CastExpr, InitList,
        Block, VarDecl, AssignStmt, AugAssignStmt, IncDecStmt, CallStmt,
        BreakStmt, ContinueStmt, ReturnStmt, IfStmt, SwitchStmt, SwitchCase,
        ForStmt, WhileStmt, DoWhileStmt, RepeatStmt, AlwaysStmt, SensitivityItem,
        ThreadStmt, InstStmt, PortConn, PortDef, ParamDef, ModuleDef,
        FuncParamDef, FuncDef, StructField, StructDef, EnumEntry, EnumDef,
        TypedefDef, StreamType, StringLit, AssertStmt, DelayStmt, TestbenchDef,
        InterfaceDef, InterfaceItem, StaticStmt, GenerateStmt
    )


class UniVRcASTVisitor(UniVRcVisitor):
    """Translates ANTLR4 CST into strongly-typed AST nodes."""

    def _loc(self, ctx: Any) -> SourceLocation:
        if ctx is None:
            return SourceLocation()
        start = getattr(ctx, 'start', None) or getattr(ctx, 'symbol', None)
        stop = getattr(ctx, 'stop', None) or start
        if start:
            line = getattr(start, 'line', 1) or 1
            col = (getattr(start, 'column', 0) or 0) + 1
            end_line = getattr(stop, 'line', line) if stop else line
            end_col = ((getattr(stop, 'column', col - 1) or 0) + 1) if stop else col
            return SourceLocation(line=line, col=col, end_line=end_line, end_col=end_col)
        return SourceLocation()

    def _parse_sized_lit(self, raw_str: str, loc: SourceLocation) -> SizedLit:
        m = re.match(r"(\d+)'([bBhHdD])([0-9a-fA-F_]+)", raw_str)
        if m:
            width = int(m.group(1))
            base = m.group(2).lower()
            raw = m.group(3)
            clean = raw.replace('_', '')
            val = int(clean, 2 if base == 'b' else 16 if base == 'h' else 10)
            return SizedLit(width=width, base=base, raw=raw, value=val, loc=loc)
        return SizedLit(width=0, base='d', raw=raw_str, value=0, loc=loc)

    # =========================================================================
    # Program & Statement Rules
    # =========================================================================

    def visitProgram(self, ctx: UniVRcParser.ProgramContext) -> Program:
        stmts: List[Statement] = []
        for stmt_ctx in ctx.statement():
            res = self.visit(stmt_ctx)
            if res is not None:
                if isinstance(res, list):
                    stmts.extend(res)
                elif isinstance(res, Statement):
                    stmts.append(res)
        return Program(statements=stmts)

    def visitStatement(self, ctx: UniVRcParser.StatementContext) -> Any:
        # statement can be simpleStmt SEMI, block, structDef, etc. or SEMI
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            # ignore standalone SEMI
            if child.getText() == ';':
                continue
            return self.visit(child)
        return None

    def visitSimpleStmt(self, ctx: UniVRcParser.SimpleStmtContext) -> Any:
        return self.visit(ctx.getChild(0))

    def visitImportStmt(self, ctx: UniVRcParser.ImportStmtContext) -> Any:
        # Imports can be ignored in AST or kept as comment/metadata
        return None

    def visitBlock(self, ctx: UniVRcParser.BlockContext) -> Block:
        attrs = [self.visit(a) for a in ctx.attr()]
        stmts: List[Statement] = []
        for s_ctx in ctx.statement():
            s = self.visit(s_ctx)
            if s is not None:
                if isinstance(s, list):
                    stmts.extend(s)
                elif isinstance(s, Statement):
                    stmts.append(s)
        return Block(statements=stmts, attributes=attrs, loc=self._loc(ctx))

    # =========================================================================
    # Attributes & Pragmas
    # =========================================================================

    def visitAttr(self, ctx: UniVRcParser.AttrContext) -> Attribute:
        # AT_NAME | AT_MODULE | AT_THREAD | AT_PARAM | AT_TESTBENCH
        token_text = ctx.getChild(0).getText()
        # strip leading '@'
        name = token_text[1:].upper() if token_text.startswith('@') else token_text.upper()
        pos_args = []
        named_args = {}
        if ctx.attrArgs():
            args_res = self.visit(ctx.attrArgs())
            if isinstance(args_res, tuple):
                pos_args, named_args = args_res
        return Attribute(name=name, args=named_args, positional_args=pos_args)

    def visitAttrArgs(self, ctx: UniVRcParser.AttrArgsContext) -> Tuple[List[Any], Dict[str, Any]]:
        pos = []
        named = {}
        for arg_ctx in ctx.attrArg():
            res = self.visit(arg_ctx)
            if isinstance(res, tuple) and len(res) == 2 and isinstance(res[0], str):
                named[res[0]] = res[1]
            elif res is not None:
                pos.append(res)
        return (pos, named)

    def visitEdgeAttrArg(self, ctx: UniVRcParser.EdgeAttrArgContext) -> Any:
        # (POSEDGE | NEGEDGE) id -> return Identifier of signal
        edge = ctx.getChild(0).getText().lower()
        sig_name = ctx.id_().getText()
        return Identifier(name=sig_name, loc=self._loc(ctx))

    def visitNamedAttrArg(self, ctx: UniVRcParser.NamedAttrArgContext) -> Tuple[str, Any]:
        name = ctx.id_().getText()
        val = self.visit(ctx.expr())
        return (name, val)

    def visitPositionalAttrArg(self, ctx: UniVRcParser.PositionalAttrArgContext) -> Any:
        return self.visit(ctx.expr())

    # =========================================================================
    # Flow & Simple Statements
    # =========================================================================

    def visitBreakStmtRule(self, ctx: UniVRcParser.BreakStmtRuleContext) -> BreakStmt:
        return BreakStmt()

    def visitContinueStmtRule(self, ctx: UniVRcParser.ContinueStmtRuleContext) -> ContinueStmt:
        return ContinueStmt()

    def visitReturnStmtRule(self, ctx: UniVRcParser.ReturnStmtRuleContext) -> ReturnStmt:
        val = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmt(value=val)

    def visitInstStmt(self, ctx: UniVRcParser.InstStmtContext) -> InstStmt:
        ids = ctx.id_()
        mod_name = ids[0].getText()
        inst_name = ids[1].getText()
        conns = self.visit(ctx.portConnections()) if ctx.portConnections() else []
        return InstStmt(module_name=mod_name, inst_name=inst_name, connections=conns, loc=self._loc(ctx))

    def visitPortConnections(self, ctx: UniVRcParser.PortConnectionsContext) -> List[PortConn]:
        return [self.visit(c) for c in ctx.portConn()]

    def visitNamedPortConn(self, ctx: UniVRcParser.NamedPortConnContext) -> PortConn:
        port_name = ctx.id_().getText()
        expr = self.visit(ctx.expr())
        return PortConn(port_name=port_name, expr=expr, loc=self._loc(ctx))

    def visitPositionalPortConn(self, ctx: UniVRcParser.PositionalPortConnContext) -> PortConn:
        expr = self.visit(ctx.expr())
        return PortConn(port_name=None, expr=expr, loc=self._loc(ctx))

    def visitAssignStmt(self, ctx: UniVRcParser.AssignStmtContext) -> AssignStmt:
        target = self.visit(ctx.lvalue())
        val = self.visit(ctx.expr())
        return AssignStmt(target=target, value=val, is_register=False, loc=self._loc(ctx))

    def visitRegAssignStmt(self, ctx: UniVRcParser.RegAssignStmtContext) -> AssignStmt:
        target = self.visit(ctx.lvalue())
        val = self.visit(ctx.expr())
        return AssignStmt(target=target, value=val, is_register=True, loc=self._loc(ctx))

    def visitAugAssignStmt(self, ctx: UniVRcParser.AugAssignStmtContext) -> AugAssignStmt:
        target = self.visit(ctx.lvalue())
        op = ctx.getChild(1).getText()
        val = self.visit(ctx.expr())
        return AugAssignStmt(target=target, op=op, value=val, is_register=False, loc=self._loc(ctx))

    def visitRegAugAssignStmt(self, ctx: UniVRcParser.RegAugAssignStmtContext) -> AugAssignStmt:
        target = self.visit(ctx.lvalue())
        op = ctx.getChild(1).getText()
        val = self.visit(ctx.expr())
        return AugAssignStmt(target=target, op=op, value=val, is_register=True, loc=self._loc(ctx))

    def visitPreIncDec(self, ctx: UniVRcParser.PreIncDecContext) -> IncDecStmt:
        op = ctx.INCOP().getText()
        target = self.visit(ctx.lvalue())
        return IncDecStmt(target=target, op=op, is_prefix=True, loc=self._loc(ctx))

    def visitPostIncDec(self, ctx: UniVRcParser.PostIncDecContext) -> IncDecStmt:
        target = self.visit(ctx.lvalue())
        op = ctx.INCOP().getText()
        return IncDecStmt(target=target, op=op, is_prefix=False, loc=self._loc(ctx))

    def visitCallStmt(self, ctx: UniVRcParser.CallStmtContext) -> CallStmt:
        func = self.visit(ctx.expr())
        args = self.visit(ctx.exprlist()) if ctx.exprlist() else []
        return CallStmt(call=CallExpr(func=func, args=args, loc=self._loc(ctx)), loc=self._loc(ctx))

    # =========================================================================
    # L-Values
    # =========================================================================

    def visitLValueId(self, ctx: UniVRcParser.LValueIdContext) -> Identifier:
        return Identifier(name=ctx.id_().getText(), loc=self._loc(ctx))

    def visitLValueMember(self, ctx: UniVRcParser.LValueMemberContext) -> MemberAccess:
        base = self.visit(ctx.lvalue())
        member = ctx.id_().getText()
        return MemberAccess(base=base, member=member, loc=self._loc(ctx))

    def visitLValueIndex(self, ctx: UniVRcParser.LValueIndexContext) -> IndexExpr:
        base = self.visit(ctx.lvalue())
        idx = self.visit(ctx.expr())
        return IndexExpr(base=base, index=idx, loc=self._loc(ctx))

    def visitLValueSlice(self, ctx: UniVRcParser.LValueSliceContext) -> SliceExpr:
        base = self.visit(ctx.lvalue())
        exprs = ctx.expr()
        msb = self.visit(exprs[0])
        lsb = self.visit(exprs[1])
        return SliceExpr(base=base, msb=msb, lsb=lsb, step=None, loc=self._loc(ctx))

    def visitLValueSliceStep(self, ctx: UniVRcParser.LValueSliceStepContext) -> SliceExpr:
        base = self.visit(ctx.lvalue())
        exprs = ctx.expr()
        msb = self.visit(exprs[0])
        lsb = self.visit(exprs[1])
        step = self.visit(exprs[2])
        return SliceExpr(base=base, msb=msb, lsb=lsb, step=step, loc=self._loc(ctx))

    def visitLValueSlicePlus(self, ctx: UniVRcParser.LValueSlicePlusContext) -> SliceIndexed:
        base = self.visit(ctx.lvalue())
        exprs = ctx.expr()
        idx = self.visit(exprs[0])
        width = self.visit(exprs[1])
        return SliceIndexed(base=base, index=idx, width=width, is_plus=True, loc=self._loc(ctx))

    def visitLValueSliceMinus(self, ctx: UniVRcParser.LValueSliceMinusContext) -> SliceIndexed:
        base = self.visit(ctx.lvalue())
        exprs = ctx.expr()
        idx = self.visit(exprs[0])
        width = self.visit(exprs[1])
        return SliceIndexed(base=base, index=idx, width=width, is_plus=False, loc=self._loc(ctx))

    def visitLValueConcat(self, ctx: UniVRcParser.LValueConcatContext) -> ConcatExpr:
        elements = [self.visit(lv) for lv in ctx.lvalueList().lvalue()]
        return ConcatExpr(elements=elements, loc=self._loc(ctx))

    # =========================================================================
    # Declarations & Types
    # =========================================================================

    def visitVarInferred(self, ctx: UniVRcParser.VarInferredContext) -> VarDecl:
        attrs = [self.visit(a) for a in ctx.attr()]
        name = ctx.id_().getText()
        init = self.visit(ctx.expr())
        return VarDecl(name=name, type_desc=None, array_dims=[], initializer=init, is_const=False, is_var=True, attributes=attrs, loc=self._loc(ctx))

    def visitVarExplicit(self, ctx: UniVRcParser.VarExplicitContext) -> VarDecl:
        attrs = [self.visit(a) for a in ctx.attr()]
        is_const = ctx.CONST() is not None
        type_desc = self.visit(ctx.typeDesc())
        name = ctx.id_().getText()
        dims = self.visit(ctx.arrayDims()) if ctx.arrayDims() else []
        init = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(name=name, type_desc=type_desc, array_dims=dims, initializer=init, is_const=is_const, attributes=attrs, loc=self._loc(ctx))

    def visitArrayDims(self, ctx: UniVRcParser.ArrayDimsContext) -> List[Expr]:
        return [self.visit(e) for e in ctx.expr()]

    def visitTypeInt(self, ctx: UniVRcParser.TypeIntContext) -> PrimitiveType:
        return PrimitiveType(name="int")

    def visitTypeFloat(self, ctx: UniVRcParser.TypeFloatContext) -> PrimitiveType:
        return PrimitiveType(name="float")

    def visitTypeBool(self, ctx: UniVRcParser.TypeBoolContext) -> PrimitiveType:
        return PrimitiveType(name="bool")

    def visitTypeReg(self, ctx: UniVRcParser.TypeRegContext) -> PrimitiveType:
        return PrimitiveType(name="reg")

    def visitTypeWire(self, ctx: UniVRcParser.TypeWireContext) -> PrimitiveType:
        return PrimitiveType(name="wire")

    def visitTypeSigned(self, ctx: UniVRcParser.TypeSignedContext) -> SizedIntType:
        w = self.visit(ctx.expr())
        return SizedIntType(is_signed=True, width=w)

    def visitTypeUnsigned(self, ctx: UniVRcParser.TypeUnsignedContext) -> SizedIntType:
        w = self.visit(ctx.expr())
        return SizedIntType(is_signed=False, width=w)

    def visitTypeFxp(self, ctx: UniVRcParser.TypeFxpContext) -> FxpType:
        exprs = ctx.expr()
        w = self.visit(exprs[0])
        frac = self.visit(exprs[1])
        return FxpType(width=w, frac=frac)

    def visitTypeStream(self, ctx: UniVRcParser.TypeStreamContext) -> StreamType:
        elem = self.visit(ctx.typeDesc())
        depth = self.visit(ctx.expr()) if ctx.expr() else None
        return StreamType(elem_type=elem, depth=depth, is_fifo=False)

    def visitTypeFifo(self, ctx: UniVRcParser.TypeFifoContext) -> StreamType:
        elem = self.visit(ctx.typeDesc())
        depth = self.visit(ctx.expr()) if ctx.expr() else None
        return StreamType(elem_type=elem, depth=depth, is_fifo=True)

    def visitTypeStructRef(self, ctx: UniVRcParser.TypeStructRefContext) -> StructRefType:
        return StructRefType(name=ctx.id_().getText())

    # =========================================================================
    # Structs, Enums, Typedefs
    # =========================================================================

    def visitStructDef(self, ctx: UniVRcParser.StructDefContext) -> StructDef:
        name = ctx.id_().getText()
        fields = [self.visit(f) for f in ctx.structField()]
        return StructDef(name=name, fields=fields, loc=self._loc(ctx))

    def visitStructField(self, ctx: UniVRcParser.StructFieldContext) -> StructField:
        td = self.visit(ctx.typeDesc())
        name = ctx.id_().getText()
        dims = self.visit(ctx.arrayDims()) if ctx.arrayDims() else []
        return StructField(type_desc=td, name=name, array_dims=dims, loc=self._loc(ctx))

    def visitEnumDef(self, ctx: UniVRcParser.EnumDefContext) -> EnumDef:
        name = ctx.id_().getText()
        width = self.visit(ctx.expr()) if ctx.expr() else None
        entries = self.visit(ctx.enumList()) if ctx.enumList() else []
        return EnumDef(name=name, width=width, entries=entries, loc=self._loc(ctx))

    def visitEnumList(self, ctx: UniVRcParser.EnumListContext) -> List[EnumEntry]:
        return [self.visit(e) for e in ctx.enumEntry()]

    def visitEnumEntry(self, ctx: UniVRcParser.EnumEntryContext) -> EnumEntry:
        name = ctx.id_().getText()
        val = self.visit(ctx.expr()) if ctx.expr() else None
        return EnumEntry(name=name, value=val, loc=self._loc(ctx))

    def visitTypedefDef(self, ctx: UniVRcParser.TypedefDefContext) -> TypedefDef:
        td = self.visit(ctx.typeDesc())
        name = ctx.id_().getText()
        dims = self.visit(ctx.arrayDims()) if ctx.arrayDims() else []
        return TypedefDef(type_desc=td, name=name, array_dims=dims, loc=self._loc(ctx))

    # =========================================================================
    # Parameters, Modules, Functions
    # =========================================================================

    def visitParamSection(self, ctx: UniVRcParser.ParamSectionContext) -> List[ParamDef]:
        return self.visit(ctx.paramList()) if ctx.paramList() else []

    def visitParamList(self, ctx: UniVRcParser.ParamListContext) -> List[ParamDef]:
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx: UniVRcParser.ParamContext) -> ParamDef:
        name = ctx.id_().getText()
        val = self.visit(ctx.expr()) if ctx.expr() else None
        return ParamDef(name=name, value=val, loc=self._loc(ctx))

    def visitModuleDef(self, ctx: UniVRcParser.ModuleDefContext) -> ModuleDef:
        attrs = [self.visit(a) for a in ctx.attr()]
        params = self.visit(ctx.paramSection()) if ctx.paramSection() else []
        name = ctx.id_().getText()
        ports = self.visit(ctx.moduleParams()) if ctx.moduleParams() else []
        body = self.visit(ctx.block())
        return ModuleDef(name=name, ports=ports, params=params, body=body, attributes=attrs, loc=self._loc(ctx))

    def visitModuleParams(self, ctx: UniVRcParser.ModuleParamsContext) -> List[PortDef]:
        return [self.visit(p) for p in ctx.moduleParam()]

    def visitModuleParam(self, ctx: UniVRcParser.ModuleParamContext) -> PortDef:
        pdir = ctx.portDir().getText()
        ptype = self.visit(ctx.typeDesc())
        name = ctx.id_().getText()
        dims = self.visit(ctx.arrayDims()) if ctx.arrayDims() else []
        init = self.visit(ctx.expr()) if ctx.expr() else None
        return PortDef(direction=pdir, type_desc=ptype, name=name, array_dims=dims, default_val=init, loc=self._loc(ctx))

    def visitFuncDefPrefixType(self, ctx: UniVRcParser.FuncDefPrefixTypeContext) -> FuncDef:
        attrs = [self.visit(a) for a in ctx.attr()]
        params_sec = self.visit(ctx.paramSection()) if ctx.paramSection() else []
        ret_type = self.visit(ctx.typeDesc())
        name = ctx.id_().getText()
        func_params = self.visit(ctx.funcParams()) if ctx.funcParams() else []
        body = self.visit(ctx.block())
        return FuncDef(name=name, params=func_params, return_type=ret_type, body=body, params_section=params_sec, attributes=attrs, loc=self._loc(ctx))

    def visitFuncDefPostfixType(self, ctx: UniVRcParser.FuncDefPostfixTypeContext) -> FuncDef:
        attrs = [self.visit(a) for a in ctx.attr()]
        params_sec = self.visit(ctx.paramSection()) if ctx.paramSection() else []
        ret_type = self.visit(ctx.typeDesc()) if ctx.typeDesc() else None
        name = ctx.id_().getText()
        func_params = self.visit(ctx.funcParams()) if ctx.funcParams() else []
        body = self.visit(ctx.block())
        return FuncDef(name=name, params=func_params, return_type=ret_type, body=body, params_section=params_sec, attributes=attrs, loc=self._loc(ctx))

    def visitInterfaceDef(self, ctx: UniVRcParser.InterfaceDefContext) -> InterfaceDef:
        attrs = [self.visit(a) for a in ctx.attr()]
        name = ctx.id_().getText()
        generics = self.visit(ctx.paramList()) if ctx.paramList() else []
        items = [self.visit(item) for item in ctx.interfaceItem()]
        return InterfaceDef(name=name, generics=generics, items=items, attributes=attrs, loc=self._loc(ctx))

    def visitInterfaceItem(self, ctx: UniVRcParser.InterfaceItemContext) -> InterfaceItem:
        if ctx.varDecl():
            vd = self.visit(ctx.varDecl())
            return InterfaceItem(var_decl=vd, loc=self._loc(ctx))
        pdir = ctx.portDir().getText() if ctx.portDir() else None
        ptype = self.visit(ctx.typeDesc()) if ctx.typeDesc() else None
        name = ctx.id_().getText() if ctx.id_() else ""
        dims = self.visit(ctx.arrayDims()) if ctx.arrayDims() else []
        init = self.visit(ctx.expr()) if ctx.expr() else None
        return InterfaceItem(direction=pdir, type_desc=ptype, name=name, array_dims=dims, default_val=init, loc=self._loc(ctx))

    def visitStaticStmt(self, ctx: UniVRcParser.StaticStmtContext) -> StaticStmt:
        body = self.visitChildren(ctx)
        return StaticStmt(body=body, loc=self._loc(ctx))

    def visitFuncParams(self, ctx: UniVRcParser.FuncParamsContext) -> List[FuncParamDef]:
        return [self.visit(p) for p in ctx.funcParam()]

    def visitFuncParam(self, ctx: UniVRcParser.FuncParamContext) -> FuncParamDef:
        ptype = self.visit(ctx.typeDesc())
        name = ctx.id_().getText()
        dims = self.visit(ctx.arrayDims()) if ctx.arrayDims() else []
        init = self.visit(ctx.expr()) if ctx.expr() else None
        return FuncParamDef(type_desc=ptype, name=name, array_dims=dims, default_val=init, loc=self._loc(ctx))

    def visitTestbenchDef(self, ctx: UniVRcParser.TestbenchDefContext) -> TestbenchDef:
        attrs = [self.visit(a) for a in ctx.attr()]
        name = ctx.id_().getText()
        params = self.visit(ctx.funcParams()) if ctx.funcParams() else []
        body = self.visit(ctx.block())
        return TestbenchDef(name=name, params=params, body=body, attributes=attrs, loc=self._loc(ctx))

    def visitAssertStmt(self, ctx: UniVRcParser.AssertStmtContext) -> AssertStmt:
        exprs = ctx.expr()
        cond = self.visit(exprs[0]) if len(exprs) > 0 else Expr()
        msg = self.visit(exprs[1]) if len(exprs) > 1 else None
        return AssertStmt(cond=cond, message=msg, loc=self._loc(ctx))

    def visitDelayStmt(self, ctx: UniVRcParser.DelayStmtContext) -> DelayStmt:
        cycles = self.visit(ctx.expr()) if ctx.expr() else Expr()
        return DelayStmt(cycles=cycles, loc=self._loc(ctx))

    def visitThreadStmt(self, ctx: UniVRcParser.ThreadStmtContext) -> ThreadStmt:
        stmts = []
        for s in ctx.statement():
            res = self.visit(s)
            if res is not None:
                if isinstance(res, list):
                    stmts.extend(res)
                elif isinstance(res, Statement):
                    stmts.append(res)
        return ThreadStmt(body=stmts)

    # =========================================================================
    # Control Flow
    # =========================================================================

    def visitIfStmt(self, ctx: UniVRcParser.IfStmtContext) -> IfStmt:
        attrs = [self.visit(a) for a in ctx.attr()]
        cond = self.visit(ctx.expr())
        then_block = self.visit(ctx.block())
        elifs = [self.visit(e) for e in ctx.elifClause()]
        else_block = self.visit(ctx.elseClause()) if ctx.elseClause() else None
        return IfStmt(cond=cond, then_block=then_block, elifs=elifs, else_block=else_block, attributes=attrs, loc=self._loc(ctx))

    def visitElifClause(self, ctx: UniVRcParser.ElifClauseContext) -> Tuple[Expr, Block]:
        cond = self.visit(ctx.expr())
        blk = self.visit(ctx.block())
        return (cond, blk)

    def visitElseClause(self, ctx: UniVRcParser.ElseClauseContext) -> Block:
        return self.visit(ctx.block())

    def visitSwitchStmt(self, ctx: UniVRcParser.SwitchStmtContext) -> SwitchStmt:
        attrs = [self.visit(a) for a in ctx.attr()]
        cond = self.visit(ctx.expr())
        cases = [self.visit(c) for c in ctx.caseClause()]
        def_blk = self.visit(ctx.defaultClause()) if ctx.defaultClause() else None
        return SwitchStmt(expr=cond, cases=cases, default_block=def_blk, attributes=attrs, loc=self._loc(ctx))

    def visitCaseClause(self, ctx: UniVRcParser.CaseClauseContext) -> SwitchCase:
        vals = self.visit(ctx.exprlist()) if ctx.exprlist() else []
        blk = self.visit(ctx.block())
        return SwitchCase(values=vals, body=blk, loc=self._loc(ctx))

    def visitDefaultClause(self, ctx: UniVRcParser.DefaultClauseContext) -> Block:
        return self.visit(ctx.block())

    def visitForStmt(self, ctx: UniVRcParser.ForStmtContext) -> ForStmt:
        attrs = [self.visit(a) for a in ctx.attr()]
        cfg = self.visit(ctx.forConfig())
        body = self.visit(ctx.block())
        return ForStmt(
            kind=cfg.get('kind', 'cstyle'),
            iterator=cfg.get('iterator'),
            start=cfg.get('start'),
            end=cfg.get('end'),
            step=cfg.get('step'),
            set_items=cfg.get('set_items'),
            init_stmt=cfg.get('init_stmt'),
            cond_expr=cfg.get('cond_expr'),
            step_stmt=cfg.get('step_stmt'),
            body=body,
            attributes=attrs,
            loc=self._loc(ctx)
        )

    def visitForConfig(self, ctx: UniVRcParser.ForConfigContext) -> Dict[str, Any]:
        return self.visit(ctx.getChild(0))

    def visitForStandardC(self, ctx: UniVRcParser.ForStandardCContext) -> Dict[str, Any]:
        init_stmt = self.visit(ctx.forInit()) if ctx.forInit() else None
        cond_expr = self.visit(ctx.expr()) if ctx.expr() else None
        step_stmt = self.visit(ctx.forStep()) if ctx.forStep() else None

        it_name = None
        start = None
        end = None
        step = None

        if isinstance(init_stmt, VarDecl):
            it_name = init_stmt.name
            start = init_stmt.initializer
        elif isinstance(init_stmt, AssignStmt) and isinstance(init_stmt.target, Identifier):
            it_name = init_stmt.target.name
            start = init_stmt.value

        if isinstance(cond_expr, BinaryOp) and cond_expr.op in ('<', '<=', '>', '>='):
            end = cond_expr.right

        if isinstance(step_stmt, IncDecStmt):
            step = NumberLit(value=1 if step_stmt.op == '++' else -1, raw="1" if step_stmt.op == '++' else "-1")
        elif isinstance(step_stmt, (AugAssignStmt, AssignStmt)):
            step = step_stmt.value

        return {
            'kind': 'standard_c',
            'iterator': it_name,
            'start': start,
            'end': end,
            'step': step,
            'init_stmt': init_stmt,
            'cond_expr': cond_expr,
            'step_stmt': step_stmt
        }

    def visitForInit(self, ctx: UniVRcParser.ForInitContext) -> Any:
        return self.visit(ctx.getChild(0))

    def visitForStep(self, ctx: UniVRcParser.ForStepContext) -> Any:
        return self.visit(ctx.getChild(0))

    def visitForIterRange(self, ctx: UniVRcParser.ForIterRangeContext) -> Dict[str, Any]:
        it_name = ctx.id_().getText()
        exprs = self.visit(ctx.exprlist()) if ctx.exprlist() else []
        start = exprs[0] if len(exprs) > 0 else None
        end = exprs[1] if len(exprs) > 1 else None
        return {'kind': 'iter_range', 'iterator': it_name, 'start': start, 'end': end}

    def visitForIterSet(self, ctx: UniVRcParser.ForIterSetContext) -> Dict[str, Any]:
        it_name = ctx.id_().getText()
        exprs = self.visit(ctx.exprlist()) if ctx.exprlist() else []
        return {'kind': 'iter_set', 'iterator': it_name, 'set_items': exprs}

    def visitForCStyleExplicit(self, ctx: UniVRcParser.ForCStyleExplicitContext) -> Dict[str, Any]:
        exprs = [self.visit(e) for e in ctx.expr()]
        start = exprs[0] if len(exprs) > 0 else None
        end = exprs[1] if len(exprs) > 1 else None
        step = exprs[2] if len(exprs) > 2 else None
        return {'kind': 'cstyle', 'start': start, 'end': end, 'step': step}

    def visitForCStyleRange(self, ctx: UniVRcParser.ForCStyleRangeContext) -> Dict[str, Any]:
        exprs = [self.visit(e) for e in ctx.expr()]
        start = exprs[0] if len(exprs) > 0 else None
        end = exprs[1] if len(exprs) > 1 else None
        step = exprs[2] if len(exprs) > 2 else None
        return {'kind': 'cstyle', 'start': start, 'end': end, 'step': step}

    def visitWhileStmt(self, ctx: UniVRcParser.WhileStmtContext) -> WhileStmt:
        attrs = [self.visit(a) for a in ctx.attr()]
        cond = self.visit(ctx.expr())
        body = self.visit(ctx.block())
        return WhileStmt(cond=cond, body=body, attributes=attrs, loc=self._loc(ctx))

    def visitDoWhileStmt(self, ctx: UniVRcParser.DoWhileStmtContext) -> DoWhileStmt:
        attrs = [self.visit(a) for a in ctx.attr()]
        body = self.visit(ctx.block())
        cond = self.visit(ctx.expr())
        return DoWhileStmt(cond=cond, body=body, attributes=attrs, loc=self._loc(ctx))

    def visitRepeatStmt(self, ctx: UniVRcParser.RepeatStmtContext) -> RepeatStmt:
        attrs = [self.visit(a) for a in ctx.attr()]
        cnt = self.visit(ctx.expr())
        body = self.visit(ctx.block())
        return RepeatStmt(count=cnt, body=body, attributes=attrs, loc=self._loc(ctx))

    # =========================================================================
    # Expressions
    # =========================================================================

    def visitTernaryExpr(self, ctx: UniVRcParser.TernaryExprContext) -> TernaryOp:
        exprs = ctx.expr()
        cond = self.visit(exprs[0])
        true_e = self.visit(exprs[1])
        false_e = self.visit(exprs[2])
        return TernaryOp(cond=cond, true_expr=true_e, false_expr=false_e, loc=self._loc(ctx))

    def visitLogicOrExpr(self, ctx: UniVRcParser.LogicOrExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        return BinaryOp(op='or', left=left, right=right, loc=self._loc(ctx))

    def visitLogicXorExpr(self, ctx: UniVRcParser.LogicXorExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        return BinaryOp(op='xor', left=left, right=right, loc=self._loc(ctx))

    def visitLogicAndExpr(self, ctx: UniVRcParser.LogicAndExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        return BinaryOp(op='and', left=left, right=right, loc=self._loc(ctx))

    def visitBitOrExpr(self, ctx: UniVRcParser.BitOrExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        return BinaryOp(op='|', left=left, right=right, loc=self._loc(ctx))

    def visitBitXorExpr(self, ctx: UniVRcParser.BitXorExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        op = ctx.getChild(1).getText()
        return BinaryOp(op=op, left=left, right=right, loc=self._loc(ctx))

    def visitBitAndExpr(self, ctx: UniVRcParser.BitAndExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        return BinaryOp(op='&', left=left, right=right, loc=self._loc(ctx))

    def visitEqualityExpr(self, ctx: UniVRcParser.EqualityExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        op = ctx.getChild(1).getText()
        return BinaryOp(op=op, left=left, right=right, loc=self._loc(ctx))

    def visitRelationalExpr(self, ctx: UniVRcParser.RelationalExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        op = ctx.getChild(1).getText()
        return BinaryOp(op=op, left=left, right=right, loc=self._loc(ctx))

    def visitShiftExpr(self, ctx: UniVRcParser.ShiftExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        op = ctx.shiftOp().getText()
        return BinaryOp(op=op, left=left, right=right, loc=self._loc(ctx))

    def visitAddExpr(self, ctx: UniVRcParser.AddExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        op = ctx.getChild(1).getText()
        return BinaryOp(op=op, left=left, right=right, loc=self._loc(ctx))

    def visitMulExpr(self, ctx: UniVRcParser.MulExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        op = ctx.getChild(1).getText()
        return BinaryOp(op=op, left=left, right=right, loc=self._loc(ctx))

    def visitPowerExpr(self, ctx: UniVRcParser.PowerExprContext) -> BinaryOp:
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        return BinaryOp(op='**', left=left, right=right, loc=self._loc(ctx))

    def visitUnaryExpr(self, ctx: UniVRcParser.UnaryExprContext) -> UnaryOp:
        op = ctx.getChild(0).getText()
        operand = self.visit(ctx.expr())
        return UnaryOp(op=op, operand=operand, loc=self._loc(ctx))

    def visitReductionExpr(self, ctx: UniVRcParser.ReductionExprContext) -> ReductionOp:
        op = ctx.RED_OP().getText()
        operand = self.visit(ctx.expr())
        return ReductionOp(op=op, operand=operand, loc=self._loc(ctx))

    def visitCallExpr(self, ctx: UniVRcParser.CallExprContext) -> CallExpr:
        func = self.visit(ctx.expr())
        args = self.visit(ctx.exprlist()) if ctx.exprlist() else []
        return CallExpr(func=func, args=args, loc=self._loc(ctx))

    def visitMemberAccessExpr(self, ctx: UniVRcParser.MemberAccessExprContext) -> MemberAccess:
        base = self.visit(ctx.expr())
        member = ctx.id_().getText()
        return MemberAccess(base=base, member=member, loc=self._loc(ctx))

    def visitIndexExpr(self, ctx: UniVRcParser.IndexExprContext) -> IndexExpr:
        exprs = ctx.expr()
        base = self.visit(exprs[0])
        idx = self.visit(exprs[1])
        return IndexExpr(base=base, index=idx, loc=self._loc(ctx))

    def visitSliceExpr(self, ctx: UniVRcParser.SliceExprContext) -> SliceExpr:
        exprs = ctx.expr()
        base = self.visit(exprs[0])
        msb = self.visit(exprs[1])
        lsb = self.visit(exprs[2])
        return SliceExpr(base=base, msb=msb, lsb=lsb, step=None, loc=self._loc(ctx))

    def visitSliceStepExpr(self, ctx: UniVRcParser.SliceStepExprContext) -> SliceExpr:
        exprs = ctx.expr()
        base = self.visit(exprs[0])
        msb = self.visit(exprs[1])
        lsb = self.visit(exprs[2])
        step = self.visit(exprs[3])
        return SliceExpr(base=base, msb=msb, lsb=lsb, step=step, loc=self._loc(ctx))

    def visitSlicePlusExpr(self, ctx: UniVRcParser.SlicePlusExprContext) -> SliceIndexed:
        exprs = ctx.expr()
        base = self.visit(exprs[0])
        idx = self.visit(exprs[1])
        width = self.visit(exprs[2])
        return SliceIndexed(base=base, index=idx, width=width, is_plus=True, loc=self._loc(ctx))

    def visitSliceMinusExpr(self, ctx: UniVRcParser.SliceMinusExprContext) -> SliceIndexed:
        exprs = ctx.expr()
        base = self.visit(exprs[0])
        idx = self.visit(exprs[1])
        width = self.visit(exprs[2])
        return SliceIndexed(base=base, index=idx, width=width, is_plus=False, loc=self._loc(ctx))

    def visitPrimaryExpr(self, ctx: UniVRcParser.PrimaryExprContext) -> Any:
        return self.visit(ctx.primary())

    # =========================================================================
    # Primary & Literals
    # =========================================================================

    def visitParenExpr(self, ctx: UniVRcParser.ParenExprContext) -> Any:
        return self.visit(ctx.expr())

    def visitNumberLitExpr(self, ctx: UniVRcParser.NumberLitExprContext) -> NumberLit:
        raw = ctx.NUMBER().getText()
        val = float(raw) if '.' in raw else int(raw)
        return NumberLit(value=val, raw=raw, loc=self._loc(ctx))

    def visitBoolLitExpr(self, ctx: UniVRcParser.BoolLitExprContext) -> BoolLit:
        val = ctx.getText() == "true"
        return BoolLit(value=val, loc=self._loc(ctx))

    def visitStringLitExpr(self, ctx: UniVRcParser.StringLitExprContext) -> StringLit:
        raw = ctx.STRING().getText()
        val = raw[1:-1] if len(raw) >= 2 else raw
        return StringLit(value=val, raw=raw, loc=self._loc(ctx))

    def visitSizedBinExpr(self, ctx: UniVRcParser.SizedBinExprContext) -> SizedLit:
        raw = ctx.SIZED_BIN().getText()
        return self._parse_sized_lit(raw, self._loc(ctx))

    def visitSizedHexExpr(self, ctx: UniVRcParser.SizedHexExprContext) -> SizedLit:
        raw = ctx.SIZED_HEX().getText()
        return self._parse_sized_lit(raw, self._loc(ctx))

    def visitSizedDecExpr(self, ctx: UniVRcParser.SizedDecExprContext) -> SizedLit:
        raw = ctx.SIZED_DEC().getText()
        return self._parse_sized_lit(raw, self._loc(ctx))

    def visitCastExprRule(self, ctx: UniVRcParser.CastExprRuleContext) -> CastExpr:
        td = self.visit(ctx.typeDesc())
        expr = self.visit(ctx.expr())
        return CastExpr(target_type=td, expr=expr, loc=self._loc(ctx))

    def visitBuiltinCallExpr(self, ctx: UniVRcParser.BuiltinCallExprContext) -> BuiltinCall:
        return self.visit(ctx.builtinCall())

    def visitBuiltinCall(self, ctx: UniVRcParser.BuiltinCallContext) -> BuiltinCall:
        name = ctx.builtinName().getText()
        args = self.visit(ctx.exprlist()) if ctx.exprlist() else []
        return BuiltinCall(name=name, args=args, loc=self._loc(ctx))

    def visitConcatPrimaryExpr(self, ctx: UniVRcParser.ConcatPrimaryExprContext) -> Any:
        return self.visit(ctx.concatExpr())

    def visitConcatList(self, ctx: UniVRcParser.ConcatListContext) -> ConcatExpr:
        elems = self.visit(ctx.exprlist()) if ctx.exprlist() else []
        return ConcatExpr(elements=elems, loc=self._loc(ctx))

    def visitConcatRep(self, ctx: UniVRcParser.ConcatRepContext) -> ReplicationExpr:
        exprs = ctx.expr()
        cnt = self.visit(exprs[0])
        val = self.visit(exprs[1])
        return ReplicationExpr(count=cnt, value=val, loc=self._loc(ctx))

    def visitInitListExpr(self, ctx: UniVRcParser.InitListExprContext) -> InitList:
        return self.visit(ctx.initList())

    def visitInitList(self, ctx: UniVRcParser.InitListContext) -> InitList:
        elems = [self.visit(e) for e in ctx.initElement()]
        return InitList(elements=elems)

    def visitNamedInit(self, ctx: UniVRcParser.NamedInitContext) -> Tuple[str, Expr]:
        name = ctx.id_().getText()
        val = self.visit(ctx.expr())
        return (name, val)

    def visitIndexedInit(self, ctx: UniVRcParser.IndexedInitContext) -> Tuple[Expr, Expr]:
        idx = self.visit(ctx.expr(0))
        val = self.visit(ctx.expr(1))
        return (idx, val)

    def visitPositionalInit(self, ctx: UniVRcParser.PositionalInitContext) -> Any:
        return self.visit(ctx.expr())

    def visitNestedInit(self, ctx: UniVRcParser.NestedInitContext) -> Any:
        return self.visit(ctx.initList())

    def visitIdExpr(self, ctx: UniVRcParser.IdExprContext) -> Identifier:
        return Identifier(name=ctx.id_().getText(), loc=self._loc(ctx))

    def visitExprlist(self, ctx: UniVRcParser.ExprlistContext) -> List[Expr]:
        return [self.visit(e) for e in ctx.expr()]

    def visitId(self, ctx: UniVRcParser.IdContext) -> str:
        return ctx.getText()
