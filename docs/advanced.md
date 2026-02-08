# Advanced Features

This guide covers advanced DBWarden features and techniques for complex migration scenarios.

## Migration Locking

DBWarden uses a locking mechanism to prevent concurrent migration execution.

### Automatic Locking

Locks are automatically acquired and released during:
- `migrate`
- `rollback`

### Manual Lock Management

Check lock status:
```bash
dbwarden lock-status
```

Force unlock (emergency):
```bash
dbwarden unlock
```

### Lock Implementation

```sql
-- strata_lock table
CREATE TABLE strata_lock (
    id INTEGER PRIMARY KEY,
    locked BOOLEAN DEFAULT FALSE,
    acquired_at DATETIME,
    release_at DATETIME
);
```

## Checksum Validation

DBWarden validates migration integrity using checksums.

### How It Works

1. **Before execution**: Calculate checksum of migration file
2. **After execution**: Store checksum in database
3. **Future runs**: Verify checksum matches stored value

### Checksum Algorithm

Uses SHA-256 hash of SQL statements:

```python
import hashlib

def calculate_checksum(sql_statements):
    content = "".join(sql_statements)
    return hashlib.sha256(content.encode()).hexdigest()
```

### Validation

On migration run:
```python
stored_checksum = get_stored_checksum()
current_checksum = calculate_checksum(sql_statements)

if stored_checksum != current_checksum:
    raise MigrationChecksumError("Migration file has been modified!")
```

## Squash Migrations

Combine multiple migrations into one.

### When to Squash

- After 10+ small migrations
- Before major releases
- During maintenance windows

### Process

```bash
# 1. Ensure all migrations applied
dbwarden migrate

# 2. Squash migrations
dbwarden squash

# 3. New migration created
ls migrations/
# V20240215_143000__initial_schema.sql  (consolidated)
```

### Before/After

**Before:**
```
V20240215_143000__create_users.sql
V20240215_143001__add_email.sql
V20240215_143002__add_username.sql
V20240215_143003__add_password.sql
V20240215_143004__add_bio.sql
```

**After:**
```
V20240215_143000__initial_schema.sql
```

### Manual Squash

For more control:

```bash
# 1. Create new migration
dbwarden new "consolidate user migrations"

# 2. Edit file, combine SQL from all migrations
```

## Custom Model Paths

Configure multiple model directories.

### Configuration

```env
STRATA_MODEL_PATHS=models/,app/models/,core/database/models/
```

### Priority

Paths are processed in order:
1. First path's models processed first
2. Duplicate tables (same `__tablename__`) are skipped after first occurrence

## PostgreSQL Schema Support

### Configuration

```env
STRATA_POSTGRES_SCHEMA=my_schema
```

### Usage

All migrations run in specified schema:
```sql
CREATE TABLE my_schema.users (... Multiple Schemas

For multiple);
```

### schemas, use fully qualified names in migrations:

```sql
-- upgrade

CREATE TABLE analytics.events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200)
);

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255)
);

-- rollback

DROP TABLE public.users;
DROP TABLE analytics.events;
```

## Transactions in Migrations

### Basic Transaction

```sql
-- upgrade

BEGIN;

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    total DECIMAL(10, 2)
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id)
);

COMMIT;

-- rollback

BEGIN;

DROP TABLE order_items;
DROP TABLE orders;

COMMIT;
```

### Complex Migration Pattern

```sql
-- upgrade

-- Step 1: Create new table with new structure
CREATE TABLE posts_new (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    slug VARCHAR(200) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Copy data with transformation
INSERT INTO posts_new (id, author_id, title, content, slug, created_at)
SELECT 
    id, 
    user_id, 
    title, 
    content, 
    LOWER(REPLACE(title, ' ', '-')),
    created_at
FROM posts;

-- Step 3: Drop old table
DROP TABLE posts;

-- Step 4: Rename new table
ALTER TABLE posts_new RENAME TO posts;

-- rollback

-- Reverse all steps
CREATE TABLE posts_old (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO posts_old (id, user_id, title, content, created_at)
SELECT id, author_id, title, content, created_at FROM posts;

DROP TABLE posts;

ALTER TABLE posts_old RENAME TO posts;
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Database Migrations

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      target:
        description: 'Target version to migrate to'
        required: false

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install DBWarden
        run: |
          pip install dbwarden
      
      - name: Run Migrations
        run: |
          if [ "${{ github.event.inputs.target }}" ]; then
            dbwarden migrate --to-version ${{ github.event.inputs.target }}
          else
            dbwarden migrate --verbose
          fi
        env:
          STRATA_SQLALCHEMY_URL: ${{ secrets.DATABASE_URL }}
          STRATA_ASYNC: ${{ secrets.STRATA_ASYNC || 'false' }}
```

