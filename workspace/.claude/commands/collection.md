# Postman Collection Generator

Genera colecciones de Postman/Newman para testing de APIs.

## Instrucciones

1. **Identifica el dominio** — ¿Qué API/servicio se va a testear?
2. **Mapea endpoints** — Todos los endpoints con sus métodos
3. **Define variables** — Ambiente, auth tokens, datos dinámicos
4. **Crea requests** — Con pre-request scripts y tests
5. **Organiza por flujos** — Agrupa requests relacionados

## Output Format

### Collection Structure

```json
{
  "info": {
    "name": "[Domain] API Tests",
    "description": "Colección de tests para [Domain] API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "{{env_base_url}}",
      "type": "string"
    },
    {
      "key": "authToken",
      "value": "",
      "type": "string"
    }
  ],
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{authToken}}",
        "type": "string"
      }
    ]
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "url": {
              "raw": "{{baseUrl}}/auth/login",
              "host": ["{{baseUrl}}"],
              "path": ["auth", "login"]
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"{{test_email}}\",\n  \"password\": \"{{test_password}}\"\n}"
            }
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status 200', () => pm.response.to.have.status(200));",
                  "pm.test('Has token', () => {",
                  "  const json = pm.response.json();",
                  "  pm.expect(json.token).to.be.a('string');",
                  "  pm.collectionVariables.set('authToken', json.token);",
                  "});"
                ]
              }
            }
          ]
        }
      ]
    },
    {
      "name": "Users",
      "item": [
        {
          "name": "Create User",
          "request": {
            "method": "POST",
            "url": "{{baseUrl}}/users",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"{{$randomFullName}}\",\n  \"email\": \"{{$randomEmail}}\"\n}"
            }
          },
          "event": [
            {
              "listen": "prerequest",
              "script": {
                "exec": [
                  "// Generate unique test data",
                  "pm.variables.set('testEmail', `test-${Date.now()}@example.com`);"
                ]
              }
            },
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status 201', () => pm.response.to.have.status(201));",
                  "pm.test('Has user ID', () => {",
                  "  const json = pm.response.json();",
                  "  pm.expect(json.id).to.exist;",
                  "  pm.collectionVariables.set('userId', json.id);",
                  "});",
                  "pm.test('Response time < 500ms', () => {",
                  "  pm.expect(pm.response.responseTime).to.be.below(500);",
                  "});"
                ]
              }
            }
          ]
        },
        {
          "name": "Get User",
          "request": {
            "method": "GET",
            "url": "{{baseUrl}}/users/{{userId}}"
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status 200', () => pm.response.to.have.status(200));",
                  "pm.test('User schema valid', () => {",
                  "  const schema = {",
                  "    type: 'object',",
                  "    required: ['id', 'name', 'email'],",
                  "    properties: {",
                  "      id: { type: 'string' },",
                  "      name: { type: 'string' },",
                  "      email: { type: 'string', format: 'email' }",
                  "    }",
                  "  };",
                  "  pm.expect(tv4.validate(pm.response.json(), schema)).to.be.true;",
                  "});"
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### Environment File

```json
{
  "name": "Staging",
  "values": [
    {
      "key": "env_base_url",
      "value": "https://api.staging.example.com",
      "enabled": true
    },
    {
      "key": "test_email",
      "value": "test@example.com",
      "enabled": true
    },
    {
      "key": "test_password",
      "value": "{{vault:test_password}}",
      "enabled": true,
      "type": "secret"
    }
  ]
}
```

### Newman CLI Commands

```bash
# Run collection
newman run collection.json -e environments/staging.json

# With reporters
newman run collection.json \
  -e environments/staging.json \
  --reporters cli,junit,htmlextra \
  --reporter-junit-export results/junit.xml \
  --reporter-htmlextra-export results/report.html

# With iterations
newman run collection.json \
  -e environments/staging.json \
  -d data/test-data.csv \
  -n 10

# CI/CD integration
newman run collection.json \
  -e environments/staging.json \
  --bail \
  --suppress-exit-code \
  --color off
```

### Data-Driven Testing

```csv
# data/users.csv
name,email,expectedStatus
"Valid User","valid@test.com",201
"","empty@test.com",400
"Test","invalid-email",400
```

```json
// In test script
const testData = pm.iterationData;
pm.test(`Create user: ${testData.get('name')}`, () => {
  pm.response.to.have.status(testData.get('expectedStatus'));
});
```

## Common Test Patterns

```javascript
// Status code
pm.test('Status 200', () => pm.response.to.have.status(200));

// Response time
pm.test('Response < 500ms', () => pm.expect(pm.response.responseTime).to.be.below(500));

// JSON schema
pm.test('Valid schema', () => {
  const schema = { /* JSON Schema */ };
  pm.expect(tv4.validate(pm.response.json(), schema)).to.be.true;
});

// Headers
pm.test('Has Content-Type', () => {
  pm.response.to.have.header('Content-Type', 'application/json');
});

// Body contains
pm.test('Has required fields', () => {
  const json = pm.response.json();
  pm.expect(json).to.have.property('id');
  pm.expect(json.items).to.be.an('array');
});

// Chaining requests
pm.collectionVariables.set('resourceId', pm.response.json().id);
```

## Consideraciones

- Organiza por dominio/feature, no por método HTTP
- Usa variables para datos dinámicos
- Incluye cleanup requests al final de cada flow
- Guarda tokens en collection variables, no environment
- Documenta precondiciones en la descripción
