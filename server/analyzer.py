"""uniVRc Syntax Analyzer / Diagnostics Server for VS Code.
Parses uniVRc (.vr) source code using ANTLR4 and returns JSON-formatted diagnostics.
"""

import sys
import os
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def setup_paths(workspace_dir=None):
    candidates = []
    if workspace_dir:
        candidates.append(os.path.join(workspace_dir, "HLS", "univrc-hls", "src"))
        candidates.append(os.path.join(workspace_dir, "HLS", "univrc-hls"))
        candidates.append(os.path.join(workspace_dir, "univrc-hls", "src"))
        candidates.append(os.path.join(workspace_dir, "univrc-hls"))
        candidates.append(workspace_dir)

    # Try looking in parent dirs
    parent = os.path.dirname(SCRIPT_DIR)
    while parent and os.path.splitdrive(parent)[1] not in ("\\", "/"):
        candidates.append(os.path.join(parent, "HLS", "univrc-hls", "src"))
        candidates.append(os.path.join(parent, "HLS", "univrc-hls"))
        candidates.append(os.path.join(parent, "univrc-hls", "src"))
        candidates.append(os.path.join(parent, "univrc-hls"))
        parent = os.path.dirname(parent)

    candidates.append("D:/UT.CE/CAD/univrc/HLS/univrc-hls/src")
    candidates.append("D:/UT.CE/CAD/univrc/HLS/univrc-hls")
    candidates.append("/mnt/d/UT.CE/CAD/univrc/HLS/univrc-hls/src")
    candidates.append("/mnt/d/UT.CE/CAD/univrc/HLS/univrc-hls")

    for cand in candidates:
        if os.path.isdir(cand) and cand not in sys.path:
            sys.path.insert(0, cand)


def analyze_code(source_code: str, workspace_dir=None):
    """Analyzes source code using ANTLR4 and returns a list of diagnostic dictionaries."""
    diagnostics = []
    if not source_code.strip():
        return diagnostics

    setup_paths(workspace_dir)

    try:
        from antlr4 import InputStream, CommonTokenStream
        from antlr4.error.ErrorListener import ErrorListener
        try:
            from frontend.antlr_gen.UniVRcLexer import UniVRcLexer
            from frontend.antlr_gen.UniVRcParser import UniVRcParser
            from frontend.antlr_visitor import UniVRcASTVisitor
        except ImportError:
            from src.frontend.antlr_gen.UniVRcLexer import UniVRcLexer
            from src.frontend.antlr_gen.UniVRcParser import UniVRcParser
            from src.frontend.antlr_visitor import UniVRcASTVisitor
    except ImportError as err:
        return [{
            "line": 1,
            "column": 1,
            "endLine": 1,
            "endColumn": 1,
            "message": f"ANTLR4 dependency import error: {str(err)}",
            "severity": "warning"
        }]

    class DiagnosticListener(ErrorListener):
        def __init__(self):
            super().__init__()
            self.errors = []

        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            length = len(offendingSymbol.text) if offendingSymbol and offendingSymbol.text else 1
            self.errors.append({
                "line": line,
                "column": column + 1,
                "endLine": line,
                "endColumn": column + 1 + length,
                "message": f"Syntax Error: {msg}",
                "severity": "error"
            })

    try:
        input_stream = InputStream(source_code)
        lexer = UniVRcLexer(input_stream)
        lexer_listener = DiagnosticListener()
        lexer.removeErrorListeners()
        lexer.addErrorListener(lexer_listener)

        token_stream = CommonTokenStream(lexer)
        parser = UniVRcParser(token_stream)
        parser_listener = DiagnosticListener()
        parser.removeErrorListeners()
        parser.addErrorListener(parser_listener)

        tree = parser.program()

        diagnostics.extend(lexer_listener.errors)
        diagnostics.extend(parser_listener.errors)

        if not diagnostics:
            visitor = UniVRcASTVisitor()
            visitor.visit(tree)

    except Exception as e:
        diagnostics.append({
            "line": 1,
            "column": 1,
            "endLine": 1,
            "endColumn": 1,
            "message": f"Parse Error: {str(e)}",
            "severity": "error"
        })

    return diagnostics


def main():
    parser = argparse.ArgumentParser(description="uniVRc Syntax Analyzer")
    parser.add_argument("--file", help="Path to .vr file to analyze")
    parser.add_argument("--stdin", action="store_true", help="Read source code from standard input")
    parser.add_argument("--workspace", help="Workspace root directory")
    args = parser.parse_args()

    source = ""
    if args.stdin:
        source = sys.stdin.read()
    elif args.file:
        if os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8") as f:
                source = f.read()
        else:
            print(json.dumps([{"line": 1, "column": 1, "endLine": 1, "endColumn": 1, "message": f"File not found: {args.file}", "severity": "error"}]))
            return
    else:
        if not sys.stdin.isatty():
            source = sys.stdin.read()

    results = analyze_code(source, workspace_dir=args.workspace)
    print(json.dumps(results))


if __name__ == "__main__":
    main()
