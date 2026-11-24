# uniVRc

<p align="center">
  <img src="https://raw.githubusercontent.com/uniVRc/uniVRc/main/icon.png" width="128" height="128" alt="uniVRc Logo" />
  <br>
  <b>The official developer extension for the uniVRc (.vr) Hardware Description Language</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-uniVRc-orange.svg" alt="uniVRc" />
  <img src="https://img.shields.io/badge/Parser-ANTLR4-blue.svg" alt="ANTLR4" />
  <img src="https://img.shields.io/badge/VS%20Code-1.60%2B-007ACC.svg" alt="VS Code" />
  <img src="https://img.shields.io/badge/Snippets-45%20Hardware%20Templates-success.svg" alt="Snippets" />
</p>

---

## About uniVRc

**uniVRc** (pronounced *Universe* / *Uni-VR-C*, with the `.vr` file extension) is a modern, unified hardware description language engineered for digital system design, high-level synthesis, and hardware verification.

uniVRc bridges the gap between algorithmic expressive power and efficient hardware architecture, providing software developers and hardware engineers with high-productivity abstractions alongside cycle-by-cycle hardware control:

- **Bit-Exact Hardware Primitives**: Native support for arbitrary bit-width integers (`unsigned<W>`, `signed<W>`), fixed-point numerics (`fxp<W,F>`), standard RTL signals (`wire`, `reg`), and hardware streaming channels (`stream<T>`, `fifo<T>`).
- **Hardware Verification & Testbenches**: First-class `@TESTBENCH` blocks, hardware assertions (`assert`), simulation delays (`delay`), and diagnostic printing for rapid verification.
- **Pipelining & Scheduling Directives**: Algorithmic pragmas (`@PIPE(II=1)`, `@UNROLL`, `@TRIPCOUNT`, `@LOOP_FLATTEN`, `@DEPENDENCE`) that directly guide scheduling algorithms and microarchitectural synthesis.
- **Conflict-Free Memory Banking**: High-level memory partitioning directives (`@PARTITION(type="cyclic|block|complete")`, `@RESHAPE`, `@BIND_STORAGE(type="ram_2p", impl="bram")`) enabling maximum parallel throughput for multi-dimensional arrays.
- **Resource Binding & Interface Protocols**: Explicit binding of arithmetic operations to dedicated hardware units (`@BIND_OP(op="mul", impl="dsp")`), and automatic generation of standard bus interfaces (`@INTERFACE(mode="axis|s_axilite|ap_none")`).
- **Concurrent Processes**: Support for synchronous sequential processes (`@THREAD` with `@RESET` and `@TRIG(posedge clk)`), combinational logic, and structured finite state machines (FSM).

---

## Prerequisites

To enable real-time syntax checking, AST diagnostics, and graph visualization, the following dependencies are required:

### 1. Python 3.8+
Make sure Python is installed and available in your system `PATH` (or configured via `univrc.pythonPath` in VS Code settings).
- Verify via terminal:
  ```bash
  python --version
  # or
  python3 --version
  ```

### 2. ANTLR4 Python Runtime (Required)
Install the official ANTLR4 Python 3 runtime library:
```bash
pip install antlr4-python3-runtime
```
> **Note for Linux / Ubuntu / WSL2**: If your system Python uses externally managed environments (PEP 668), run:
> ```bash
> pip install --break-system-packages antlr4-python3-runtime
> ```
> or install it inside your active virtual environment (`.venv`).

### 3. Graphviz (Optional - for CDFG/CFG Visualizer)
Graphviz is only needed if you wish to render graphical Control Data Flow Graphs (CDFG) and Control Flow Graphs (CFG) inside the interactive visualizer webview:
- **Ubuntu / Debian / WSL**:
  ```bash
  sudo apt update && sudo apt install -y graphviz
  ```
- **Windows**:
  ```bash
  winget install Graphviz.Graphviz
  # or
  choco install graphviz
  ```
- **macOS**:
  ```bash
  brew install graphviz
  ```

---

## Features

### Real-Time ANTLR4 Syntax Diagnostics & Linter
- **Live ANTLR4 Parsing**: Powered by the native ANTLR4 parser engine (`UniVRc.g4`) running in real-time.
- **Inline Error Squiggles**: Instant red squiggly underlines on syntax errors with line and column precision.
- **VS Code Problems Panel (`Ctrl + Shift + M`)**: Full diagnostic reporting in the Problems view with one-click navigation to error locations.
- **Status Bar Indicator**:
  - `$(check) uniVRc: Valid` when error-free.
  - `$(error) uniVRc: N error(s)` when errors are detected (click to open Problems panel).
- **Manual Trigger**: Run `Ctrl + Shift + P` -> `uniVRc: Check Syntax of Active File`.

