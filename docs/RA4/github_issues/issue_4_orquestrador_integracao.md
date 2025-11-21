# Issue Principal 4: Orquestrador Principal & Integração

**Responsável:** Aluno 4
**Labels:** `phase-4`, `integration`, `testing`, `aluno-4`

## Descrição

Integrar todas as 4 fases, criar arquivos de teste, validar no hardware Arduino, e gerar documentação completa.

## Entrada

- Arquivos fonte .txt (programas de teste)
- Argumento de linha de comando

## Saída

- Todos os arquivos intermediários de todas as fases
- Arquivo program.hex
- Documentação completa
- Evidências de validação

---

## Sub-Issues

### 4.1 Implementação da Função Main
**Descrição:**
- Fazer parse de linha de comando: `./compilador <arquivo.txt>`
- Orquestrar execução de todas as 4 fases:
  1. Análise Léxica (RA1)
  2. Análise Sintática (RA2)
  3. Análise Semântica (RA3)
  4. Geração de TAC
  5. Otimização de TAC
  6. Geração de Assembly
- Tratar erros em cada fase

**Critério de Aceitação:**
- [ ] Todas as fases executam em sequência
- [ ] Argumentos de linha de comando funcionam
- [ ] Tratamento de erro em cada fase
- [ ] Mensagens de progresso apropriadas

---

### 4.2 Gerenciamento de I/O de Arquivos
**Descrição:**
- Ler arquivo fonte
- Escrever todas as saídas intermediárias:
  - tokens.txt (Fase 1)
  - arvore_sintatica.json (Fase 2)
  - arvore_atribuida.json (Fase 3)
  - TAC.txt, TAC.json (Fase 4.1)
  - TAC_otimizado.txt, TAC_otimizado.json (Fase 4.2)
  - program.s (Fase 4.3)
- Criar estrutura de diretórios de saída

**Estrutura de Diretórios:**
```
outputs/
  RA1/
    tokens/
      tokens_gerados.txt
  RA2/
    arvore_sintatica.json
  RA3/
    arvore_atribuida.json
    relatorios/
  RA4/
    TAC.txt
    TAC.json
    TAC_otimizado.txt
    TAC_otimizado.json
    relatorio_otimizacoes.md
    program.s
    program.hex
```

**Critério de Aceitação:**
- [ ] Todos os arquivos escritos nos locais corretos
- [ ] Estrutura de diretórios criada automaticamente
- [ ] Tratamento de erro de I/O
- [ ] Permissões de arquivo corretas

---

### 4.3 Arquivo de Teste: fatorial.txt
**Descrição:**
- Implementar cálculo de fatorial de 1 a 8 (conforme spec do RA4)
- Usar notação RPN exclusivamente

**Requisitos:**
- Calcular n! para n = 1 a 8
- Usar estrutura de laço
- Armazenar/exibir resultados
- Demonstrar uso de variáveis

**Valores Esperados:**
```
1! = 1
2! = 2
3! = 6
4! = 24
5! = 120
6! = 720
7! = 5040
8! = 40320
```

**Critério de Aceitação:**
- [ ] Produz valores de fatorial corretos
- [ ] Usa sintaxe RPN válida
- [ ] Compila através de todas as fases
- [ ] Executa corretamente no Arduino

---

### 4.4 Arquivo de Teste: fibonacci.txt
**Descrição:**
- Implementar sequência de Fibonacci até a 24ª posição
- Usar notação RPN

**Requisitos:**
- Calcular os primeiros 24 números de Fibonacci
- Usar estrutura de laço
- Armazenar/exibir resultados
- Usar MEM para armazenamento de variáveis

**Valores Esperados:**
```
F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
...
F(24) = 46368
```

**Critério de Aceitação:**
- [ ] Produz sequência de Fibonacci correta
- [ ] Usa sintaxe RPN válida
- [ ] Compila através de todas as fases
- [ ] Executa corretamente no Arduino

---

