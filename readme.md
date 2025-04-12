# Flask API Base Project

A production-ready Flask API base project with best practices and common features built-in. This project serves as a foundation for building scalable REST APIs with Python and Flask.

## Dependencies

- Python 3.11
- Flask
- PostgreSQL
- Docker & Docker Compose
- psycopg2
- python-dotenv
- PyJWT

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11 (for local development)
- PostgreSQL (if running locally)

### Environment Setup

1. Clone the repository:

2. Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET_KEY=your-secret-key
```

### Running with Docker

1. Build and start the containers:
```bash
docker-compose up -d
```

2. The API will be available at `http://localhost:5050`

### Local Development

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
flask run
```

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Users
- `GET /users/` - List users
- `GET /users/<id>` - Get user details
- `PUT /users/<id>` - Update user
- `DELETE /users/<id>` - Delete user

## Security

- JWT-based authentication
- Environment variable configuration
- Database connection pooling
- Request timeout handling
- Query timeout protection