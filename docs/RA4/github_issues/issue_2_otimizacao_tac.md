# Issue Principal 2: Otimização de TAC (otimizarTAC)

**Responsável:** Aluno 2
**Labels:** `phase-4`, `optimization`, `aluno-2`

## Descrição

Implementar técnicas de otimização local no TAC para reduzir contagem de instruções e melhorar eficiência.

## Entrada

- Lista de instruções TAC de `gerarTAC()`
- Arquivo TAC.json

## Saída

- Lista otimizada de instruções TAC
- Arquivo: `TAC_otimizado.json` (dados estruturados para gerador Assembly)
- Arquivo: `TAC_otimizado.md` (representação markdown legível)
- Arquivo: `relatorio_otimizacoes.md` (relatório completo de otimizações)

---

## Sub-Issues

### 2.1 Parser de TAC e Estrutura de Dados
**Descrição:**
- Fazer parse de TAC.json em objetos de instrução
- Validar formato TAC do Aluno 1
- Criar representação interna para passes de otimização

**Critério de Aceitação:**
- [ ] Pode carregar e fazer parse de TAC do Aluno 1
- [ ] Validação de formato funciona
- [ ] Estrutura de dados interna está definida

---

### 2.2 Implementação de Constant Folding
**Descrição:**
- Implementar como **passagem separada** que varre todo o TAC
- Detectar expressões constantes em tempo de compilação
- Avaliar: `t1 = 2 + 3` → `t1 = 5`
- Tratar todos os operadores aritméticos
- Tratar tipos inteiros e reais
- Retornar `True` se alguma mudança foi feita, `False` caso contrário

**Exemplo:**
```
Antes: t1 = 2 + 3
       t2 = 10 * 5
Depois: t1 = 5
        t2 = 50
```

**Critério de Aceitação:**
- [ ] Todas as expressões constantes são avaliadas em tempo de compilação
- [ ] Funciona com operadores: +, -, *, /, |, %, ^
- [ ] Trata tipos int e real corretamente
- [ ] Não altera semântica do programa

---

### 2.3 Implementação de Constant Propagation
**Descrição:**
- Implementar como **passagem separada** que varre todo o TAC
- Rastrear valores constantes conhecidos
- Propagar através de instruções subsequentes
- Substituir referências de variáveis por constantes
- Retornar `True` se alguma mudança foi feita, `False` caso contrário

**Exemplo:**
```
Antes: t1 = 5
       t2 = t1 + 3
       t3 = t1 * 2
Depois: t1 = 5
        t2 = 8
        t3 = 10
```

**Critério de Aceitação:**
- [ ] Constantes são propagadas através do código
- [ ] Mapa de valores conhecidos é mantido
- [ ] Funciona com múltiplas referências
- [ ] Não propaga além de redefinições

---

### 2.4 Implementação de Dead Code Elimination
**Descrição:**
- Implementar como **passagem separada** que varre todo o TAC
- Construir cadeias use-def
- Identificar temporários não utilizados
- Remover atribuições que nunca são lidas
- Remover código inalcançável após saltos incondicionais
- Retornar `True` se alguma mudança foi feita, `False` caso contrário

**Exemplo:**
```
Antes: t1 = 5
       t2 = 3          // t2 nunca usado
       t3 = t1 + 2
       goto L1
       t4 = 10         // código inalcançável
       L1:
Depois: t1 = 5
        t3 = t1 + 2
        goto L1
        L1:
```

**Critério de Aceitação:**
- [ ] Código não utilizado é removido com segurança
- [ ] Código inalcançável é detectado e removido
- [ ] Análise use-def está funcionando
- [ ] Semântica do programa é preservada

---

### 2.5 Eliminação de Saltos Redundantes
**Descrição:**
- Implementar como **passagem separada** que varre todo o TAC
- Detectar saltos para próxima instrução
- Detectar saltos para rótulos não utilizados
- Remover rótulos desnecessários
- Retornar `True` se alguma mudança foi feita, `False` caso contrário

**Exemplo:**
```
Antes: goto L1
       L1:
       t1 = 5
       goto L2
       L2:
       t2 = 3
Depois: t1 = 5
        t2 = 3
```

**Critério de Aceitação:**
- [ ] Saltos redundantes são eliminados
- [ ] Rótulos não utilizados são removidos
- [ ] Saltos para próxima instrução removidos
- [ ] Fluxo de controle permanece correto

---

### 2.6 Análise de Liveness (Auxiliar)
**Descrição:**
- Implementar análise básica de liveness
- Rastrear uso de variáveis através de instruções
- Suportar dead code elimination

**Critério de Aceitação:**
- [ ] Rastreia tempo de vida de variáveis com precisão
- [ ] Identifica última utilização de variável
- [ ] Suporta análise através de rótulos
- [ ] Funciona com saltos condicionais

---

### 2.7 Geração de Relatórios e Documentação
**Descrição:**
- Gerar `TAC_otimizado.md` (representação legível do TAC otimizado)
- Gerar `relatorio_otimizacoes.md` (relatório completo conforme especificação)
- Contar instruções antes/depois de cada otimização
- Rastrear temporários eliminados

**Formato TAC_otimizado.md:**
```markdown
# TAC Otimizado - [nome_arquivo]

## Linha X: [expressão original]
[instruções TAC otimizadas]

## Estatísticas
- Total de instruções: N
- Temporários criados: N
- Rótulos: N
```

