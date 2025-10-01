# Notifications API

Manage real-time and email notifications for users across the platform.

## Overview

- **Base URL**: `/api/notifications`
- **Authentication**: Required
- **Rate Limiting**: 150 requests per minute
- **Delivery**: In-app, Email, Push, Webhook
- **Real-time**: WebSocket connection available

## Notification Types

- `mention` - User mentioned in comment
- `assignment` - Task assigned to user
- `comment` - New comment on watched item
- `status_change` - Task/project status updated
- `deadline` - Upcoming or overdue deadline
- `approval` - Approval request
- `security_alert` - Security vulnerability detected
- `deployment` - Deployment status change
- `invitation` - Team or project invitation
- `announcement` - System announcement

## Endpoints

### GET /api/notifications

List user notifications.

**Query Parameters:**
- `read` (boolean): Filter by read status
- `type` (string): Filter by notification type
- `priority` (string): Filter by priority (`low`, `medium`, `high`, `urgent`)
- `category` (string): Filter by category
- `startDate` (string): From date (ISO 8601)
- `endDate` (string): To date (ISO 8601)
- `page` (integer): Page number
- `limit` (integer): Items per page (max 100)

**Response:**
```json
{
  "success": true,
  "data": {
    "notifications": [
      {
        "id": "notif_abc123",
        "type": "mention",
        "priority": "medium",
        "title": "Jane Doe mentioned you",
        "message": "Jane mentioned you in a comment on \"Update API docs\"",
        "avatar": "https://avatar.example.com/jane.jpg",
        "actionUrl": "/tasks/task_456#comment-123",
        "actionText": "View comment",
        "metadata": {
          "commentId": "cmt_123",
          "taskId": "task_456",
          "userId": "usr_789"
        },
        "read": false,
        "readAt": null,
        "channels": ["in_app", "email"],
        "createdAt": "2024-03-21T10:00:00Z"
      },
      {
        "id": "notif_def456",
        "type": "assignment",
        "priority": "high",
        "title": "New task assigned",
        "message": "You have been assigned to \"Fix login bug\"",
        "avatar": null,
        "actionUrl": "/tasks/task_789",
        "actionText": "View task",
        "metadata": {
          "taskId": "task_789",
          "assignedBy": "usr_111"
        },
        "read": true,
        "readAt": "2024-03-21T10:05:00Z",
        "channels": ["in_app", "email", "push"],
        "createdAt": "2024-03-21T09:00:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 12,
      "totalItems": 234
    },
    "summary": {
      "unread": 45,
      "urgent": 2
    }
  }
}
```

### GET /api/notifications/unread-count

Get count of unread notifications.

**Response:**
```json
{
  "success": true,
  "data": {
    "count": 45,
    "byPriority": {
      "urgent": 2,
      "high": 8,
      "medium": 20,
      "low": 15
    },
    "byType": {
      "mention": 10,
      "assignment": 5,
      "comment": 15,
      "security_alert": 2
    }
  }
}
```

### GET /api/notifications/:id

Get a specific notification.

