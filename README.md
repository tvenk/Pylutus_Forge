# Pylutus Forge

**Pylutus Forge** is a Python-to-Plutus compiler designed to let developers write Cardano smart contracts in Python-like syntax. It translates `.pylutus` files into valid Plutus (Haskell) code ready for on-chain deployment on the Cardano blockchain.


## 📁 Directory Structure

```bash
pylutus_forge/
├── compiler/
│   ├── __init__.py
│   ├── ast_parser.py
│   ├── type_checker.py
│   ├── semantic_validator.py
│   ├── utils.py
│   └── generator/
│       ├── haskell_generator.py
│       ├── intermediate_repr.py
│       └── macros.py
├── tests/
│   ├── easy_contract.pylutus
│   ├── payment_contract.pylutus
│   ├── complex_contract.pylutus
│   ├── invalid_contract.pylutus
│   ├── unreachable_contract.pylutus
│   └── invalid_payment.pylutus
├── pylutus_forge.py
├── pylutus_key.json
├── output_contract.hs
├── test_ast_parser_updated.py
├── test_semantic_validator.py
├── test_symbol_table.py
├── test_type_checker.py
├── test_utils.py
├── LICENSE
└── README.md
```

---

## 🚀 Overview

**Pylutus Forge** reduces the barrier for Cardano dApp developers by enabling them to write smart contracts using a simple domain-specific language (DSL) built on Python.

The tool compiles `.pylutus` files into Plutus scripts using the following stages:

* **Parser**: Extracts functions and logic from Python-style syntax (`if/else`, `return`, etc.).
* **Type Checker**: Ensures type safety and enforces Cardano-specific constraints.
* **Semantic Validator**: Detects non-deterministic or unreachable logic.
* **Macro Engine**: Expands `pylutus_sig(...)`, `pylutus_pay(...)` using external key maps (`pylutus_key.json`).
* **Intermediate Representation (IR)**: Organizes logic in an abstract layer before Haskell generation.
* **Code Generator**: Emits valid Plutus code using `PlutusTx` libraries and templates.

---

## ✅ Phase 1 — Core Compiler (Complete)

* 🔍 **AST Parser**: Supports `def`, `if/else`, `return`, `pylutus_*()` syntax.
* 🧰 **Macro Engine**: Custom DSL functions expanded to Plutus primitives.
* ⚙️ **Haskell Code Generator**: Emits traceable, valid Haskell scripts.
* 🔐 **Basic Validator Logic**: Signature checks using `txSignedBy`.
* 📄 **Output**: Final contract is written to `output_contract.hs`.

---

## ✅ Phase 2 — Type System & Semantic Validation (Complete)

* 🧠 **Static Type Checker**: Verifies `ctx: ScriptContext` and return types.
* 🧾 **Symbol Table**: Tracks scope, variable types, and function correctness.
* 🛑 **Semantic Validator**: Catches unreachable conditions, illogical `if True`, etc.
* 💸 **Payment Support**: `pylutus_pay(...)` enforces amount/address checks.

---

## ✅ Phase 3 — IR + Multi-Clause Support (Complete)

* 🧱 **Typed Intermediate Representation (IR)**: Enables modular and testable contract logic flow.
* 🧩 **Multi-Clause Handling**: Correct translation of nested `if/else` branches.
* 🔗 **Chained Logic**: Inline boolean logic, multiple condition guards supported.
* 📐 **Consistent Haskell Structure**: Output is clean, minimal, and idiomatic.

---

## 🚧 Phase 4 — In Progress

⚠️ Minor Gaps and Improvements to Consider
These don’t prevent it from working, but prevent it from being mature production tooling:

* ❌ **Unused Function Emission**
  Helper functions like `checkPayment` are always emitted even if not referenced. This affects code hygiene and should be optimized.

* ❌ **No Real Type Checker Yet**
  Invalid Python-style contracts (e.g., wrong args to `pylutus_sig()`) may not fail gracefully or provide meaningful errors. A robust transpiler should validate DSL syntax and types before IR generation.

* ❌ **Missing Pythonic Extras**
  Currently unsupported but highly desirable features include:

  * Contract-level docstrings
  * Constant definitions (e.g., `OWNER = "abc123"`)
  * Decorators or Python-style annotations
    These additions would improve DSL expressiveness and developer experience.

* ❌ **Deployment Pipeline**
  The current tool generates Plutus code but lacks:

  * Haskell formatting / linting
  * UPLC generation
  * On-chain validator test stubs
    These features are expected in production-ready tooling.

---

## 📦 How to Use

### 1. Write a `.pylutus` contract:

**`tests/complex_contract.pylutus`**:

```python
def validator(ctx: ScriptContext) -> bool:
    if pylutus_sig("abc123"):
        pylutus_pay("def456", 2000000)
        return True
    else:
        return False
```

### 2. Compile it:

```bash
python3 pylutus_forge.py tests/complex_contract.pylutus
```

### 3. Result:

**`output_contract.hs`**:

```haskell
{-# INLINABLE mkValidator #-}
import PlutusTx.Prelude
import Plutus.V1.Ledger.Api

mkValidator :: ScriptContext -> Bool
mkValidator ctx =
    if txSignedBy ctx (PubKeyHash "abc123") then
        traceIfFalse "Valid" (
            traceIfFalse "Payment failed" (checkPayment ctx (PubKeyHash "def456") 2000000)
            && traceIfFalse "Return" True
        )
    else
        traceIfFalse "Invalid" False

checkPayment :: ScriptContext -> PubKeyHash -> Integer -> Bool
checkPayment ctx pkh amount =
    any (\o -> txOutValue o == lovelaceValueOf amount && txOutAddress o == pubKeyHashAddress pkh)
        (txInfoOutputs $ scriptContextTxInfo ctx)
```

---

## 🔭 Phase 5 and Beyond — Production Tooling

| Feature                                   | Status |
| ----------------------------------------- | ------ |
| 🧠 Type Safety on Macros                  | 🔜     |
| 📏 Inline Constants                       | 🔜     |
| ✍️ Better Error Messages                  | 🔜     |
| 📦 Haskell Formatter + Plutus CLI hooks   | 🔜     |
| 💬 Docstring and Metadata Support         | 🔜     |
| 🧪 Auto Test Harness (golden test output) | 🔜     |
| 🚀 On-chain Validator Build & Deploy CLI  | 🔜     |

---

## 🧪 Run Unit Tests

```bash
python3 test_ast_parser_updated.py
python3 test_type_checker.py
python3 test_semantic_validator.py
python3 test_symbol_table.py
python3 test_utils.py
```

---

## 📝 License

MIT License

---

## 📬 Contact

**Author**: tvenk
**GitHub**: [tvenk](https://github.com/tvenk)
---
