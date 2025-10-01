# Comments API

Manage comments, discussions, and threaded conversations across tasks, projects, and documents.

## Overview

- **Base URL**: `/api/comments`
- **Authentication**: Required
- **Rate Limiting**: 200 requests per minute
- **Nested Comments**: Up to 10 levels deep

## Comment Structure

Comments support:
- Rich text formatting (Markdown)
- @mentions with notifications
- File attachments
- Emoji reactions
- Edit history tracking
- Thread resolution status

## Endpoints

### GET /api/comments

List comments with filtering options.

**Query Parameters:**
- `taskId` (string): Filter by task
- `projectId` (string): Filter by project
- `documentId` (string): Filter by document
- `userId` (string): Filter by author
- `parentId` (string): Get replies to a specific comment
- `resolved` (boolean): Filter by resolution status
- `page` (integer): Page number
- `limit` (integer): Items per page (max 100)
- `sort` (string): Sort field (`createdAt`, `updatedAt`, `reactions`)
- `order` (string): Sort order

**Response:**
```json
{
  "success": true,
  "data": {
    "comments": [
      {
        "id": "cmt_abc123",
        "content": "This looks great! Just a few suggestions...",
        "contentHtml": "<p>This looks great! Just a few suggestions...</p>",
        "author": {
          "id": "usr_789",
          "name": "Jane Doe",
          "email": "jane@acme.com",
          "avatar": "https://avatar.example.com/jane.jpg"
        },
        "taskId": "task_456",
        "projectId": "proj_123",
        "parentId": null,
        "replyCount": 3,
        "reactions": {
          "👍": 5,
          "❤️": 2,
          "🎉": 1
        },
        "userReaction": "👍",
        "attachments": [
          {
            "id": "file_xyz",
            "name": "screenshot.png",
            "url": "https://cdn.example.com/files/xyz.png"
          }
        ],
        "mentions": ["usr_111", "usr_222"],
        "resolved": false,
        "edited": false,
        "editedAt": null,
        "createdAt": "2024-03-21T10:00:00Z",
        "updatedAt": "2024-03-21T10:00:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 89
    }
  }
}
```

### GET /api/comments/:id

Get a specific comment with all replies.

**Path Parameters:**
- `id` (string): Comment ID

**Response:**
```json
{
  "success": true,
  "data": {
    "comment": {
      "id": "cmt_abc123",
      "content": "This looks great! Just a few suggestions...",
      "contentHtml": "<p>This looks great! Just a few suggestions...</p>",
      "author": {
        "id": "usr_789",
        "name": "Jane Doe",
        "email": "jane@acme.com",
        "avatar": "https://avatar.example.com/jane.jpg"
      },
      "taskId": "task_456",
      "replies": [
        {
          "id": "cmt_def456",
          "content": "Thanks for the feedback!",
          "author": {
            "id": "usr_111",
            "name": "John Smith"
          },
          "createdAt": "2024-03-21T10:05:00Z"
        }
      ],
      "history": [
        {
          "version": 1,
          "content": "Original content",
          "editedBy": "usr_789",
          "editedAt": "2024-03-21T10:00:00Z"
        }
      ]
    }
  }
}
```

### POST /api/comments

Create a new comment.

**Request Body:**
```json
{
  "content": "This looks great! Just a few suggestions...",
  "taskId": "task_456",
  "projectId": "proj_123",
  "documentId": null,
  "parentId": null,
  "attachments": ["file_xyz"],
  "mentions": ["usr_111", "usr_222"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "comment": {
      "id": "cmt_new123",
      "content": "This looks great! Just a few suggestions...",
      "createdAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

**Status Codes:**
- `201` - Comment created successfully
- `400` - Invalid request
- `404` - Parent comment or resource not found

### PATCH /api/comments/:id

Edit a comment. Only the author can edit.

**Request Body:**
```json
{
  "content": "Updated comment content..."
}
```

### DELETE /api/comments/:id

Delete a comment. Only author or admins can delete.

**Response:**
```json
{
  "success": true,
  "message": "Comment deleted successfully"
}
```

## Reactions

### POST /api/comments/:id/reactions

Add a reaction to a comment.

**Request Body:**
```json
{
  "emoji": "👍"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "reactions": {
      "👍": 6,
      "❤️": 2
    }
  }
}
```

### DELETE /api/comments/:id/reactions

Remove your reaction from a comment.

**Request Body:**
```json
{
  "emoji": "👍"
}
```

## Resolution

### POST /api/comments/:id/resolve

Mark a comment thread as resolved.

**Response:**
```json
{
  "success": true,
  "data": {
    "comment": {
      "id": "cmt_abc123",
      "resolved": true,
      "resolvedBy": {
        "id": "usr_789",
        "name": "Jane Doe"
      },
      "resolvedAt": "2024-03-21T11:00:00Z"
    }
  }
}
```

### POST /api/comments/:id/unresolve

Reopen a resolved comment thread.

## Mentions

When mentioning users with `@username` syntax:
- Mentioned users receive notifications
- Mentioned users are added to the `mentions` array
- Mentions are parsed and linked in `contentHtml`

**Example:**
```markdown
@jane.doe can you review this?
```

## Webhooks

Comment events trigger webhooks:

**Events:**
- `comment.created`
- `comment.updated`
- `comment.deleted`
- `comment.resolved`
- `comment.reaction_added`

**Payload:**
```json
{
  "event": "comment.created",
  "timestamp": "2024-03-21T10:00:00Z",
  "data": {
    "comment": {
      "id": "cmt_abc123",
      "content": "...",
      "author": {...},
      "taskId": "task_456"
    }
  }
}
```

## Examples

### Create a comment
```javascript
const createComment = async (taskId, content) => {
  const response = await fetch('/api/comments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      taskId,
      content,
      mentions: extractMentions(content)
    })
  });

  return response.json();
};
```

### Reply to a comment
```javascript
const replyToComment = async (parentId, content) => {
  const response = await fetch('/api/comments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      parentId,
      content
    })
  });

  return response.json();
};
```

### Add reaction
```javascript
const addReaction = async (commentId, emoji) => {
  const response = await fetch(`/api/comments/${commentId}/reactions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ emoji })
  });

  return response.json();
};
```

### Load comment thread
```javascript
const loadCommentThread = async (commentId) => {
  const response = await fetch(`/api/comments/${commentId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const data = await response.json();
  return data.data.comment;
};
```