**Response:**
```json
{
  "success": true,
  "data": {
    "notification": {
      "id": "notif_abc123",
      "type": "mention",
      "title": "Jane Doe mentioned you",
      "message": "Jane mentioned you in a comment on \"Update API docs\"",
      "actionUrl": "/tasks/task_456#comment-123",
      "metadata": {
        "commentId": "cmt_123",
        "taskId": "task_456",
        "comment": {
          "id": "cmt_123",
          "content": "Hey @john, can you review this?",
          "author": {
            "id": "usr_789",
            "name": "Jane Doe"
          }
        }
      },
      "read": false,
      "createdAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

### PATCH /api/notifications/:id/read

Mark a notification as read.

**Response:**
```json
{
  "success": true,
  "data": {
    "notification": {
      "id": "notif_abc123",
      "read": true,
      "readAt": "2024-03-21T10:30:00Z"
    }
  }
}
```

### PATCH /api/notifications/read-all

Mark all notifications as read.

**Request Body:**
```json
{
  "type": "mention",
  "olderThan": "2024-03-20T00:00:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "markedRead": 45
  }
}
```

### DELETE /api/notifications/:id

Delete a notification.

**Response:**
```json
{
  "success": true,
  "message": "Notification deleted"
}
```

### DELETE /api/notifications

Delete multiple notifications.

**Request Body:**
```json
{
  "ids": ["notif_123", "notif_456"],
  "type": "mention",
  "olderThan": "2024-03-01T00:00:00Z"
}
```

## Notification Preferences

### GET /api/notifications/preferences

Get user notification preferences.

**Response:**
```json
{
  "success": true,
  "data": {
    "preferences": {
      "mention": {
        "in_app": true,
        "email": true,
        "push": true,
        "digest": false
      },
      "assignment": {
        "in_app": true,
        "email": true,
        "push": true,
        "digest": false
      },
      "comment": {
        "in_app": true,
        "email": false,
        "push": false,
        "digest": true
      },
      "security_alert": {
        "in_app": true,
        "email": true,
        "push": true,
        "digest": false
      },
      "digest_schedule": "daily",
      "quiet_hours": {
        "enabled": true,
        "start": "22:00",
        "end": "08:00",
        "timezone": "America/New_York"
      },
      "email_frequency": "immediate"
    }
  }
}
```

### PATCH /api/notifications/preferences

Update notification preferences.

**Request Body:**
```json
{
  "mention": {
    "email": false
  },
  "quiet_hours": {
    "enabled": true,
    "start": "23:00",
    "end": "07:00"
  }
}
```

## Real-time Notifications

### WebSocket Connection

Connect to WebSocket for real-time notifications:

```javascript
const ws = new WebSocket('wss://api.example.com/notifications/stream');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'bearer_token'
  }));
};

ws.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  console.log('New notification:', notification);

  // Display notification in UI
  showNotification(notification);
};
```

**Message Format:**
```json
{
  "type": "notification",
  "data": {
    "id": "notif_abc123",
    "type": "mention",
    "title": "Jane Doe mentioned you",
    "message": "...",
    "priority": "medium"
  }
}
```

## Notification Digest

Users can receive notification digests via email:

- **Immediate**: Real-time email for each notification
- **Hourly**: Batched every hour
- **Daily**: Once per day at preferred time
- **Weekly**: Once per week

### GET /api/notifications/digest/preview

Preview digest email content.

**Response:**
```json
{
  "success": true,
  "data": {
    "digest": {
      "period": "daily",
      "startDate": "2024-03-21T00:00:00Z",
      "endDate": "2024-03-22T00:00:00Z",
      "notifications": [...],
      "summary": {
        "total": 24,
        "byType": {
          "mention": 8,
          "assignment": 4,
          "comment": 12
        }
      }
    }
  }
}
```

## Examples

### Fetch notifications
```javascript
const getNotifications = async (page = 1) => {
  const response = await fetch(`/api/notifications?page=${page}&limit=20`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const data = await response.json();
  return data.data.notifications;
};
```

### Mark as read
```javascript
const markAsRead = async (notificationId) => {
  await fetch(`/api/notifications/${notificationId}/read`, {
    method: 'PATCH',
    headers: { 'Authorization': `Bearer ${token}` }
  });
};
```

### Update preferences
```javascript
const updatePreferences = async (preferences) => {
  const response = await fetch('/api/notifications/preferences', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(preferences)
  });

  return response.json();
};
```

### Subscribe to real-time notifications
```javascript
const subscribeToNotifications = (onNotification) => {
  const ws = new WebSocket('wss://api.example.com/notifications/stream');

  ws.onopen = () => {
    ws.send(JSON.stringify({ type: 'auth', token }));
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'notification') {
      onNotification(data.data);
    }
  };

  return ws;
};
```