### 4.5 Arquivo de Teste: taylor.txt
**Descrição:**
- Implementar série de Taylor para cosseno (4 termos)
- Fórmula: `cos(x) ≈ 1 - x²/2! + x⁴/4! - x⁶/6!`
- Usar notação RPN com divisão real `|`

**Requisitos:**
- Usar operações de ponto flutuante
- Armazenar valor de X em MEM
- Calcular e armazenar resultado
- Demonstrar precisão de float de 16 bits

**Teste com x=1.0:**
- Esperado: ~0.54 (considerando perda de precisão)
- Real: cos(1.0) = 0.5403023...

**Critério de Aceitação:**
- [ ] Demonstra capacidade de ponto flutuante
- [ ] Usa divisão real `|`
- [ ] Usa literais de ponto flutuante (1.0, 2.0, etc.)
- [ ] Resultado está dentro de margem de erro esperada
- [ ] Compila e executa no Arduino

---

### 4.6 Scripts de Automação de Build
**Descrição:**
- Criar script para compilar Assembly para HEX:
  ```bash
  avr-gcc -mmcu=atmega328p -o program.elf program.s
  avr-objcopy -O ihex program.elf program.hex
  ```
- Tratar erros de build
- Automatizar processo

**Critério de Aceitação:**
- [ ] Processo de build automatizado funciona
- [ ] Erros são capturados e reportados
- [ ] program.hex gerado corretamente
- [ ] Script funciona em Linux/macOS

---

### 4.7 Script de Upload para Arduino
**Descrição:**
- Criar script de upload:
  ```bash
  avrdude -c arduino -p atmega328p -P /dev/ttyACM0 -b 9600 -U flash:w:program.hex
  ```
- Suportar configuração de porta serial customizada
- Detectar Arduino automaticamente se possível

**Critério de Aceitação:**
- [ ] Pode fazer upload para Arduino Uno
- [ ] Suporta múltiplas portas seriais
- [ ] Erros de upload são tratados
- [ ] Instruções de uso documentadas

---

### 4.8 Validação no Arduino
**Descrição:**
- Fazer upload de todos os 3 programas de teste para Arduino
- Verificar execução:
  - Saída serial (9600 baud)
  - Indicadores LED
  - Display LCD (se disponível)
- Capturar resultados (screenshots/vídeos)
- Criar `validacao_arduino.md` (conforme linha 474 da especificação)

**Formato validacao_arduino.md:**
```markdown
# Validação no Arduino Uno - Projeto RA4

## 1. Informações do Hardware
- Placa: Arduino Uno R3
- Microcontrolador: ATmega328P
- Porta Serial: /dev/ttyACM0
- Baud Rate: 9600

## 2. Teste 1: fatorial.txt

### Processo de Upload
- Comando: `avrdude -c arduino -p atmega328p -P /dev/ttyACM0 -b 9600 -U flash:w:fatorial.hex`
- Status: ✅ Sucesso

### Resultados Observados
[Inserir foto/screenshot da saída serial ou LEDs]

**Saída Serial:**
```
[log da saída serial]
```

### Resultados Esperados
```
1! = 1
2! = 2
3! = 6
...
```

### Análise
- ✅ Resultados correspondem ao esperado
- Observações: [qualquer nota relevante]

## 3. Teste 2: fibonacci.txt
[mesmo formato]

## 4. Teste 3: taylor.txt

### Análise de Precisão (16-bit float)
- Valor calculado: [valor]
- Valor esperado: cos(1.0) = 0.5403023...
- Erro absoluto: [diferença]
- Análise: [discussão sobre perda de precisão com 16-bit]

## 5. Evidências
- [x] Fotos do Arduino em execução
- [x] Vídeos da execução (se aplicável)
- [x] Logs completos da saída serial
- [x] Screenshots do monitor serial

## 6. Conclusão
[Resumo da validação no hardware]
```

**Critério de Aceitação:**
- [ ] Todos os 3 programas rodam corretamente no hardware
- [ ] Resultados são observáveis
- [ ] validacao_arduino.md criado e completo
- [ ] Evidências capturadas (fotos/vídeos/logs serial)
- [ ] Resultados correspondem aos esperados
- [ ] Análise de precisão para taylor.txt incluída

