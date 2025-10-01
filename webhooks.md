# Webhooks API

Configure webhooks to receive real-time HTTP callbacks when events occur in your workspace.

## Overview

- **Base URL**: `/api/webhooks`
- **Authentication**: Required
- **Rate Limiting**: 100 requests per minute
- **Delivery**: HTTP POST to your endpoint
- **Retry Logic**: 3 attempts with exponential backoff
- **Timeout**: 10 seconds

## Webhook Structure

Webhooks deliver JSON payloads to your configured endpoint:

```json
{
  "id": "evt_abc123",
  "event": "task.created",
  "timestamp": "2024-03-21T10:00:00Z",
  "webhookId": "hook_xyz789",
  "data": {
    "task": {
      "id": "task_456",
      "title": "Fix login bug",
      "status": "open"
    }
  }
}
```

## Security

All webhook requests include:
- **Signature Header**: `X-Webhook-Signature` (HMAC-SHA256)
- **Timestamp Header**: `X-Webhook-Timestamp`
- **ID Header**: `X-Webhook-ID`

Verify signatures to ensure authenticity:
```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const digest = hmac.update(payload).digest('hex');
  return signature === digest;
}
```

## Supported Events

### Task Events
- `task.created` - New task created
- `task.updated` - Task updated
- `task.deleted` - Task deleted
- `task.assigned` - Task assigned to user
- `task.completed` - Task marked complete
- `task.reopened` - Task reopened

### Project Events
- `project.created`
- `project.updated`
- `project.deleted`
- `project.member_added`
- `project.member_removed`

### Comment Events
- `comment.created`
- `comment.updated`
- `comment.deleted`

### File Events
- `file.uploaded`
- `file.deleted`

### Security Events
- `security.alert_created`
- `security.alert_resolved`
- `security.vulnerability_detected`

### User Events
- `user.created`
- `user.updated`
- `user.deleted`

### Organization Events
- `organization.updated`
- `organization.member_added`
- `organization.member_removed`

## Endpoints

### GET /api/webhooks

List all webhooks.

**Query Parameters:**
- `active` (boolean): Filter by active status
- `event` (string): Filter by event type
- `page` (integer): Page number
- `limit` (integer): Items per page

