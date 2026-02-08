# CLI Reference

Complete command-line interface reference for DBWarden.

## Synopsis

```bash
dbwarden [OPTIONS] COMMAND [ARGS]...
```

## Global Options

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Show help message |
| `--version` | Show version information |

## Commands

### Initialization

#### init

Initialize the migrations directory.

```bash
dbwarden init
```

**No arguments or options.**

---

### Migration Management

#### make-migrations

Auto-generate SQL migration from SQLAlchemy models.

```bash
dbwarden make-migrations [DESCRIPTION] [OPTIONS]
```

**Arguments:**
- `DESCRIPTION`: Description for the migration (optional)

**Options:**
- `--verbose`, `-v`: Enable verbose logging

**Examples:**
```bash
dbwarden make-migrations "create users table"
dbwarden make-migrations "add posts" --verbose
dbwarden make-migrations
```

---

#### new

Create a new manual migration file.

```bash
dbwarden new DESCRIPTION [OPTIONS]
```

**Arguments:**
- `DESCRIPTION`: Description of the migration (required)

**Options:**
- `--version`, `-v: Version of the migration

**Examples:**
```bash
dbwarden new "add index to users email"
dbwarden new "custom migration" --version 2.0.0
```

---

#### migrate

Apply pending migrations to the database.

```bash
dbwarden migrate [OPTIONS]
```

**Options:**
- `--count`, `-c`: Number of migrations to apply
- `--to-version`, `-t`: Migrate to a specific version
- `--verbose`, `-v`: Enable verbose logging

**Examples:**
```bash
dbwarden migrate
dbwarden migrate --verbose
dbwarden migrate --count 2
dbwarden migrate --to-version 20240215_143000
```

---

#### rollback

Rollback the last applied migration.

```bash
dbwarden rollback [OPTIONS]
```

**Options:**
- `--count`, `-c: Number of migrations to rollback
- `--to-version`, `-t`: Rollback to a specific version
- `--verbose`, `-v: Enable verbose logging

**Examples:**
```bash
dbwarden rollback
dbwarden rollback --count 2
dbwarden rollback --to-version 20240215_143000
```

---

#### squash

Merge multiple consecutive migrations into one.

```bash
dbwarden squash [OPTIONS]
```

**Options:**
- `--verbose`, `-v`: Enable verbose logging

**Example:**
```bash
dbwarden squash
```

---

### Status and Information

#### history

Show the full migration history.

```bash
dbwarden history
```

**No arguments or options.**

---

#### status

Show migration status (applied and pending).

```bash
dbwarden status
```

**No arguments or options.**

---

#### mode

Display whether execution is sync or async.

```bash
dbwarden mode
```

**No arguments or options.**

---

#### version

Display DBWarden version and compatibility information.

```bash
dbwarden version
```

**No arguments or options.**

---

#### env

Display relevant environment variables without leaking secrets.

```bash
dbwarden env
```

**No arguments or options.**

---

### Database Inspection

#### check-db

Inspect the live database schema.

```bash
dbwarden check-db [OPTIONS]
```

**Options:**
- `--out`, `-o: Output format (json, yaml, txt)

**Examples:**
```bash
dbwarden check-db
dbwarden check-db --out json
dbwarden check-db --out yaml
```

---

#### diff

Show structural differences between models and database.

```bash
dbwarden diff [TYPE] [OPTIONS]
```

**Arguments:**
- `TYPE`: Type of diff (models, migrations, all) - default: all

**Options:**
- `--verbose`, `-v: Enable verbose logging

**Examples:**
```bash
dbwarden diff
dbwarden diff --verbose
dbwarden diff models
```

---

### Lock Management

#### lock-status

Check if migration is currently locked.

```bash
dbwarden lock-status
```

**No arguments or options.**

---

#### unlock

Release the migration lock.

```bash
dbwarden unlock
```

**No arguments or options.**

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | Migration error |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `STRATA_SQLALCHEMY_URL` | Yes | Database connection URL |
| `STRATA_ASYNC` | No | Enable async mode (true/false) |
| `STRATA_MODEL_PATHS` | No | Paths to SQLAlchemy models |
| `STRATA_POSTGRES_SCHEMA` | No | PostgreSQL schema |

## Configuration File

DBWarden uses `.env` file for configuration:

```env
STRATA_SQLALCHEMY_URL=postgresql://user:pass@localhost:5432/db
STRATA_ASYNC=false
STRATA_MODEL_PATHS=models/
STRATA_POSTGRES_SCHEMA=public
```

## Shortcuts

Some commands have shortcuts:

| Command | Shortcut |
|---------|-----------|
| `dbwarden --help` | `dbwarden -h` |
| `dbwarden --verbose` | `dbwarden -v` |
| `dbwarden --count` | `dbwarden -c` |
| `dbwarden --to-version` | `dbwarden -t` |
| `dbwarden --out` | `dbwarden -o` |

## Tab Completion

Enable tab completion for bash:

```bash
eval "$(dbwarden --print-completion bash)"
```

For zsh:

```bash
eval "$(dbwarden --print-completion zsh)"
```

## Logging Levels

| Level | Description |
|-------|-------------|
| INFO | General information |
| WARNING | Potential issues |
| ERROR | Errors |
| DEBUG | Detailed debugging (with --verbose) |

## Troubleshooting

### Command Not Found

```bash
# Check installation
pip show dbwarden

# Reinstall
pip install --upgrade dbwarden
```

### Permission Denied

```bash
# Make sure scripts are executable
chmod +x /path/to/dbwarden
```

### Invalid Configuration

```bash
# Validate .env file
dbwarden env

# Check file exists
ls -la .env
```

## See Also

- [Commands Overview](commands.md): Command categories and usage patterns
- [Configuration](configuration.md): Environment variable details
- [Installation](installation.md): Installation troubleshooting
