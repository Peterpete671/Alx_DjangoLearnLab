## Posts Endpoints

### 1. List All Posts

**Endpoint:** `GET /api/posts/`

**Description:** Retrieve a paginated list of all posts.

**Authentication:** Not required (read-only)

**Query Parameters:**

- `page` - Page number (default: 1)
- `page_size` - Results per page (default: 10)
- `search` - Search in title and content
- `ordering` - Order by field (e.g., `-created_at`, `title`)

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?page=1&search=django"
```

**Example Response (200 OK):**

```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": {
        "id": 1,
        "username": "johndoe",
        "profile_picture": null
      },
      "title": "Getting Started with Django",
      "content": "Django is a powerful web framework...",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "comments_count": 5
    }
  ]
}
```

---

### 2. Retrieve a Single Post

**Endpoint:** `GET /api/posts/{id}/`

**Description:** Retrieve detailed information about a specific post including all comments.

**Authentication:** Not required (read-only)

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/api/posts/1/"
```

**Example Response (200 OK):**

```json
{
  "id": 1,
  "author": {
    "id": 1,
    "username": "johndoe",
    "profile_picture": null
  },
  "title": "Getting Started with Django",
  "content": "Django is a powerful web framework for building web applications...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "comments": [
    {
      "id": 1,
      "post": 1,
      "author": {
        "id": 2,
        "username": "janedoe",
        "profile_picture": null
      },
      "content": "Great post! Very helpful.",
      "created_at": "2024-01-15T11:00:00Z",
      "updated_at": "2024-01-15T11:00:00Z"
    }
  ],
  "comments_count": 1
}
```

---

### 3. Create a New Post

**Endpoint:** `POST /api/posts/`

**Description:** Create a new post.

**Authentication:** Required (Token)

**Headers:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "My New Post",
  "content": "This is the content of my new post."
}
```

**Example Request:**

```bash
curl -X POST "http://127.0.0.1:8000/api/posts/" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Post",
    "content": "This is the content of my new post."
  }'
```

**Example Response (201 Created):**

```json
{
  "message": "Post created successfully",
  "post": {
    "id": 2,
    "author": {
      "id": 1,
      "username": "johndoe",
      "profile_picture": null
    },
    "title": "My New Post",
    "content": "This is the content of my new post.",
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-15T14:30:00Z",
    "comments": [],
    "comments_count": 0
  }
}
```

**Validation Errors (400 Bad Request):**

```json
{
  "title": ["This field is required."],
  "content": ["Content cannot be empty."]
}
```

---

### 4. Update a Post (Full Update)

**Endpoint:** `PUT /api/posts/{id}/`

**Description:** Fully update a post (all fields required).

**Authentication:** Required (Token, must be post author)

**Headers:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "Updated Post Title",
  "content": "Updated post content."
}
```

**Example Response (200 OK):**

```json
{
  "message": "Post updated successfully",
  "post": {
    "id": 2,
    "author": {
      "id": 1,
      "username": "johndoe",
      "profile_picture": null
    },
    "title": "Updated Post Title",
    "content": "Updated post content.",
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-15T15:00:00Z",
    "comments": [],
    "comments_count": 0
  }
}
```

---

### 5. Update a Post (Partial Update)

**Endpoint:** `PATCH /api/posts/{id}/`

**Description:** Partially update a post (only specified fields).

**Authentication:** Required (Token, must be post author)

**Headers:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "New Title Only"
}
```

**Example Request:**

```bash
curl -X PATCH "http://127.0.0.1:8000/api/posts/2/" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title Only"}'
```

**Example Response (200 OK):**

```json
{
  "message": "Post updated successfully",
  "post": {
    "id": 2,
    "author": {
      "id": 1,
      "username": "johndoe",
      "profile_picture": null
    },
    "title": "New Title Only",
    "content": "Updated post content.",
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-15T15:30:00Z",
    "comments": [],
    "comments_count": 0
  }
}
```

---

### 6. Delete a Post

**Endpoint:** `DELETE /api/posts/{id}/`

**Description:** Delete a post (also deletes all associated comments).

**Authentication:** Required (Token, must be post author)

**Headers:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Example Request:**

```bash
curl -X DELETE "http://127.0.0.1:8000/api/posts/2/" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Example Response (204 No Content):**

