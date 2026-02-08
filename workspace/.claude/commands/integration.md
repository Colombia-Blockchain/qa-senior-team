# Integration Test Generator

Diseña y genera tests de integración para APIs y servicios.

## Instrucciones

1. **Identifica endpoints/servicios** — ¿Qué se va a testear?
2. **Define contratos** — Request/response esperados
3. **Crea test cases** — Happy path + edge cases
4. **Genera código** — Tests con mocks apropiados
5. **Define fixtures** — Datos de prueba necesarios

## Output Format

### Test Structure

```typescript
// tests/integration/[service].integration.test.ts

import { describe, it, expect, beforeAll, afterAll } from 'vitest'; // or jest
import { setupTestDatabase, teardownTestDatabase } from './fixtures';

describe('[Service/API] Integration Tests', () => {
  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  describe('POST /api/resource', () => {
    it('should create resource with valid data', async () => {
      // Arrange
      const payload = {
        name: 'Test Resource',
        type: 'example'
      };

      // Act
      const response = await fetch('/api/resource', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      // Assert
      expect(response.status).toBe(201);
      const data = await response.json();
      expect(data.id).toBeDefined();
      expect(data.name).toBe(payload.name);
    });

    it('should return 400 for invalid payload', async () => {
      const response = await fetch('/api/resource', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });

      expect(response.status).toBe(400);
      const error = await response.json();
      expect(error.message).toContain('validation');
    });

    it('should return 401 without authentication', async () => {
      const response = await fetch('/api/resource', {
        method: 'POST',
        body: JSON.stringify({ name: 'test' })
      });

      expect(response.status).toBe(401);
    });
  });
});
```

### Contract Testing (Pact-style)

```typescript
// Contract definition
const contract = {
  consumer: 'Frontend',
  provider: 'UserService',
  interactions: [
    {
      description: 'get user by id',
      request: {
        method: 'GET',
        path: '/users/123',
        headers: { Authorization: 'Bearer token' }
      },
      response: {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: '123',
          name: expect.any(String),
          email: expect.stringMatching(/@/)
        }
      }
    }
  ]
};
```

### Database Integration

```typescript
describe('Database Integration', () => {
  it('should handle transactions correctly', async () => {
    const trx = await db.transaction();

    try {
      await trx('users').insert({ name: 'Test' });
      await trx('profiles').insert({ user_id: 1 });
      await trx.commit();
    } catch (error) {
      await trx.rollback();
      throw error;
    }

    const user = await db('users').where({ name: 'Test' }).first();
    expect(user).toBeDefined();
  });

  it('should rollback on error', async () => {
    const initialCount = await db('users').count();

    try {
      await db.transaction(async (trx) => {
        await trx('users').insert({ name: 'Test' });
        throw new Error('Simulated failure');
      });
    } catch {
      // Expected
    }

    const finalCount = await db('users').count();
    expect(finalCount).toEqual(initialCount);
  });
});
```

### External Service Mocking

```typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('https://api.external.com/data', (req, res, ctx) => {
    return res(ctx.json({ result: 'mocked' }));
  }),

  rest.post('https://api.external.com/data', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json({ id: 'new-123' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Test Categories

| Category | Focus | Tools |
|----------|-------|-------|
| API | HTTP endpoints | supertest, fetch |
| Database | Data layer | testcontainers, sqlite |
| Queue | Message handling | bull-mock |
| Cache | Redis/Memcached | ioredis-mock |
| External | Third-party APIs | msw, nock |

## Consideraciones

- Usa test containers para DBs reales cuando sea crítico
- Mockea servicios externos para evitar flakiness
- Limpia datos entre tests para independencia
- Testea timeouts y error handling
- Valida contratos entre servicios
