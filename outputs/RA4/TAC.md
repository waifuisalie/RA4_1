# Saída TAC - arvore_atribuida.json

**Gerado:** 2025-11-21 18:43:46

## Estatísticas

| Métrica | Valor |
|---------|-------|
| total_instrucoes | 102 |
| contador_temp | 73 |
| contador_rotulo | 10 |
| tamanho_historico_resultados | 19 |

## Instruções

```
# Linha 1
    t0 = 5  ; [int]
    t1 = 3  ; [int]
    t2 = t0 + t1  ; [int]

# Linha 2
    t3 = 10.5  ; [real]
    t4 = 2.0  ; [real]
    t5 = t3 * t4  ; [real]

# Linha 3
    t6 = 100  ; [int]
    t7 = 50  ; [int]
    t8 = t6 + t7  ; [int]

# Linha 4
    t9 = 15  ; [int]
    t10 = 7  ; [int]
    t11 = t9 / t10  ; [int]

# Linha 5
    t12 = 23  ; [int]
    t13 = 6  ; [int]
    t14 = t12 % t13  ; [int]

# Linha 6
    t15 = 2.5  ; [real]
    t16 = 3  ; [int]
    t17 = t15 ^ t16  ; [real]

# Linha 7
    t18 = 5.5  ; [real]
    t19 = 3.2  ; [real]
    t20 = t18 > t19  ; [boolean]

# Linha 8
    t21 = 5  ; [int]
    t22 = 3  ; [int]
    t23 = t21 > t22  ; [boolean]
    t24 = 2  ; [int]
    t25 = 1  ; [int]
    t26 = t24 < t25  ; [boolean]
    t27 = t23 && t26  ; [boolean]

# Linha 9
    t28 = 10  ; [int]
    X = t28  ; [int]

# Linha 10
    t29 = 20  ; [int]
    A = t29  ; [int]

# Linha 11
    t30 = 10  ; [int]
    I = t30  ; [int]

# Linha 12
    t31 = 0  ; [int]
    COUNTER = t31  ; [int]

# Linha 13
    t32 = 5  ; [int]
    t33 = X + t32  ; [int]
    Y = t33  ; [int]

# Linha 14
    t34 = A - X  ; [int]
    B = t34  ; [int]

# Linha 15
    t35 = 1  ; [int]

# Linha 16
    t36 = 2  ; [int]

# Linha 17
    L0:
    t37 = 5  ; [int]
    t38 = COUNTER < t37  ; [boolean]
    ifFalse t38 goto L1
    t39 = 1  ; [int]
    t40 = COUNTER + t39  ; [int]
    COUNTER = t40  ; [int]
    goto L0
    L1:

# Linha 18
    L2:
    t41 = 0  ; [int]
    t42 = B > t41  ; [boolean]
    ifFalse t42 goto L3
    t43 = 1  ; [int]
    t44 = B - t43  ; [int]
    B = t44  ; [int]
    goto L2
    L3:

# Linha 19
    t45 = 1  ; [int]
    t46 = 10  ; [int]
    t47 = 1  ; [int]
    t48 = t45  ; [int]
    L4:
    t49 = t48 <= t46  ; [boolean]
    ifFalse t49 goto L5
    t50 = 2  ; [int]
    t51 = I * t50  ; [int]
    t52 = t48 + t47  ; [int]
    t48 = t52  ; [int]
    goto L4
    L5:

# Linha 20
    t53 = 15  ; [int]
    t54 = X > t53  ; [boolean]
    ifFalse t54 goto L6
    t55 = 100  ; [int]
    goto L7
    L6:
    t56 = 200  ; [int]
    L7:

# Linha 21
    t57 = 10  ; [int]
    t58 = A > t57  ; [boolean]
    t59 = 5  ; [int]
    t60 = Y > t59  ; [boolean]
    t61 = t58 && t60  ; [boolean]
    ifFalse t61 goto L8
    t62 = A + Y  ; [int]
    t63 = 2.0  ; [real]
    t64 = t62 | t63  ; [real]
    goto L9
    L8:
    t65 = A * Y  ; [int]
    L9:

# Linha 22
    t66 = 5  ; [int]
    t67 = 3  ; [int]
    t68 = t66 + t67  ; [int]
    t69 = 2  ; [int]
    t70 = 4  ; [int]
    t71 = t69 * t70  ; [int]
    t72 = t68 * t71  ; [int]
```

## Resumo

- **Total de Instruções:** 102
- **Tipos de Instrução:**
  - TACAtribuicao: 43
  - TACCopia: 10
  - TACDesvio: 5
  - TACOperacaoBinaria: 29
  - TACRotulo: 10
  - TACSeNaoDesvio: 5