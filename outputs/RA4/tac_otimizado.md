# TAC Otimizado - tac_instructions

## Linha 1: t0 = 0

## Linha 2: FIB_0 = t0

## Linha 3: t1 = 1

## Linha 4: FIB_1 = t1

## Linha 5: t2 = 2

## Linha 6: COUNTER = t2

## Linha 7: t3 = 24

## Linha 8: LIMIT = t3

## Linha 9: L0:

## Linha 10: t4 = COUNTER <= LIMIT

## Linha 11: ifFalse t4 goto L1

## Linha 12: t5 = FIB_0 + FIB_1

## Linha 13: FIB_NEXT = t5

## Linha 14: FIB_0 = FIB_1

## Linha 15: FIB_1 = FIB_NEXT

## Linha 16: t7 = COUNTER + 1

## Linha 17: COUNTER = t7

## Linha 18: goto L0

## Linha 19: L1:

## Linha 20: RESULT = FIB_NEXT

## Estatísticas
- Total de instruções: 20
- Temporários criados: 7
