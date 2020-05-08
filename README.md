#discord-bots

A collection of discord bots.

## Agda Guru

Searches the standard library for a function name and returns all the matches it can find.

### Usage
* `$agda <function>` Finds all instances of a function called `<function>` in the standard library
* `$agda <module> <function>` Finds an instance of a function called `<function>` in module `<module>`

### Example
`$agda Data.Nat.Properties +-comm`

returns

```agda
+-comm : Commutative _+_
+-comm zero    n = sym (+-identityʳ n)
+-comm (suc m) n = begin-equality
  suc m + n   ≡⟨⟩
  suc (m + n) ≡⟨ cong suc (+-comm m n) ⟩
  suc (n + m) ≡⟨ sym (+-suc n m) ⟩
  n + suc m   ∎
  ```
