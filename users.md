# Users API

Comprehensive API for managing user accounts, profiles, and user-related operations.

## Overview

- **Base URL**: `/api/users`
- **Authentication**: Required (JWT Bearer token)
- **Rate Limiting**: 200 requests per minute
- **Version**: v1

## Endpoints

### GET /api/users

Retrieve a paginated list of all users.

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Items per page (default: 20, max: 100)
- `sort` (string, optional): Sort field (default: `createdAt`)
- `order` (string, optional): Sort order (`asc` or `desc`, default: `desc`)
- `search` (string, optional): Search by name or email
- `role` (string, optional): Filter by user role
- `status` (string, optional): Filter by status (`active`, `inactive`, `suspended`)

**Example Request:**
```bash
GET /api/users?page=1&limit=20&sort=lastName&order=asc&search=john
```

**Response:**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": "usr_abc123",
        "email": "john.doe@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "role": "user",
        "status": "active",
        "avatar": "https://cdn.example.com/avatars/usr_abc123.jpg",
        "createdAt": "2024-01-15T10:30:00Z",
        "lastLoginAt": "2024-03-20T14:22:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 92,
      "itemsPerPage": 20,
      "hasNextPage": true,
      "hasPreviousPage": false
    }
  }
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `403` - Forbidden (insufficient permissions)
- `429` - Rate limit exceeded

### GET /api/users/:id

Retrieve detailed information about a specific user.

**Path Parameters:**
- `id` (string, required): User ID

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_abc123",
      "email": "john.doe@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "displayName": "John D.",
      "role": "user",
      "status": "active",
      "avatar": "https://cdn.example.com/avatars/usr_abc123.jpg",
      "bio": "Software engineer passionate about building great products",
      "location": "San Francisco, CA",
      "website": "https://johndoe.dev",
      "socialLinks": {
        "twitter": "johndoe",
        "linkedin": "johndoe",
        "github": "johndoe"
      },
      "preferences": {
        "emailNotifications": true,
        "pushNotifications": false,
        "theme": "dark",
        "language": "en"
      },
      "metadata": {
        "signupSource": "web",
        "referralCode": "REF123",
        "totalLogins": 145
      },
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-03-20T14:22:00Z",
      "lastLoginAt": "2024-03-20T14:22:00Z"
    }
  }
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `404` - User not found

### POST /api/users

Create a new user account (admin only).

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "firstName": "Jane",
  "lastName": "Smith",
  "role": "user",
  "sendWelcomeEmail": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_xyz789",
      "email": "newuser@example.com",
      "firstName": "Jane",
      "lastName": "Smith",
      "role": "user",
      "status": "active",
      "createdAt": "2024-03-21T09:15:00Z"
    }
  }
}
```

**Status Codes:**
- `201` - User created
- `400` - Invalid request data
- `401` - Unauthorized
- `403` - Forbidden (not admin)
- `409` - Email already exists

### PATCH /api/users/:id

Update user information.

**Path Parameters:**
- `id` (string, required): User ID

**Request Body (all fields optional):**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "displayName": "JD",
  "bio": "Updated bio text",
  "location": "New York, NY",
  "website": "https://newsite.com",
  "avatar": "https://cdn.example.com/avatars/new.jpg",
  "socialLinks": {
    "twitter": "newhandle"
  },
  "preferences": {
    "theme": "light"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_abc123",
      "email": "john.doe@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "updatedAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

**Status Codes:**
- `200` - User updated
- `400` - Invalid request data
- `401` - Unauthorized
- `403` - Forbidden (can only update own profile)
- `404` - User not found

### DELETE /api/users/:id

Delete a user account (admin only or own account).

**Path Parameters:**
- `id` (string, required): User ID

**Response:**
```json
{
  "success": true,
  "message": "User account deleted successfully"
}
```

**Status Codes:**
- `200` - User deleted
- `401` - Unauthorized
- `403` - Forbidden
- `404` - User not found

## User Roles

The system supports the following user roles:

- **admin**: Full system access, can manage all users
- **moderator**: Can manage users and content
- **user**: Standard user with basic permissions
- **guest**: Limited read-only access

## User Status Values

- **active**: User can access the system normally
- **inactive**: User account exists but cannot log in
- **suspended**: User temporarily blocked due to violations
- **deleted**: User account marked for deletion

## Permissions

Different operations require different permission levels:

| Operation | Required Role |
|-----------|---------------|
| List users | user+ |
| View user details | user+ (own), admin (any) |
| Create user | admin |
| Update user | user (own), admin (any) |
| Delete user | user (own), admin (any) |
| Change user role | admin |
| Suspend user | moderator+ |

## Webhooks

The Users API can trigger webhooks for the following events:

- `user.created` - New user account created
- `user.updated` - User profile updated
- `user.deleted` - User account deleted
- `user.suspended` - User account suspended
- `user.login` - User logged in

## Examples

### Search for users
```javascript
const searchUsers = async (query) => {
  const response = await fetch(`/api/users?search=${query}&limit=10`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
};
```

### Update user profile
```javascript
const updateProfile = async (userId, updates) => {
  const response = await fetch(`/api/users/${userId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
  return response.json();
};
```

### Get user with error handling
```javascript
try {
  const response = await fetch(`/api/users/${userId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const data = await response.json();
  console.log(data.data.user);
} catch (error) {
  console.error('Failed to fetch user:', error);
}
```