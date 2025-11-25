# TAC Output - C:\Users\Francisco\OneDrive - Grupo Marista\Desktop\2025-02\Compiladores\RA4\RA4_1\outputs\RA3\arvore_atribuida.json

**Generated:** 2025-11-24 23:26:07

---

## Instructions

```
Line  1: t0 = 0                   [type: int]
Line  1: FIB_0 = t0               [type: int]
Line  2: t1 = 1                   [type: int]
Line  2: FIB_1 = t1               [type: int]
Line  3: t2 = 2                   [type: int]
Line  3: INICIO = t2              [type: int]
Line  4: t3 = 24                  [type: int]
Line  4: FIM = t3                 [type: int]
Line  5: t4 = 1                   [type: int]
Line  5: PASSO = t4               [type: int]
Line  6: t5 = INICIO              [type: int]
Line  6: L0:                      
Line  6: t6 = t5 <= FIM           [type: boolean]
Line  6: ifFalse t6 goto L1       
Line  6: t7 = FIB_0 + FIB_1       [type: int]
Line  6: FIB_NEXT = t7            [type: int]
Line  6: FIB_1 = FIB_NEXT         
Line  6: FIB_0 = FIB_1            [type: int]
Line  6: t8 = t5 + PASSO          [type: int]
Line  6: t5 = t8                  [type: int]
Line  6: goto L0                  
Line  6: L1:                      
Line  7: RESULT = FIB_NEXT        
```

---

## Statistics

- **total_instructions:** 23
- **temp_count:** 9
- **label_count:** 2
- **result_history_size:** 6