---

### 4.9 Sistema de Tratamento de Erros
**Descrição:**
- Implementar detecção de erro para cada fase:
  - Erros léxicos (do RA1)
  - Erros sintáticos (do RA2)
  - Erros semânticos (do RA3)
  - Erros de geração de TAC
  - Erros de otimização
  - Erros de geração de Assembly
  - Erros de build
- Mensagens de erro claras com números de linha

**Critério de Aceitação:**
- [ ] Relatório de erro amigável ao usuário
- [ ] Números de linha incluídos quando aplicável
- [ ] Tipo de erro claramente identificado
- [ ] Mensagens sugerem possíveis correções

---

### 4.10 Documentação README.md
**Descrição:**
- Atualizar README conforme seção 13.4 da especificação com:
  - Nome da instituição de ensino, ano, disciplina, professor
  - Integrantes do grupo em ordem alfabética (com usuários GitHub)
  - Instruções para compilar, executar e depurar todas as fases
  - Como executar: `./compilador <arquivo.txt>`
  - Como fazer build para Arduino
  - Como fazer upload para Arduino
  - **Documentação das otimizações implementadas**
  - **Documentação das convenções de registradores AVR**
  - Descrições dos 3 arquivos de teste
  - Exemplos de uso e resultados esperados

**Seções Obrigatórias do README:**
```markdown
# Compilador RPN para Arduino Uno - RA4

## 1. Informações Institucionais
- Instituição: [nome]
- Curso: [nome]
- Disciplina: [nome]
- Professor: [nome]
- Ano: 2025

## 2. Integrantes do Grupo
- Nome 1 - GitHub: @username1
- Nome 2 - GitHub: @username2
- Nome 3 - GitHub: @username3
- Nome 4 - GitHub: @username4

## 3. Descrição do Projeto
[Breve descrição]

## 4. Instruções de Compilação
[Como compilar o compilador]

## 5. Instruções de Execução
```bash
./compilador fatorial.txt
./compilador fibonacci.txt
./compilador taylor.txt
```

## 6. Build para Arduino
[Passos completos]

## 7. Upload para Arduino
[Instruções detalhadas]

## 8. Otimizações Implementadas
### 8.1 Constant Folding
[Descrição breve]

### 8.2 Constant Propagation
[Descrição breve]

### 8.3 Dead Code Elimination
[Descrição breve]

### 8.4 Eliminação de Saltos Redundantes
[Descrição breve]

## 9. Convenções de Registradores AVR
[Resumo das convenções - link para convencoes_registradores.md]

## 10. Arquivos de Teste
### fatorial.txt
[Descrição e resultados esperados]

### fibonacci.txt
[Descrição e resultados esperados]

### taylor.txt
[Descrição e resultados esperados]

## 11. Estrutura de Arquivos Gerados
[Lista dos 11 arquivos por teste]

## 12. Exemplos de Uso
[Exemplos práticos completos]
```

**Critério de Aceitação:**
- [ ] README completo conforme seção 13.4
- [ ] Todas as seções obrigatórias presentes
- [ ] Informações institucionais corretas
- [ ] Integrantes em ordem alfabética com GitHub
- [ ] Instruções para todas as fases
- [ ] Documentação de otimizações implementadas incluída
- [ ] Documentação de convenções de registradores incluída
- [ ] Instruções são claras e testadas
- [ ] Formatação markdown correta
- [ ] Exemplos funcionam

---

### 4.11 Testes de Integração Final
**Descrição:**
- Testar pipeline completo para todos os 3 arquivos
- Verificar todos os arquivos de saída gerados
- Checar consistência de arquivos
- Benchmark de performance

**Critério de Aceitação:**
- [ ] Testes end-to-end passam
- [ ] Todos os arquivos de saída são válidos
- [ ] Sem erros de integração
- [ ] Performance é aceitável

---

