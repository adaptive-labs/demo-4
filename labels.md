# Backman

Create and manage labels for organizing tasks, projects, and other resources.

## Overview

- **Base URL**: `/api/labels`
- **Authentication**: Required
- **Rate Limiting**: 200 requests per minute
- **Scope**: Organization-wide or project-specific
- **Color Palette**: Predefined colors or custom hex codes

## Label Structure

Labels have:
- Name and description
- Color (hex code)
- Scope (organization or project)
- Usage statistics
- Icon (optional)

## Endpoints

### GET /api/labels

List all labels accessible to the user.

**Query Parameters:**
- `projectId` (string): Filter by project
- `scope` (string): Filter by scope (`organization`, `project`)
- `color` (string): Filter by color
- `search` (string): Search by name
- `page` (integer): Page number
- `limit` (integer): Items per page (max 100)
- `sort` (string): Sort field (`name`, `createdAt`, `usageCount`)
- `order` (string): Sort order

**Response:**
```json
{
  "success": true,
  "data": {
    "labels": [
      {
        "id": "lbl_abc123",
        "name": "bug",
        "description": "Something isn't working",
        "color": "#d73a4a",
        "textColor": "#ffffff",
        "icon": "bug",
        "scope": "organization",
        "projectId": null,
        "usageCount": 145,
        "createdBy": {
          "id": "usr_789",
          "name": "Jane Doe"
        },
        "createdAt": "2024-01-15T10:00:00Z",
        "updatedAt": "2024-03-21T10:00:00Z"
      },
      {
        "id": "lbl_def456",
        "name": "enhancement",
        "description": "New feature or request",
        "color": "#a2eeef",
        "textColor": "#000000",
        "icon": "sparkles",
        "scope": "organization",
        "usageCount": 89,
        "createdAt": "2024-01-15T10:00:00Z"
      },
      {
        "id": "lbl_ghi789",
        "name": "high priority",
        "description": "Needs immediate attention",
        "color": "#ff6b6b",
        "textColor": "#ffffff",
        "icon": "alert-triangle",
        "scope": "project",
        "projectId": "proj_123",
        "usageCount": 23,
        "createdAt": "2024-02-10T10:00:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 2,
      "totalItems": 24
    }
  }
}
```

### GET /api/labels/:id

