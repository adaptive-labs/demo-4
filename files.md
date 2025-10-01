# Files API

Upload, manage, and organize files and attachments across your projects.

## Overview

- **Base URL**: `/api/files`
- **Authentication**: Required
- **Rate Limiting**: 100 requests per minute
- **Max File Size**: 100MB per file
- **Allowed Types**: Images, documents, videos, archives

## File Storage

Files are stored securely in cloud storage with:
- Automatic virus scanning
- Encryption at rest
- CDN distribution for fast delivery
- Automatic thumbnail generation for images
- Preview generation for documents

## Endpoints

### GET /api/files

List all files with filtering options.

**Query Parameters:**
- `projectId` (string): Filter by project
- `taskId` (string): Filter by task
- `type` (string): Filter by file type (`image`, `document`, `video`, `other`)
- `uploadedBy` (string): Filter by uploader user ID
- `search` (string): Search filenames
- `page` (integer): Page number
- `limit` (integer): Items per page (max 100)
- `sort` (string): Sort field (`createdAt`, `size`, `name`)
- `order` (string): Sort order

**Response:**
```json
{
  "success": true,
  "data": {
    "files": [
      {
        "id": "file_abc123",
        "name": "design-mockup.png",
        "originalName": "Website Design Mockup v2.png",
        "mimeType": "image/png",
        "size": 2456789,
        "type": "image",
        "url": "https://cdn.example.com/files/abc123/design-mockup.png",
        "thumbnailUrl": "https://cdn.example.com/thumbs/abc123.jpg",
        "projectId": "proj_123",
        "taskId": "task_456",
        "uploadedBy": {
          "id": "usr_789",
          "name": "Jane Doe"
        },
        "metadata": {
          "width": 1920,
          "height": 1080,
          "format": "PNG"
        },
        "virus Scan": {
          "status": "clean",
          "scannedAt": "2024-03-21T10:05:00Z"
        },
        "createdAt": "2024-03-21T10:00:00Z",
        "expiresAt": null
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 8,
      "totalItems": 156
    },
    "stats": {
      "totalSize": 458963214,
      "totalFiles": 156
    }
  }
}
```

### GET /api/files/:id

Get detailed information about a specific file.

**Path Parameters:**
- `id` (string): File ID

**Response:**
```json
{
  "success": true,
  "data": {
    "file": {
      "id": "file_abc123",
      "name": "design-mockup.png",
      "originalName": "Website Design Mockup v2.png",
      "description": "Homepage design mockup for review",
      "mimeType": "image/png",
      "size": 2456789,
      "type": "image",
      "url": "https://cdn.example.com/files/abc123/design-mockup.png",
      "downloadUrl": "https://cdn.example.com/download/abc123",
      "thumbnailUrl": "https://cdn.example.com/thumbs/abc123.jpg",
      "previewUrl": "https://cdn.example.com/preview/abc123",
      "projectId": "proj_123",
      "taskId": "task_456",
      "uploadedBy": {
        "id": "usr_789",
        "name": "Jane Doe",
        "email": "jane@acme.com"
      },
      "metadata": {
        "width": 1920,
        "height": 1080,
        "format": "PNG",
        "colorSpace": "RGB",
        "dpi": 72
      },
      "virusScan": {
        "status": "clean",
        "scannedAt": "2024-03-21T10:05:00Z",
        "engine": "ClamAV"
      },
      "versions": [
        {
          "version": 1,
          "uploadedAt": "2024-03-21T10:00:00Z",
          "uploadedBy": "usr_789"
        }
      ],
      "permissions": {
        "canView": true,
        "canDownload": true,
        "canDelete": true,
        "canShare": true
      },
      "stats": {
        "downloads": 45,
        "views": 123
      },
      "createdAt": "2024-03-21T10:00:00Z",
      "updatedAt": "2024-03-21T10:00:00Z",
      "expiresAt": null
    }
  }
}
```

### POST /api/files

