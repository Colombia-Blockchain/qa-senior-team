# Test Plan Generator

Genera un plan de pruebas completo para la feature o componente especificado.

## Instrucciones

1. **Analiza el contexto** — Lee los archivos relevantes del proyecto para entender la feature
2. **Identifica el scope** — Qué se va a testear y qué queda fuera
3. **Define la estrategia** — Tipos de tests necesarios (E2E, integration, unit)
4. **Crea la matriz de tests** — Lista todos los escenarios con prioridad
5. **Identifica riesgos** — Qué puede fallar y cómo mitigarlo

## Output Format

```markdown
## Test Plan: [Feature Name]

### Overview
[Breve descripción de la feature y su importancia]

### Scope
**In Scope:**
- ...

**Out of Scope:**
- ...

### Test Strategy

| Type | Coverage | Priority | Automation |
|------|----------|----------|------------|
| E2E | Critical user flows | P0 | Yes |
| Integration | API contracts, DB | P1 | Yes |
| Edge Cases | Error handling | P2 | Partial |

### Test Matrix

| ID | Scenario | Type | Priority | Preconditions | Expected Result |
|----|----------|------|----------|---------------|-----------------|
| TC-001 | ... | E2E | P0 | ... | ... |

### Test Data Requirements
- ...

### Environment Requirements
- ...

### Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| ... | High | Medium | ... |

### Dependencies
- ...

### Acceptance Criteria
- [ ] All P0 tests pass
- [ ] All P1 tests pass
- [ ] Coverage > 80%
```

## Consideraciones

- Prioriza por impacto en el usuario/negocio
- Incluye tanto happy paths como edge cases
- Considera dependencias externas y cómo mockearlas
- Define claramente qué datos de prueba se necesitan
