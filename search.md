# Search API

Global search across all resources with advanced filtering and faceting.

## Overview

- **Base URL**: `/api/search`
- **Authentication**: Required
- **Rate Limiting**: 100 requests per minute
- **Search Engine**: Elasticsearch-powered full-text search
- **Indexing**: Real-time indexing with sub-second latency
- **Features**: Fuzzy matching, highlighting, autocomplete, facets

## Search Types

- **Global**: Search across all resource types
- **Scoped**: Search within specific resource types
- **Autocomplete**: Fast suggestion-based search
- **Advanced**: Complex boolean queries

## Endpoints

### GET /api/search

Global search across all resources.

**Query Parameters:**
- `q` (string, required): Search query
- `type` (string): Filter by resource type
- `projectId` (string): Filter by project
- `userId` (string): Filter by creator/assignee
- `startDate` (string): Filter by date range start
- `endDate` (string): Filter by date range end
- `status` (string): Filter by status
- `labels` (string[]): Filter by labels
- `page` (integer): Page number
- `limit` (integer): Items per page (max 100)
- `highlight` (boolean): Enable result highlighting (default: true)
- `fuzzy` (boolean): Enable fuzzy matching (default: true)

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "login bug",
    "results": [
      {
        "type": "task",
        "id": "task_abc123",
        "score": 0.95,
        "title": "Fix <em>login</em> <em>bug</em> on mobile",
        "description": "Users experiencing <em>login</em> issues...",
        "url": "/tasks/task_abc123",
        "metadata": {
          "projectId": "proj_123",
          "projectName": "Mobile App",
          "status": "open",
          "assignee": {
            "id": "usr_789",
            "name": "Jane Doe"
          },
          "labels": ["bug", "high-priority"],
          "createdAt": "2024-03-20T10:00:00Z"
        },
        "highlights": {
          "title": ["Fix <em>login</em> <em>bug</em> on mobile"],
          "description": ["Users experiencing <em>login</em> issues on iOS devices"]
        }
      },
      {
        "type": "comment",
        "id": "cmt_def456",
        "score": 0.82,
        "content": "This <em>login</em> <em>bug</em> is causing issues...",
        "url": "/tasks/task_456#comment-def456",
        "metadata": {
          "taskId": "task_456",
          "taskTitle": "Authentication refactor",
          "author": {
            "id": "usr_111",
            "name": "John Smith"
          },
          "createdAt": "2024-03-19T15:30:00Z"
        }
      },
      {
        "type": "document",
        "id": "doc_ghi789",
        "score": 0.78,
        "title": "<em>Login</em> Flow Documentation",
        "excerpt": "...troubleshooting <em>login</em> <em>bugs</em> and errors...",
        "url": "/docs/doc_ghi789",
        "metadata": {
          "category": "Authentication",
          "lastUpdated": "2024-03-15T10:00:00Z"
        }
      }
    ],
    "facets": {
      "type": {
        "task": 45,
        "comment": 23,
        "document": 12,
        "project": 5,
        "user": 2
      },
      "project": {
        "proj_123": 34,
        "proj_456": 28,
        "proj_789": 15
      },
      "status": {
        "open": 56,
        "in_progress": 18,
        "closed": 13
      },
      "labels": {
        "bug": 45,
        "high-priority": 23,
        "authentication": 12
      }
    },
    "pagination": {
      "currentPage": 1,
      "totalPages": 9,
      "totalItems": 87
    },
    "searchTime": 45
  }
}
```

### GET /api/search/tasks

Search specifically within tasks.

**Query Parameters:**
Same as global search, plus:
- `assignee` (string): Filter by assignee
- `priority` (string): Filter by priority
- `dueDate` (string): Filter by due date

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "api",
    "results": [
      {
        "id": "task_abc123",
        "score": 0.95,
        "title": "Update <em>API</em> documentation",
        "description": "Add examples to <em>API</em> docs...",
        "projectId": "proj_123",
        "status": "open",
        "assignee": {
          "id": "usr_789",
          "name": "Jane Doe"
        },
        "priority": "high",
        "labels": ["documentation", "api"],
        "dueDate": "2024-03-25T00:00:00Z",
        "createdAt": "2024-03-20T10:00:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 45
    }
  }
}
```

### GET /api/search/projects

Search within projects.

### GET /api/search/documents

Search within documentation.

### GET /api/search/users

