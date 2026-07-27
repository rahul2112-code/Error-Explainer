import re

# The exact error from your GCC
error_message = "expected ';' before 'return'"

# Our patterns
patterns = {
    "Pattern 1": r"expected ';' before",
    "Pattern 2": r"expected .* before",
    "Pattern 3": r"expected",
    "Pattern 4": r"';'",
}

print(f"Testing error message: {repr(error_message)}")
print(f"Length: {len(error_message)}")
print(f"Bytes: {error_message.encode('utf-8')}")
print("\n" + "="*60 + "\n")

for name, pattern in patterns.items():
    result = re.search(pattern, error_message)
    if result:
        print(f"✅ {name}: MATCHED")
        print(f"   Pattern: {pattern}")
        print(f"   Match: {result.group()}")
    else:
        print(f"❌ {name}: NO MATCH")
        print(f"   Pattern: {pattern}")
    print()