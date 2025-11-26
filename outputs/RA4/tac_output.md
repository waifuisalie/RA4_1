# TAC Output - /home/waifuisalie/Documents/RA4_Compiladores/RA4_1/outputs/RA3/arvore_atribuida.json

**Generated:** 2025-11-25 23:25:08

---

## Instructions

```
Line  1: t0 = 0                   [type: int]
Line  1: FIB_0 = t0               [type: int]
Line  2: t1 = 1                   [type: int]
Line  2: FIB_1 = t1               [type: int]
Line  3: t2 = 2                   [type: int]
Line  3: COUNTER = t2             [type: int]
Line  4: t3 = 24                  [type: int]
Line  4: LIMIT = t3               [type: int]
Line  5: L0:                      
Line  5: t4 = COUNTER <= LIMIT    [type: boolean]
Line  5: ifFalse t4 goto L1       
Line  5: t5 = FIB_0 + FIB_1       [type: int]
Line  5: FIB_NEXT = t5            [type: int]
Line  5: FIB_0 = FIB_1            [type: int]
Line  5: FIB_1 = FIB_NEXT         [type: int]
Line  5: t6 = 1                   [type: int]
Line  5: t7 = COUNTER + t6        [type: int]
Line  5: COUNTER = t7             [type: int]
Line  5: goto L0                  
Line  5: L1:                      
Line  6: RESULT = FIB_NEXT        [type: int]
```

---

## Statistics

- **total_instructions:** 21
- **temp_count:** 8
- **label_count:** 2
- **result_history_size:** 5