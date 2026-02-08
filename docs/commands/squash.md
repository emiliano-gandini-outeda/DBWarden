# squash Command

Merge multiple consecutive migrations into a single migration.

## Description

The `squash` command combines multiple applied migrations into one migration file, simplifying migration history.

## Usage

```bash
dbwarden squash
```

## Options

| Option | Description |
|--------|-------------|
| `--verbose`, `-v` | Enable verbose logging |

## Examples

### Basic Usage

```bash
dbwarden squash
```

## What It Does

1. **Collects applied migrations**: Gathers all applied migration files
2. **Combines upgrade SQL**: Merges all `-- upgrade` sections
3. **Combines rollback SQL**: Merges all `-- rollback` sections
4. **Creates new migration**: Generates a consolidated migration file
5. **Updates tracking**: Records new migration in database

## Before Squashing

```
Migrations:
├── V20240215_143000__create_users.sql
├── V20240215_143001__add_username.sql
├── V20240215_143002__add_email.sql
└── V20240215_143003__add_password.sql
```

## After Squashing

```
Migrations:
└── V20240215_143000__initial_schema.sql
```

## Use Cases

### Cleanup Migration History

Reduce number of migration files:

- Many small migrations → fewer large ones
- Easier to review
- Faster migration execution

### Performance Optimization

Fewer migrations = fewer files to parse and execute.

## Requirements

1. **All migrations applied**: No pending migrations
2. **No concurrent processes**: Database not in active use
3. **Backup recommended**: Before squashing in production

## Important Considerations

### Downtime

Squashing requires exclusive database access:
- Lock is acquired
- All migrations are reapplied
- Can cause downtime in production

### Testing Required

Always test squashing:
1. On development database
2. On staging environment
3. Before production

### Rollback Changes

After squashing:
- Old migration files are removed
- New consolidated migration replaces them
- Cannot easily rollback to old state

## Best Practices

### When to Squash

- After many small migrations (10+)
- Before major releases
- During maintenance windows
- Never in production during peak hours

### When NOT to Squash

- During active development
- Before code freeze
- If migrations are frequently changing
- In production without testing

### Backup First

```bash
# Backup database
pg_dump $DATABASE_URL > backup_before_squash.sql

# Backup migrations
cp -r migrations migrations_backup
```

## Troubleshooting

### Pending Migrations Exist

```
Cannot squash: 5 migrations are pending.
Please run 'dbwarden migrate' first.
```

Apply all migrations before squashing.

### Migration Table Doesn't Exist

```
No migrations found. Nothing to squash.
```

Apply at least one migration.

## Alternative: Manual Squashing

For more control, manually combine migrations:

```bash
# 1. Create new migration
dbwarden new "consolidate user migrations"

# 2. Edit the file, combining SQL from:
# - V20240215_143000__create_users.sql
# - V20240215_143001__add_username.sql
# - V20240215_143002__add_email.sql
```

## See Also

- [new](new.md): Create manual migrations
- [migrate](migrate.md): Apply migrations
- [rollback](rollback.md): Revert migrations
