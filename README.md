# discord-bots

A collection of (one) discord bots.

## Agda Guru

Searches the standard library for a function name and returns all the matches it can find.

### Usage
* `$agda <function>` Finds all instances of a function called `<function>` in the standard library
* `$agda <module> <function>` Finds an instance of a function called `<function>` in module containing `<module>`
* `$agda <library> <module> <function>` Finds an instance of a function called `<function>` in module containing `<module>` from library `<library>`

#### Flags

* `-l` Specify a library
* `-m` Specify a module

### Example
```
$agda -l agda-stdlib -m Data.Nat +-comm
```

returns

>In `Data.Nat.Properties` from `agda-stdlib`:

```agda
+-comm : Commutative _+_
+-comm zero    n = sym (+-identityʳ n)
+-comm (suc m) n = begin-equality
  suc m + n   ≡⟨⟩
  suc (m + n) ≡⟨ cong suc (+-comm m n) ⟩
  suc (n + m) ≡⟨ sym (+-suc n m) ⟩
  n + suc m   ∎
```

>In `Data.Nat.Binary.Properties` from `agda-stdlib`:

```agda
+-comm : Commutative _+_
+-comm = +-Monomorphism.comm ℕₚ.+-isMagma ℕₚ.+-comm
```
