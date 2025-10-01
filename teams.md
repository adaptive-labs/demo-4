# Teams API

Manage teams within your organization for collaboration and access control.

## Overview

- **Base URL**: `/api/teams`
- **Authentication**: Required
- **Rate Limiting**: 150 requests per minute
- **Hierarchy**: Organization → Teams → Members
- **Permissions**: Team-level access control

## Team Structure

Teams have:
- Name and description
- Members with roles
- Project assignments
- Access permissions
- Settings and preferences
- Custom properties

## Endpoints

### GET /api/teams

List all teams in the organization.

**Query Parameters:**
- `organizationId` (string): Filter by organization
- `memberId` (string): Filter teams by member
- `projectId` (string): Filter teams assigned to project
- `search` (string): Search by name
- `page` (integer): Page number
- `limit` (integer): Items per page (max 100)
- `sort` (string): Sort field (`name`, `memberCount`, `createdAt`)
- `order` (string): Sort order

**Response:**
```json
{
  "success": true,
  "data": {
    "teams": [
      {
        "id": "team_abc123",
        "name": "Platform Team",
        "slug": "platform-team",
        "description": "Core platform development and infrastructure",
        "avatar": "https://avatar.example.com/team/platform.png",
        "organizationId": "org_123",
        "visibility": "private",
        "memberCount": 12,
        "projectCount": 8,
        "settings": {
          "defaultRole": "member",
          "allowMemberInvites": true,
          "requireApproval": false
        },
        "permissions": {
          "canView": true,
          "canEdit": true,
          "canDelete": false,
          "canManageMembers": true
        },
        "createdAt": "2024-01-15T10:00:00Z",
        "updatedAt": "2024-03-21T10:00:00Z"
      },
      {
        "id": "team_def456",
        "name": "Frontend Team",
        "slug": "frontend-team",
        "description": "UI/UX and frontend development",
        "avatar": null,
        "organizationId": "org_123",
        "visibility": "public",
        "memberCount": 8,
        "projectCount": 5,
        "createdAt": "2024-01-20T10:00:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 3,
      "totalItems": 12
    }
  }
}
```

### GET /api/teams/:id

Get detailed information about a specific team.

