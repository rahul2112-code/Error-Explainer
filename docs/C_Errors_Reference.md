# C Language — Error Reference Guide

## Friendly Compiler: Complete List of Detectable C Errors

This document lists every type of error that the Friendly Compiler can detect, explain, and translate when compiling C programs using GCC.

---

## Error Categories Overview

The system detects **30 distinct error patterns** for C, across **8 categories**:

| # | Category | Count | Severity |
|---|----------|-------|----------|
| 1 | Syntax Errors | 7 | Error |
| 2 | Undeclared Identifier Errors | 3 | Error |
| 3 | Type Errors | 7 | Error / Warning |
| 4 | Function Call Errors | 3 | Error |
| 5 | Return Errors | 3 | Error / Warning |
| 6 | Array Errors | 2 | Error |
| 7 | Control Flow Errors | 3 | Error |
| 8 | Warnings | 2 | Warning |

---

## 1. Syntax Errors

### 1.1 Missing Semicolon or Comma
- **GCC Message:** `expected ';' before 'return'`
- **Pattern:** `expected.*[;,].*before`
- **Explanation:** You're missing a semicolon (;) or comma (,). Every statement in C must end with a semicolon.
- **Confidence:** 95%

```c
int x = 5     // Missing semicolon!
return 0;
```

### 1.2 Missing Closing Parenthesis
- **GCC Message:** `expected ')' before ...`
- **Explanation:** You're missing a closing parenthesis ')'.
- **Confidence:** 95%

### 1.3 Missing Closing Brace
- **GCC Message:** `expected '}' at end of input`
- **Explanation:** You're missing a closing brace '}'. Count your braces — they should match!
- **Confidence:** 95%

### 1.4 Missing Declaration Specifiers
- **GCC Message:** `expected declaration specifiers before ...`
- **Explanation:** You need to specify the data type (like int, float, char) for your variable.
- **Confidence:** 90%

### 1.5 Expected Expression
- **GCC Message:** `expected expression before ...`
- **Explanation:** The compiler expected an expression but found something else.
- **Confidence:** 85%

### 1.6 Stray Character
- **GCC Message:** `stray '\302' in program`
- **Explanation:** There's an unexpected character in your code.
- **Confidence:** 90%

### 1.7 Expected Identifier or Parenthesis
- **GCC Message:** `expected identifier or '(' before ...`
- **Confidence:** 85%

---

## 2. Undeclared Identifier Errors

### 2.1 Undeclared Variable
- **GCC Message:** `'y' undeclared (first use in this function)`
- **Explanation:** You're using a variable without declaring it first.
- **Confidence:** 95%

```c
int main() {
    y = 10;     // 'y' was never declared!
}
```

### 2.2 Implicit Function Declaration
- **GCC Message:** `implicit declaration of function 'add'`
- **Explanation:** You're calling a function but haven't declared it. Include the header or add a forward declaration.
- **Confidence:** 95%

### 2.3 Unknown Type Name
- **GCC Message:** `unknown type name 'string'`
- **Explanation:** The compiler doesn't recognize this type. Check spelling or include a header file.
- **Confidence:** 90%

---

## 3. Type Errors

### 3.1 Conflicting Types
- **GCC Message:** `conflicting types for 'add'`
- **Explanation:** You've declared something with different types in different places.
- **Confidence:** 90%

### 3.2 Void Value Misuse
- **GCC Message:** `void value not ignored as it ought to be`
- **Explanation:** You're trying to use the return value of a void function.
- **Confidence:** 90%

### 3.3 Incompatible Pointer Assignment
- **GCC Message:** `assignment makes pointer from incompatible pointer type`
- **Confidence:** 85%

### 3.4 Storage Size Unknown
- **GCC Message:** `storage size of 'myStruct' isn't known`
- **Confidence:** 85%

### 3.5 Incompatible Pointer Initialization
- **Confidence:** 85%

