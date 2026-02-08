# E2E Test Generator

Diseña y genera tests end-to-end para flujos completos de usuario.

## Instrucciones

1. **Identifica el flujo** — ¿Qué journey del usuario estamos testeando?
2. **Mapea los pasos** — Cada acción del usuario y respuesta esperada
3. **Define assertions** — Qué validar en cada paso
4. **Genera el código** — Tests en Playwright o Cypress según el proyecto

## Output Format

### Para Playwright:

```typescript
import { test, expect } from '@playwright/test';

test.describe('[Flow Name]', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: login, seed data, etc.
  });

  test('should [expected behavior]', async ({ page }) => {
    // Arrange
    await page.goto('/path');

    // Act
    await page.getByRole('button', { name: 'Action' }).click();

    // Assert
    await expect(page.getByText('Expected')).toBeVisible();
  });

  test.afterEach(async ({ page }) => {
    // Cleanup
  });
});
```

### Para Cypress:

```typescript
describe('[Flow Name]', () => {
  beforeEach(() => {
    // Setup
    cy.login();
  });

  it('should [expected behavior]', () => {
    // Arrange
    cy.visit('/path');

    // Act
    cy.get('[data-testid="action"]').click();

    // Assert
    cy.contains('Expected').should('be.visible');
  });

  afterEach(() => {
    // Cleanup
  });
});
```

## Page Object Model (si aplica)

```typescript
// pages/[page-name].page.ts
export class PageName {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('/path');
  }

  async doAction() {
    await this.page.getByRole('button', { name: 'Action' }).click();
  }

  async expectResult() {
    await expect(this.page.getByText('Result')).toBeVisible();
  }
}
```

## Consideraciones

- Usa selectores estables (data-testid, roles, labels)
- Evita waits hardcodeados, usa assertions que esperen
- Incluye cleanup para evitar tests flaky
- Considera diferentes viewports si es responsive
- Mockea servicios externos cuando sea necesario
