# Authentication API

The MyApp Authentication API provides secure user authentication using JWT tokens.

## Overview

- **Base URL**: `/api/auth`
- **Authentication**: JWT Bearer tokens
- **Rate Limiting**: 100 requests per minute per IP

## Endpoints

### POST /api/auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "createdAt": "2024-01-01T00:00:00Z"
    },
    "token": "jwt.token.here"
  }
}
```

**Status Codes:**
- `201` - User created successfully
- `400` - Invalid request data
- `409` - Email already exists

### POST /api/auth/login

Authenticate an existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe"
    },
    "token": "jwt.token.here",
    "expiresAt": "2024-01-01T01:00:00Z"
  }
}
```

**Status Codes:**
- `200` - Login successful
- `401` - Invalid credentials
- `429` - Too many attempts

### POST /api/auth/logout

Invalidate the current user's token.

**Headers:**
```
Authorization: Bearer jwt.token.here
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Status Codes:**
- `200` - Logout successful
- `401` - Invalid or missing token

### GET /api/auth/me

Get current user information.

**Headers:**
```
Authorization: Bearer jwt.token.here
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user",
      "createdAt": "2024-01-01T00:00:00Z",
      "lastLoginAt": "2024-01-01T12:00:00Z"
    }
  }
}
```

## Authentication Flow

1. **Registration**: User creates account with email/password
2. **Login**: User authenticates and receives JWT token
3. **Token Usage**: Include token in Authorization header for protected routes
4. **Token Refresh**: Tokens expire after 1 hour, use refresh endpoint
5. **Logout**: Invalidate token server-side

## Security Features

- **Password Hashing**: bcrypt with salt rounds
- **JWT Tokens**: RS256 signed tokens
- **Rate Limiting**: Prevents brute force attacks
- **Input Validation**: All inputs sanitized and validated
- **HTTPS Only**: All auth endpoints require HTTPS in production

## Error Handling

All authentication errors follow this format:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Email or password is incorrect",
    "details": {}
  }
}
```

**Common Error Codes:**
- `INVALID_CREDENTIALS` - Wrong email/password
- `TOKEN_EXPIRED` - JWT token has expired
- `TOKEN_INVALID` - JWT token is malformed
- `EMAIL_EXISTS` - Email already registered
- `VALIDATION_ERROR` - Input validation failed
- `RATE_LIMITED` - Too many requests

## Code Examples

### JavaScript/Fetch
```javascript
// Register new user
const response = await fetch('/api/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securePassword123',
    firstName: 'John',
    lastName: 'Doe'
  })
});

const data = await response.json();
if (data.success) {
  localStorage.setItem('token', data.data.token);
}
```

### cURL
```bash
# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123"
  }'

# Access protected route
curl -X GET http://localhost:3000/api/auth/me \
  -H "Authorization: Bearer jwt.token.here"
```