### 3.6 Pointer from Integer Without Cast
- **GCC Message:** `passing argument 1 of 'func' makes pointer from integer without a cast`
- **Explanation:** You're passing an integer where a pointer is expected. Forgot the '&' operator?
- **Confidence:** 90%

### 3.7 Integer from Pointer Without Cast
- **GCC Message:** `passing argument 1 of 'func' makes integer from pointer without a cast`
- **Explanation:** You're passing a pointer where an integer is expected. Need to dereference with '*'?
- **Confidence:** 90%

---

## 4. Function Call Errors

### 4.1 Too Few Arguments
- **GCC Message:** `too few arguments to function 'add'`
- **Confidence:** 95%

```c
int add(int a, int b) { return a + b; }
int main() {
    int result = add(5);  // Needs 2 arguments!
}
```

### 4.2 Too Many Arguments
- **GCC Message:** `too many arguments to function 'add'`
- **Confidence:** 95%

### 4.3 Incompatible Argument Type
- **GCC Message:** `incompatible type for argument 1 of 'func'`
- **Confidence:** 90%

---

## 5. Return & Redefinition Errors

### 5.1 Control Reaches End of Non-Void Function
- **GCC Message:** `control reaches end of non-void function`
- **Confidence:** 90%

```c
int add(int a, int b) {
    int sum = a + b;
    // Missing: return sum;
}
```

### 5.2 Return with No Value
- **GCC Message:** `return-statement with no value, in function returning...`
- **Confidence:** 95%

### 5.3 Redefinition / Redeclaration
- **GCC Messages:** `redefinition of 'x'` / `redeclaration of 'x' with no linkage`
- **Confidence:** 90-95%

---

## 6. Array Errors

### 6.1 Non-Array Subscript
- **GCC Message:** `subscripted value is not an array, pointer, or vector`
- **Confidence:** 90%

### 6.2 Non-Integer Subscript
- **GCC Message:** `array subscript is not an integer`
- **Confidence:** 90%

---

## 7. Control Flow Errors

### 7.1 Break Outside Loop/Switch
- **GCC Message:** `break statement not within loop or switch`
- **Confidence:** 95%

### 7.2 Continue Outside Loop
- **GCC Message:** `continue statement not within a loop`
- **Confidence:** 95%

### 7.3 Case Outside Switch
- **GCC Message:** `case label not within a switch statement`
- **Confidence:** 95%

---

## 8. Warnings

### 8.1 Unused Variable
- **GCC Message:** `unused variable 'x'`
- **Explanation:** You declared a variable but never used it. This is just a warning.
- **Confidence:** 95%

### 8.2 Format String Mismatch
- **GCC Message:** `format '%d' expects argument of type 'int', but argument 2 has type...`
- **Explanation:** Your printf/scanf format specifier doesn't match the data type.
- **Confidence:** 95%

```c
float pi = 3.14;
printf("%d", pi);  // %d is for int, use %f for float!
```

---

## 9. Assignment Errors

### 9.1 LValue Required
- **GCC Message:** `lvalue required as left operand of assignment`
- **Explanation:** You can only assign values to variables, not to expressions or constants.
- **Confidence:** 90%

---

## Confidence Score System

| Range | Rating | Meaning |
|-------|--------|---------|
| 85-100% | High | Very reliable pattern |
| 70-84% | Medium | Good, may occasionally misidentify edge cases |
| 0-69% | Low | Experimental or broad pattern |

**Score Formula:** 30% Pattern Specificity + 50% User Feedback + 20% Base Confidence

---

## Test Files Included

| File | Errors Demonstrated |
|------|-------------------|
| `test.c` | Missing semicolon, implicit function declaration, missing return |
| `test1.c` | Missing semicolon |
| `test2.c` | Missing semicolons, undeclared variables |
| `test3.c` | Format string argument count mismatch |
| `test4.c` | Pointer/integer format warning |
