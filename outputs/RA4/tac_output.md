# TAC Output - Generated from arvore_atribuida.json

**Generated:** 2025-11-22 15:42:38

---

## Instructions

```
Line  1: t0 = 5                    [type: int]
Line  1: t1 = 3                    [type: int]
Line  1: t2 = t0 + t1              [type: int]
Line  2: t3 = 10.5                 [type: real]
Line  2: t4 = 2.0                  [type: real]
Line  2: t5 = t3 * t4              [type: real]
Line  3: t6 = 100                  [type: int]
Line  3: t7 = 50                   [type: int]
Line  3: t8 = t6 + t7              [type: int]
Line  4: t9 = 15                   [type: int]
Line  4: t10 = 7                   [type: int]
Line  4: t11 = t9 / t10            [type: int]
Line  5: t12 = 23                  [type: int]
Line  5: t13 = 6                   [type: int]
Line  5: t14 = t12 % t13           [type: int]
Line  6: t15 = 2.5                 [type: real]
Line  6: t16 = 3                   [type: int]
Line  6: t17 = t15 ^ t16           [type: real]
Line  7: t18 = 5.5                 [type: real]
Line  7: t19 = 3.2                 [type: real]
Line  7: t20 = t18 > t19           [type: boolean]
Line  8: t21 = 3                   [type: int]
Line  8: t22 = !t21                [type: boolean]
Line  9: t23 = 5                   [type: int]
Line  9: t24 = 3                   [type: int]
Line  9: t25 = t23 > t24           [type: boolean]
Line  9: t26 = 2                   [type: int]
Line  9: t27 = 1                   [type: int]
Line  9: t28 = t26 < t27           [type: boolean]
Line  9: t29 = t25 && t28          [type: boolean]
Line 10: t30 = 10                  [type: int]
Line 10: X = t30                   [type: int]
Line 11: t31 = 20                  [type: int]
Line 11: A = t31                   [type: int]
Line 12: t32 = 10                  [type: int]
Line 12: I = t32                   [type: int]
Line 13: t33 = 0                   [type: int]
Line 13: COUNTER = t33             [type: int]
Line 14: t34 = 5                   [type: int]
Line 14: t35 = X + t34             [type: int]
Line 14: Y = t35                   [type: int]
Line 15: t36 = A - X               [type: int]
Line 15: B = t36                   [type: int]
Line 16: t37 = 1                   [type: int]
Line 17: t38 = 2                   [type: int]
Line 18: L0:                       
Line 18: t39 = 5                   [type: int]
Line 18: t40 = COUNTER < t39       [type: boolean]
Line 18: ifFalse t40 goto L1       
Line 18: t41 = 1                   [type: int]
Line 18: t42 = COUNTER + t41       [type: int]
Line 18: COUNTER = t42             [type: int]
Line 18: goto L0                   
Line 18: L1:                       
Line 19: L2:                       
Line 19: t43 = 0                   [type: int]
Line 19: t44 = B > t43             [type: boolean]
Line 19: ifFalse t44 goto L3       
Line 19: t45 = 1                   [type: int]
Line 19: t46 = B - t45             [type: int]
Line 19: B = t46                   [type: int]
Line 19: goto L2                   
Line 19: L3:                       
Line 20: t47 = 1                   [type: int]
Line 20: t48 = 10                  [type: int]
Line 20: t49 = 1                   [type: int]
Line 20: t50 = t47                 [type: int]
Line 20: L4:                       
Line 20: t51 = t50 <= t48          [type: boolean]
Line 20: ifFalse t51 goto L5       
Line 20: t52 = 2                   [type: int]
Line 20: t53 = I * t52             [type: int]
Line 20: t54 = t50 + t49           [type: int]
Line 20: t50 = t54                 [type: int]
Line 20: goto L4                   
Line 20: L5:                       
Line 21: t55 = 15                  [type: int]
Line 21: t56 = X > t55             [type: boolean]
Line 21: ifFalse t56 goto L6       
Line 21: t57 = 100                 [type: int]
Line 21: goto L7                   
Line 21: L6:                       
Line 21: t58 = 200                 [type: int]
Line 21: L7:                       
Line 22: t59 = 10                  [type: int]
Line 22: t60 = A > t59             [type: boolean]
Line 22: t61 = 5                   [type: int]
Line 22: t62 = Y > t61             [type: boolean]
Line 22: t63 = t60 && t62          [type: boolean]
Line 22: ifFalse t63 goto L8       
Line 22: t64 = A + Y               [type: int]
Line 22: t65 = 2.0                 [type: real]
Line 22: t66 = t64 | t65           [type: real]
Line 22: goto L9                   
Line 22: L8:                       
Line 22: t67 = A * Y               [type: int]
Line 22: L9:                       
Line 23: t68 = 5                   [type: int]
Line 23: t69 = 3                   [type: int]
Line 23: t70 = t68 + t69           [type: int]
Line 23: t71 = 2                   [type: int]
Line 23: t72 = 4                   [type: int]
Line 23: t73 = t71 * t72           [type: int]
Line 23: t74 = t70 * t73           [type: int]
```

---

## Statistics

- **total_instructions:** 104
- **temp_count:** 75
- **label_count:** 10
- **result_history_size:** 20
