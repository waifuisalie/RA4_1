# Phase 4 Flowchart - Code Generation

## Complete Phase 4 Architecture

```mermaid
flowchart TB
    Start([Input: Source Code .txt file])

    subgraph Previous["Previous Phases (Already Implemented)"]
        Phase1[Phase 1: Lexical Analysis]
        Phase2[Phase 2: Syntax Analysis]
        Phase3[Phase 3: Semantic Analysis]

        Phase1 -->|Token Stream| Phase2
        Phase2 -->|Abstract Syntax Tree| Phase3
    end

    Start --> Phase1

    subgraph Phase4["Phase 4: Code Generation (NEW)"]
        direction TB

        Input[Input: Attributed AST<br/>from Phase 3]

        subgraph Student1["Student 1: TAC Generation"]
            direction TB
            GenTAC[Function: gerarTAC]
            TempVars[Manage Temporaries<br/>t0, t1, t2, ...]
            Labels[Manage Labels<br/>L0, L1, L2, ...]
            Traverse[Traverse AST<br/>Post-order]

            GenTAC --> Traverse
            Traverse --> TempVars
            Traverse --> Labels
        end

        subgraph Student2["Student 2: TAC Optimization"]
            direction TB
            OptTAC[Function: otimizarTAC]
            ConstFold[Constant Folding<br/>2 + 3 → 5]
            ConstProp[Constant Propagation<br/>t1=5; t2=t1+3 → t2=8]
            DeadCode[Dead Code Elimination<br/>Remove unused vars]
            JumpElim[Redundant Jump<br/>Elimination]

            OptTAC --> ConstFold
            OptTAC --> ConstProp
            OptTAC --> DeadCode OptTAC --> JumpElim end
        subgraph Student3["Student 3: Assembly Generation"]
            direction TB
            GenAsm[Function: gerarAssembly]
            RegAlloc[Register Allocation<br/>R16-R23 for temps]
            Mapping[TAC to AVR<br/>Instruction Mapping]
            FloatOps[Floating Point<br/>16-bit operations]

            GenAsm --> RegAlloc
            GenAsm --> Mapping
            GenAsm --> FloatOps
        end

        subgraph Student4["Student 4: Integration & Testing"]
            direction TB
            MainFunc[Function: main]
            Integration[Integrate All Phases<br/>1 → 2 → 3 → 4]
            Testing[Create Test Files<br/>fatorial.txt<br/>fibonacci.txt<br/>taylor.txt]
            Validation[Arduino Validation<br/>Compile & Upload]

            MainFunc --> Integration
            Integration --> Testing
            Testing --> Validation
        end

        Input --> GenTAC
        GenTAC -->|TAC Instructions| TACFile1[Output: TAC.txt]
        GenTAC -->|List of Instructions| OptTAC

        OptTAC -->|Optimized TAC| TACFile2[Output: TAC_optimized.txt]
        OptTAC -->|Optimized Instructions| GenAsm

        GenAsm -->|AVR Assembly Code| AsmFile[Output: program.s]
        GenAsm --> MainFunc
    end

    Phase3 -->|Attributed AST| Input

    subgraph Build["Build & Deploy Pipeline"]
        direction TB
        AsmFile --> Compile[avr-gcc compile]
        Compile -->|ELF binary| ObjCopy[avr-objcopy]
        ObjCopy -->|HEX file| HexFile[Output: program.hex]
        HexFile --> Upload[avrdude upload<br/>9600 baud]
        Upload --> Arduino[Arduino Uno<br/>Execution]
    end

    subgraph Deliverables["Final Deliverables"]
        direction LR
        D1[tokens.txt<br/>Phase 1]
        D2[syntax_tree.txt<br/>Phase 2]
        D3[attributed_ast.txt<br/>Phase 3]
        D4[TAC.txt<br/>Phase 4]
        D5[TAC_optimized.txt<br/>Phase 4]
        D6[program.s<br/>Assembly]
        D7[program.hex<br/>Executable]
        D8[README.md<br/>Documentation]
        D9[optimization_report.md<br/>Analysis]
    end

    Arduino --> Results[Validation Results<br/>Serial Output<br/>LED/LCD Display]

    style Phase4 fill:#e1f5ff
    style Student1 fill:#fff4e6
    style Student2 fill:#e8f5e9
    style Student3 fill:#f3e5f5
    style Student4 fill:#fce4ec
    style Build fill:#fff9c4
    style Deliverables fill:#f1f8e9
```

---

## Data Flow Between Functions