```json
{
  "message": "Post deleted successfully"
}
```

---

### 7. Get Post Comments

**Endpoint:** `GET /api/posts/{id}/comments/`

**Description:** Retrieve all comments for a specific post.

**Authentication:** Not required

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/api/posts/1/comments/"
```

**Example Response (200 OK):**

```json
[
  {
    "id": 1,
    "post": 1,
    "author": {
      "id": 2,
      "username": "janedoe",
      "profile_picture": null
    },
    "content": "Great post!",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  },
  {
    "id": 2,
    "post": 1,
    "author": {
      "id": 3,
      "username": "bobsmith",
      "profile_picture": null
    },
    "content": "Very informative, thanks!",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  }
]
```

---

## Comments Endpoints

### 1. List All Comments

**Endpoint:** `GET /api/comments/`

**Description:** Retrieve a paginated list of all comments.

**Authentication:** Not required (read-only)

**Query Parameters:**

- `page` - Page number
- `post` - Filter by post ID
- `author` - Filter by author ID
- `search` - Search in content
- `ordering` - Order by field

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/api/comments/?post=1"
```

**Example Response (200 OK):**

```json
{
  "count": 15,
  "next": "http://127.0.0.1:8000/api/comments/?page=2&post=1",
  "previous": null,
  "results": [
    {
      "id": 1,
      "post": 1,
      "author": {
        "id": 2,
        "username": "janedoe",
        "profile_picture": null
      },
      "content": "Great post!",
      "created_at": "2024-01-15T11:00:00Z",
      "updated_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

---

### 2. Retrieve a Single Comment

**Endpoint:** `GET /api/comments/{id}/`

**Description:** Retrieve detailed information about a specific comment.

**Authentication:** Not required

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/api/comments/1/"
```

**Example Response (200 OK):**

```json
{
  "id": 1,
  "post": 1,
  "author": {
    "id": 2,
    "username": "janedoe",
    "profile_picture": null
  },
  "content": "Great post!",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

---

### 3. Create a New Comment

**Endpoint:** `POST /api/comments/`

**Description:** Create a new comment on a post.

**Authentication:** Required (Token)

**Headers:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```

**Request Body:**

```json
{
  "post": 1,
  "content": "This is my comment on the post."
}
```

**Example Request:**

```bash
curl -X POST "http://127.0.0.1:8000/api/comments/" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "This is my comment on the post."
  }'
```

**Example Response (201 Created):**

```json
{
  "message": "Comment created successfully",
  "comment": {
    "id": 3,
    "post": 1,
    "author": {
      "id": 1,
      "username": "johndoe",
      "profile_picture": null
    },
    "content": "This is my comment on the post.",
    "created_at": "2024-01-15T16:00:00Z",
    "updated_at": "2024-01-15T16:00:00Z"
  }
}
```

---

### 4. Update a Comment

**Endpoint:** `PATCH /api/comments/{id}/`

**Description:** Update a comment (author only).

**Authentication:** Required (Token, must be comment author)

**Headers:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```

**Request Body:**

```json
{
  "content": "Updated comment content."
}
```

**Example Request:**

```bash
curl -X PATCH "http://127.0.0.1:8000/api/comments/3/" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated comment content."}'
```

**Example Response (200 OK):**

```json
{
  "message": "Comment updated successfully",
  "comment": {
    "id": 3,
    "post": 1,
    "author": {
      "id": 1,
      "username": "johndoe",
      "profile_picture": null
    },
    "content": "Updated comment content.",
    "created_at": "2024-01-15T16:00:00Z",
    "updated_at": "2024-01-15T16:30:00Z"
  }
}
```

---

### 5. Delete a Comment

**Endpoint:** `DELETE /api/comments/{id}/`

**Description:** Delete a comment (author only).

**Authentication:** Required (Token, must be comment author)

**Headers:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Example Request:**

```bash
curl -X DELETE "http://127.0.0.1:8000/api/comments/3/" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Example Response (204 No Content):**

