# Relatório de Erros Semânticos

**Gerado em:** 2025-11-05 15:16:19

##  Erros Encontrados (4)

### Erro 1
```
ERRO SEMÂNTICO [Linha 10]: Operador '/' requer operandos inteiros. Recebido: real, int
Contexto: (5.5 / 2)
```

### Erro 2
```
ERRO SEMÂNTICO [Linha 11]: Operador '%' requer operandos inteiros. Recebido: real, int
Contexto: (10.5 % 3)
```

### Erro 3
```
ERRO SEMÂNTICO [Linha 12]: Operador '^' requer base numérica e expoente inteiro. Recebido: base=int, expoente=real
Contexto: (2 ^ 3.5)
```

### Erro 4
```
ERRO SEMÂNTICO [Linha 13]: Variável 'UNDEFINED_VAR' não declarada
Contexto: (UNDEFINED_VAR)
```

## Resumo

- **Total de erros:** 4
- **Status:** Análise semântica falhou

---
*Relatório gerado automaticamente pelo Compilador RA3_1*