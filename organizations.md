# Organizations API

Manage organizations, teams, and organizational hierarchies within the platform.

## Overview

- **Base URL**: `/api/organizations`
- **Authentication**: Required (JWT Bearer token)
- **Rate Limiting**: 150 requests per minute
- **Version**: v1

## Core Concepts

Organizations represent companies or groups using the platform. Each organization can have:
- Multiple teams
- Custom billing plans
- Organization-wide settings
- Member management with roles
- Shared resources and assets

## Endpoints

### GET /api/organizations

List all organizations accessible to the current user.

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Results per page (default: 20, max: 100)
- `type` (string): Filter by type (`company`, `team`, `personal`)
- `industry` (string): Filter by industry
- `size` (string): Filter by size (`startup`, `small`, `medium`, `enterprise`)

**Response:**
```json
{
  "success": true,
  "data": {
    "organizations": [
      {
        "id": "org_abc123",
        "name": "Acme Corporation",
        "slug": "acme-corp",
        "type": "company",
        "industry": "technology",
        "size": "medium",
        "logo": "https://cdn.example.com/logos/acme.png",
        "website": "https://acme.com",
        "description": "Leading provider of innovative solutions",
        "location": {
          "city": "San Francisco",
          "state": "CA",
          "country": "US"
        },
        "memberCount": 45,
        "plan": "business",
        "createdAt": "2023-06-15T00:00:00Z",
        "isOwner": true,
        "role": "admin"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 3,
      "totalItems": 52
    }
  }
}
```

### GET /api/organizations/:id

Get detailed information about a specific organization.

**Path Parameters:**
- `id` (string): Organization ID or slug

**Response:**
```json
{
  "success": true,
  "data": {
    "organization": {
      "id": "org_abc123",
      "name": "Acme Corporation",
      "slug": "acme-corp",
      "type": "company",
      "industry": "technology",
      "size": "medium",
      "logo": "https://cdn.example.com/logos/acme.png",
      "website": "https://acme.com",
      "description": "Leading provider of innovative solutions",
      "location": {
        "address": "123 Market St",
        "city": "San Francisco",
        "state": "CA",
        "zipCode": "94103",
        "country": "US"
      },
      "contact": {
        "email": "info@acme.com",
        "phone": "+1-555-0123",
        "supportEmail": "support@acme.com"
      },
      "social": {
        "twitter": "acmecorp",
        "linkedin": "company/acme",
        "github": "acmecorp"
      },
      "settings": {
        "allowPublicProfile": true,
        "requireTwoFactor": true,
        "defaultRole": "member",
        "allowInvites": true
      },
      "billing": {
        "plan": "business",
        "status": "active",
        "billingEmail": "billing@acme.com",
        "nextBillingDate": "2024-04-01T00:00:00Z"
      },
      "stats": {
        "memberCount": 45,
        "teamCount": 8,
        "projectCount": 23,
        "storageUsed": 15728640000
      },
      "createdAt": "2023-06-15T00:00:00Z",
      "updatedAt": "2024-03-15T10:00:00Z"
    }
  }
}
```

### POST /api/organizations

Create a new organization.

**Request Body:**
```json
{
  "name": "New Company Inc",
  "slug": "new-company",
  "type": "company",
  "industry": "finance",
  "size": "startup",
  "description": "A new innovative fintech startup",
  "website": "https://newcompany.com",
  "location": {
    "city": "Austin",
    "state": "TX",
    "country": "US"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "organization": {
      "id": "org_xyz789",
      "name": "New Company Inc",
      "slug": "new-company",
      "type": "company",
      "createdAt": "2024-03-21T10:30:00Z",
      "role": "owner"
    }
  }
}
```

**Status Codes:**
- `201` - Organization created
- `400` - Invalid request data
- `409` - Slug already exists

### PATCH /api/organizations/:id

Update organization information.

**Path Parameters:**
- `id` (string): Organization ID

**Request Body:**
```json
{
  "name": "Updated Company Name",
  "description": "Updated description",
  "logo": "https://cdn.example.com/newlogo.png",
  "website": "https://newwebsite.com",
  "settings": {
    "requireTwoFactor": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "organization": {
      "id": "org_abc123",
      "name": "Updated Company Name",
      "updatedAt": "2024-03-21T11:00:00Z"
    }
  }
}
```

### DELETE /api/organizations/:id

Delete an organization (owner only).

**Path Parameters:**
- `id` (string): Organization ID

**Query Parameters:**
- `confirm` (string, required): Must be the organization name to confirm deletion

**Response:**
```json
{
  "success": true,
  "message": "Organization deleted successfully"
}
```

## Organization Members

### GET /api/organizations/:id/members

List all members of an organization.

**Query Parameters:**
- `role` (string): Filter by role
- `status` (string): Filter by status
- `search` (string): Search by name or email

**Response:**
```json
{
  "success": true,
  "data": {
    "members": [
      {
        "id": "mem_123",
        "userId": "usr_abc",
        "organizationId": "org_abc123",
        "role": "admin",
        "status": "active",
        "user": {
          "id": "usr_abc",
          "email": "john@acme.com",
          "firstName": "John",
          "lastName": "Doe",
          "avatar": "https://cdn.example.com/avatars/john.jpg"
        },
        "joinedAt": "2023-06-15T00:00:00Z",
        "lastActiveAt": "2024-03-21T09:00:00Z"
      }
    ],
    "totalMembers": 45
  }
}
```

### POST /api/organizations/:id/members

Invite a new member to the organization.

**Request Body:**
```json
{
  "email": "newmember@example.com",
  "role": "member",
  "teams": ["team_123", "team_456"],
  "sendEmail": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "invitation": {
      "id": "inv_xyz",
      "email": "newmember@example.com",
      "role": "member",
      "status": "pending",
      "expiresAt": "2024-03-28T00:00:00Z",
      "createdAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

### PATCH /api/organizations/:orgId/members/:memberId

Update a member's role or status.

**Request Body:**
```json
{
  "role": "admin",
  "teams": ["team_123", "team_789"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "member": {
      "id": "mem_123",
      "role": "admin",
      "updatedAt": "2024-03-21T11:00:00Z"
    }
  }
}
```

### DELETE /api/organizations/:orgId/members/:memberId

Remove a member from the organization.

**Response:**
```json
{
  "success": true,
  "message": "Member removed from organization"
}
```

## Organization Roles

Available roles within an organization:

- **owner**: Full control, can delete organization
- **admin**: Manage members, settings, and billing
- **manager**: Manage teams and projects
- **member**: Standard access to organization resources
- **guest**: Limited read-only access

## Organization Types

- **company**: Standard company organization
- **team**: Small team or group
- **personal**: Personal workspace
- **non-profit**: Non-profit organization
- **educational**: School or educational institution

## Webhooks

Organization-related webhook events:

- `organization.created`
- `organization.updated`
- `organization.deleted`
- `organization.member.added`
- `organization.member.removed`
- `organization.member.role_changed`

## Best Practices

1. **Slug Selection**: Choose unique, URL-friendly slugs
2. **Member Management**: Regularly audit member roles
3. **Settings**: Enable two-factor authentication for sensitive operations
4. **Billing**: Keep billing information up to date
5. **Data Retention**: Export data before deleting organizations