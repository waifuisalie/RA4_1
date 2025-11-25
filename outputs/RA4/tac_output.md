# TAC Output - /Users/thaismonteiro/Documents/RA4_1/outputs/RA3/arvore_atribuida.json

**Generated:** 2025-11-25 14:16:58

---

## Instructions

```
Line  1: t0 = 1.0                 [type: real]
Line  1: X_VAL = t0               [type: real]
Line  2: t1 = 1.0                 [type: real]
Line  2: TERM1 = t1               [type: real]
Line  3: t2 = 1                   [type: int]
Line  3: COUNTER = t2             [type: int]
Line  4: L0:                      
Line  4: t3 = 1                   [type: int]
Line  4: t4 = COUNTER <= t3       [type: boolean]
Line  4: ifFalse t4 goto L1       
Line  4: t5 = X_VAL * X_VAL       [type: real]
Line  4: X_SQUARE = t5            [type: real]
Line  4: t6 = 2.0                 [type: real]
Line  4: FACT_2 = t6              [type: real]
Line  4: t7 = X_SQUARE | FACT_2   [type: real]
Line  4: TEMP2 = t7               [type: real]
Line  4: t8 = 0.0                 [type: real]
Line  4: t9 = t8 - TEMP2          [type: real]
Line  4: TERM2 = t9               [type: real]
Line  4: t10 = X_SQUARE * X_SQUARE[type: real]
Line  4: X_FOURTH = t10           [type: real]
Line  4: t11 = 4.0                [type: real]
Line  4: t12 = 3.0                [type: real]
Line  4: t13 = t11 * t12          [type: real]
Line  4: TEMP4A = t13             [type: real]
Line  4: t14 = 2.0                [type: real]
Line  4: t15 = TEMP4A * t14       [type: real]
Line  4: TEMP4B = t15             [type: real]
Line  4: t16 = 1.0                [type: real]
Line  4: t17 = TEMP4B * t16       [type: real]
Line  4: FACT_4 = t17             [type: real]
Line  4: t18 = X_FOURTH | FACT_4  [type: real]
Line  4: TERM3 = t18              [type: real]
Line  4: t19 = X_FOURTH * X_SQUARE[type: real]
Line  4: X_SIXTH = t19            [type: real]
Line  4: t20 = 6.0                [type: real]
Line  4: t21 = 5.0                [type: real]
Line  4: t22 = t20 * t21          [type: real]
Line  4: TEMP6A = t22             [type: real]
Line  4: t23 = 4.0                [type: real]
Line  4: t24 = TEMP6A * t23       [type: real]
Line  4: TEMP6B = t24             [type: real]
Line  4: t25 = 3.0                [type: real]
Line  4: t26 = TEMP6B * t25       [type: real]
Line  4: TEMP6C = t26             [type: real]
Line  4: t27 = 2.0                [type: real]
Line  4: t28 = TEMP6C * t27       [type: real]
Line  4: TEMP6D = t28             [type: real]
Line  4: t29 = 1.0                [type: real]
Line  4: t30 = TEMP6D * t29       [type: real]
Line  4: FACT_6 = t30             [type: real]
Line  4: t31 = X_SIXTH | FACT_6   [type: real]
Line  4: TEMP8 = t31              [type: real]
Line  4: t32 = 0.0                [type: real]
Line  4: t33 = t32 - TEMP8        [type: real]
Line  4: TERM4 = t33              [type: real]
Line  4: t34 = TERM1 + TERM2      [type: real]
Line  4: SUM12 = t34              [type: real]
Line  4: t35 = SUM12 + TERM3      [type: real]
Line  4: SUM123 = t35             [type: real]
Line  4: t36 = SUM123 + TERM4     [type: real]
Line  4: RESULT_COS = t36         [type: real]
Line  4: FINAL_COS = RESULT_COS   [type: real]
Line  4: t37 = 1                  [type: int]
Line  4: t38 = COUNTER + t37      [type: int]
Line  4: COUNTER = t38            [type: int]
Line  4: goto L0                  
Line  4: L1:                      
```

---

## Statistics

- **total_instructions:** 68
- **temp_count:** 39
- **label_count:** 2
- **result_history_size:** 3