
# 🧪 Messaging API Postman Testing Guide

This guide documents how to test all major API endpoints for the Django messaging application using **Postman**, including authentication, conversation management, and message access.

---

## 🔐 Authentication Setup

1. **Login** and obtain your access & refresh tokens (JWT):
    - **POST** `/api/token/`
    - **Body (JSON):**
      ```json
      {
        "username": "your_username",
        "password": "your_password"
      }
      ```
    - **Response:**
      ```json
      {
        "access": "your-access-token",
        "refresh": "your-refresh-token"
      }
      ```

2. Use the **Access Token** in every request:
    - In Postman → `Authorization` tab → Bearer Token → paste `access` token.

---

## 👤 Users Endpoint

### 🔹 Get All Users
- **GET** `/api/users/`
- ✅ Requires: Bearer token (authenticated)
- 🔄 Response: List of all users

---

## 💬 Conversations

### 🔹 Get User’s Conversations
- **GET** `/api/conversations/`
- ✅ Requires: Bearer token
- 🔁 Response: All conversations where the user is a participant

### 🔹 Create a New Conversation
- **POST** `/api/conversations/`
- ✅ Requires: Bearer token
- 📥 Body:
  ```json
  {
    "recipient_id": 2
  }
  ```
- 🔁 Response: Created conversation

---

## ✉️ Messages

### 🔹 Get All Messages (User Is a Participant)
- **GET** `/api/messages/`
- ✅ Requires: Bearer token
- 🔄 Optional Query: `?status=read` or `?status=unread`

### 🔹 Send a Message
- **POST** `/api/messages/`
- ✅ Requires: Bearer token
- 📥 Body:
  ```json
  {
    "conversation": "uuid-of-conversation",
    "message_body": "Hello there!"
  }
  ```

---

## ❌ Forbidden Access (403)

- A user will get `403 Forbidden` if:
  - They try to access a conversation or message they are not a participant of.
  - They are not authenticated.

---

## ✅ Success Codes

- `200 OK` – GET requests successful
- `201 Created` – POST success
- `400 Bad Request` – Validation errors (e.g. missing fields)
- `403 Forbidden` – Unauthorized access
- `404 Not Found` – Endpoint or object not found

---

## 🧪 Testing Suggestions

| Action                        | Method | URL                        | Requires Auth | Notes |
|-----------------------------|--------|----------------------------|---------------|-------|
| Get all users               | GET    | `/api/users/`              | ✅            | -     |
| Create conversation         | POST   | `/api/conversations/`      | ✅            | Use `recipient_id` |
| View user conversations     | GET    | `/api/conversations/`      | ✅            | User must be a participant |
| Post message                | POST   | `/api/messages/`           | ✅            | Requires conversation UUID |
| Get messages                | GET    | `/api/messages/`           | ✅            | Can filter by `status` |

---

## 📌 Tip

Use `/api/conversations/` to get the UUIDs for your conversations to test messages.

---