### 4.12 Organização do Repositório
**Descrição:**
- Garantir histórico de commits limpo
- Criar pull requests para features principais
- Marcar release final
- Organizar estrutura de diretórios:
  ```
  /src/RA1/   - Analisador léxico
  /src/RA2/   - Analisador sintático
  /src/RA3/   - Analisador semântico
  /src/RA4/   - Gerador de código
  /tests/     - Arquivos de teste
  /outputs/   - Arquivos gerados
  /docs/      - Documentação
  /scripts/   - Scripts de build e upload
  ```

**Critério de Aceitação:**
- [ ] Repositório limpo e profissional
- [ ] Histórico de commits é significativo
- [ ] Pull requests usados apropriadamente
- [ ] Estrutura de diretórios organizada
- [ ] Arquivo .gitignore apropriado

---

## Dependências

- Requer trabalho de todos os alunos (1, 2, 3) estar completo
- Precisa de acesso a hardware Arduino Uno
- Precisa de toolchain AVR instalada

## Critérios de Aceitação Gerais

- [ ] Função main orquestra todas as fases
- [ ] Todos os 3 arquivos de teste criados e funcionando
- [ ] Scripts de automação de build funcionando
- [ ] Todos os 3 programas validados no Arduino
- [ ] validacao_arduino.md criado e completo
- [ ] Evidências de execução no Arduino (fotos/vídeos/logs serial)
- [ ] README.md completo conforme seção 13.4
- [ ] Todos os arquivos de saída gerados corretamente
- [ ] Tratamento de erro para todas as fases
- [ ] Repositório bem organizado
- [ ] Histórico Git limpo com commits significativos

## Checklist de Validação Final

### Para Cada Arquivo de Teste (fatorial, fibonacci, taylor):
- [ ] Compila sem erros léxicos
- [ ] Compila sem erros sintáticos
- [ ] Compila sem erros semânticos
- [ ] TAC gerado corretamente
- [ ] TAC otimizado mostra melhorias
- [ ] Assembly gerado sem erros
- [ ] Assembly compila para .hex
- [ ] .hex pode ser carregado no Arduino
- [ ] Programa executa corretamente no hardware
- [ ] Resultados correspondem aos esperados

### Arquivos de Saída (33 total: 11 por teste):

**Arquivos de Dados:**
- [ ] tokens.txt (3 arquivos - RA1)
- [ ] arvore_sintatica.json (3 arquivos - RA2)
- [ ] arvore_atribuida.json (3 arquivos - RA3)
- [ ] TAC.json (3 arquivos - RA4)
- [ ] TAC_otimizado.json (3 arquivos - RA4)
- [ ] program.s (3 arquivos - RA4)
- [ ] program.hex (3 arquivos - RA4)

**Arquivos de Documentação (Markdown):**
- [ ] TAC.md (3 arquivos - representação legível do TAC)
- [ ] TAC_otimizado.md (3 arquivos - representação legível do TAC otimizado)
- [ ] relatorio_otimizacoes.md (3 arquivos - relatório completo de otimizações)
- [ ] assembly.md (3 arquivos - documentação do Assembly gerado)

### Documentação Geral (repositório):
- [ ] README.md completo (conforme seção 13.4)
- [ ] convencoes_registradores.md (documentação de registradores AVR)
- [ ] validacao_arduino.md (processo de validação no hardware)
- [ ] INTERFACES.md (acordos de interface entre alunos)

## Ferramentas Necessárias

- **Toolchain AVR:**
  ```bash
  sudo apt-get install gcc-avr avr-libc avrdude
  ```
- **Arduino Uno** ou SimulIDE para simulação
- **Monitor Serial:** Arduino IDE ou `screen`/`minicom`

## Exemplo de Uso

```bash
# Compilar programa de teste
./compilador tests/fatorial.txt

# Arquivos gerados em outputs/RA4/
ls outputs/RA4/
# TAC.txt  TAC_otimizado.txt  program.s  program.hex

# Fazer upload para Arduino
./scripts/upload_arduino.sh outputs/RA4/program.hex

# Monitorar saída serial
screen /dev/ttyACM0 9600
```
