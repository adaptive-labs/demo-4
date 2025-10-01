# Tasks API

Manage tasks, subtasks, and task-related operations within projects.

## Overview

- **Base URL**: `/api/tasks`
- **Authentication**: Required
- **Rate Limiting**: 300 requests per minute
- **Version**: v1

## Task Structure

Tasks are the fundamental unit of work within projects. Each task can have:

- Title and detailed description
- Assignees and watchers
- Due dates and time estimates
- Priority and status
- Labels and tags
- Subtasks and dependencies
- Comments and attachments
- Time tracking
- Custom fields

## Endpoints

### GET /api/tasks

Retrieve a list of tasks with filtering and pagination.

**Query Parameters:**
- `projectId` (string): Filter by project
- `assignee` (string): Filter by assignee user ID
- `status` (string): Filter by status
- `priority` (string): Filter by priority
- `labels` (string): Comma-separated label IDs
- `dueBefore` (string): Tasks due before date (ISO 8601)
- `dueAfter` (string): Tasks due after date
- `search` (string): Search in title and description
- `page` (integer): Page number
- `limit` (integer): Items per page (max 100)
- `sort` (string): Sort field (`createdAt`, `dueDate`, `priority`, `title`)
- `order` (string): Sort order (`asc`, `desc`)

**Response:**
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "task_abc123",
        "number": 42,
        "title": "Implement user authentication",
        "description": "Add JWT-based authentication system",
        "status": "in_progress",
        "priority": "high",
        "projectId": "proj_123",
        "assignees": [
          {
            "id": "usr_456",
            "name": "John Doe",
            "avatar": "https://cdn.example.com/avatars/john.jpg"
          }
        ],
        "reporter": {
          "id": "usr_789",
          "name": "Jane Smith"
        },
        "labels": [
          {
            "id": "lbl_001",
            "name": "backend",
            "color": "#3B82F6"
          }
        ],
        "estimate": {
          "value": 8,
          "unit": "hours"
        },
        "timeSpent": 4.5,
        "progress": 60,
        "dates": {
          "createdAt": "2024-03-15T10:00:00Z",
          "updatedAt": "2024-03-21T14:30:00Z",
          "startDate": "2024-03-16T00:00:00Z",
          "dueDate": "2024-03-25T00:00:00Z",
          "completedAt": null
        },
        "counts": {
          "subtasks": 3,
          "completedSubtasks": 2,
          "comments": 8,
          "attachments": 2
        }
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 12,
      "totalItems": 234,
      "hasNextPage": true
    }
  }
}
```

### GET /api/tasks/:id

Get detailed information about a specific task.

**Path Parameters:**
- `id` (string): Task ID or task number (with project context)

**Response:**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "task_abc123",
      "number": 42,
      "title": "Implement user authentication",
      "description": "Add JWT-based authentication system with the following requirements:\n\n- JWT token generation\n- Token refresh mechanism\n- Password hashing with bcrypt\n- Rate limiting on auth endpoints",
      "status": "in_progress",
      "priority": "high",
      "type": "feature",
      "projectId": "proj_123",
      "parentTaskId": null,
      "assignees": [
        {
          "id": "usr_456",
          "name": "John Doe",
          "email": "john@acme.com",
          "avatar": "https://cdn.example.com/avatars/john.jpg"
        }
      ],
      "watchers": [
        {
          "id": "usr_789",
          "name": "Jane Smith"
        }
      ],
      "reporter": {
        "id": "usr_789",
        "name": "Jane Smith"
      },
      "labels": [
        {
          "id": "lbl_001",
          "name": "backend",
          "color": "#3B82F6"
        },
        {
          "id": "lbl_002",
          "name": "security",
          "color": "#EF4444"
        }
      ],
      "estimate": {
        "value": 8,
        "unit": "hours",
        "remainingTime": 3.5
      },
      "timeSpent": 4.5,
      "progress": 60,
      "dependencies": {
        "blockedBy": [],
        "blocks": ["task_xyz789"]
      },
      "customFields": {
        "sprint": "Sprint 12",
        "storyPoints": 5,
        "reviewers": ["usr_111", "usr_222"]
      },
      "dates": {
        "createdAt": "2024-03-15T10:00:00Z",
        "updatedAt": "2024-03-21T14:30:00Z",
        "startDate": "2024-03-16T00:00:00Z",
        "dueDate": "2024-03-25T00:00:00Z",
        "completedAt": null
      },
      "counts": {
        "subtasks": 3,
        "completedSubtasks": 2,
        "comments": 8,
        "attachments": 2,
        "relatedTasks": 4
      }
    }
  }
}
```

### POST /api/tasks

Create a new task.

