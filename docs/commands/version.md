# version Command

Display DBWarden version and compatibility information.

## Usage

```bash
dbwarden version
```

## Examples

```
DBWarden version: 1.0.0
Python version: 3.12.0
SQLAlchemy version: 2.0.10
```

## What It Shows

| Component | Version |
|-----------|---------|
| DBWarden | Current version |
| Python | Python interpreter version |
| SQLAlchemy | SQLAlchemy library version |

## Use Cases

### Bug Reports

Include version info in bug reports:

```bash
dbwarden version
# Include in GitHub issue
```

### Compatibility Check

Verify compatibility:

```bash
dbwarden version
# Check requirements match
```

### Upgrade Verification

After upgrading:

```bash
dbwarden --version
# Should show new version
```

## Versioning

DBWarden uses [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## See Also

- [Installation](../installation.md): Installation requirements