```mermaid
flowchart LR
    AST[Attributed AST<br/>Type: Tree Structure]

    TAC_List1[TAC Instructions<br/>Type: List]
    TAC_File1[TAC.txt<br/>Type: File]

    TAC_List2[Optimized TAC<br/>Type: List]
    TAC_File2[TAC_optimized.txt<br/>Type: File]

    ASM_Code[Assembly Code<br/>Type: String]
    ASM_File[program.s<br/>Type: File]

    AST -->|Input| gerarTAC
    gerarTAC -->|Returns| TAC_List1
    gerarTAC -->|Writes| TAC_File1

    TAC_List1 -->|Input| otimizarTAC
    otimizarTAC -->|Returns| TAC_List2
    otimizarTAC -->|Writes| TAC_File2

    TAC_List2 -->|Input| gerarAssembly
    gerarAssembly -->|Returns| ASM_Code
    gerarAssembly -->|Writes| ASM_File

    style gerarTAC fill:#fff4e6
    style otimizarTAC fill:#e8f5e9
    style gerarAssembly fill:#f3e5f5
```

## Student Responsibilities Summary

```mermaid
graph TD
    subgraph S1["Student 1: TAC Generator"]
        T1[Implement gerarTAC function]
        T2[AST traversal post-order]
        T3[Generate TAC instructions]
        T4[Manage temporaries & labels]
        T5[Handle RPN expressions]
        T6[Support MEM and RES commands]
    end

    subgraph S2["Student 2: TAC Optimizer"]
        O1[Implement otimizarTAC function]
        O2[Constant Folding]
        O3[Constant Propagation]
        O4[Dead Code Elimination]
        O5[Jump Optimization]
        O6[Document optimizations]
    end

    subgraph S3["Student 3: Assembly Generator"]
        A1[Implement gerarAssembly function]
        A2[Define register conventions]
        A3[Map TAC to AVR instructions]
        A4[Handle floating-point ops]
        A5[Generate prologue/epilogue]
        A6[Memory access implementation]
    end

    subgraph S4["Student 4: Integration & Testing"]
        I1[Implement main function]
        I2[Chain all 4 phases]
        I3[Create test files]
        I4[Build automation scripts]
        I5[Arduino validation]
        I6[Generate all documentation]
    end

    style S1 fill:#fff4e6
    style S2 fill:#e8f5e9
    style S3 fill:#f3e5f5
    style S4 fill:#fce4ec
```

## Execution Flow in main()

```mermaid
sequenceDiagram
    participant User
    participant Main as main()
    participant Lex as Lexical Analyzer
    participant Syn as Syntax Analyzer
    participant Sem as Semantic Analyzer
    participant TAC as gerarTAC()
    participant Opt as otimizarTAC()
    participant Asm as gerarAssembly()
    participant Build as Build System

    User->>Main: ./compilador fatorial.txt
    Main->>Lex: Analyze tokens
    Lex-->>Main: Token list
    Main->>Syn: Build syntax tree
    Syn-->>Main: AST
    Main->>Sem: Semantic analysis
    Sem-->>Main: Attributed AST

    rect rgb(255, 244, 230)
        Note over Main,TAC: Phase 4 starts here
        Main->>TAC: Generate TAC
        TAC-->>Main: TAC instructions + TAC.txt
    end

    rect rgb(232, 245, 233)
        Main->>Opt: Optimize TAC
        Opt-->>Main: Optimized TAC + TAC_optimized.txt
    end

    rect rgb(243, 229, 245)
        Main->>Asm: Generate Assembly
        Asm-->>Main: Assembly code + program.s
    end

    rect rgb(255, 249, 196)
        Main->>Build: Compile to HEX
        Build-->>Main: program.hex
    end

    Main-->>User: All files generated
    User->>Build: Upload to Arduino
    Build-->>User: Execution results
```

## TAC Instruction Types

```mermaid
classDiagram
    class TACInstruction {
        <<abstract>>
        +String toString()
    }

    class Assignment {
        +String dest
        +String source
        // t1 = a
    }

    class BinaryOp {
        +String result
        +String operand1
        +String operator
        +String operand2
        // t1 = a + b
    }

    class UnaryOp {
        +String result
        +String operator
        +String operand
        // t1 = -a
    }

    class Label {
        +String name
        // L1:
    }

    class Jump {
        +String target
        // goto L1
    }

    class ConditionalJump {
        +String condition
        +String target
        +boolean isNegated
        // if a goto L1
        // ifFalse a goto L1
    }

    class MemoryAccess {
        +String result
        +String address
        +boolean isStore
        // t1 = MEM[a]
        // MEM[a] = t1
    }

    TACInstruction <|-- Assignment
    TACInstruction <|-- BinaryOp
    TACInstruction <|-- UnaryOp
    TACInstruction <|-- Label
    TACInstruction <|-- Jump
    TACInstruction <|-- ConditionalJump
    TACInstruction <|-- MemoryAccess
```
