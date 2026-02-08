# Supported Databases

DBWarden supports multiple database backends. This guide covers configuration and considerations for each.

## Overview

| Database | Sync Mode | Async Mode | Driver Required |
|----------|-----------|------------|-----------------|
| PostgreSQL | Yes | Yes | `psycopg2-binary` (sync) / `asyncpg` (async) |
| MySQL | Yes | No | `mysql-connector-python` |
| SQLite | Yes | Yes | Built-in / `aiosqlite` (async) |

## PostgreSQL

### Connection URL

```env
STRATA_SQLALCHEMY_URL=postgresql://user:password@localhost:5432/mydb
```

### Sync Mode

```env
STRATA_ASYNC=false
STRATA_SQLALCHEMY_URL=postgresql://user:password@localhost:5432/mydb
```

**Requirements:**
```bash
pip install psycopg2-binary
```

### Async Mode

```env
STRATA_ASYNC=true
STRATA_SQLALCHEMY_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
```

**Requirements:**
```bash
pip install asyncpg
```

### Features

- Full support for all PostgreSQL features
- UUID types
- JSON/JSONB columns
- Array types (via manual migration)
- Full-text search (via manual migration)
- PostgreSQL-specific constraints

### PostgreSQL Schema

Set default schema:

```env
STRATA_POSTGRES_SCHEMA=public  # default
# or
STRATA_POSTGRES_SCHEMA=custom_schema
```

### Example PostgreSQL Migration

```sql
-- upgrade

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_ossp_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- rollback

DROP INDEX idx_users_email;
DROP TABLE users;
```

## MySQL

### Connection URL

```env
STRATA_SQLALCHEMY_URL=mysql://user:password@localhost:3306/mydb
```

### Sync Mode Only

MySQL does not support asynchronous connections in DBWarden.

```env
STRATA_ASYNC=false
```

**Requirements:**
```bash
pip install mysql-connector-python
```

### Features

- Full support for MySQL features
- ENUM types
- SET types
- Full-text indexes (MyISAM, InnoDB 5.6+)
- AUTO_INCREMENT

### Limitations

- No async mode
- Some PostgreSQL-specific types not available
- Different default string lengths

### Example MySQL Migration

```sql
-- upgrade

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    status ENUM('active', 'inactive', 'pending') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_users_email ON users(email);

-- rollback

DROP INDEX idx_users_email;
DROP TABLE users;
```

## SQLite

### Connection URL

```env
# File-based
STRATA_SQLALCHEMY_URL=sqlite:///./mydb.db

# In-memory
STRATA_SQLALCHEMY_URL=sqlite:///:memory:
```

### Sync Mode (Default)

```env
STRATA_ASYNC=false
```

No additional drivers needed.

### Async Mode

```env
STRATA_ASYNC=true
STRATA_SQLALCHEMY_URL=sqlite+aiosqlite:///./mydb.db
```

**Requirements:**
```bash
pip install aiosqlite
```

### Features

- Simple file-based database
- Zero configuration
- Good for development/testing
- Full SQLite feature support

### Limitations

- No concurrent connections (file-based)
- Limited ALTER TABLE support
- Different type system (type affinity)

### Example SQLite Migration

```sql
-- upgrade

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- rollback

DROP TABLE users;
```

## Connection Pooling

### Sync Mode

SQLAlchemy creates an engine with connection pool:

```python
from sqlalchemy import create_engine
engine = create_engine(url, pool_size=5, max_overflow=10)
```

### Async Mode

Async connection handling:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
```

## SSL/TLS Connections

### PostgreSQL with SSL

```env
STRATA_SQLALCHEMY_URL=postgresql://user:password@host:5432/db?sslmode=require
```

### MySQL with SSL

```env
STRATA_SQLALCHEMY_URL=mysql://user:password@host:3306/db?ssl=true
```

## Connection Strings Reference

### PostgreSQL

```
postgresql://user:pass@localhost:5432/mydb
postgresql+asyncpg://user:pass@localhost:5432/mydb
postgresql://user:pass@host:5432/mydb?sslmode=require
postgresql://user:pass@host:5432/mydb?channel_binding=require
```

### MySQL

```
mysql://user:pass@localhost:3306/mydb
mysql+pymysql://user:pass@localhost:3306/mydb
mysql+mysqlconnector://user:pass@localhost:3306/mydb
```

### SQLite

```
sqlite:///./mydb.db           # Relative path
sqlite:////absolute/path.db   # Absolute path
sqlite:///:memory:            # In-memory
sqlite+aiosqlite:///./mydb.db # Async
```

## Database-Specific SQL

### PostgreSQL

```sql
-- Create UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Use current timestamp with timezone
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
```

### MySQL

```sql
-- AUTO_INCREMENT
id INT AUTO_INCREMENT PRIMARY KEY

-- ENUM type
status ENUM('active', 'inactive')
```

### SQLite

```sql
-- AUTOINCREMENT
id INTEGER PRIMARY KEY AUTOINCREMENT

-- No boolean, use integer
is_active INTEGER DEFAULT 1
```

## Testing Different Databases

### Development (SQLite)

```env
STRATA_SQLALCHEMY_URL=sqlite:///./dev.db
STRATA_ASYNC=false
```

### Staging (PostgreSQL)

```env
STRATA_SQLALCHEMY_URL=postgresql://user:pass@staging.example.com:5432/staging_db
STRATA_ASYNC=true
```

### Production (PostgreSQL)

```env
STRATA_SQLALCHEMY_URL=postgresql://user:pass@prod.example.com:5432/prod_db
STRATA_ASYNC=true
```

## Best Practices

### 1. Match Development and Production

Use same database in development as production when possible.

### 2. Test Migrations on All Databases

If supporting multiple databases:
1. Test PostgreSQL migrations on PostgreSQL
2. Test MySQL migrations on MySQL
3. Test SQLite migrations on SQLite

### 3. Use Database-Agnostic Types

```python
# GOOD: Database-agnostic
from sqlalchemy import Integer, String, DateTime

# LESS PORTABLE: Database-specific
from sqlalchemy.dialects.postgresql import UUID
```

### 4. Handle Edge Cases

```sql
-- PostgreSQL: Create extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- MySQL: Safe drop
DROP TABLE IF EXISTS users;

-- SQLite: Limited ALTER TABLE
-- Use CREATE TABLE + COPY + DROP pattern
```

## Troubleshooting

### Connection Refused

1. Check database is running
2. Verify host and port
3. Check credentials
4. Test with direct client:

```bash
psql $DATABASE_URL
mysql -u $USER -p $DATABASE
```

### Driver Not Found

```bash
# PostgreSQL sync
pip install psycopg2-binary

# PostgreSQL async
pip install asyncpg

# MySQL
pip install mysql-connector-python

# SQLite async
pip install aiosqlite
```

### SSL/TLS Errors

1. Check SSL mode in connection string
2. Verify SSL certificates
3. Try `sslmode=prefer` for testing

## See Also

- [Configuration](configuration.md): Environment variables
- [Migration Files](migration-files.md): Writing database-specific SQL
- [Models](models.md): Defining models for each database
