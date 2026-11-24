# Generated from /mnt/d/UT.CE/CAD/univrc/HLS/univrc-hls/src/frontend/UniVRc.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .UniVRcParser import UniVRcParser
else:
    from UniVRcParser import UniVRcParser

# This class defines a complete generic visitor for a parse tree produced by UniVRcParser.

class UniVRcVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by UniVRcParser#program.
    def visitProgram(self, ctx:UniVRcParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#statement.
    def visitStatement(self, ctx:UniVRcParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#simpleStmt.
    def visitSimpleStmt(self, ctx:UniVRcParser.SimpleStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#importStmt.
    def visitImportStmt(self, ctx:UniVRcParser.ImportStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#block.
    def visitBlock(self, ctx:UniVRcParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#attr.
    def visitAttr(self, ctx:UniVRcParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#attrArgs.
    def visitAttrArgs(self, ctx:UniVRcParser.AttrArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#EdgeAttrArg.
    def visitEdgeAttrArg(self, ctx:UniVRcParser.EdgeAttrArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#NamedAttrArg.
    def visitNamedAttrArg(self, ctx:UniVRcParser.NamedAttrArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#PositionalAttrArg.
    def visitPositionalAttrArg(self, ctx:UniVRcParser.PositionalAttrArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#BreakStmtRule.
    def visitBreakStmtRule(self, ctx:UniVRcParser.BreakStmtRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ContinueStmtRule.
    def visitContinueStmtRule(self, ctx:UniVRcParser.ContinueStmtRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ReturnStmtRule.
    def visitReturnStmtRule(self, ctx:UniVRcParser.ReturnStmtRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#instStmt.
    def visitInstStmt(self, ctx:UniVRcParser.InstStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#portConnections.
    def visitPortConnections(self, ctx:UniVRcParser.PortConnectionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#NamedPortConn.
    def visitNamedPortConn(self, ctx:UniVRcParser.NamedPortConnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#PositionalPortConn.
    def visitPositionalPortConn(self, ctx:UniVRcParser.PositionalPortConnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#assignStmt.
    def visitAssignStmt(self, ctx:UniVRcParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#regAssignStmt.
    def visitRegAssignStmt(self, ctx:UniVRcParser.RegAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#augAssignStmt.
    def visitAugAssignStmt(self, ctx:UniVRcParser.AugAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#regAugAssignStmt.
    def visitRegAugAssignStmt(self, ctx:UniVRcParser.RegAugAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#PreIncDec.
    def visitPreIncDec(self, ctx:UniVRcParser.PreIncDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#PostIncDec.
    def visitPostIncDec(self, ctx:UniVRcParser.PostIncDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#callStmt.
    def visitCallStmt(self, ctx:UniVRcParser.CallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LValueMember.
    def visitLValueMember(self, ctx:UniVRcParser.LValueMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LValueIndex.
    def visitLValueIndex(self, ctx:UniVRcParser.LValueIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LValueSliceStep.
    def visitLValueSliceStep(self, ctx:UniVRcParser.LValueSliceStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LValueSlice.
    def visitLValueSlice(self, ctx:UniVRcParser.LValueSliceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LValueSlicePlus.
    def visitLValueSlicePlus(self, ctx:UniVRcParser.LValueSlicePlusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LValueSliceMinus.
    def visitLValueSliceMinus(self, ctx:UniVRcParser.LValueSliceMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LValueId.
    def visitLValueId(self, ctx:UniVRcParser.LValueIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#VarInferred.
    def visitVarInferred(self, ctx:UniVRcParser.VarInferredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#VarExplicit.
    def visitVarExplicit(self, ctx:UniVRcParser.VarExplicitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#assignOp.
    def visitAssignOp(self, ctx:UniVRcParser.AssignOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#arrayDims.
    def visitArrayDims(self, ctx:UniVRcParser.ArrayDimsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeInt.
    def visitTypeInt(self, ctx:UniVRcParser.TypeIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeFloat.
    def visitTypeFloat(self, ctx:UniVRcParser.TypeFloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeBool.
    def visitTypeBool(self, ctx:UniVRcParser.TypeBoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeReg.
    def visitTypeReg(self, ctx:UniVRcParser.TypeRegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeWire.
    def visitTypeWire(self, ctx:UniVRcParser.TypeWireContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeSigned.
    def visitTypeSigned(self, ctx:UniVRcParser.TypeSignedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeUnsigned.
    def visitTypeUnsigned(self, ctx:UniVRcParser.TypeUnsignedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeFxp.
    def visitTypeFxp(self, ctx:UniVRcParser.TypeFxpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeStream.
    def visitTypeStream(self, ctx:UniVRcParser.TypeStreamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeFifo.
    def visitTypeFifo(self, ctx:UniVRcParser.TypeFifoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TypeStructRef.
    def visitTypeStructRef(self, ctx:UniVRcParser.TypeStructRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#structDef.
    def visitStructDef(self, ctx:UniVRcParser.StructDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#structField.
    def visitStructField(self, ctx:UniVRcParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#enumDef.
    def visitEnumDef(self, ctx:UniVRcParser.EnumDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#enumList.
    def visitEnumList(self, ctx:UniVRcParser.EnumListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#enumEntry.
    def visitEnumEntry(self, ctx:UniVRcParser.EnumEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#typedefDef.
    def visitTypedefDef(self, ctx:UniVRcParser.TypedefDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#paramSection.
    def visitParamSection(self, ctx:UniVRcParser.ParamSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#paramList.
    def visitParamList(self, ctx:UniVRcParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#param.
    def visitParam(self, ctx:UniVRcParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#moduleDef.
    def visitModuleDef(self, ctx:UniVRcParser.ModuleDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#moduleParams.
    def visitModuleParams(self, ctx:UniVRcParser.ModuleParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#moduleParam.
    def visitModuleParam(self, ctx:UniVRcParser.ModuleParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#portDir.
    def visitPortDir(self, ctx:UniVRcParser.PortDirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#FuncDefWithAttr.
    def visitFuncDefWithAttr(self, ctx:UniVRcParser.FuncDefWithAttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#FuncDefWithType.
    def visitFuncDefWithType(self, ctx:UniVRcParser.FuncDefWithTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#FuncDefStandard.
    def visitFuncDefStandard(self, ctx:UniVRcParser.FuncDefStandardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#funcParams.
    def visitFuncParams(self, ctx:UniVRcParser.FuncParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#funcParam.
    def visitFuncParam(self, ctx:UniVRcParser.FuncParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#testbenchDef.
    def visitTestbenchDef(self, ctx:UniVRcParser.TestbenchDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#assertStmt.
    def visitAssertStmt(self, ctx:UniVRcParser.AssertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#delayStmt.
    def visitDelayStmt(self, ctx:UniVRcParser.DelayStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#threadStmt.
    def visitThreadStmt(self, ctx:UniVRcParser.ThreadStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ifStmt.
    def visitIfStmt(self, ctx:UniVRcParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#elifClause.
    def visitElifClause(self, ctx:UniVRcParser.ElifClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#elseClause.
    def visitElseClause(self, ctx:UniVRcParser.ElseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#switchStmt.
    def visitSwitchStmt(self, ctx:UniVRcParser.SwitchStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#caseClause.
    def visitCaseClause(self, ctx:UniVRcParser.CaseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#defaultClause.
    def visitDefaultClause(self, ctx:UniVRcParser.DefaultClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#forStmt.
    def visitForStmt(self, ctx:UniVRcParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#forConfig.
    def visitForConfig(self, ctx:UniVRcParser.ForConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#forStandardC.
    def visitForStandardC(self, ctx:UniVRcParser.ForStandardCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#forInit.
    def visitForInit(self, ctx:UniVRcParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#forStep.
    def visitForStep(self, ctx:UniVRcParser.ForStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#forIterRange.
    def visitForIterRange(self, ctx:UniVRcParser.ForIterRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#forIterSet.
    def visitForIterSet(self, ctx:UniVRcParser.ForIterSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ForCStyleExplicit.
    def visitForCStyleExplicit(self, ctx:UniVRcParser.ForCStyleExplicitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ForCStyleRange.
    def visitForCStyleRange(self, ctx:UniVRcParser.ForCStyleRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#whileStmt.
    def visitWhileStmt(self, ctx:UniVRcParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#doWhileStmt.
    def visitDoWhileStmt(self, ctx:UniVRcParser.DoWhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#repeatStmt.
    def visitRepeatStmt(self, ctx:UniVRcParser.RepeatStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#MulExpr.
    def visitMulExpr(self, ctx:UniVRcParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#SliceMinusExpr.
    def visitSliceMinusExpr(self, ctx:UniVRcParser.SliceMinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#SliceStepExpr.
    def visitSliceStepExpr(self, ctx:UniVRcParser.SliceStepExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#AddExpr.
    def visitAddExpr(self, ctx:UniVRcParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#BitAndExpr.
    def visitBitAndExpr(self, ctx:UniVRcParser.BitAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#RelationalExpr.
    def visitRelationalExpr(self, ctx:UniVRcParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LogicAndExpr.
    def visitLogicAndExpr(self, ctx:UniVRcParser.LogicAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#BitOrExpr.
    def visitBitOrExpr(self, ctx:UniVRcParser.BitOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:UniVRcParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#IndexExpr.
    def visitIndexExpr(self, ctx:UniVRcParser.IndexExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#PowerExpr.
    def visitPowerExpr(self, ctx:UniVRcParser.PowerExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ReductionExpr.
    def visitReductionExpr(self, ctx:UniVRcParser.ReductionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#EqualityExpr.
    def visitEqualityExpr(self, ctx:UniVRcParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LogicOrExpr.
    def visitLogicOrExpr(self, ctx:UniVRcParser.LogicOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#PrimaryExpr.
    def visitPrimaryExpr(self, ctx:UniVRcParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#SliceExpr.
    def visitSliceExpr(self, ctx:UniVRcParser.SliceExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#CallExpr.
    def visitCallExpr(self, ctx:UniVRcParser.CallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#LogicXorExpr.
    def visitLogicXorExpr(self, ctx:UniVRcParser.LogicXorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#MemberAccessExpr.
    def visitMemberAccessExpr(self, ctx:UniVRcParser.MemberAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ShiftExpr.
    def visitShiftExpr(self, ctx:UniVRcParser.ShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#BitXorExpr.
    def visitBitXorExpr(self, ctx:UniVRcParser.BitXorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#SlicePlusExpr.
    def visitSlicePlusExpr(self, ctx:UniVRcParser.SlicePlusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#TernaryExpr.
    def visitTernaryExpr(self, ctx:UniVRcParser.TernaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#shiftOp.
    def visitShiftOp(self, ctx:UniVRcParser.ShiftOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ParenExpr.
    def visitParenExpr(self, ctx:UniVRcParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#NumberLitExpr.
    def visitNumberLitExpr(self, ctx:UniVRcParser.NumberLitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#BoolLitExpr.
    def visitBoolLitExpr(self, ctx:UniVRcParser.BoolLitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#StringLitExpr.
    def visitStringLitExpr(self, ctx:UniVRcParser.StringLitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#SizedBinExpr.
    def visitSizedBinExpr(self, ctx:UniVRcParser.SizedBinExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#SizedHexExpr.
    def visitSizedHexExpr(self, ctx:UniVRcParser.SizedHexExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#SizedDecExpr.
    def visitSizedDecExpr(self, ctx:UniVRcParser.SizedDecExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#CastExprRule.
    def visitCastExprRule(self, ctx:UniVRcParser.CastExprRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#BuiltinCallExpr.
    def visitBuiltinCallExpr(self, ctx:UniVRcParser.BuiltinCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ConcatPrimaryExpr.
    def visitConcatPrimaryExpr(self, ctx:UniVRcParser.ConcatPrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#InitListExpr.
    def visitInitListExpr(self, ctx:UniVRcParser.InitListExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#IdExpr.
    def visitIdExpr(self, ctx:UniVRcParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#initList.
    def visitInitList(self, ctx:UniVRcParser.InitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#NamedInit.
    def visitNamedInit(self, ctx:UniVRcParser.NamedInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#IndexedInit.
    def visitIndexedInit(self, ctx:UniVRcParser.IndexedInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#PositionalInit.
    def visitPositionalInit(self, ctx:UniVRcParser.PositionalInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#NestedInit.
    def visitNestedInit(self, ctx:UniVRcParser.NestedInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ConcatList.
    def visitConcatList(self, ctx:UniVRcParser.ConcatListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#ConcatRep.
    def visitConcatRep(self, ctx:UniVRcParser.ConcatRepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#builtinCall.
    def visitBuiltinCall(self, ctx:UniVRcParser.BuiltinCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#builtinName.
    def visitBuiltinName(self, ctx:UniVRcParser.BuiltinNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#exprlist.
    def visitExprlist(self, ctx:UniVRcParser.ExprlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UniVRcParser#id.
    def visitId(self, ctx:UniVRcParser.IdContext):
        return self.visitChildren(ctx)



del UniVRcParser