### Dedicated "VR" File Icon Theme
- Authentic geometric orange **VR** logo for all `*.vr` and `*.VR` files.
- **How to enable**: Press `Ctrl + Shift + P` -> type `Preferences: File Icon Theme` -> select **`uniVRc File Icons`**.

### Interactive CDFG & Schedule Visualizer
- **Multi-View Dashboard**: Inspect Control Data Flow Graphs (CDFG), Control Flow Graphs (CFG), AST trees, memory hazard edges, and cycle-by-cycle schedules directly inside VS Code.
- **How to open**:
  - Click the **Graph Icon** in the top-right editor title bar.
  - Right-click anywhere in a `.vr` file -> **uniVRc: Show CDFG & Schedule Visualization**.
  - Or press `Ctrl + Shift + P` -> **uniVRc: Show CDFG & Schedule Visualization**.

### Hover Tooltips & Documentation
- Hover over any pragma (`@PIPE`, `@PARTITION`, `@MODULE`, `@BIND_OP`, etc.), bit-exact type (`unsigned<W>`, `fxp<W,F>`, `wire`), or operator (`:=`, `+:`, `<&`) to view instant Markdown documentation, explanations, and usage examples.

### Document Symbols & Outline
- Full integration with VS Code's **Outline** view and **Breadcrumbs**.
- Instantly browse and jump to Modules, Threads, Functions, Structs, and Enums.

### Auto-Formatter
- Automatically formats and cleans up `.vr` code using `Shift + Alt + F` or Format Document:
  - Smart indentation for `{}` blocks and `switch/case` statements.
  - Standardizes spacing around operators (`:=`, `=`, `==`, `!=`, `<=`, `>=`).
  - Cleans up trailing whitespace and collapses redundant empty lines.

### Go to Definition (`F12`) & Rename Symbol (`F2`)
- Instantly jump to declarations of variables, ports, registers, parameters, functions, structs, and enums using `F12` or `Ctrl + Click`.
- Safely rename symbols across the entire document using `F2`.

### Code Snippets
Catalog of 45 production-ready boilerplate templates triggered by typing the prefix and hitting `Tab`:
- **Architecture**: `mod` (Hardware Module), `mod_axis` (AXI-Stream Interface), `mod_axilite` (AXI-Lite Slave), `inst` (Submodule Instantiation), `param` (Generics/Parameters).
- **Sequential Logic & FSM**: `thread_sync` (Clocked Process with Reset), `thread_comb` (Combinational Process), `fsm_3state` (3-State Moore/Mealy FSM), `shift_reg` (Pipelined Shift Register), `counter` (Hardware Up-Counter).
- **Optimization Pragmas**: `pipe` (`@PIPE(II=1)`), `unroll`, `tripcount`, `flatten`, `dependence`, `part_cyclic`, `part_block`, `part_complete`, `mem_bram`, `bind_dsp`, `bind_storage`, `dataflow`, `inline`.
- **Loops & Branches**: `for_pipe`, `for_c`, `for_range`, `for_set`, `for_2d`, `while`, `repeat`, `switch_case`, `if_elif`.
- **Types & Channels**: `wire`, `reg`, `fxp`, `stream`, `fifo`, `struct`, `enum`, `typedef`.
- **DSP & Verification**: `fir_filter` (FIR Filter Kernel with MAC), `matmul_kernel` (2D Matrix Multiply), `func`, `testbench` (Simulation Testbench), `assert_stmt`.
- **Bit Operations & Slicing**: `concat`, `rep`, `slice_plus`, `slice_minus`, `cast`.

---

## Configuration Settings

You can customize the extension via VS Code Settings (`Ctrl + ,`):

| Setting | Default | Description |
| :--- | :--- | :--- |
| `univrc.pythonPath` | `"python"` | Path or command name for the Python executable (e.g. `"python3"`, `"/usr/bin/python3"`, or a virtual environment path). |
| `univrc.enableSyntaxAnalysis` | `true` | Enable or disable real-time background ANTLR4 syntax analysis and inline error reporting. |

---

## Installation

### Installing from VSIX Package
The extension is packaged as a standalone `.vsix` file:
```text
univrc-0.4.0.vsix
```

1. In VS Code, open the Extensions view (`Ctrl + Shift + X`).
2. Click the `...` menu at the top right of the Extensions panel.
3. Select **Install from VSIX...** and choose `univrc-0.4.0.vsix`.

*(Alternatively, run from terminal)*:
```bash
code --install-extension univrc-0.4.0.vsix
```

> **WSL & Remote Containers**: This extension is configured with `["workspace", "ui"]` support, meaning it runs seamlessly both in local Windows/macOS/Linux environments and inside Remote WSL workspaces.
