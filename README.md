# RESTful API with FastAPI, SQLAlchemy and MySQL

This repository implements a RESTful service with elemental **CRUD** operations. The idea behind this repository is to be able to create users and let them create posts, this is achieved using two entities:

- Users

  | Fields     |
  |------------|
  | id         |
  | email      |
  | password   |
  | created_at |
- Posts

  | Fields     |
  |------------|
  | id         |
  | title      |
  | content    |
  | published  |
  | created_at |
  | user_id    |

These entities are related with a One-To-Many realtionship, where one user can have many posts but each posts can only be owned by one user.

The operations per entity are:

- Users:
  - Create user
  - Get user (this one is not used just yet)
- Posts:
  - Create posts
  - Get my posts (Pagination is configured)
  - Get all posts (This endpoinst is not exactly protected)
  - Get post by ID
  - Update post
  - Delete post
- Auth:
  - Login

This API is protected with the Oauth2 specification that comes implemented with FastApi and accondinly to its documentation works thorugh dependency injection.

Some of the plus features you can find here are:

- Password hashing
- JWT (Generation and validation)
- Functional login
- Pagination (When looking for personal posts keywords can be used)
- Schemas for incoming requests bodies validation
- Schemas for responses
- HTTP status and exceptions implemented
- DB models
- Environment variables verification with pydantic

Even though this API has a considerable amount of features it is incomplete, yet it is fully functional at this point.

Update, a voting system so express agreement with a posts has been implemented. This was made through a many to many relationship.