Upload a new file.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file` (file, required): The file to upload
  - `projectId` (string, optional): Associated project
  - `taskId` (string, optional): Associated task
  - `description` (string, optional): File description
  - `folder` (string, optional): Folder path

**Response:**
```json
{
  "success": true,
  "data": {
    "file": {
      "id": "file_xyz789",
      "name": "document.pdf",
      "size": 1048576,
      "type": "document",
      "url": "https://cdn.example.com/files/xyz789/document.pdf",
      "createdAt": "2024-03-21T11:00:00Z"
    }
  }
}
```

**Status Codes:**
- `201` - File uploaded successfully
- `400` - Invalid file or request
- `413` - File too large
- `415` - Unsupported file type

### PATCH /api/files/:id

Update file metadata.

**Request Body:**
```json
{
  "name": "updated-filename.png",
  "description": "Updated description",
  "folder": "/designs/homepage"
}
```

### DELETE /api/files/:id

Delete a file permanently.

**Response:**
```json
{
  "success": true,
  "message": "File deleted successfully"
}
```

## File Types

Supported file types and MIME types:

### Images
- JPEG/JPG (`image/jpeg`)
- PNG (`image/png`)
- GIF (`image/gif`)
- WebP (`image/webp`)
- SVG (`image/svg+xml`)
- BMP (`image/bmp`)

### Documents
- PDF (`application/pdf`)
- Word (`application/msword`, `.docx`)
- Excel (`application/vnd.ms-excel`, `.xlsx`)
- PowerPoint (`application/vnd.ms-powerpoint`, `.pptx`)
- Text (`text/plain`)
- Markdown (`text/markdown`)

### Archives
- ZIP (`application/zip`)
- RAR (`application/x-rar-compressed`)
- 7z (`application/x-7z-compressed`)
- TAR (`application/x-tar`)

### Videos
- MP4 (`video/mp4`)
- WebM (`video/webm`)
- AVI (`video/x-msvideo`)
- MOV (`video/quicktime`)

### Audio
- MP3 (`audio/mpeg`)
- WAV (`audio/wav`)
- OGG (`audio/ogg`)

## File Operations

### POST /api/files/:id/copy

Create a copy of a file.

**Request Body:**
```json
{
  "projectId": "proj_456",
  "name": "copy-of-file.png"
}
```

### POST /api/files/:id/move

Move file to different project or folder.

**Request Body:**
```json
{
  "projectId": "proj_789",
  "folder": "/archived"
}
```

### POST /api/files/:id/share

Generate a shareable link.

**Request Body:**
```json
{
  "expiresIn": 7,
  "password": "optional-password",
  "allowDownload": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "shareLink": "https://app.example.com/share/abc123xyz",
    "expiresAt": "2024-03-28T11:00:00Z"
  }
}
```

### GET /api/files/:id/versions

Get all versions of a file.

**Response:**
```json
{
  "success": true,
  "data": {
    "versions": [
      {
        "version": 2,
        "size": 2456789,
        "uploadedBy": {
          "id": "usr_789",
          "name": "Jane Doe"
        },
        "uploadedAt": "2024-03-21T14:00:00Z",
        "url": "https://cdn.example.com/files/abc123/v2/file.png"
      },
      {
        "version": 1,
        "size": 2123456,
        "uploadedBy": {
          "id": "usr_789",
          "name": "Jane Doe"
        },
        "uploadedAt": "2024-03-21T10:00:00Z",
        "url": "https://cdn.example.com/files/abc123/v1/file.png"
      }
    ]
  }
}
```

## Bulk Operations

### POST /api/files/bulk-upload

Upload multiple files at once.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Multiple `files[]` fields

**Response:**
```json
{
  "success": true,
  "data": {
    "uploaded": 8,
    "failed": 0,
    "files": [
      {
        "id": "file_001",
        "name": "file1.jpg"
      }
    ]
  }
}
```

### POST /api/files/bulk-delete

Delete multiple files.

**Request Body:**
```json
{
  "fileIds": ["file_001", "file_002", "file_003"]
}
```

### POST /api/files/bulk-move

Move multiple files.

**Request Body:**
```json
{
  "fileIds": ["file_001", "file_002"],
  "projectId": "proj_789",
  "folder": "/archived"
}
```

## Storage Quotas

Storage limits by plan:

- **Free**: 5 GB
- **Pro**: 100 GB
- **Business**: 1 TB
- **Enterprise**: Unlimited

Check usage:

### GET /api/files/storage-usage

**Response:**
```json
{
  "success": true,
  "data": {
    "used": 45896321400,
    "limit": 107374182400,
    "percentage": 42.7,
    "byProject": [
      {
        "projectId": "proj_123",
        "projectName": "Website",
        "used": 12345678900
      }
    ]
  }
}
```

## Security

- All files scanned for viruses on upload
- Encrypted at rest with AES-256
- Encrypted in transit with TLS 1.3
- Access controlled by project permissions
- Automatic expiration for shared links
- Audit logs for all file operations

## Examples

### Upload file with fetch
```javascript
const uploadFile = async (file, projectId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('projectId', projectId);

  const response = await fetch('/api/files', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });

  return response.json();
};
```

### Download file
```javascript
const downloadFile = async (fileId) => {
  const response = await fetch(`/api/files/${fileId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const data = await response.json();
  window.location.href = data.data.file.downloadUrl;
};
```

### Upload progress tracking
```javascript
const uploadWithProgress = (file, onProgress) => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('file', file);

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const progress = (e.loaded / e.total) * 100;
        onProgress(progress);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status === 201) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(new Error(`Upload failed: ${xhr.status}`));
      }
    });

    xhr.open('POST', '/api/files');
    xhr.setRequestHeader('Authorization', `Bearer ${token}`);
    xhr.send(formData);
  });
};
```