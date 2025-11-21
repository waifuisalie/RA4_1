# Issue Principal 1: Geração de TAC (gerarTAC)

**Responsável:** Aluno 1
**Labels:** `phase-4`, `tac-generation`, `aluno-1`

## Descrição

Implementar o gerador de Código de Três Endereços (TAC - Three Address Code) que transforma a AST atribuída da Fase 3 em representação intermediária TAC.

## Entrada

- AST atribuída da Fase 3 (formato JSON de `/outputs/RA3/arvore_atribuida.json`)
- Estrutura inclui: `tipo_vertice`, `tipo_inferido`, `operador`, `valor`, `filhos`, `numero_linha`

## Saída

- Lista de instruções TAC (lista Python/array)
- Arquivo: `TAC.json` (dados estruturados para otimizador processar)
- Arquivo: `TAC.md` (representação markdown legível para humanos)

---

## Sub-Issues

### 1.1 Definir Estruturas de Dados TAC
**Descrição:**
- Criar classe/interface base `TACInstruction`
- Implementar tipos de instrução:
  - `Assignment` (t1 = a)
  - `BinaryOp` (t1 = a op b)
  - `UnaryOp` (t1 = -a)
  - `Label` (L1:)
  - `Jump` (goto L1)
  - `ConditionalJump` (if a goto L1, ifFalse a goto L1)
  - `MemoryAccess` (t1 = MEM[a], MEM[a] = t1)
- Adicionar método `toString()` para saída em arquivo

**Critério de Aceitação:**
- [ ] Todas as classes de instrução definidas com atributos apropriados
- [ ] Método `toString()` funcionando para todas as instruções

---

### 1.2 Implementar Gerenciamento de Temporários e Rótulos
**Descrição:**
- Criar contador para temporários: `t0`, `t1`, `t2`, ...
- Criar contador para rótulos: `L0`, `L1`, `L2`, ...
- Funções: `newTemp()`, `newLabel()`, `resetCounters()`

**Critério de Aceitação:**
- [ ] Pode gerar temporários únicos
- [ ] Pode gerar rótulos únicos
- [ ] Contadores podem ser resetados entre programas

---

### 1.3 Motor de Travessia da AST
**Descrição:**
- Implementar travessia em pós-ordem da AST atribuída
- Visitar filhos antes dos pais (bottom-up)
- Rastrear números de linha para relatório de erros

**Critério de Aceitação:**
- [ ] Pode percorrer toda a estrutura da AST do RA3
- [ ] Travessia em pós-ordem funciona corretamente
- [ ] Números de linha são preservados

---

### 1.4 Geração de Expressões Aritméticas
**Descrição:**
- Tratar operadores: `+`, `-`, `*`, `/`, `|`, `%`, `^`
- Gerar código para operações binárias em formato RPN `(A B op)`
- Tratar informação de tipo de `tipo_inferido`

**Exemplo:**
```
Entrada: (5 3 +) com tipo_inferido=int
Saída:
  t0 = 5
  t1 = 3
  t2 = t0 + t1
```

**Critério de Aceitação:**
- [ ] Todos os operadores aritméticos geram TAC correto
- [ ] Tipos int e real são tratados corretamente
- [ ] Expressões aninhadas funcionam

---

### 1.5 Operações de Comparação e Lógicas
**Descrição:**
- Tratar: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Tratar: `&&`, `||`, `!`
- Gerar temporários para resultados booleanos

**Critério de Aceitação:**
- [ ] Operações de comparação produzem TAC correto
- [ ] Operações lógicas funcionam
- [ ] Resultados booleanos são tratados corretamente

---

### 1.6 Comandos Especiais (RES e MEM)
**Descrição:**
- Implementar `(N RES)`: Acessar resultado N linhas anteriores
- Implementar `(V MEM)`: Armazenar valor na memória
- Implementar `(MEM)`: Recuperar da memória
- Manter array de histórico de resultados
- Gerenciar nomenclatura de variáveis de memória

**Critério de Aceitação:**
- [ ] Comando RES funciona corretamente
- [ ] Comando MEM (armazenar) funciona
- [ ] Comando MEM (recuperar) funciona
- [ ] Histórico de resultados é mantido

---

### 1.7 Estruturas de Fluxo de Controle
**Descrição:**
- Gerar TAC para declarações if-else
- Gerar TAC para laços (while, for)
- Criar rótulos para ramificações
- Gerar saltos condicionais

**Critério de Aceitação:**
- [ ] Estruturas de controle produzem lógica de salto correta
- [ ] Laços while funcionam
- [ ] Laços for funcionam
- [ ] If-else funciona corretamente

---

### 1.8 Saída de Arquivo e Serialização
**Descrição:**
- Escrever TAC.json para entrada do otimizador (dados estruturados)
- Escrever TAC.md em formato markdown legível para humanos
- Incluir comentários com números de linha originais no .md
- Incluir estatísticas no .md (total de instruções, temporários, rótulos)

**Formato TAC.md:**
```markdown
# TAC Gerado - [nome_arquivo]

## Linha X: [expressão original]
[instruções TAC]

## Estatísticas
- Total de instruções: N
- Temporários criados: N
- Rótulos: N
```

**Critério de Aceitação:**
- [ ] TAC.json gerado corretamente com estrutura válida
- [ ] TAC.md gerado em formato markdown legível
- [ ] TAC.md inclui números de linha originais
- [ ] TAC.md inclui seção de estatísticas
- [ ] Ambos os arquivos têm conteúdo consistente

---

## Dependências

- Requer saída do RA3 (AST atribuída) no formato correto
- Deve coordenar formato TAC com Aluno 2 (entrada do otimizador)

## Critérios de Aceitação Gerais

- [ ] Todos os tipos de instrução TAC implementados
- [ ] Processa com sucesso todos os 3 arquivos de teste (fatorial, fibonacci, taylor)
- [ ] TAC.json tem dados estruturados para otimizador
- [ ] TAC.md é legível em markdown com formatação correta
- [ ] Trata todos os operadores RPN corretamente
- [ ] Comandos RES e MEM funcionam
- [ ] Sem crashes em entrada válida
- [ ] Mensagens de erro claras para AST inválida
- [ ] Estatísticas corretas no TAC.md

## Interface com Outros Componentes

**Entrada esperada do RA3:**
```json
{
  "arvore_atribuida": [
    {
      "tipo_vertice": "LINHA",
      "tipo_inferido": "int",
      "numero_linha": 1,
      "operador": "+",
      "filhos": [
        {
          "tipo_vertice": "ARITH_OP",
          "operador": "+",
          "tipo_inferido": "int",
          "filhos": [
            {"valor": "5", "tipo_inferido": "int", "subtipo": "numero_inteiro"},
            {"valor": "3", "tipo_inferido": "int", "subtipo": "numero_inteiro"}
          ]
        }
      ]
    }
  ]
}
```

**Saída esperada (TAC.json):**
```json
{
  "instructions": [
    {"type": "assignment", "dest": "t0", "source": "5", "line": 1},
    {"type": "assignment", "dest": "t1", "source": "3", "line": 1},
    {"type": "binary_op", "result": "t2", "op1": "t0", "operator": "+", "op2": "t1", "line": 1}
  ]
}
```
