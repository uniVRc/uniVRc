grammar UniVRc;

// =============================================================================
// uniVRc ANTLR4 Formal Grammar Specification
// =============================================================================

// ==========================================
// Parser Rules
// ==========================================

program
    : statement* EOF
    ;

statement
    : simpleStmt SEMI
    | block
    | importStmt
    | structDef
    | enumDef
    | typedefDef
    | interfaceDef
    | staticStmt
    | moduleDef
    | testbenchDef
    | funcDef
    | ifStmt
    | switchStmt
    | forStmt
    | whileStmt
    | doWhileStmt
    | repeatStmt
    | flowStmt
    | threadStmt
    | assertStmt
    | delayStmt
    | SEMI
    ;

simpleStmt
    : varDecl
    | instStmt
    | assignStmt
    | regAssignStmt
    | augAssignStmt
    | regAugAssignStmt
    | incDecStmt
    | callStmt
    ;

importStmt
    : (AT_IMPORT LPAREN STRING RPAREN | IMPORT STRING) SEMI?
    ;

block
    : attr* LBRACE attr* statement* RBRACE
    ;

// --- Attributes / Pragmas ---
attr
    : (AT_NAME | AT_THREAD | AT_PARAM) (LPAREN attrArgs? RPAREN)?
    ;

attrArgs
    : attrArg (COMMA attrArg)*
    ;

attrArg
    : (POSEDGE | NEGEDGE) id                           # EdgeAttrArg
    | id ASSIGN expr                                    # NamedAttrArg
    | expr                                              # PositionalAttrArg
    ;

// --- Flow Statements ---
flowStmt
    : BREAK SEMI                                        # BreakStmtRule
    | CONTINUE SEMI                                     # ContinueStmtRule
    | RETURN expr? SEMI                                 # ReturnStmtRule
    ;

// --- Hardware Instantiation ---
instStmt
    : attr* id paramOverrideClause? id LPAREN portConnections? RPAREN
    ;

paramOverrideClause
    : LT paramOverrideList GT
    ;

paramOverrideList
    : paramOverride (COMMA paramOverride)*
    ;

paramOverride
    : DOT id LPAREN expr RPAREN                          # NamedParamOverride
    | id ASSIGN expr                                     # AssignParamOverride
    | expr                                               # PositionalParamOverride
    ;

portConnections
    : portConn (COMMA portConn)*
    ;

portConn
    : DOT id LPAREN expr RPAREN                         # NamedPortConn
    | expr                                              # PositionalPortConn
    ;

// --- Assignments ---
assignStmt
    : lvalue ASSIGN expr
    ;

regAssignStmt
    : lvalue REG_ASSIGN expr
    ;

augAssignStmt
    : lvalue (AUGOP | SHL_ASSIGN | SHR_ASSIGN | GT GT ASSIGN) expr
    ;

regAugAssignStmt
    : lvalue (REG_AUGOP | REG_SHL_ASSIGN | REG_SHR_ASSIGN | COLON GT GT ASSIGN) expr
    ;

incDecStmt
    : INCOP lvalue                                      # PreIncDec
    | lvalue INCOP                                      # PostIncDec
    ;

callStmt
    : expr LPAREN exprlist? RPAREN
    ;

// --- L-Values ---
lvalue
    : id                                                # LValueId
    | lvalue DOT id                                     # LValueMember
    | lvalue LBRACK expr RBRACK                         # LValueIndex
    | lvalue LBRACK expr COLON expr RBRACK              # LValueSlice
    | lvalue LBRACK expr COLON expr COLON expr RBRACK   # LValueSliceStep
    | lvalue LBRACK expr (SLICE_PLUS | '+:') expr RBRACK  # LValueSlicePlus
    | lvalue LBRACK expr (SLICE_MINUS | '-:') expr RBRACK # LValueSliceMinus
    | DOLLAR LBRACE lvalueList RBRACE                   # LValueConcat
    ;

lvalueList
    : lvalue (COMMA lvalue)*
    ;

// --- Declarations ---
varDecl
    : attr* VAR id ASSIGN expr                                      # VarInferred
    | attr* CONST? typeDesc id arrayDims (assignOp expr)?          # VarExplicit
    ;

assignOp
    : ASSIGN | REG_ASSIGN
    ;

