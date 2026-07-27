# Java Language — Error Reference Guide

## Friendly Compiler: Complete List of Detectable Java Errors

This document lists every type of error that the Friendly Java Compiler can detect, explain, and translate when compiling Java programs using `javac`.

---

## Error Categories Overview

The system detects **30 distinct error patterns** for Java, across **10 categories**:

| # | Category | Count | Severity |
|---|----------|-------|----------|
| 1 | Syntax Errors | 7 | Error |
| 2 | Undeclared Symbol Errors | 4 | Error |
| 3 | Type Mismatch Errors | 4 | Error |
| 4 | Static Context Errors | 2 | Error |
| 5 | Missing Return | 1 | Error |
| 6 | Unreachable Code | 1 | Error / Warning |
| 7 | Control Flow Errors | 2 | Error |
| 8 | Exception Handling Errors | 2 | Error |
| 9 | Argument Mismatch Errors | 2 | Error |
| 10 | Other Errors | 5 | Error |

---

## 1. Syntax Errors

### 1.1 Missing Semicolon
- **javac Message:** `';' expected`
- **Pattern:** `';' expected`
- **Explanation:** You forgot a semicolon ';' at the end of a statement. In Java, every statement must end with a semicolon.
- **Confidence:** 95%

```java
public class Main {
    public static void main(String[] args) {
        int x = 5     // Missing semicolon!
    }
}
```

### 1.2 Reached End of File While Parsing
- **javac Message:** `reached end of file while parsing`
- **Explanation:** Java reached the end of your file but was still expecting more code. You have an unclosed brace or parenthesis.
- **Confidence:** 95%

### 1.3 Illegal Start of Expression
- **javac Message:** `illegal start of expression`
- **Explanation:** Java doesn't understand the start of this line. Check for extra braces, keywords in wrong places, or missing operators.
- **Confidence:** 80%

### 1.4 Not a Statement
- **javac Message:** `not a statement`
- **Explanation:** This line is not a valid Java statement. You might have written an expression that does nothing or forgotten an assignment.
- **Confidence:** 85%

### 1.5 '.class' Expected
- **javac Message:** `'.class' expected`
- **Explanation:** A type name was used in an unusual way. Often from incorrect array syntax.
- **Confidence:** 75%

### 1.6 Illegal Character
- **javac Message:** `illegal character: '\u00a0'`
- **Explanation:** There is an unexpected character in your code that Java doesn't understand.
- **Confidence:** 90%

### 1.7 Unclosed String Literal
- **javac Message:** `unclosed string literal`
- **Explanation:** You started a String with a quote `"` but never closed it with a matching `"`.
- **Confidence:** 97%

---

## 2. Undeclared Symbol Errors

### 2.1 Cannot Find Variable
- **javac Message:** `cannot find symbol ... variable x`
- **Pattern:** `cannot find symbol.*variable\s+([a-zA-Z0-9_]+)`
- **Explanation:** Java doesn't know what the variable is. You either forgot to declare it, misspelled it, or used it outside its scope.
- **Confidence:** 92%

```java
public class Main {
    public static void main(String[] args) {
        System.out.println(x);  // 'x' was never declared!
    }
}
```

### 2.2 Cannot Find Class
- **javac Message:** `cannot find symbol ... class Scanner`
- **Pattern:** `cannot find symbol.*class\s+([a-zA-Z0-9_]+)`
- **Explanation:** Java doesn't recognize the class. You might need to import it: e.g., `import java.util.Scanner;`
- **Confidence:** 90%

### 2.3 Cannot Find Method
- **javac Message:** `cannot find symbol ... method add(int,int)`
- **Pattern:** `cannot find symbol.*method\s+([a-zA-Z0-9_]+)\(([^)]*)\)`
- **Explanation:** The method doesn't exist or wasn't found. Check spelling and argument types.
- **Confidence:** 88%

### 2.4 Generic Cannot Find Symbol
- **javac Message:** `cannot find symbol`
- **Explanation:** Java encountered a name it doesn't recognize. Check for spelling mistakes or missing declarations/imports.
- **Confidence:** 80%

---

## 3. Type Mismatch Errors

### 3.1 Incompatible Types (Detailed)
- **javac Message:** `incompatible types: String cannot be converted to int`
- **Pattern:** `incompatible types[:\s]+(.+?) cannot be converted to (.+)`
- **Explanation:** Type mismatch! You're trying to put one type where another is expected.
- **Confidence:** 92%

### 3.2 Incompatible Types (Generic)
- **javac Message:** `incompatible types`
- **Explanation:** You have a type mismatch. Check that your variable types match your assignments.
- **Confidence:** 80%