**Formato relatorio_otimizacoes.md (conforme seção 13.5 do documento):**
```markdown
# Relatório de Otimizações - [nome_arquivo]

## 1. Resumo Executivo
- Instruções antes: X
- Instruções depois: Y
- Redução: Z%
- Temporários eliminados: N

## 2. Técnicas Implementadas

### 2.1 Constant Folding
**Descrição:** [explicação da técnica]

**Exemplo:**
Antes:
[código TAC]

Depois:
[código TAC otimizado]

**Impacto:** [estatísticas]

### 2.2 Constant Propagation
[mesmo formato]

### 2.3 Dead Code Elimination
[mesmo formato]

### 2.4 Eliminação de Saltos Redundantes
[mesmo formato]

## 3. Estatísticas Detalhadas
- Número de instruções TAC antes: X
- Número de instruções TAC depois: Y
- Número de temporários eliminados: Z
- Redução percentual: W%

## 4. Análise do Impacto no Código Assembly Gerado
[análise de como as otimizações afetaram o Assembly final]
```

**Critério de Aceitação:**
- [ ] TAC_otimizado.md gerado em formato markdown legível
- [ ] relatorio_otimizacoes.md completo conforme especificação oficial
- [ ] Descrição de cada técnica de otimização implementada
- [ ] Exemplos de código TAC antes e depois de cada otimização
- [ ] Estatísticas: número de instruções antes/depois, temporários eliminados
- [ ] Análise do impacto no código Assembly gerado
- [ ] Formatação markdown correta

---

### 2.8 Pipeline de Otimização Multi-Pass
**Descrição:**
- Implementar cada otimização como **uma passagem separada** (conforme linha 338 da especificação)
- Executar passagens em ordem ótima
- Iterar até ponto fixo (sem mais mudanças possíveis)

**Ordem de Passagens (Passes):**
1. **Pass 1:** Constant Folding - varrer TAC e avaliar expressões constantes
2. **Pass 2:** Constant Propagation - varrer TAC e propagar constantes conhecidas
3. **Pass 3:** Dead Code Elimination - varrer TAC e remover código não utilizado
4. **Pass 4:** Eliminação de Saltos Redundantes - varrer TAC e otimizar saltos

**Algoritmo Multi-Pass:**
```
mudou = True
iteracao = 0

while mudou:
    iteracao++
    mudou = False

    # Pass 1: Constant Folding
    if aplicar_constant_folding(tac):
        mudou = True

    # Pass 2: Constant Propagation
    if aplicar_constant_propagation(tac):
        mudou = True

    # Pass 3: Dead Code Elimination
    if aplicar_dead_code_elimination(tac):
        mudou = True

    # Pass 4: Jump Elimination
    if aplicar_jump_elimination(tac):
        mudou = True

    # Limite de segurança
    if iteracao > 100:
        break
```

**Por que Multi-Pass?**
- Uma otimização pode criar oportunidades para outra
- Exemplo: constant folding pode criar código morto que será eliminado no próximo pass
- Repetir até nenhuma otimização ter efeito (ponto fixo)

**Critério de Aceitação:**
- [ ] Cada otimização implementada como passagem separada (conforme spec)
- [ ] Múltiplos passes/iterações melhoram otimização
- [ ] Converge para ponto fixo (mudou = False)
- [ ] Não entra em loop infinito (limite de iterações)
- [ ] Ordem de passes está documentada
- [ ] Registra número de iterações até convergência

---

## Dependências

- Requer formato TAC do Aluno 1 estar estável
- Deve produzir formato TAC compatível com Aluno 3 (gerador Assembly)

## Critérios de Aceitação Gerais

- [ ] Todas as 4 técnicas de otimização implementadas
- [ ] Cada técnica documentada com exemplos no relatório
- [ ] TAC_otimizado.json gerado corretamente
- [ ] TAC_otimizado.md gerado em formato markdown legível
- [ ] relatorio_otimizacoes.md completo conforme seção 13.5 da especificação
- [ ] Relatório mostra melhorias mensuráveis
- [ ] Funciona em todos os 3 arquivos de teste
- [ ] Preserva semântica do programa (corretude)
- [ ] Itera até ponto fixo
- [ ] Sem loops infinitos no otimizador

## Métricas de Sucesso

Para cada arquivo de teste, o relatório deve mostrar:
- **Redução de instruções:** Antes vs. Depois
- **Temporários eliminados:** Contagem
- **Constantes dobradas:** Número de expressões avaliadas
- **Saltos removidos:** Contagem

Exemplo esperado:
```
fatorial.txt:
  - Instruções: 50 → 35 (30% redução)
  - Temporários eliminados: 8
  - Expressões constantes avaliadas: 5
  - Saltos redundantes removidos: 3
```

## Interface com Outros Componentes

**Entrada esperada (do Aluno 1):**
```json
{
  "instructions": [
    {"type": "assignment", "dest": "t0", "source": "2", "line": 1},
    {"type": "assignment", "dest": "t1", "source": "3", "line": 1},
    {"type": "binary_op", "result": "t2", "op1": "t0", "operator": "+", "op2": "t1", "line": 1}
  ]
}
```

**Saída esperada (para Aluno 3):**
```json
{
  "instructions": [
    {"type": "assignment", "dest": "t2", "source": "5", "line": 1}
  ]
}
```
