# Test Review

Revisa tests existentes y sugiere mejoras.

## Instrucciones

1. **Lee los tests** — Analiza la estructura y cobertura
2. **Identifica gaps** — ¿Qué falta por testear?
3. **Evalúa calidad** — ¿Son mantenibles, claros, independientes?
4. **Detecta anti-patterns** — Tests flaky, acoplados, lentos
5. **Sugiere mejoras** — Recomendaciones concretas

## Output Format

```markdown
## Test Review: [Component/Feature]

### Summary
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Test Count | X | - | - |
| Coverage | X% | 80% | ⚠️ |
| Pass Rate | X% | 95% | ✅ |
| Avg Duration | Xs | <5s | ✅ |

---

### Coverage Analysis

#### Covered Scenarios ✅
- [x] Happy path: user creation
- [x] Validation: empty fields
- [x] Auth: unauthorized access

#### Missing Scenarios ⚠️
| Scenario | Priority | Type | Suggested Test |
|----------|----------|------|----------------|
| Concurrent updates | P1 | Integration | `should handle race conditions` |
| Network timeout | P2 | Integration | `should retry on timeout` |
| Max payload size | P2 | Unit | `should reject >1MB payload` |

---

### Code Quality

#### Strengths 💪
- Clear test names following "should [behavior]" pattern
- Good use of fixtures for test data
- Proper cleanup in afterEach

#### Issues Found 🔍

**1. Flaky Test Risk**
```typescript
// ❌ Current: depends on timing
test('should complete within timeout', async () => {
  const result = await slowOperation();
  expect(result).toBeDefined();
});

// ✅ Suggested: explicit wait with assertion
test('should complete within timeout', async () => {
  const result = await waitFor(() => slowOperation(), { timeout: 5000 });
  expect(result).toBeDefined();
});
```

**2. Coupled Tests**
```typescript
// ❌ Current: test depends on previous test's state
test('should update user', async () => {
  // Uses userId from previous test
});

// ✅ Suggested: independent setup
test('should update user', async () => {
  const user = await createTestUser();
  // Use user.id
});
```

**3. Magic Numbers**
```typescript
// ❌ Current
expect(response.status).toBe(422);

// ✅ Suggested
expect(response.status).toBe(HTTP_UNPROCESSABLE_ENTITY);
// or add comment explaining the status
```

---

### Performance

| Test | Duration | Issue | Recommendation |
|------|----------|-------|----------------|
| `should sync all users` | 12s | Full DB scan | Use pagination or limit |
| `should send emails` | 8s | Real SMTP | Mock email service |
| `should process file` | 5s | Large fixture | Use smaller test file |

---

### Anti-Patterns Detected

| Pattern | Count | Impact | Fix |
|---------|-------|--------|-----|
| Sleep/setTimeout | 3 | Flaky | Use waitFor/polling |
| Shared state | 2 | Coupled | Isolate test data |
| No assertions | 1 | False positive | Add explicit expects |
| Console.log | 5 | Noise | Remove or use logger |

---

### Recommendations

#### High Priority
1. **Add missing edge case tests** — Especially error handling
2. **Fix flaky tests** — Replace timeouts with proper waits
3. **Isolate test data** — Each test creates its own data

#### Medium Priority
4. **Improve naming** — Make test names describe behavior
5. **Add schema validation** — Verify response structures
6. **Mock external services** — Reduce flakiness

#### Low Priority
7. **Organize test files** — Group by feature, not by type
8. **Add test documentation** — Explain complex setups
9. **Optimize slow tests** — Target < 5s per test

---

### Test Pyramid Assessment

```
        ▲ E2E (10%)
       ╱ ╲  Currently: 5% ⚠️
      ╱───╲
     ╱     ╲ Integration (30%)
    ╱  ───  ╲ Currently: 25% ⚠️
   ╱         ╲
  ╱───────────╲ Unit (60%)
 ╱             ╲ Currently: 70% ✅
╱───────────────╲

Recommendation: Add more integration and E2E tests
```

---

### Action Items

- [ ] P0: Fix 3 flaky tests identified
- [ ] P1: Add 5 missing edge case tests
- [ ] P1: Mock email service in 2 tests
- [ ] P2: Refactor shared test utilities
- [ ] P2: Add test for concurrent updates
```

## Checklist for Review

### Structure
- [ ] Tests organized by feature/module
- [ ] Clear describe/it nesting
- [ ] Proper setup/teardown

### Quality
- [ ] Descriptive test names
- [ ] Single assertion per test (when practical)
- [ ] No test interdependencies

### Coverage
- [ ] Happy paths covered
- [ ] Edge cases covered
- [ ] Error scenarios covered
- [ ] Boundary conditions tested

### Performance
- [ ] No unnecessary waits
- [ ] External services mocked
- [ ] Reasonable test data size

### Maintainability
- [ ] No magic numbers
- [ ] Reusable fixtures
- [ ] Comments for complex logic