### 3.3 Possible Loss of Precision
- **javac Message:** `possible loss of precision`
- **Explanation:** You're assigning a bigger type (double/long) into a smaller type (int/float). Use casting: `int x = (int) myDouble;`
- **Confidence:** 90%

### 3.4 Int Cannot Be Dereferenced
- **javac Message:** `int cannot be dereferenced`
- **Explanation:** You're trying to call a method on a primitive int. Use `Integer.toString(myInt)` instead of `myInt.toString()`.
- **Confidence:** 92%

---

## 4. Static Context Errors

### 4.1 Non-Static Method from Static Context
- **javac Message:** `non-static method myMethod cannot be referenced from a static context`
- **Explanation:** The method belongs to an object but you're calling it from a static method like `main`. Create an object first.
- **Confidence:** 95%

```java
public class Main {
    void greet() { System.out.println("Hi"); }
    public static void main(String[] args) {
        greet();  // Error! Must create object first:
        // Main obj = new Main(); obj.greet();
    }
}
```

### 4.2 Non-Static Variable from Static Context
- **javac Message:** `non-static variable x cannot be referenced from a static context`
- **Explanation:** The variable belongs to an object. Either make it `static` or create an object first.
- **Confidence:** 95%

---

## 5. Missing Return

### 5.1 Missing Return Statement
- **javac Message:** `missing return statement`
- **Explanation:** This method says it will return a value but there's no `return` statement at the end.
- **Confidence:** 95%

```java
public static int add(int a, int b) {
    int sum = a + b;
    // Missing: return sum;
}
```

---

## 6. Unreachable Code

### 6.1 Unreachable Statement
- **javac Message:** `unreachable statement`
- **Explanation:** Code after a `return` statement can never execute. Move the `return` to the end.
- **Confidence:** 95%

---

## 7. Control Flow Errors

### 7.1 Break Outside Switch or Loop
- **javac Message:** `break outside switch or loop`
- **Confidence:** 95%

### 7.2 Continue Outside of Loop
- **javac Message:** `continue outside of loop`
- **Confidence:** 95%

---

## 8. Exception Handling Errors

### 8.1 Unreported Exception
- **javac Message:** `unreported exception IOException;`
- **Explanation:** A checked exception might be thrown but is never caught. Wrap in try-catch or add `throws` to the method.
- **Confidence:** 92%

### 8.2 Throws Clause Required
- **javac Message:** `throws clause required for...`
- **Explanation:** The operation can throw a checked exception. You must handle it with try-catch or add a throws clause.
- **Confidence:** 88%

---

## 9. Argument Mismatch Errors

### 9.1 Method Cannot Be Applied
- **javac Message:** `method add in class Main cannot be applied to given types`
- **Explanation:** You're giving the method wrong number or types of arguments.
- **Confidence:** 88%

### 9.2 Cannot Be Applied To
- **javac Message:** `cannot be applied to (int, String)`
- **Explanation:** The arguments you provided don't match what this method expects.
- **Confidence:** 82%

---

## 10. Other Errors

### 10.1 Duplicate Definition
- **javac Message:** `x is already defined in...`
- **Explanation:** You declared the same name twice in the same scope.
- **Confidence:** 95%

### 10.2 Filename Mismatch
- **javac Message:** `class Main is public, should be declared in a file named Main.java`
- **Explanation:** In Java, a public class name MUST match the filename. Rename one to match.
- **Confidence:** 98%

### 10.3 Void Type Not Allowed
- **javac Message:** `void type not allowed here`
- **Explanation:** You're trying to use the return value of a void method in an expression.
- **Confidence:** 90%

### 10.4 Duplicate Case Label
- **javac Message:** `duplicate case label`
- **Explanation:** Two case statements with the same value in a switch block.
- **Confidence:** 95%

### 10.5 Package Not Found
- **javac Message:** `package com.example does not exist`
- **Explanation:** The package doesn't exist. Check spelling or ensure the library is available.
- **Confidence:** 93%

---

## Uninitialized Variable

### Variable Not Initialized
- **javac Message:** `variable x might not have been initialized`
- **Explanation:** You're using a variable before giving it a value. Give it a starting value: `int x = 0;`
- **Confidence:** 95%

---

## Array Errors

### Array Required
- **javac Message:** `array required, but int found`
- **Explanation:** You're using `[]` on a variable that isn't an array.
- **Confidence:** 90%

### Operator Error
- **javac Message:** `operator + cannot be applied to int, boolean`
- **Explanation:** The operator cannot be used between these types.
- **Confidence:** 85%

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
| `test_java.java` | Missing semicolon, missing return statement |