**Request Body:**
```json
{
  "projectId": "proj_123",
  "title": "Fix memory leak in worker process",
  "description": "Investigate and fix memory leak causing high memory usage",
  "status": "todo",
  "priority": "urgent",
  "type": "bug",
  "assignees": ["usr_456"],
  "labels": ["lbl_001", "lbl_003"],
  "dueDate": "2024-03-30T00:00:00Z",
  "estimate": {
    "value": 4,
    "unit": "hours"
  },
  "customFields": {
    "sprint": "Sprint 12",
    "storyPoints": 3
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "task_xyz789",
      "number": 43,
      "title": "Fix memory leak in worker process",
      "status": "todo",
      "projectId": "proj_123",
      "createdAt": "2024-03-21T15:00:00Z"
    }
  }
}
```

**Status Codes:**
- `201` - Task created successfully
- `400` - Invalid request data
- `403` - Forbidden (no access to project)
- `404` - Project not found

### PATCH /api/tasks/:id

Update an existing task.

**Path Parameters:**
- `id` (string): Task ID

**Request Body (all fields optional):**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "high",
  "assignees": ["usr_456", "usr_789"],
  "labels": ["lbl_001"],
  "dueDate": "2024-04-15T00:00:00Z",
  "progress": 75,
  "customFields": {
    "storyPoints": 8
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "task_abc123",
      "title": "Updated task title",
      "updatedAt": "2024-03-21T15:30:00Z"
    }
  }
}
```

### DELETE /api/tasks/:id

Delete a task permanently.

**Path Parameters:**
- `id` (string): Task ID

**Response:**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Status Codes:**
- `200` - Task deleted
- `403` - Forbidden
- `404` - Task not found

## Task Status Values

Standard task statuses:

- **todo**: Task is ready to be worked on
- **in_progress**: Task is currently being worked on
- **in_review**: Task is under review
- **blocked**: Task is blocked by dependencies
- **completed**: Task is finished
- **cancelled**: Task was cancelled

Custom statuses can be configured per project.

## Task Priority Levels

- **urgent**: Needs immediate attention
- **high**: Important and should be done soon
- **medium**: Normal priority
- **low**: Can be done when time permits

## Task Types

- **feature**: New feature or enhancement
- **bug**: Bug fix
- **task**: General task
- **improvement**: Improvement to existing feature
- **documentation**: Documentation work
- **research**: Research or investigation

## Subtasks

### GET /api/tasks/:id/subtasks

Get all subtasks of a task.

**Response:**
```json
{
  "success": true,
  "data": {
    "subtasks": [
      {
        "id": "task_sub001",
        "number": 44,
        "title": "Design authentication endpoints",
        "status": "completed",
        "assignee": {
          "id": "usr_456",
          "name": "John Doe"
        },
        "completedAt": "2024-03-20T10:00:00Z"
      }
    ]
  }
}
```

### POST /api/tasks/:id/subtasks

Create a subtask.

**Request Body:**
```json
{
  "title": "Write unit tests",
  "assignee": "usr_456",
  "estimate": {
    "value": 2,
    "unit": "hours"
  }
}
```

## Task Comments

### GET /api/tasks/:id/comments

Get all comments on a task.

**Response:**
```json
{
  "success": true,
  "data": {
    "comments": [
      {
        "id": "cmt_123",
        "content": "Started working on this task",
        "author": {
          "id": "usr_456",
          "name": "John Doe"
        },
        "createdAt": "2024-03-16T09:00:00Z",
        "updatedAt": null,
        "reactions": {
          "👍": 3,
          "🎉": 1
        }
      }
    ]
  }
}
```

### POST /api/tasks/:id/comments

Add a comment to a task.

**Request Body:**
```json
{
  "content": "This is a comment with **markdown** support",
  "mentionedUsers": ["usr_789"]
}
```

## Time Tracking

### POST /api/tasks/:id/time-entries

Log time spent on a task.

**Request Body:**
```json
{
  "duration": 2.5,
  "date": "2024-03-21",
  "description": "Implemented JWT token generation"
}
```

### GET /api/tasks/:id/time-entries

Get all time entries for a task.

## Webhooks

Task-related webhook events:

- `task.created`
- `task.updated`
- `task.deleted`
- `task.status_changed`
- `task.assigned`
- `task.completed`
- `task.comment_added`

## Examples

### Create task with assignees
```javascript
const createTask = async (projectId, taskData) => {
  const response = await fetch('/api/tasks', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      projectId,
      ...taskData
    })
  });
  return response.json();
};
```

### Update task status
```javascript
const updateTaskStatus = async (taskId, newStatus) => {
  const response = await fetch(`/api/tasks/${taskId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ status: newStatus })
  });
  return response.json();
};
```

### Search tasks
```javascript
const searchTasks = async (filters) => {
  const params = new URLSearchParams(filters);
  const response = await fetch(`/api/tasks?${params}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};

// Usage
const bugs = await searchTasks({
  projectId: 'proj_123',
  type: 'bug',
  status: 'todo',
  priority: 'high'
});
```