arrayDims
    : (LBRACK expr RBRACK)*
    ;

// --- Types ---
typeDesc
    : INT                                               # TypeInt
    | FLOAT                                             # TypeFloat
    | BOOL                                              # TypeBool
    | REG                                               # TypeReg
    | WIRE (LT expr GT)?                                # TypeWire
    | SIGNED LT expr GT                                 # TypeSigned
    | UNSIGNED LT expr GT                               # TypeUnsigned
    | FXP LT expr COMMA expr GT                         # TypeFxp
    | STREAM LT typeDesc (COMMA expr)? GT               # TypeStream
    | FIFO LT typeDesc (COMMA expr)? GT                 # TypeFifo
    | STRUCT? id                                        # TypeStructRef
    ;

// --- Structs, Enums, Typedefs ---
structDef
    : STRUCT id LBRACE structField+ RBRACE SEMI
    ;

structField
    : typeDesc id arrayDims SEMI
    ;

enumDef
    : ENUM id (LT expr GT)? LBRACE enumList? RBRACE SEMI
    ;

enumList
    : enumEntry (COMMA enumEntry)* COMMA?
    ;

enumEntry
    : id (ASSIGN expr)?
    ;

typedefDef
    : TYPEDEF typeDesc id arrayDims SEMI
    ;

// --- Interfaces & Static Elaboration ---
interfaceDef
    : attr* INTERFACE id (LT paramList? GT)? LBRACE interfaceItem* RBRACE SEMI?
    ;

interfaceItem
    : attr* portDir attr* typeDesc id arrayDims (ASSIGN expr)? SEMI?
    | varDecl SEMI?
    ;

staticStmt
    : STATIC (ifStmt | forStmt | block)
    ;

// --- Parameters & Modules ---
paramSection
    : AT_PARAM LPAREN paramList? RPAREN
    ;

paramList
    : param (COMMA param)*
    ;

param
    : id (ASSIGN expr)?
    ;

moduleDef
    : attr* AT_MODULE (LPAREN attrArgs? RPAREN)? attr* paramSection? id LPAREN moduleParams? RPAREN block
    ;

moduleParams
    : moduleParam (COMMA moduleParam)*
    ;

moduleParam
    : attr* portDir attr* typeDesc id arrayDims (ASSIGN expr)?
    ;

portDir
    : IN | OUT | INOUT
    ;

// --- Functions & Threads ---
funcDef
    : attr* paramSection? typeDesc id (LPAREN funcParams? RPAREN)? block                           # FuncDefPrefixType
    | attr* paramSection? (VOID | FUNC)? id (LPAREN funcParams? RPAREN)? (COLON typeDesc)? block   # FuncDefPostfixType
    ;

funcParams
    : funcParam (COMMA funcParam)*
    ;

funcParam
    : attr* typeDesc id arrayDims (ASSIGN expr)?
    ;

// --- Verification & Control ---
testbenchDef
    : attr* AT_TESTBENCH attr* id (LPAREN funcParams? RPAREN)? block
    ;

assertStmt
    : ASSERT LPAREN? expr (COMMA expr)? RPAREN? SEMI
    ;

delayStmt
    : DELAY LPAREN? expr RPAREN? SEMI
    ;

threadStmt
    : AT_THREAD statement*
    ;

// --- Control Flow ---
ifStmt
    : attr* IF LPAREN expr RPAREN block elifClause* elseClause?
    ;

elifClause
    : ELIF LPAREN expr RPAREN block
    ;

elseClause
    : ELSE block
    ;

switchStmt
    : attr* SWITCH LPAREN expr RPAREN LBRACE caseClause* defaultClause? RBRACE
    ;

caseClause
    : CASE LPAREN exprlist RPAREN block
    ;

defaultClause
    : DEFAULT block
    ;

forStmt
    : attr* FOR LPAREN forConfig RPAREN block
    ;

forConfig
    : forStandardC
    | forIterRange
    | forIterSet
    | forCStyle
    ;

forStandardC
    : forInit? SEMI expr? SEMI forStep?
    ;

forInit
    : varDecl
    | assignStmt
    ;

forStep
    : incDecStmt
    | augAssignStmt
    | regAugAssignStmt
    | assignStmt
    ;

