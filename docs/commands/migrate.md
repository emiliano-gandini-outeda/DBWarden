# migrate Command

Apply pending migrations to the database.

## Description

The `migrate` command executes all pending migration files, updating the database schema to match your current migration state.

## Usage

```bash
dbwarden migrate
```

## Options

| Option | Description |
|--------|-------------|
| `--count`, `-c` | Number of migrations to apply |
| `--to-version`, `-t` | Migrate to a specific version |
| `--verbose`, `-v` | Enable verbose logging |

## Examples

### Apply All Pending Migrations

```bash
dbwarden migrate
```

### Apply with Verbose Output

```bash
dbwarden migrate --verbose
```

### Apply Specific Number of Migrations

```bash
# Apply next 2 migrations
dbwarden migrate --count 2
```

### Migrate to Specific Version

```bash
dbwarden migrate --to-version 20240215_143000
```

## How It Works

1. **Creates migrations tracking table**: Creates `dbwarden_migrations` table if it doesn't exist
2. **Creates lock table**: Creates `dbwarden_lock` table for concurrency control
3. **Finds pending migrations**: Identifies migrations not yet applied
4. **Applies migrations**: Executes each migration in order
5. **Records execution**: Stores migration metadata in database

## Internal Process

```
┌─────────────────────────────────────────────────────────┐
│  1. Create dbwarden_migrations table (if not exists)  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  2. Create dbwarden_lock table (if not exists)        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  3. Acquire migration lock                             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  4. Find pending migrations                             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  5. Parse migration files (upgrade statements)         │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  6. Execute SQL statements                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  7. Record migration in database                         │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  8. Release lock                                         │
└─────────────────────────────────────────────────────────┘
```

## Migrations Tracking Table

DBWarden creates a `dbwarden_migrations` table to track applied migrations:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Auto-increment ID |
| `version` | VARCHAR | Migration version |
| `description` | VARCHAR | Migration description |
| `filename` | VARCHAR | Migration filename |
| `migration_type` | VARCHAR | Type (versioned) |
| `checksum` | VARCHAR | File checksum for validation |
| `applied_at` | DATETIME | Timestamp of application |

## Locking Mechanism

DBWarden uses a locking mechanism to prevent concurrent migration execution:

- **Automatic lock acquisition**: Lock is acquired before any migration
- **Lock release**: Lock is released after completion or error
- **Lock timeout**: Prevents stale locks

### Checking Lock Status

```bash
dbwarden lock-status
```

### Force Unlock (Emergency)

```bash
dbwarden unlock
```

**Warning**: Only use `unlock` if you're certain no other migration process is running.

## Output Examples

### Successful Migration

```
[INFO] Applying migration: 0001_create_users.sql
[INFO] Applying migration: 0002_create_posts.sql
Migrations completed successfully: 2 migrations applied.
```

### Verbose Output

```
[INFO] Mode: sync
[INFO] Pending migrations: 0001_create_users, 0002_create_posts
[INFO] Starting migration: 0001_create_users.sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL
)
[INFO] Migration completed: 0001_create_users.sql in 0.05s
[INFO] Starting migration: 0002_create_posts.sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title VARCHAR(200) NOT NULL
)
[INFO] Migration completed: 0002_create_posts.sql in 0.03s
Migrations completed successfully: 2 migrations applied.
```

### No Pending Migrations

```
Migrations are up to date.
```

## Error Handling

### Migration Execution Errors

If a migration fails:

1. The migration is not recorded
2. Database changes are rolled back (if in transaction)
3. Error message is displayed

### Checksum Validation

DBWarden validates migration file checksums to ensure integrity:

- **Before execution**: Verifies file hasn't been modified
- **Integrity check**: Compares stored checksum with current file

## Best Practices

1. **Always use --verbose in production**: Log all SQL statements
2. **Test migrations first**: Run on staging before production
3. **Backup before migrating**: Especially in production
4. **Don't modify applied migrations**: Create new migrations instead

## Rollback Strategy

Before running migrations, understand your rollback options:

```bash
# Check what will be rolled back
dbwarden history

# Rollback if needed
dbwarden rollback
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Database Migrations

on:
  push:
    branches: [main]

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install dbwarden
      
      - name: Run migrations
        run: dbwarden migrate --verbose
        env:
          DBWARDEN_SQLALCHEMY_URL: ${{ secrets.DATABASE_URL }}
```

## Troubleshooting

### "Migrations are up to date" but you expect changes

1. Check migrations directory exists
2. Verify migrations are in correct format
3. Check `dbwarden status` for pending migrations

### Migration fails silently

Run with `--verbose` to see detailed logs.

### Lock held by another process

```bash
dbwarden lock-status
# If locked, wait or use:
dbwarden unlock
```

## See Also

- [rollback](rollback.md): Revert applied migrations
- [status](status.md): Check migration status
- [history](history.md): View migration history
- [Lock Management](lock.md): Understanding migration locks
