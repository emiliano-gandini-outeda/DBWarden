# env Command

Display environment configuration without exposing sensitive data.

## Description

The `env` command shows relevant environment variables for DBWarden, masking sensitive information like passwords.

## Usage

```bash
dbwarden env
```

## Examples

### Basic Usage

```bash
$ dbwarden env
DBWARDEN_SQLALCHEMY_URL: ***
DBWARDEN_ASYNC: true
DBWARDEN_MODEL_PATHS: models/,app/models/
DBWARDEN_POSTGRES_SCHEMA: public
```

### Missing Variables

If some variables are not set, they won't appear in output.

## What It Shows

| Variable | Displayed As | Description |
|----------|--------------|-------------|
| `DBWARDEN_SQLALCHEMY_URL` | `***` | Database URL (masked) |
| `DBWARDEN_ASYNC` | Actual value | Sync/async mode |
| `DBWARDEN_MODEL_PATHS` | Actual value | Model paths |
| `DBWARDEN_POSTGRES_SCHEMA` | Actual value | PostgreSQL schema |

## Use Cases

### Debugging Configuration

Verify configuration is loaded:

```bash
dbwarden env
# Check values are as expected
```

### Sharing Configuration

Safely share configuration (without secrets):

```bash
dbwarden env
# Copy output to share (no passwords visible)
```

### CI/CD Debugging

Debug environment in CI:

```bash
dbwarden env
# Log output (safe, no secrets)
```

## Security

The `env` command is designed to be safe for:
- Debugging logs
- Error messages
- CI/CD output
- Team communication

**Secrets are never displayed.**

## Related Commands

### Validate Configuration

```bash
dbwarden env        # Check config
dbwarden status     # Validate migrations
```

### Check Mode

```bash
dbwarden env        # Shows DBWARDEN_ASYNC
dbwarden mode       # Shows just the mode
```

## See Also

- [mode](mode.md): Display sync/async mode
- [configuration](../configuration.md): Environment variable reference
