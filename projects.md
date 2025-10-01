# Projects API

Create and manage projects within your organization.

## Overview

- **Base URL**: `/api/projects`
- **Authentication**: Required
- **Rate Limiting**: 200 requests per minute

## What is a Project?

Projects are collaborative workspaces where teams can organize tasks, documents, and resources. Each project belongs to an organization and can have:

- Custom settings and permissions
- Multiple team members with different roles
- Associated tasks and milestones
- File attachments and documents
- Activity timeline
- Integration with external tools

## Endpoints

### GET /api/projects

List all projects accessible to the current user.

**Query Parameters:**
- `organizationId` (string): Filter by organization
- `status` (string): Filter by status (`active`, `archived`, `completed`)
- `page` (integer): Page number
- `limit` (integer): Items per page (max 100)
- `sort` (string): Sort field
- `order` (string): Sort order (`asc`, `desc`)
- `search` (string): Search project names and descriptions

**Response:**
```json
{
  "success": true,
  "data": {
    "projects": [
      {
        "id": "proj_abc123",
        "name": "Website Redesign",
        "slug": "website-redesign",
        "description": "Complete redesign of company website",
        "status": "active",
        "visibility": "private",
        "color": "#3B82F6",
        "icon": "🚀",
        "organization": {
          "id": "org_123",
          "name": "Acme Corp"
        },
        "owner": {
          "id": "usr_456",
          "name": "John Doe"
        },
        "stats": {
          "memberCount": 8,
          "taskCount": 45,
          "completedTasks": 23,
          "progress": 51
        },
        "dates": {
          "startDate": "2024-01-15T00:00:00Z",
          "dueDate": "2024-06-30T00:00:00Z",
          "createdAt": "2024-01-10T10:00:00Z",
          "updatedAt": "2024-03-20T14:30:00Z"
        }
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 92
    }
  }
}
```

### GET /api/projects/:id

Get detailed information about a specific project.

**Path Parameters:**
- `id` (string): Project ID or slug

**Response:**
```json
{
  "success": true,
  "data": {
    "project": {
      "id": "proj_abc123",
      "name": "Website Redesign",
      "slug": "website-redesign",
      "description": "Complete redesign of company website with focus on user experience and performance",
      "status": "active",
      "visibility": "private",
      "color": "#3B82F6",
      "icon": "🚀",
      "organizationId": "org_123",
      "ownerId": "usr_456",
      "settings": {
        "allowGuestAccess": false,
        "requireApproval": true,
        "enableComments": true,
        "enableTimeTracking": true,
        "defaultView": "board",
        "taskPrefix": "WR"
      },
      "integrations": {
        "github": {
          "enabled": true,
          "repository": "acme/website"
        },
        "slack": {
          "enabled": true,
          "channel": "#website-redesign"
        }
      },
      "stats": {
        "memberCount": 8,
        "taskCount": 45,
        "completedTasks": 23,
        "openTasks": 22,
        "progress": 51,
        "timeSpent": 14400,
        "filesCount": 156,
        "commentsCount": 234
      },
      "dates": {
        "startDate": "2024-01-15T00:00:00Z",
        "dueDate": "2024-06-30T00:00:00Z",
        "createdAt": "2024-01-10T10:00:00Z",
        "updatedAt": "2024-03-20T14:30:00Z",
        "lastActivityAt": "2024-03-21T09:15:00Z"
      }
    }
  }
}
```

### POST /api/projects

Create a new project.

**Request Body:**
```json
{
  "name": "Mobile App Development",
  "slug": "mobile-app",
  "description": "Native mobile app for iOS and Android",
  "organizationId": "org_123",
  "status": "active",
  "visibility": "private",
  "color": "#10B981",
  "icon": "📱",
  "startDate": "2024-04-01",
  "dueDate": "2024-12-31",
  "template": "software-development",
  "settings": {
    "allowGuestAccess": false,
    "requireApproval": true,
    "enableTimeTracking": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "project": {
      "id": "proj_xyz789",
      "name": "Mobile App Development",
      "slug": "mobile-app",
      "status": "active",
      "createdAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

**Status Codes:**
- `201` - Project created
- `400` - Invalid request
- `403` - Forbidden
- `409` - Slug already exists

### PATCH /api/projects/:id

Update project details.

**Path Parameters:**
- `id` (string): Project ID

**Request Body:**
```json
{
  "name": "Updated Project Name",
  "description": "Updated description",
  "status": "archived",
  "color": "#EF4444",
  "dueDate": "2024-12-31",
  "settings": {
    "allowGuestAccess": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "project": {
      "id": "proj_abc123",
      "name": "Updated Project Name",
      "updatedAt": "2024-03-21T11:00:00Z"
    }
  }
}
```

### DELETE /api/projects/:id

Delete a project permanently.

**Path Parameters:**
- `id` (string): Project ID

**Query Parameters:**
- `confirm` (string, required): Must be project name to confirm

**Response:**
```json
{
  "success": true,
  "message": "Project deleted successfully"
}
```

## Project Members

### GET /api/projects/:id/members

List all project members.

**Response:**
```json
{
  "success": true,
  "data": {
    "members": [
      {
        "id": "pm_123",
        "projectId": "proj_abc123",
        "userId": "usr_456",
        "role": "admin",
        "user": {
          "id": "usr_456",
          "name": "John Doe",
          "email": "john@acme.com",
          "avatar": "https://cdn.example.com/avatars/john.jpg"
        },
        "permissions": ["read", "write", "delete", "manage"],
        "joinedAt": "2024-01-15T00:00:00Z"
      }
    ]
  }
}
```

### POST /api/projects/:id/members

Add a member to the project.

**Request Body:**
```json
{
  "userId": "usr_789",
  "role": "member"
}
```

### DELETE /api/projects/:projectId/members/:memberId

Remove a member from the project.

**Response:**
```json
{
  "success": true,
  "message": "Member removed from project"
}
```

## Project Status Values

- **active**: Project is currently in progress
- **completed**: Project has been finished
- **on_hold**: Project is paused temporarily
- **archived**: Project is archived for reference
- **cancelled**: Project was cancelled

## Project Visibility

- **private**: Only members can access
- **organization**: All organization members can view
- **public**: Anyone with the link can view

## Project Roles

- **admin**: Full project management
- **manager**: Manage tasks and members
- **member**: Create and edit tasks
- **viewer**: Read-only access
- **guest**: Limited temporary access

## Project Templates

Available project templates:

- `software-development`: Software development project
- `marketing-campaign`: Marketing campaign planning
- `product-launch`: Product launch coordination
- `event-planning`: Event organization
- `content-creation`: Content production
- `research`: Research project
- `blank`: Empty project

## Webhooks

Project webhook events:

- `project.created`
- `project.updated`
- `project.deleted`
- `project.status_changed`
- `project.member.added`
- `project.member.removed`
- `project.completed`

## Examples

### Create project with template
```javascript
const createProject = async (data) => {
  const response = await fetch('/api/projects', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      ...data,
      template: 'software-development'
    })
  });
  return response.json();
};
```

### Update project status
```javascript
const archiveProject = async (projectId) => {
  const response = await fetch(`/api/projects/${projectId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ status: 'archived' })
  });
  return response.json();
};
```

### Search projects
```javascript
const searchProjects = async (query, organizationId) => {
  const params = new URLSearchParams({
    search: query,
    organizationId,
    status: 'active'
  });

  const response = await fetch(`/api/projects?${params}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};
```