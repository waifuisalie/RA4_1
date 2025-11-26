# TAC Otimizado - tac_instructions

## Linha 1: t0 = 100

## Linha 2: X_VAL = t0

## Linha 3: t1 = 100

## Linha 4: TERM1 = t1

## Linha 5: t2 = 1

## Linha 6: COUNTER = t2

## Linha 7: L0:

## Linha 8: t4 = COUNTER <= 1

## Linha 9: ifFalse t4 goto L1

## Linha 10: t5 = X_VAL * X_VAL

## Linha 11: X_SQUARE = t5

## Linha 12: t6 = 200

## Linha 13: FACT_2 = t6

## Linha 14: t7 = X_SQUARE | FACT_2

## Linha 15: TEMP2 = t7

## Linha 16: t9 = 0 - TEMP2

## Linha 17: TERM2 = t9

## Linha 18: t10 = X_SQUARE * X_SQUARE

## Linha 19: X_FOURTH = t10

## Linha 20: t13 = 120000

## Linha 21: TEMP4A = t13

## Linha 22: t15 = TEMP4A * 200

## Linha 23: TEMP4B = t15

## Linha 24: t17 = TEMP4B * 100

## Linha 25: FACT_4 = t17

## Linha 26: t18 = X_FOURTH | FACT_4

## Linha 27: TERM3 = t18

## Linha 28: t19 = X_FOURTH * X_SQUARE

## Linha 29: X_SIXTH = t19

## Linha 30: t22 = 300000

## Linha 31: TEMP6A = t22

## Linha 32: t24 = TEMP6A * 400

## Linha 33: TEMP6B = t24

## Linha 34: t26 = TEMP6B * 300

## Linha 35: TEMP6C = t26

## Linha 36: t28 = TEMP6C * 200

## Linha 37: TEMP6D = t28

## Linha 38: t30 = TEMP6D * 100

## Linha 39: FACT_6 = t30

## Linha 40: t31 = X_SIXTH | FACT_6

## Linha 41: TEMP8 = t31

## Linha 42: t33 = 0 - TEMP8

## Linha 43: TERM4 = t33

## Linha 44: t34 = TERM1 + TERM2

## Linha 45: SUM12 = t34

## Linha 46: t35 = SUM12 + TERM3

## Linha 47: SUM123 = t35

## Linha 48: t36 = SUM123 + TERM4

## Linha 49: RESULT_COS = t36

## Linha 50: t38 = COUNTER + 1

## Linha 51: COUNTER = t38

## Linha 52: goto L0

## Linha 53: L1:

## Linha 54: FINAL_COS = RESULT_COS

## Estatísticas
- Total de instruções: 54
- Temporários criados: 25