forIterRange
    : INDEX ASSIGN id COMMA RANGE ASSIGN LPAREN exprlist RPAREN
    ;

forIterSet
    : INDEX ASSIGN id COMMA SET ASSIGN LBRACE exprlist RBRACE
    ;

forCStyle
    : FROM ASSIGN expr COMMA TO ASSIGN expr (COMMA STEP ASSIGN expr)? # ForCStyleExplicit
    | expr TO expr (COMMA STEP ASSIGN expr)?                         # ForCStyleRange
    ;

whileStmt
    : attr* WHILE LPAREN expr RPAREN DO? block
    ;

doWhileStmt
    : attr* DO block WHILE LPAREN expr RPAREN SEMI
    ;

repeatStmt
    : attr* REPEAT LPAREN expr RPAREN block
    ;

// --- Expressions ---
expr
    : expr LBRACK expr COLON expr COLON expr RBRACK                    # SliceStepExpr
    | expr LBRACK expr COLON expr RBRACK                               # SliceExpr
    | expr LBRACK expr (SLICE_PLUS | '+:') expr RBRACK                 # SlicePlusExpr
    | expr LBRACK expr (SLICE_MINUS | '-:') expr RBRACK                # SliceMinusExpr
    | expr LBRACK expr RBRACK                                          # IndexExpr
    | expr DOT id                                                      # MemberAccessExpr
    | expr LPAREN exprlist? RPAREN                                     # CallExpr
    | <assoc=right> expr POW expr                                      # PowerExpr
    | (PLUS | MINUS | BNOT | LNOT) expr                                # UnaryExpr
    | RED_OP expr                                                      # ReductionExpr
    | expr (STAR | SLASH | PERCENT) expr                               # MulExpr
    | expr (PLUS | MINUS) expr                                         # AddExpr
    | expr shiftOp expr                                                # ShiftExpr
    | expr (LE | GE | LT | GT) expr                                    # RelationalExpr
    | expr (EQ | NE) expr                                              # EqualityExpr
    | expr BAND expr                                                   # BitAndExpr
    | expr (BXOR | BXNOR) expr                                         # BitXorExpr
    | expr BOR expr                                                    # BitOrExpr
    | expr LAND expr                                                   # LogicAndExpr
    | expr LXOR expr                                                   # LogicXorExpr
    | expr LOR expr                                                    # LogicOrExpr
    | <assoc=right> expr QUESTION expr COLON expr                      # TernaryExpr
    | primary                                                          # PrimaryExpr
    ;

shiftOp
    : ASHL
    | GT GT GT
    | SHL
    | GT GT
    | ROL
    | ROR
    ;

primary
    : LPAREN expr RPAREN                                               # ParenExpr
    | NUMBER                                                           # NumberLitExpr
    | (TRUE | FALSE)                                                   # BoolLitExpr
    | STRING                                                           # StringLitExpr
    | SIZED_BIN                                                        # SizedBinExpr
    | SIZED_HEX                                                        # SizedHexExpr
    | SIZED_DEC                                                        # SizedDecExpr
    | CAST LT typeDesc GT LPAREN expr RPAREN                           # CastExprRule
    | builtinCall                                                      # BuiltinCallExpr
    | concatExpr                                                       # ConcatPrimaryExpr
    | initList                                                         # InitListExpr
    | id                                                               # IdExpr
    ;

initList
    : LBRACE (initElement (COMMA initElement)* COMMA?)? RBRACE
    ;

initElement
    : DOT id ASSIGN expr                                               # NamedInit
    | LBRACK expr RBRACK ASSIGN expr                                   # IndexedInit
    | expr                                                             # PositionalInit
    | initList                                                         # NestedInit
    ;

concatExpr
    : DOLLAR LBRACE exprlist RBRACE                                    # ConcatList
    | DOLLAR LBRACE expr LBRACE expr RBRACE RBRACE                     # ConcatRep
    ;

builtinCall
    : builtinName LPAREN exprlist? RPAREN
    ;

builtinName
    : MIN | MAX | ABS | PRINT_KW
    ;

exprlist
    : expr (COMMA expr)*
    ;

id
    : ID
    | IN
    | OUT
    | INOUT
    | FROM
    | TO
    | STEP
    | INDEX
    | RANGE
    | SET
    | MIN
    | MAX
    | ABS
    | PRINT_KW
    | INTERFACE
    | STATIC
    | VOID
    | FUNC
    ;