Get a specific label with detailed usage statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "label": {
      "id": "lbl_abc123",
      "name": "bug",
      "description": "Something isn't working",
      "color": "#d73a4a",
      "textColor": "#ffffff",
      "icon": "bug",
      "scope": "organization",
      "projectId": null,
      "usageStats": {
        "totalUsage": 145,
        "tasks": 132,
        "projects": 8,
        "documents": 5,
        "byProject": [
          {
            "projectId": "proj_123",
            "projectName": "Website",
            "count": 45
          },
          {
            "projectId": "proj_456",
            "projectName": "Mobile App",
            "count": 38
          }
        ]
      },
      "recentlyUsed": [
        {
          "resourceType": "task",
          "resourceId": "task_123",
          "resourceTitle": "Fix login error",
          "usedAt": "2024-03-21T10:00:00Z"
        }
      ],
      "createdBy": {
        "id": "usr_789",
        "name": "Jane Doe",
        "email": "jane@acme.com"
      },
      "createdAt": "2024-01-15T10:00:00Z",
      "updatedAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

### POST /api/labels

Create a new label.

**Request Body:**
```json
{
  "name": "documentation",
  "description": "Documentation improvements",
  "color": "#0075ca",
  "icon": "book",
  "scope": "organization",
  "projectId": null
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "label": {
      "id": "lbl_new123",
      "name": "documentation",
      "color": "#0075ca",
      "textColor": "#ffffff",
      "createdAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

**Status Codes:**
- `201` - Label created successfully
- `400` - Invalid request (duplicate name, invalid color)
- `403` - Insufficient permissions

### PATCH /api/labels/:id

Update a label.

**Request Body:**
```json
{
  "name": "bug-fix",
  "description": "Bug fixes and patches",
  "color": "#ff0000"
}
```

### DELETE /api/labels/:id

Delete a label. This removes the label from all resources.

**Query Parameters:**
- `removeFromResources` (boolean): Remove from all resources (default: true)

**Response:**
```json
{
  "success": true,
  "message": "Label deleted successfully",
  "data": {
    "removedFrom": {
      "tasks": 132,
      "projects": 8,
      "documents": 5
    }
  }
}
```

## Label Colors

### GET /api/labels/colors

Get predefined color palette.

**Response:**
```json
{
  "success": true,
  "data": {
    "colors": [
      {
        "name": "Red",
        "value": "#d73a4a",
        "textColor": "#ffffff"
      },
      {
        "name": "Orange",
        "value": "#ff9800",
        "textColor": "#000000"
      },
      {
        "name": "Yellow",
        "value": "#ffeb3b",
        "textColor": "#000000"
      },
      {
        "name": "Green",
        "value": "#4caf50",
        "textColor": "#ffffff"
      },
      {
        "name": "Blue",
        "value": "#2196f3",
        "textColor": "#ffffff"
      },
      {
        "name": "Purple",
        "value": "#9c27b0",
        "textColor": "#ffffff"
      },
      {
        "name": "Gray",
        "value": "#9e9e9e",
        "textColor": "#ffffff"
      }
    ]
  }
}
```

## Resource Labeling

### GET /api/tasks/:id/labels

Get labels for a task.

**Response:**
```json
{
  "success": true,
  "data": {
    "labels": [
      {
        "id": "lbl_abc123",
        "name": "bug",
        "color": "#d73a4a"
      },
      {
        "id": "lbl_ghi789",
        "name": "high priority",
        "color": "#ff6b6b"
      }
    ]
  }
}
```

### POST /api/tasks/:id/labels

Add labels to a task.

**Request Body:**
```json
{
  "labelIds": ["lbl_abc123", "lbl_def456"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "task_123",
      "labels": [
        {
          "id": "lbl_abc123",
          "name": "bug",
          "color": "#d73a4a"
        },
        {
          "id": "lbl_def456",
          "name": "enhancement",
          "color": "#a2eeef"
        }
      ]
    }
  }
}
```

### DELETE /api/tasks/:id/labels/:labelId

Remove a label from a task.

## Label Groups

Organize related labels into groups:

### GET /api/label-groups

List label groups.

**Response:**
```json
{
  "success": true,
  "data": {
    "groups": [
      {
        "id": "grp_abc123",
        "name": "Type",
        "description": "Issue type classification",
        "labels": [
          {
            "id": "lbl_bug",
            "name": "bug",
            "color": "#d73a4a"
          },
          {
            "id": "lbl_enhancement",
            "name": "enhancement",
            "color": "#a2eeef"
          },
          {
            "id": "lbl_question",
            "name": "question",
            "color": "#d876e3"
          }
        ],
        "multiSelect": false,
        "required": true
      },
      {
        "id": "grp_def456",
        "name": "Priority",
        "description": "Priority level",
        "labels": [
          {
            "id": "lbl_low",
            "name": "low priority",
            "color": "#00ff00"
          },
          {
            "id": "lbl_medium",
            "name": "medium priority",
            "color": "#ffff00"
          },
          {
            "id": "lbl_high",
            "name": "high priority",
            "color": "#ff6b6b"
          }
        ],
        "multiSelect": false,
        "required": false
      }
    ]
  }
}
```

## Bulk Operations

### POST /api/labels/bulk-apply

Apply labels to multiple resources.

**Request Body:**
```json
{
  "labelIds": ["lbl_abc123", "lbl_def456"],
  "resources": [
    {
      "type": "task",
      "id": "task_123"
    },
    {
      "type": "task",
      "id": "task_456"
    }
  ]
}
```

### POST /api/labels/bulk-remove

Remove labels from multiple resources.

## Examples

### Create label
```javascript
const createLabel = async (name, color) => {
  const response = await fetch('/api/labels', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      name,
      color,
      scope: 'organization'
    })
  });

  return response.json();
};
```

### Add label to task
```javascript
const addLabelToTask = async (taskId, labelId) => {
  const response = await fetch(`/api/tasks/${taskId}/labels`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      labelIds: [labelId]
    })
  });

  return response.json();
};
```

### Filter tasks by label
```javascript
const getTasksByLabel = async (labelId) => {
  const response = await fetch(
    `/api/tasks?labelId=${labelId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );

  const data = await response.json();
  return data.data.tasks;
};
```