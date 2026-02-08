# lock-status and unlock Commands

Manage migration locking to prevent concurrent execution.

## Description

DBWarden uses a locking mechanism to ensure only one migration process can run at a time. These commands allow you to check and manage the lock state.

## Commands

### lock-status

Check if a migration lock is currently active.

```bash
dbwarden lock-status
```

**Output (Lock Active):**
```
Migration lock: ACTIVE
Another migration process may be running.
```

**Output (No Lock):**
```
Migration lock: INACTIVE
```

### unlock

Release the migration lock (emergency use only).

```bash
dbwarden unlock
```

**Output:**
```
Migration lock released successfully.
```

Or if no lock was held:
```
Failed to release lock. Lock may not be held.
```

## Locking Mechanism

### Purpose

Prevent concurrent migration execution:
- Avoids race conditions
- Prevents schema conflicts
- Ensures migration order

### How It Works

1. Lock is acquired before any migration operation
2. Lock is released after completion or error
3. Other processes wait or fail when lock is held

### Lock Table

DBWarden creates a `dbwarden_lock` table:

```sql
CREATE TABLE dbwarden_lock (
    id INTEGER PRIMARY KEY,
    locked BOOLEAN DEFAULT FALSE,
    acquired_at DATETIME,
    release_at DATETIME
);
```

## When Locks Are Used

| Command | Acquires Lock | Releases Lock |
|---------|--------------|---------------|
| `migrate` | Yes | Yes |
| `rollback` | Yes | Yes |
| `make-migrations` | No | No |
| `new` | No | No |
| `history` | No | No |
| `status` | No | No |
| `check-db` | No | No |

## Common Scenarios

### Scenario 1: Normal Operation

```bash
# Terminal 1
dbwarden migrate
# Lock acquired, migration runs, lock released

# Terminal 2 (while T1 running)
dbwarden migrate
# Sees lock, waits or fails
```

### Scenario 2: Lock Held After Error

```bash
# Migration fails mid-way
# Lock is NOT released
# Database may be in inconsistent state

# Check lock status
dbwarden lock-status
# Shows: ACTIVE

# Investigate issue first
# Then release if safe
dbwarden unlock
```

### Scenario 3: Stuck Process

```bash
# Process killed or crashed
# Lock remains active

# Check
dbwarden lock-status
# ACTIVE

# Force unlock (after verifying no other process)
dbwarden unlock
```

## Best Practices

### Do

- Check `lock-status` before assuming deadlock
- Investigate why lock exists
- Ensure no other process is running
- Document lock releases

### Don't

- Don't `unlock` without checking
- Don't `unlock` if another process is running
- Don't run concurrent migrations manually

## Troubleshooting

### Lock Active During Deployment

```bash
# 1. Check what's running
ps aux | grep dbwarden

# 2. Check lock status
dbwarden lock-status

# 3. Wait if safe
# OR force unlock if certain
dbwarden unlock
```

### Lock Not Releasing

```bash
# Check database state
dbwarden check-db --out txt
# Look for dbwarden_lock table

# Manual lock check
psql $DATABASE_URL -c "SELECT * FROM dbwarden_lock;"
```

### Migration Stuck at Lock

```bash
# Kill stuck process
pkill -f dbwarden

# Release lock
dbwarden unlock

# Check status
dbwarden status
dbwarden history
```

## Emergency Procedures

### Force Unlock (When Safe)

```bash
# 1. Verify no dbwarden process running
ps aux | grep -i dbwarden

# 2. Check no connections
# PostgreSQL:
psql $DATABASE_URL -c "SELECT pid FROM pg_stat_activity WHERE state = 'active';"

# 3. Release lock
dbwarden unlock

# 4. Verify
dbwarden lock-status
```

### Manual Lock Release

If `unlock` fails:

```sql
-- SQL to manually release lock
UPDATE dbwarden_lock SET locked = FALSE, release_at = NOW();
```

## See Also

- [migrate](migrate.md): Migration execution
- [rollback](rollback.md): Rollback execution
