# TAC Output - arvore_atribuida.json

**Generated:** 2025-11-21 15:23:14

## Statistics

| Metric | Value |
|--------|-------|
| total_instructions | 166 |
| temp_count | 108 |
| label_count | 20 |
| result_history_size | 34 |

## Instructions

```
# Line 1
    t0 = 10  ; [int]
    A = t0  ; [int]

# Line 2
    t1 = 20  ; [int]
    B = t1  ; [int]

# Line 3
    t2 = 5.5  ; [real]
    X = t2  ; [real]

# Line 4
    t3 = 3.14  ; [real]
    Y = t3  ; [real]

# Line 5
    t4 = A + B  ; [int]

# Line 6
    t5 = X * Y  ; [real]

# Line 7
    t6 = 2  ; [int]
    t7 = A - t6  ; [int]

# Line 8
    t8 = 3  ; [int]
    t9 = B / t8  ; [int]

# Line 9
    t10 = 2.0  ; [real]
    t11 = X | t10  ; [real]

# Line 10
    t12 = 10  ; [int]
    t13 = 5.5  ; [real]
    t14 = t12 + t13  ; [real]

# Line 11
    t15 = 3.14  ; [real]
    t16 = 2  ; [int]
    t17 = t15 * t16  ; [real]

# Line 12
    t18 = 50.0  ; [real]
    t19 = 10  ; [int]
    t20 = t18 - t19  ; [real]

# Line 13
    t21 = A > B  ; [boolean]

# Line 14
    t22 = X < Y  ; [boolean]

# Line 15
    t23 = 10  ; [int]
    t24 = A == t23  ; [boolean]

# Line 16
    t25 = 20  ; [int]
    t26 = B >= t25  ; [boolean]

# Line 17
    t27 = 5.0  ; [real]
    t28 = X <= t27  ; [boolean]

# Line 18
    t29 = A > B  ; [boolean]
    t30 = X < Y  ; [boolean]
    t31 = t29 && t30  ; [boolean]

# Line 19
    t32 = 10  ; [int]
    t33 = A == t32  ; [boolean]
    t34 = 20  ; [int]
    t35 = B > t34  ; [boolean]
    t36 = t33 || t35  ; [boolean]

# Line 20
    t37 = 5.0  ; [real]
    t38 = X > t37  ; [boolean]
    t39 = !t38  ; [boolean]

# Line 21
    t40 = A < B  ; [boolean]
    t41 = X >= Y  ; [boolean]
    t42 = t40 && t41  ; [boolean]

# Line 22
    t43 = 10  ; [int]
    t44 = 5  ; [int]
    t45 = t43 > t44  ; [boolean]
    t46 = 3.14  ; [real]
    t47 = 2.0  ; [real]
    t48 = t46 < t47  ; [boolean]
    t49 = t45 || t48  ; [boolean]

# Line 23
    t50 = A + B
    SUM = t50

# Line 24
    t51 = X * Y
    PRODUCT = t51

# Line 27
    t52 = 10  ; [int]
    t53 = SUM + t52
    RESULT = t53

# Line 29
    t54 = 100  ; [int]
    COUNTER = t54  ; [int]

# Line 30
    t55 = 0  ; [int]
    INDEX = t55  ; [int]

# Line 31
    t56 = A > B  ; [boolean]
    ifFalse t56 goto L0
    t57 = 100  ; [int]
    goto L1
    L0:
    t58 = 200  ; [int]
    L1:

# Line 32
    t59 = 5.0  ; [real]
    t60 = X < t59  ; [boolean]
    ifFalse t60 goto L2
    t61 = 10  ; [int]
    goto L3
    L2:
    t62 = 20  ; [int]
    L3:

# Line 33
    t63 = 100  ; [int]
    t64 = SUM >= t63  ; [boolean]
    ifFalse t64 goto L4
    t65 = 10  ; [int]
    t66 = SUM - t65
    goto L5
    L4:
    t67 = 10  ; [int]
    t68 = SUM + t67
    L5:

# Line 34
    t69 = 50  ; [int]
    t70 = COUNTER > t69  ; [boolean]
    ifFalse t70 goto L6
    t71 = 1  ; [int]
    goto L7
    L6:
    t72 = 0  ; [int]
    L7:

# Line 35
    L8:
    t73 = 100  ; [int]
    t74 = COUNTER < t73  ; [boolean]
    ifFalse t74 goto L9
    t75 = 1  ; [int]
    t76 = COUNTER + t75
    COUNTER = t76
    goto L8
    L9:

# Line 36
    L10:
    t77 = 50  ; [int]
    t78 = INDEX < t77  ; [boolean]
    ifFalse t78 goto L11
    t79 = 2  ; [int]
    t80 = INDEX + t79
    INDEX = t80
    goto L10
    L11:

# Line 37
    L12:
    t81 = 200  ; [int]
    t82 = A < t81  ; [boolean]
    ifFalse t82 goto L13
    t83 = 5  ; [int]
    t84 = A + t83
    A = t84
    goto L12
    L13:

# Line 38
    t85 = 1  ; [int]
    t86 = 10  ; [int]
    t87 = 1  ; [int]
    t88 = t85  ; [int]
    L14:
    t89 = t88 <= t86  ; [boolean]
    ifFalse t89 goto L15
    t90 = 1  ; [int]
    t91 = I + t90
    I = t91
    t92 = t88 + t87  ; [int]
    t88 = t92  ; [int]
    goto L14
    L15:

# Line 39
    t93 = 0  ; [int]
    t94 = 20  ; [int]
    t95 = 2  ; [int]
    t96 = t93  ; [int]
    L16:
    t97 = t96 <= t94  ; [boolean]
    ifFalse t97 goto L17
    t98 = 2  ; [int]
    t99 = J * t98
    J = t99
    t100 = t96 + t95  ; [int]
    t96 = t100  ; [int]
    goto L16
    L17:

# Line 40
    t101 = 1  ; [int]
    t102 = 5  ; [int]
    t103 = 1  ; [int]
    t104 = t101  ; [int]
    L18:
    t105 = t104 <= t102  ; [boolean]
    ifFalse t105 goto L19
    t106 = SUM + K
    SUM = t106
    t107 = t104 + t103  ; [int]
    t104 = t107  ; [int]
    goto L18
    L19:
```

## Summary

- **Total Instructions:** 166
- **Instruction Types:**
  - TACAssignment: 54
  - TACBinaryOp: 50
  - TACCopy: 21
  - TACGoto: 10
  - TACIfFalseGoto: 10
  - TACLabel: 20
  - TACUnaryOp: 1