Search for users.

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "jane",
    "results": [
      {
        "id": "usr_789",
        "name": "<em>Jane</em> Doe",
        "email": "<em>jane</em>@acme.com",
        "title": "Senior Developer",
        "avatar": "https://avatar.example.com/jane.jpg",
        "teams": ["Platform Team", "Frontend Team"]
      }
    ]
  }
}
```

## Autocomplete

### GET /api/search/autocomplete

Get search suggestions as the user types.

**Query Parameters:**
- `q` (string, required): Partial query
- `type` (string): Filter suggestions by type
- `limit` (integer): Max suggestions (default: 10)

**Response:**
```json
{
  "success": true,
  "data": {
    "suggestions": [
      {
        "text": "login bug",
        "type": "query",
        "count": 45
      },
      {
        "text": "login flow documentation",
        "type": "document",
        "id": "doc_123"
      },
      {
        "text": "Fix login error on iOS",
        "type": "task",
        "id": "task_456"
      }
    ]
  }
}
```

## Advanced Search

### POST /api/search/advanced

Execute complex boolean queries.

**Request Body:**
```json
{
  "query": {
    "must": [
      { "match": { "title": "login" } },
      { "match": { "description": "bug" } }
    ],
    "filter": [
      { "term": { "status": "open" } },
      { "range": { "createdAt": { "gte": "2024-03-01" } } }
    ],
    "must_not": [
      { "term": { "labels": "duplicate" } }
    ]
  },
  "sort": [
    { "createdAt": "desc" },
    { "_score": "desc" }
  ],
  "page": 1,
  "limit": 20
}
```

**Response:**
Similar to global search response with matching results.

## Search Filters

### GET /api/search/filters

Get available filter options for search refinement.

**Response:**
```json
{
  "success": true,
  "data": {
    "filters": {
      "projects": [
        {
          "id": "proj_123",
          "name": "Mobile App",
          "count": 45
        }
      ],
      "users": [
        {
          "id": "usr_789",
          "name": "Jane Doe",
          "count": 34
        }
      ],
      "statuses": [
        { "value": "open", "count": 56 },
        { "value": "in_progress", "count": 18 }
      ],
      "labels": [
        { "id": "lbl_bug", "name": "bug", "count": 45 },
        { "id": "lbl_priority", "name": "high-priority", "count": 23 }
      ],
      "dateRanges": [
        { "label": "Today", "value": "today", "count": 12 },
        { "label": "This week", "value": "week", "count": 34 },
        { "label": "This month", "value": "month", "count": 87 }
      ]
    }
  }
}
```

## Saved Searches

### GET /api/search/saved

Get user's saved searches.

**Response:**
```json
{
  "success": true,
  "data": {
    "searches": [
      {
        "id": "search_abc123",
        "name": "My Open Bugs",
        "query": "login bug",
        "filters": {
          "type": "task",
          "status": "open",
          "assignee": "usr_789",
          "labels": ["bug"]
        },
        "notificationsEnabled": true,
        "createdAt": "2024-03-15T10:00:00Z"
      }
    ]
  }
}
```

### POST /api/search/saved

Save a search.

**Request Body:**
```json
{
  "name": "My Open Bugs",
  "query": "login bug",
  "filters": {
    "type": "task",
    "status": "open",
    "assignee": "me"
  },
  "notificationsEnabled": true
}
```

### DELETE /api/search/saved/:id

Delete a saved search.

## Search Analytics

### GET /api/search/analytics

Get search analytics and trending queries.

**Response:**
```json
{
  "success": true,
  "data": {
    "trending": [
      { "query": "login bug", "count": 45, "growth": 23.5 },
      { "query": "api documentation", "count": 34, "growth": 12.3 }
    ],
    "popular": [
      { "query": "authentication", "count": 234 },
      { "query": "deployment", "count": 189 }
    ],
    "noResults": [
      { "query": "xyz feature", "count": 12 },
      { "query": "old api", "count": 8 }
    ]
  }
}
```

## Examples

### Basic search
```javascript
const search = async (query) => {
  const response = await fetch(
    `/api/search?q=${encodeURIComponent(query)}&limit=20`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );

  const data = await response.json();
  return data.data.results;
};
```

### Search with filters
```javascript
const searchWithFilters = async (query, filters) => {
  const params = new URLSearchParams({
    q: query,
    type: filters.type,
    projectId: filters.projectId,
    status: filters.status
  });

  const response = await fetch(`/api/search?${params}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  return response.json();
};
```

### Autocomplete
```javascript
const autocomplete = async (query) => {
  const response = await fetch(
    `/api/search/autocomplete?q=${encodeURIComponent(query)}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );

  const data = await response.json();
  return data.data.suggestions;
};
```

### Save search
```javascript
const saveSearch = async (name, query, filters) => {
  const response = await fetch('/api/search/saved', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      name,
      query,
      filters,
      notificationsEnabled: true
    })
  });

  return response.json();
};
```