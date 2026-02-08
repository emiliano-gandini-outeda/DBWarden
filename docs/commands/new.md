# new Command

Create a new manual migration file.

## Description

The `new` command creates a blank migration file for manual SQL authoring. Use this when you need to write custom SQL that cannot be auto-generated from models.

## Usage

```bash
dbwarden new "description of migration"
```

## Arguments

| Argument | Description |
|----------|-------------|
| `description` | **Required** - A descriptive name for the migration |

## Options

| Option | Description |
|--------|-------------|
| `--version`, `-v` | Specific version number for the migration |

## Examples

### Basic Usage

```bash
dbwarden new "add index to users email"
```

### With Custom Version

```bash
dbwarden new "migrate data from old schema" --version 2.0.0
```

## Generated File Structure

```sql
-- migrations/V20240215_143000__add_index_to_users_email.sql

-- upgrade

-- add index to users email

-- rollback

-- add index to users email
```

## When to Use Manual Migrations

Use `new` instead of `make-migrations` when you need to:

- **Add indexes**: Performance optimizations
- **Add constraints**: Advanced constraints not in models
- **Custom data migrations**: Transform or clean existing data
- **Database-specific features**: Use features specific to your database
- **Complex alterations**: Modify multiple tables atomically

## Example: Adding an Index

```sql
-- migrations/V20240215_143000__add_users_email_index.sql

-- upgrade

CREATE INDEX idx_users_email ON users(email);

-- rollback

DROP INDEX idx_users_email;
```

## Example: Data Migration

```sql
-- migrations/V20240215_143001__normalize_usernames.sql

-- upgrade

UPDATE users
SET username = LOWER(username)
WHERE username IS NOT NULL;

-- rollback

-- No rollback needed for data normalization
```

## Example: Complex Schema Change

```sql
-- migrations/V20240215_143002__add_post_status.sql

-- upgrade

ALTER TABLE posts ADD COLUMN status VARCHAR(20) DEFAULT 'draft';

CREATE TYPE post_status AS ENUM ('draft', 'published', 'archived');

ALTER TABLE posts DROP COLUMN status;
ALTER TABLE posts ADD COLUMN status post_status DEFAULT 'draft';

-- rollback

DROP TYPE post_status;
ALTER TABLE posts DROP COLUMN status;
ALTER TABLE posts ADD COLUMN status VARCHAR(20) DEFAULT 'draft';
```

## Version Numbering

If you don't specify a version, a timestamp-based version is generated:

```
V{YYYYMMDD_HHMMSS}__{description}.sql
```

Custom versions must be unique and typically follow semantic versioning:

```
V1.0.0__initial_schema.sql
V1.1.0__add_users.sql
V1.2.0__add_posts.sql
V2.0.0__breaking_changes.sql
```

## Best Practices

1. **Descriptive names**: Include what the migration does:
   ```
   V20240215_143000__add_users_email_index.sql
   # NOT
   V20240215_143000__index.sql
   ```

2. **Test rollback SQL**: Ensure `-- rollback` section works correctly

3. **Idempotent migrations**: Write SQL that can be run multiple times safely

4. **Document complex migrations**: Add comments explaining complex operations

5. **Separate concerns**: One migration per logical change

## Comparison: make-migrations vs new

| Aspect | make-migrations | new |
|--------|-----------------|-----|
| **Source** | SQLAlchemy models | Manual |
| **Use Case** | Schema from models | Custom SQL |
| **Automation** | Full | None |
| **Complexity** | Simple | Complex |
| **Risk** | Lower | Higher |

## Tips for Writing Manual Migrations

### 1. Always Include Rollback

```sql
-- GOOD
CREATE INDEX idx_users_email ON users(email);
-- rollback
DROP INDEX idx_users_email;

-- BAD (no rollback)
CREATE INDEX idx_users_email ON users(email);
```

### 2. Use Transactions When Possible

```sql
-- upgrade
BEGIN;
-- your SQL here
COMMIT;
```

### 3. Handle Existing Data

```sql
-- upgrade
ALTER TABLE users ADD COLUMN new_field VARCHAR(100);

UPDATE users SET new_field = 'default' WHERE new_field IS NULL;

ALTER TABLE users ALTER COLUMN new_field SET NOT NULL;
```

## Troubleshooting

### Version Already Exists

```
Error: Migration version already exists.
```

Use a different version or description.

### Empty Migration

Ensure you write SQL in both `-- upgrade` and `-- rollback` sections.

## See Also

- [make-migrations](make-migrations.md): Auto-generate from models
- [migrate](migrate.md): Apply manual migrations
- [Migration Files](../migration-files.md): Migration file format