**Response:**
```json
{
  "success": true,
  "data": {
    "team": {
      "id": "team_abc123",
      "name": "Platform Team",
      "slug": "platform-team",
      "description": "Core platform development and infrastructure",
      "avatar": "https://avatar.example.com/team/platform.png",
      "organizationId": "org_123",
      "organization": {
        "id": "org_123",
        "name": "Acme Corp"
      },
      "visibility": "private",
      "memberCount": 12,
      "projectCount": 8,
      "members": [
        {
          "id": "usr_789",
          "name": "Jane Doe",
          "email": "jane@acme.com",
          "avatar": "https://avatar.example.com/jane.jpg",
          "role": "maintainer",
          "joinedAt": "2024-01-15T10:00:00Z"
        },
        {
          "id": "usr_111",
          "name": "John Smith",
          "email": "john@acme.com",
          "avatar": "https://avatar.example.com/john.jpg",
          "role": "member",
          "joinedAt": "2024-01-20T10:00:00Z"
        }
      ],
      "projects": [
        {
          "id": "proj_123",
          "name": "Core API",
          "description": "REST API backend"
        },
        {
          "id": "proj_456",
          "name": "Infrastructure",
          "description": "Cloud infrastructure"
        }
      ],
      "settings": {
        "defaultRole": "member",
        "allowMemberInvites": true,
        "requireApproval": false,
        "notificationPreferences": {
          "mentions": true,
          "assignments": true,
          "updates": false
        }
      },
      "customProperties": {
        "slack_channel": "#platform-team",
        "meeting_day": "Monday",
        "oncall_rotation": true
      },
      "stats": {
        "openTasks": 23,
        "completedTasks": 456,
        "activeProjects": 8
      },
      "createdBy": {
        "id": "usr_789",
        "name": "Jane Doe"
      },
      "createdAt": "2024-01-15T10:00:00Z",
      "updatedAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

### POST /api/teams

Create a new team.

**Request Body:**
```json
{
  "name": "Backend Team",
  "slug": "backend-team",
  "description": "Backend services and APIs",
  "organizationId": "org_123",
  "visibility": "private",
  "settings": {
    "defaultRole": "member",
    "allowMemberInvites": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "team": {
      "id": "team_new123",
      "name": "Backend Team",
      "slug": "backend-team",
      "createdAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

**Status Codes:**
- `201` - Team created successfully
- `400` - Invalid request (duplicate slug, invalid org)
- `403` - Insufficient permissions

### PATCH /api/teams/:id

Update team details.

**Request Body:**
```json
{
  "name": "Platform Engineering Team",
  "description": "Updated description",
  "visibility": "public",
  "settings": {
    "requireApproval": true
  }
}
```

### DELETE /api/teams/:id

Delete a team.

**Query Parameters:**
- `transferProjectsTo` (string): Team ID to transfer projects to

**Response:**
```json
{
  "success": true,
  "message": "Team deleted successfully",
  "data": {
    "transferredProjects": 8,
    "removedMembers": 12
  }
}
```

## Team Members

### GET /api/teams/:id/members

Get all members of a team.

**Query Parameters:**
- `role` (string): Filter by role
- `search` (string): Search by name or email
- `page` (integer): Page number
- `limit` (integer): Items per page

**Response:**
```json
{
  "success": true,
  "data": {
    "members": [
      {
        "id": "usr_789",
        "name": "Jane Doe",
        "email": "jane@acme.com",
        "avatar": "https://avatar.example.com/jane.jpg",
        "role": "maintainer",
        "status": "active",
        "joinedAt": "2024-01-15T10:00:00Z",
        "stats": {
          "assignedTasks": 12,
          "completedTasks": 89
        }
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 1,
      "totalItems": 12
    }
  }
}
```

### POST /api/teams/:id/members

Add members to a team.

**Request Body:**
```json
{
  "userIds": ["usr_111", "usr_222"],
  "role": "member",
  "sendInvitation": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "added": [
      {
        "userId": "usr_111",
        "role": "member",
        "status": "active"
      },
      {
        "userId": "usr_222",
        "role": "member",
        "status": "pending"
      }
    ],
    "failed": []
  }
}
```

### PATCH /api/teams/:id/members/:userId

Update a member's role.

**Request Body:**
```json
{
  "role": "maintainer"
}
```

### DELETE /api/teams/:id/members/:userId

Remove a member from the team.

**Response:**
```json
{
  "success": true,
  "message": "Member removed from team"
}
```

## Team Roles

Available roles:
- **Owner**: Full control over team
- **Maintainer**: Can manage members and settings
- **Member**: Standard access
- **Guest**: Limited read-only access

### GET /api/teams/:id/roles

Get role definitions and permissions.

**Response:**
```json
{
  "success": true,
  "data": {
    "roles": [
      {
        "name": "owner",
        "displayName": "Owner",
        "permissions": [
          "team.delete",
          "team.update",
          "members.manage",
          "projects.manage"
        ]
      },
      {
        "name": "maintainer",
        "displayName": "Maintainer",
        "permissions": [
          "team.update",
          "members.manage",
          "projects.manage"
        ]
      },
      {
        "name": "member",
        "displayName": "Member",
        "permissions": [
          "projects.view",
          "tasks.create",
          "tasks.update"
        ]
      }
    ]
  }
}
```

## Team Projects

### GET /api/teams/:id/projects

Get projects assigned to a team.

**Response:**
```json
{
  "success": true,
  "data": {
    "projects": [
      {
        "id": "proj_123",
        "name": "Core API",
        "description": "REST API backend",
        "status": "active",
        "memberCount": 8,
        "taskCount": 45
      }
    ]
  }
}
```

### POST /api/teams/:id/projects

Assign projects to a team.

**Request Body:**
```json
{
  "projectIds": ["proj_123", "proj_456"]
}
```

### DELETE /api/teams/:id/projects/:projectId

Unassign a project from the team.

## Examples

### Create team
```javascript
const createTeam = async (name, organizationId) => {
  const response = await fetch('/api/teams', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      name,
      organizationId,
      visibility: 'private',
      settings: {
        defaultRole: 'member'
      }
    })
  });

  return response.json();
};
```

### Add members
```javascript
const addTeamMembers = async (teamId, userIds) => {
  const response = await fetch(`/api/teams/${teamId}/members`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      userIds,
      role: 'member'
    })
  });

  return response.json();
};
```

### Get team projects
```javascript
const getTeamProjects = async (teamId) => {
  const response = await fetch(`/api/teams/${teamId}/projects`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const data = await response.json();
  return data.data.projects;
};
```