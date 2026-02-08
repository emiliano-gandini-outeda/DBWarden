# Commands Overview

DBWarden provides a comprehensive set of commands for managing database migrations. This page provides an overview of all available commands.

## Command Categories

### Initialization Commands

| Command | Description |
|---------|-------------|
| [init](commands/init.md) | Initialize the migrations directory |

### Migration Management

| Command | Description |
|---------|-------------|
| [make-migrations](commands/make-migrations.md) | Auto-generate SQL migrations from SQLAlchemy models |
| [new](commands/new.md) | Create a manual migration file |
| [migrate](commands/migrate.md) | Apply pending migrations |
| [rollback](commands/rollback.md) | Rollback applied migrations |
| [squash](commands/squash.md) | Merge multiple migrations into one |

### Status and Information

| Command | Description |
|---------|-------------|
| [history](commands/history.md) | Show migration history |
| [status](commands/status.md) | Show migration status |
| [mode](commands/mode.md) | Display sync/async mode |
| [version](commands/version.md) | Display DBWarden version |
| [env](commands/env.md) | Display environment configuration |

### Database Inspection

| Command | Description |
|---------|-------------|
| [check-db](commands/check-db.md) | Inspect database schema |
| [diff](commands/diff.md) | Compare models vs database |

### Lock Management

| Command | Description |
|---------|-------------|
| [lock-status](commands/lock.md) | Check migration lock status |
| [unlock](commands/lock.md) | Release the migration lock |

## Global Options

All commands support the following options:

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Show help message |
| `--verbose`, `-v` | Enable verbose logging |

## Usage Patterns

### Apply Migrations

```bash
# Apply all pending migrations
dbwarden migrate

# Apply with verbose output
dbwarden migrate --verbose

# Apply specific number of migrations
dbwarden migrate --count 2

# Migrate to a specific version
dbwarden migrate --to-version 20240215_143000
```

### Generate Migrations

```bash
# Generate from models with description
dbwarden make-migrations "create users table"

# Generate with verbose logging
dbwarden make-migrations "add posts table" --verbose
```

### Rollback Migrations

```bash
# Rollback the last migration
dbwarden rollback

# Rollback 2 migrations
dbwarden rollback --count 2

# Rollback to specific version
dbwarden rollback --to-version 20240215_143000
```

### Check Status

```bash
# View all migrations and their status
dbwarden status

# View migration history
dbwarden history

# Check database schema
dbwarden check-db --out json
```

## Command Execution Flow

```
┌─────────────────────────────────────────────────┐
│  dbwarden <command>                             │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  1. Load Configuration (.env)                  │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  2. Validate Environment                        │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  3. Execute Command Logic                       │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  4. Display Results                             │
└─────────────────────────────────────────────────┘
```

## Error Handling

DBWarden provides clear error messages for common issues:

- **Missing .env file**: "STRATA_SQLALCHEMY_URL is required"
- **Migrations directory not found**: "Please run 'dbwarden init' first"
- **Pending migrations**: "Cannot generate migrations while X migrations are pending"
- **Lock active**: "Migration is currently locked"

## Output Formats

Some commands support different output formats:

| Command | Formats |
|---------|---------|
| `check-db` | `txt` (default), `json`, `yaml` |

Example:

```bash
dbwarden check-db --out json
dbwarden check-db --out yaml
```

## Getting Help

Get help for any command:

```bash
# General help
dbwarden --help

# Command-specific help
dbwarden migrate --help
dbwarden make-migrations --help
```
