# TAC Otimizado - tac_instructions

## Linha 1: FIB_0 = t0

## Linha 2: FIB_1 = t1

## Linha 3: INICIO = t2

## Linha 4: FIM = t3

## Linha 5: PASSO = t4

## Linha 6: t5 = INICIO

## Linha 7: L0:

## Linha 8: t6 = t5 <= FIM

## Linha 9: ifFalse t6 goto L1

## Linha 10: t7 = FIB_0 + FIB_1

## Linha 11: FIB_NEXT = t7

## Linha 12: FIB_1 = FIB_NEXT

## Linha 13: FIB_0 = FIB_1

## Linha 14: t8 = t5 + PASSO

## Linha 15: t5 = t8

## Linha 16: L1:

## Linha 17: RESULT = FIB_NEXT

## Estatísticas
- Total de instruções: 17
- Temporários criados: 9