### GitLab CI

```yaml
stages:
  - migrate

migrate:
  stage: migrate
  image: python:3.11
  script:
    - pip install dbwarden
    - dbwarden migrate --verbose
  variables:
    STRATA_SQLALCHEMY_URL: $DATABASE_URL
  only:
    - main
```

### Docker Integration

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install dbwarden

# Run migrations on container start
CMD ["sh", "-c", "dbwarden migrate && your_app"]
```

### Kubernetes

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: dbwarden-migrate
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: your-app:latest
        command: ["dbwarden", "migrate", "--verbose"]
        env:
        - name: STRATA_SQLALCHEMY_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
      restartPolicy: OnFailure
```

## Environment-Specific Migrations

### Using Migration Tags

```sql
-- V20240215_143000__base_schema.sql (always run)

-- upgrade
CREATE TABLE users (id INT PRIMARY KEY, email VARCHAR(255));
-- rollback
DROP TABLE users;
```

```sql
-- V20240215_143001__demo_data.sql (demo only)

-- upgrade
INSERT INTO users (email) VALUES ('demo@example.com');
-- rollback
DELETE FROM users WHERE email = 'demo@example.com';
```

### Programmatic Execution

```python
from dbwarden.config import get_config
from dbwarden.commands.migrate import migrate_cmd

# Apply migrations with target version
migrate_cmd(to_version="20240215_143000", verbose=True)
```

## Performance Optimization

### Batch Migrations

For many small migrations:

```bash
# Apply all pending
dbwarden migrate

# Or apply specific number
dbwarden migrate --count 10
```

### Parallel Checks (Future)

Currently migrations run sequentially for safety.

## Migration Recovery

### After Failed Migration

1. Check lock status
2. Unlock if necessary
3. Verify database state
4. Fix migration file
5. Re-apply

```bash
dbwarden lock-status
dbwarden unlock  # if locked
dbwarden history
dbwarden status
# Fix migration file
dbwarden migrate
```

### Manual State Correction

In emergencies, manually update migration records:

```sql
-- Remove last migration record
DELETE FROM strata_migrations 
WHERE version = '20240215_143000'
ORDER BY applied_at DESC 
LIMIT 1;
```

## Best Practices Summary

| Practice | Description |
|----------|-------------|
| **Idempotent migrations** | Safe to run multiple times |
| **Include rollback** | Always have a rollback plan |
| **Test migrations** | On staging before production |
| **Backup first** | Especially in production |
| **Version control** | Commit migration files |
| **Review SQL** | Before applying |
| **Document complex migrations** | Comment your SQL |
| **Use transactions** | For multi-step changes |

## Common Patterns

### Pattern 1: Safe Column Addition

```sql
-- upgrade
ALTER TABLE users ADD COLUMN bio TEXT;
UPDATE users SET bio = '' WHERE bio IS NULL;
ALTER TABLE users ALTER COLUMN bio SET NOT NULL;

-- rollback
ALTER TABLE users ALTER COLUMN bio DROP NOT NULL;
ALTER TABLE users DROP COLUMN bio;
```

### Pattern 2: Safe Data Migration

```sql
-- upgrade
ALTER TABLE users ADD COLUMN new_email VARCHAR(255);

UPDATE users SET new_email = email;

-- AFTER VERIFICATION:
-- ALTER TABLE users DROP COLUMN email;
-- ALTER TABLE users RENAME COLUMN new_email TO email;
```

### Pattern 3: Version-Based Feature Flags

```sql
-- upgrade
CREATE TABLE feature_flags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    enabled BOOLEAN DEFAULT FALSE
);

INSERT INTO feature_flags (name, enabled) VALUES ('new_checkout', FALSE);

-- rollback
DROP TABLE feature_flags;
```

## See Also

- [Commands](commands.md): All command reference
- [Migration Files](migration-files.md): Writing advanced migrations
- [Models](models.md): Advanced model patterns
