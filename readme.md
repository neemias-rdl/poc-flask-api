# Flask API Base Project

A production-ready Flask API base project with best practices and common features built-in. This project serves as a foundation for building scalable REST APIs with Python and Flask.

## Features

- Clean Architecture with Domain-Driven Design (DDD)
- JWT Authentication
- PostgreSQL Database Integration
- Docker & Docker Compose Support
- Dependency Injection
- Type Hints
- Repository Pattern
- Service Layer Pattern
- DTOs for Request/Response Handling
- Environment-based Configuration
- Modular Blueprint Structure

## Tech Stack

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

## Project Structure

```
.
├── app.py                 # Application entry point
├── config.py             # Configuration setup
├── controllers/          # API endpoints and request handling
│   ├── dtos/            # Data Transfer Objects
│   └── user/            # User-related controllers
├── data/                # Data layer
│   ├── database/        # Database configuration
│   └── repositories/    # Repository implementations
├── domain/              # Domain layer
│   ├── entities/        # Domain entities
│   └── services/        # Business logic
├── helpers/             # Utility functions and helpers
└── tests/               # Test files
```

## API Endpoints

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

## Testing

Run tests using:
```bash
python -m pytest
```

## Best Practices

This project follows several best practices:
- Clean Architecture principles
- SOLID principles
- Repository pattern for data access
- Service layer for business logic
- DTOs for data transfer
- Environment-based configuration
- Docker for containerization
- Type hints for better code quality

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask documentation
- Clean Architecture by Robert C. Martin
- Domain-Driven Design by Eric Evans
