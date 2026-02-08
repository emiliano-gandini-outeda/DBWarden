# Configuration

DBWarden is configured through environment variables stored in a `.env` file. This guide covers all configuration options.

## Environment File

DBWarden looks for a `.env` file in the current working directory or any parent directory. This file must contain at minimum the database connection URL.

### Creating the .env File

Create a `.env` file in your project root:

```env
STRATA_SQLALCHEMY_URL=postgresql://user:password@localhost:5432/mydb
```

### .env File Location

DBWarden searches for `.env` in the following order:

1. Current working directory
2. Parent directories (up to the filesystem root)

This allows you to have a single `.env` file at your project root that applies to all subdirectories.

## Required Configuration

### STRATA_SQLALCHEMY_URL

The SQLAlchemy database connection URL. This is the only required configuration variable.

**Format:**

```
STRATA_SQLALCHEMY_URL=dialect+driver://username:password@host:port/database
```

**Examples:**

```env
# PostgreSQL
STRATA_SQLALCHEMY_URL=postgresql://user:password@localhost:5432/mydb

# PostgreSQL with async
STRATA_SQLALCHEMY_URL=postgresql+asyncpg://user:password@localhost:5432/mydb

# MySQL
STRATA_SQLALCHEMY_URL=mysql://user:password@localhost:3306/mydb

# SQLite
STRATA_SQLALCHEMY_URL=sqlite:///./mydb.db

# SQLite in memory
STRATA_SQLALCHEMY_URL=sqlite:///:memory:
```

## Optional Configuration

### STRATA_ASYNC

Enable or disable asynchronous database operations.

| Value | Mode |
|-------|------|
| `true`, `1`, `yes` | Asynchronous |
| `false`, `0`, `no` | Synchronous (default) |

**Example:**

```env
STRATA_ASYNC=true
STRATA_SQLALCHEMY_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
```

### STRATA_MODEL_PATHS

Comma-separated list of paths to directories containing SQLAlchemy models.

**Example:**

```env
STRATA_MODEL_PATHS=models/,app/models/,core/database/models/
```

If not specified, DBWarden will automatically look for `models/` or `model/` directories.

### STRATA_POSTGRES_SCHEMA

PostgreSQL schema to use (PostgreSQL only).

**Example:**

```env
STRATA_POSTGRES_SCHEMA=public
```

## Complete .env Example

```env
# Database Connection
STRATA_SQLALCHEMY_URL=postgresql://myuser:mypassword@localhost:5432/myapp
STRATA_ASYNC=true

# Model Discovery
STRATA_MODEL_PATHS=app/models/,models/

# PostgreSQL Schema
STRATA_POSTGRES_SCHEMA=public
```

## Configuration in Different Environments

### Development Environment

```env
STRATA_SQLALCHEMY_URL=postgresql://dev:dev123@localhost:5432/dev_db
STRATA_ASYNC=false
```

### Staging Environment

```env
STRATA_SQLALCHEMY_URL=postgresql://staging:staging123@staging.example.com:5432/staging_db
STRATA_ASYNC=true
```

### Production Environment

```env
STRATA_SQLALCHEMY_URL=postgresql://prod:securepass@prod.example.com:5432/prod_db
STRATA_ASYNC=true
```

## Configuration Validation

Use the `dbwarden env` command to verify your configuration without exposing sensitive information:

```bash
dbwarden env
```

Output:

```
STRATA_SQLALCHEMY_URL: ***
STRATA_ASYNC: true
STRATA_MODEL_PATHS: models/
STRATA_POSTGRES_SCHEMA: public
```

## Environment Variables Precedence

DBWarden checks environment variables in the following order:

1. System environment variables (highest priority)
2. `.env` file in current directory
3. `.env` file in parent directories

This means you can override `.env` file values with system environment variables if needed.

## Special Characters in Passwords

If your database password contains special characters, URL-encode them:

```env
# Password: p@ss:word/123
STRATA_SQLALCHEMY_URL=postgresql://user:p%40ss%3Aword%2F123@localhost:5432/mydb
```

## Troubleshooting Configuration

### Missing STRATA_SQLALCHEMY_URL

```
Error: STRATA_SQLALCHEMY_URL is required in .env file.
```

Make sure your `.env` file exists and contains the required variable.

### Invalid URL Format

```
Error: Could not parse SQLAlchemy URL
```

Check that your URL follows the correct format: `dialect+driver://username:password@host:port/database`

### Database Connection Failed

```
Error: could not connect to server
```

Verify that:
1. The database server is running
2. The host and port are correct
3. The username and password are valid
4. The database exists

## Best Practices

1. **Never commit `.env` to version control**: Add `.env` to your `.gitignore` file
2. **Use different configurations per environment**: Create `.env.example` as a template
3. **Secure your credentials**: Use secrets management in production
4. **Validate configuration**: Run `dbwarden env` before applying migrations
