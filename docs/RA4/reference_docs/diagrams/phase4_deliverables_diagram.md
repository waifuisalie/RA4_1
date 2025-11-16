# Phase 4 Deliverables Flow Diagram

## Complete Compiler Pipeline with Deliverables

```mermaid
flowchart TD
    Start([Input File<br/>fatorial.txt, fibonacci.txt, taylor.txt])

    %% Phase 1
    P1[Phase 1: Lexical Analysis<br/>analisadorLexico]
    D1[(Deliverable 1:<br/>tokens.txt)]

    %% Phase 2
    P2[Phase 2: Syntax Analysis<br/>analisadorSintatico]
    D2[(Deliverable 2:<br/>syntax_tree.txt)]

    %% Phase 3
    P3[Phase 3: Semantic Analysis<br/>analisadorSemantico]
    D3[(Deliverable 3:<br/>attributed_ast.txt)]

    %% Phase 4.1
    P4_1[Phase 4.1: TAC Generation<br/>gerarTAC arvoreAtribuida]
    D4[(Deliverable 4:<br/>tac_unoptimized.txt)]

    %% Phase 4.2
    P4_2[Phase 4.2: TAC Optimization<br/>otimizarTAC tac]
    D5[(Deliverable 5:<br/>tac_optimized.txt)]

    %% Phase 4.3
    P4_3[Phase 4.3: Assembly Generation<br/>gerarAssembly tacOtimizado]
    D6[(Deliverable 6:<br/>program.s)]

    %% External Tools
    AVR[AVR Toolchain<br/>avr-gcc + avr-objcopy]
    D7[(Deliverable 7:<br/>program.hex)]

    Upload[Arduino Upload<br/>avrdude]
    Final([Running on Arduino Uno<br/>Serial/LED/LCD Output])

    %% Flow
    Start --> P1
    P1 --> D1
    D1 --> P2
    P2 --> D2
    D2 --> P3
    P3 --> D3
    D3 --> P4_1
    P4_1 --> D4
    D4 --> P4_2
    P4_2 --> D5
    D5 --> P4_3
    P4_3 --> D6
    D6 --> AVR
    AVR --> D7
    D7 --> Upload
    Upload --> Final

    %% Styling
    classDef phase fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef deliverable fill:#50C878,stroke:#2E7D4E,stroke-width:2px,color:#fff
    classDef external fill:#F39C12,stroke:#B8750A,stroke-width:2px,color:#fff
    classDef endpoint fill:#E74C3C,stroke:#A93226,stroke-width:2px,color:#fff

    class P1,P2,P3,P4_1,P4_2,P4_3 phase
    class D1,D2,D3,D4,D5,D6,D7 deliverable
    class AVR,Upload external
    class Start,Final endpoint
```

## Phase 4 Detailed Function Flow

```mermaid
flowchart LR
    subgraph Input
        AST[Attributed AST<br/>from Phase 3]
    end

    subgraph Phase4_1[Phase 4.1: TAC Generation]
        F1[gerarTAC arvoreAtribuida]
        F1_Steps[• Traverse AST<br/>• Generate temps t0, t1, t2...<br/>• Generate labels L0, L1, L2...<br/>• Convert RPN to TAC<br/>• Handle RES, MEM]
    end

    subgraph Phase4_2[Phase 4.2: TAC Optimization]
        F2[otimizarTAC tac]
        F2_Steps[• Constant Folding<br/>• Constant Propagation<br/>• Dead Code Elimination<br/>• Redundant Jump Removal]
    end

    subgraph Phase4_3[Phase 4.3: Assembly Generation]
        F3[gerarAssembly tacOtimizado]
        F3_Steps[• Map TAC to AVR<br/>• Allocate registers R16-R23<br/>• Generate prologue/epilogue<br/>• Handle 16-bit float ops<br/>• Create data section]
    end

    subgraph Outputs
        O1[(tac_unoptimized.txt)]
        O2[(tac_optimized.txt)]
        O3[(program.s)]
    end

    AST --> F1
    F1 --> F1_Steps
    F1_Steps --> O1
    O1 --> F2
    F2 --> F2_Steps
    F2_Steps --> O2
    O2 --> F3
    F3 --> F3_Steps
    F3_Steps --> O3

    classDef func fill:#9B59B6,stroke:#6C3483,stroke-width:2px,color:#fff
    classDef steps fill:#3498DB,stroke:#21618C,stroke-width:2px,color:#fff
    classDef output fill:#2ECC71,stroke:#1E8449,stroke-width:2px,color:#fff
    classDef input fill:#E67E22,stroke:#A04000,stroke-width:2px,color:#fff

    class F1,F2,F3 func
    class F1_Steps,F2_Steps,F3_Steps steps
    class O1,O2,O3 output
    class AST input
```

## TAC Optimization Techniques Detail

```mermaid
flowchart TD
    Input[Unoptimized TAC]

    subgraph Optimizations
        CF[Constant Folding<br/>t1 = 2 + 3 → t1 = 5]
        CP[Constant Propagation<br/>t1 = 5; t2 = t1 + 3 → t2 = 8]
        DCE[Dead Code Elimination<br/>Remove unused temps]
        RJE[Redundant Jump Elimination<br/>goto L1; L1: → L1:]
    end

    Output[Optimized TAC]

    Input --> CF
    CF --> CP
    CP --> DCE
    DCE --> RJE
    RJE --> Output

    classDef opt fill:#16A085,stroke:#0E6655,stroke-width:2px,color:#fff
    class CF,CP,DCE,RJE opt
```

## Test Files to Deliverables Mapping

```mermaid
flowchart LR
    subgraph TestFiles[Input Files]
        T1[fatorial.txt]
        T2[fibonacci.txt]
        T3[taylor.txt]
    end

    subgraph Deliverables[7 Deliverables Each]
        D1[1. tokens.txt]
        D2[2. syntax_tree.txt]
        D3[3. attributed_ast.txt]
        D4[4. tac_unoptimized.txt]
        D5[5. tac_optimized.txt]
        D6[6. program.s]
        D7[7. program.hex]
    end

    T1 --> D1
    T2 --> D1
    T3 --> D1

    D1 --> D2 --> D3 --> D4 --> D5 --> D6 --> D7

    Total[Total: 21 output files]
    Deliverables --> Total

    classDef test fill:#E74C3C,stroke:#922B21,stroke-width:2px,color:#fff
    classDef deliv fill:#27AE60,stroke:#145A32,stroke-width:2px,color:#fff

    class T1,T2,T3 test
    class D1,D2,D3,D4,D5,D6,D7 deliv
```

## Usage

You can copy the Mermaid code blocks and paste them into:
- GitHub/GitLab markdown files (renders automatically)
- Mermaid Live Editor: https://mermaid.live
- VS Code with Mermaid extension
- Documentation tools that support Mermaid