// ==========================================
// Lexer Rules
// ==========================================

BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';
IF: 'if';
ELIF: 'elif';
ELSE: 'else';
SWITCH: 'switch';
CASE: 'case';
DEFAULT: 'default';
FOR: 'for';
WHILE: 'while';
DO: 'do';
REPEAT: 'repeat';
STRUCT: 'struct';
ENUM: 'enum';
TYPEDEF: 'typedef';
CAST: 'cast';
INDEX: 'index';
RANGE: 'range';
SET: 'set';
FROM: 'from';
TO: 'to';
STEP: 'step';
IN: 'in';
OUT: 'out';
INOUT: 'inout';
VAR: 'var';
CONST: 'const';
INT: 'int';
FLOAT: 'float';
BOOL: 'bool';
WIRE: 'wire';
REG: 'reg';
SIGNED: 'signed';
UNSIGNED: 'unsigned';
FXP: 'fxp';
STREAM: 'stream';
FIFO: 'fifo';
ASSERT: 'assert';
DELAY: 'delay' | 'wait_cycles';
IMPORT: 'import';
INTERFACE: 'interface';
STATIC: 'static';
VOID: 'void';
FUNC: 'func';

TRUE: 'true';
FALSE: 'false';

MIN: 'min';
MAX: 'max';
ABS: 'abs';
PRINT_KW: 'print' | 'println' | '$display' | '$write';

POSEDGE: [pP][oO][sS][eE][dD][gG][eE];
NEGEDGE: [nN][eE][gG][eE][dD][gG][eE];

AT_MODULE: '@' [mM][oO][dD][uU][lL][eE];
AT_TESTBENCH: '@' [tT][eE][sS][tT][bB][eE][nN][cC][hH];
AT_PARAM: '@' [pP][aA][rR][aA][mM];
AT_THREAD: '@' [tT][hH][rR][eE][aA][dD];
AT_IMPORT: '@' [iI][mM][pP][oO][rR][tT];
AT_NAME: '@' [a-zA-Z_][a-zA-Z0-9_]*;

SIZED_BIN: [0-9][0-9_]* '\'' [bB] [01][01_]*;
SIZED_HEX: [0-9][0-9_]* '\'' [hH] [0-9a-fA-F][0-9a-fA-F_]*;
SIZED_DEC: [0-9][0-9_]* '\'' [dD] [0-9][0-9_]*;

RED_OP: '<&' | '<|' | '<^' | '<!' | '<~|' | '<~^';

ASHL: '<<<';
SHL: '<<';
ROL: '<<o';
ROR: '>>o';

SHL_ASSIGN: '<<=';
SHR_ASSIGN: '>>=';
REG_SHL_ASSIGN: ':<<=';
REG_SHR_ASSIGN: ':>>=';

REG_AUGOP: ':+=' | ':-=' | ':*=' | ':/=' | ':%=' | ':&=' | ':|=' | ':^=';
AUGOP: '+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=';
INCOP: '++' | '--';

REG_ASSIGN: ':=';
ASSIGN: '=';

EQ: '==';
NE: '!=';
LE: '<=';
GE: '>=';
LT: '<';
GT: '>';

LOR: 'or' | '||';
LXOR: 'xor' | '^^';
LAND: 'and' | '&&';

BOR: '|';
BXNOR: '~^' | '^~';
BXOR: '^';
BAND: '&';

BNOT: '~';
LNOT: '!' | 'not';

POW: '**';
PLUS: '+';
MINUS: '-';
STAR: '*';
SLASH: '/';
PERCENT: '%';

QUESTION: '?';
COLON: ':';
SEMI: ';';
COMMA: ',';
DOT: '.';
DOLLAR: '$';

SLICE_PLUS: '+:';
SLICE_MINUS: '-:';

LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';

ID: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER: [0-9]+ ('.' [0-9]+)?;

STRING
    : '"' (~["\r\n\\] | '\\' .)* '"'
    | '\'' (~['\r\n\\] | '\\' .)* '\''
    ;

LINE_COMMENT: ('//' ~[\r\n]* | '#' ~[\r\n]*) -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
WS: [ \t\r\n]+ -> skip;