```json
{
  "message": "Comment deleted successfully"
}
```

---

## Filtering and Search

### Search Posts

Search posts by title or content:

```bash
GET /api/posts/?search=django
```

### Filter Comments by Post

Get all comments for a specific post:

```bash
GET /api/comments/?post=1
```

### Filter Comments by Author

Get all comments by a specific author:

```bash
GET /api/comments/?author=2
```

### Ordering

Order results by any field (use `-` prefix for descending):

```bash
GET /api/posts/?ordering=-created_at
GET /api/posts/?ordering=title
GET /api/comments/?ordering=-created_at
```

### Combined Filtering

Combine multiple filters:

```bash
GET /api/posts/?search=python&ordering=-created_at
GET /api/comments/?post=1&ordering=created_at
```

---

## Pagination

All list endpoints support pagination with the following parameters:

- `page` - Page number (starts at 1)
- `page_size` - Number of results per page (default: 10, max: 100)

**Example:**

```bash
GET /api/posts/?page=2&page_size=20
```

**Response Structure:**

```json
{
    "count": 45,
    "next": "http://127.0.0.1:8000/api/posts/?page=3&page_size=20",
    "previous": "http://127.0.0.1:8000/api/posts/?page=1&page_size=20",
    "results": [...]
}
```

---

## Permissions

### Post Permissions

- **List/Retrieve**: Anyone (no authentication required)
- **Create**: Authenticated users only
- **Update**: Post author only
- **Delete**: Post author only

### Comment Permissions

- **List/Retrieve**: Anyone (no authentication required)
- **Create**: Authenticated users only
- **Update**: Comment author only
- **Delete**: Comment author only

---

## Error Responses

### 400 Bad Request

Invalid data submitted:

```json
{
  "title": ["This field is required."],
  "content": ["Content cannot be empty."]
}
```

### 401 Unauthorized

Missing or invalid authentication token:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

Attempting to modify someone else's content:

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

Resource doesn't exist:

```json
{
  "detail": "Not found."
}
```

---

## Complete Postman Collection Example

### Environment Variables

Create an environment with:

- `base_url`: `http://127.0.0.1:8000`
- `auth_token`: Your authentication token

### Collection Structure

1. **Authentication**

   - Register User
   - Login User
   - Get Profile

2. **Posts**

   - List All Posts
   - Get Single Post
   - Create Post
   - Update Post
   - Delete Post
   - Get Post Comments
   - Search Posts

3. **Comments**
   - List All Comments
   - Get Single Comment
   - Create Comment
   - Update Comment
   - Delete Comment
   - Filter Comments by Post

---

## Testing Checklist

- [ ] Create a post as authenticated user
- [ ] Try to create a post without authentication (should fail)
- [ ] Update own post
- [ ] Try to update another user's post (should fail)
- [ ] Delete own post
- [ ] Try to delete another user's post (should fail)
- [ ] Search posts by keyword
- [ ] Filter posts with pagination
- [ ] Create a comment on a post
- [ ] Update own comment
- [ ] Try to update another user's comment (should fail)
- [ ] Delete own comment
- [ ] Get all comments for a specific post
- [ ] Filter comments by author

### Follow / Unfollow

- **POST** `/api/accounts/follow/<user_id>/` — follow user with `id=user_id`. Auth required.
- **POST** `/api/accounts/unfollow/<user_id>/` — unfollow user with `id=user_id`. Auth required.
- **GET** `/api/accounts/following/?user_id=<id>` — list users followed by the requested user (defaults to current user).
- **GET** `/api/accounts/followers/?user_id=<id>` — list followers of the requested user (defaults to current user).

### Feed

- **GET** `/api/posts/feed/` — returns posts created by users the current user follows, ordered by `created_at` descending.
