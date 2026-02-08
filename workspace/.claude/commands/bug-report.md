# Bug Report Generator

Documenta bugs de forma estructurada y reproducible.

## Instrucciones

1. **Describe el problema** — ¿Qué está mal?
2. **Clasifica severidad** — Impacto en usuarios/negocio
3. **Documenta pasos** — Cómo reproducir
4. **Adjunta evidencia** — Logs, screenshots, requests
5. **Sugiere causa** — Si es posible identificarla

## Output Format

```markdown
## Bug: [Title - Short descriptive title]

### Metadata
| Field | Value |
|-------|-------|
| **ID** | BUG-XXXX |
| **Severity** | Critical / High / Medium / Low |
| **Priority** | P0 / P1 / P2 / P3 |
| **Status** | New / In Progress / Fixed / Verified |
| **Environment** | Production / Staging / Dev |
| **Component** | [Affected component] |
| **Reporter** | [Name] |
| **Assignee** | [Name] |
| **Date** | YYYY-MM-DD |

---

### Summary
[1-2 sentences describing the bug and its impact]

---

### Steps to Reproduce

**Preconditions:**
- User role: [role]
- Data state: [required data]
- Environment: [specific setup]

**Steps:**
1. Navigate to [URL]
2. Click on [element]
3. Enter [data]
4. Click [submit]

**Frequency:** Always / Intermittent (X of Y attempts)

---

### Expected Result
[What should happen]

---

### Actual Result
[What actually happens]

---

### Evidence

**Screenshots:**
![Description](url)

**Logs:**
```
[Relevant log entries]
```

**Request/Response:**
```json
// Request
{
  "endpoint": "POST /api/resource",
  "body": { ... }
}

// Response
{
  "status": 500,
  "error": "..."
}
```

**Console Errors:**
```
[Browser console errors]
```

---

### Technical Analysis

**Suspected Cause:**
[If identifiable, explain the root cause]

**Affected Code:**
- File: `path/to/file.ts`
- Function: `functionName()`
- Line: ~123

**Related Issues:**
- #123 - [Related issue title]

---

### Impact Assessment

| Impact Area | Description |
|-------------|-------------|
| Users Affected | All / Subset / Specific role |
| Data Impact | None / Corrupted / Lost |
| Business Impact | Revenue / UX / Security |
| Workaround | Available / Not available |

**Workaround (if available):**
[Steps to work around the issue]

---

### Environment Details

| Component | Version |
|-----------|---------|
| Browser | Chrome 120 |
| OS | macOS 14.2 |
| App Version | v2.3.1 |
| API Version | v1.5.0 |
| Node | 20.10.0 |

---

### Regression Info
- [ ] This is a regression
- [ ] Previously worked in version: [version]
- [ ] Introduced in: [commit/PR/version]
```

## Severity Guide

| Severity | Criteria |
|----------|----------|
| **Critical** | System down, data loss, security breach |
| **High** | Major feature broken, no workaround |
| **Medium** | Feature impaired, workaround exists |
| **Low** | Minor issue, cosmetic, edge case |

## Consideraciones

- Sé específico y objetivo
- Incluye toda la información para reproducir
- No asumas conocimiento previo del lector
- Separa hechos de especulaciones
- Actualiza el bug cuando haya nueva información