**Response:**
```json
{
  "success": true,
  "data": {
    "webhooks": [
      {
        "id": "hook_xyz789",
        "name": "Production Notifications",
        "url": "https://example.com/webhooks/tasks",
        "events": ["task.created", "task.updated"],
        "active": true,
        "secret": "whsec_abc123...",
        "lastDelivery": {
          "status": "success",
          "timestamp": "2024-03-21T09:45:00Z",
          "responseCode": 200
        },
        "stats": {
          "totalDeliveries": 1234,
          "successRate": 99.2,
          "averageResponseTime": 245
        },
        "createdAt": "2024-01-15T10:00:00Z",
        "updatedAt": "2024-03-21T09:45:00Z"
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

### GET /api/webhooks/:id

Get a specific webhook.

**Response:**
```json
{
  "success": true,
  "data": {
    "webhook": {
      "id": "hook_xyz789",
      "name": "Production Notifications",
      "description": "Webhook for production task updates",
      "url": "https://example.com/webhooks/tasks",
      "events": ["task.created", "task.updated", "task.completed"],
      "active": true,
      "secret": "whsec_abc123...",
      "headers": {
        "X-Custom-Header": "value"
      },
      "filters": {
        "projectId": ["proj_123", "proj_456"]
      },
      "retryConfig": {
        "maxAttempts": 3,
        "backoffMultiplier": 2
      },
      "stats": {
        "totalDeliveries": 1234,
        "successfulDeliveries": 1224,
        "failedDeliveries": 10,
        "successRate": 99.2,
        "averageResponseTime": 245
      },
      "createdBy": {
        "id": "usr_789",
        "name": "Jane Doe"
      },
      "createdAt": "2024-01-15T10:00:00Z"
    }
  }
}
```

### POST /api/webhooks

Create a new webhook.

**Request Body:**
```json
{
  "name": "Production Notifications",
  "description": "Webhook for production task updates",
  "url": "https://example.com/webhooks/tasks",
  "events": ["task.created", "task.updated"],
  "active": true,
  "headers": {
    "X-Custom-Header": "value"
  },
  "filters": {
    "projectId": ["proj_123"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "webhook": {
      "id": "hook_new123",
      "name": "Production Notifications",
      "url": "https://example.com/webhooks/tasks",
      "secret": "whsec_generated_secret_here",
      "createdAt": "2024-03-21T10:00:00Z"
    }
  }
}
```

**Status Codes:**
- `201` - Webhook created
- `400` - Invalid request
- `403` - Insufficient permissions

### PATCH /api/webhooks/:id

Update a webhook.

**Request Body:**
```json
{
  "name": "Updated Name",
  "events": ["task.created", "task.updated", "task.deleted"],
  "active": false
}
```

### DELETE /api/webhooks/:id

Delete a webhook.

**Response:**
```json
{
  "success": true,
  "message": "Webhook deleted successfully"
}
```

## Webhook Deliveries

### GET /api/webhooks/:id/deliveries

Get delivery history for a webhook.

**Query Parameters:**
- `status` (string): Filter by status (`success`, `failed`, `pending`)
- `event` (string): Filter by event type
- `startDate` (string): From date
- `endDate` (string): To date
- `page` (integer): Page number
- `limit` (integer): Items per page

**Response:**
```json
{
  "success": true,
  "data": {
    "deliveries": [
      {
        "id": "del_abc123",
        "event": "task.created",
        "status": "success",
        "attempts": 1,
        "responseCode": 200,
        "responseTime": 245,
        "payload": {
          "id": "evt_xyz",
          "event": "task.created",
          "data": {...}
        },
        "response": {
          "status": 200,
          "body": "{\"success\": true}"
        },
        "createdAt": "2024-03-21T10:00:00Z",
        "deliveredAt": "2024-03-21T10:00:01Z"
      },
      {
        "id": "del_def456",
        "event": "task.updated",
        "status": "failed",
        "attempts": 3,
        "responseCode": 500,
        "responseTime": 10000,
        "error": "Connection timeout",
        "nextRetry": "2024-03-21T10:15:00Z",
        "createdAt": "2024-03-21T10:00:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 45,
      "totalItems": 892
    }
  }
}
```

### GET /api/webhooks/:id/deliveries/:deliveryId

Get details of a specific delivery.

### POST /api/webhooks/:id/deliveries/:deliveryId/retry

Manually retry a failed delivery.

**Response:**
```json
{
  "success": true,
  "data": {
    "delivery": {
      "id": "del_def456",
      "status": "pending",
      "retryScheduledFor": "2024-03-21T10:05:00Z"
    }
  }
}
```

## Testing

### POST /api/webhooks/:id/test

Send a test payload to your webhook endpoint.

**Request Body:**
```json
{
  "event": "task.created"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "delivery": {
      "status": "success",
      "responseCode": 200,
      "responseTime": 234,
      "response": "{\"success\": true}"
    }
  }
}
```

## Examples

### Create webhook
```javascript
const createWebhook = async (config) => {
  const response = await fetch('/api/webhooks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      name: 'My Webhook',
      url: 'https://myapp.com/webhook',
      events: ['task.created', 'task.updated'],
      active: true
    })
  });

  const data = await response.json();
  console.log('Webhook secret:', data.data.webhook.secret);
  return data.data.webhook;
};
```

### Verify webhook signature
```javascript
const express = require('express');
const crypto = require('crypto');

app.post('/webhook', express.raw({type: 'application/json'}), (req, res) => {
  const signature = req.headers['x-webhook-signature'];
  const payload = req.body.toString();

  const hmac = crypto.createHmac('sha256', WEBHOOK_SECRET);
  const digest = hmac.update(payload).digest('hex');

  if (signature !== digest) {
    return res.status(401).send('Invalid signature');
  }

  const event = JSON.parse(payload);
  console.log('Received event:', event.event);

  // Process webhook
  handleWebhook(event);

  res.json({ success: true });
});
```

### List delivery history
```javascript
const getDeliveryHistory = async (webhookId) => {
  const response = await fetch(
    `/api/webhooks/${webhookId}/deliveries?status=failed`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );

  const data = await response.json();
  return data.data.deliveries;
};
```