# init Command

Initialize the DBWarden migrations directory.

## Description

The `init` command creates the `migrations/` directory that will store all your migration files. This is the first command you run when setting up DBWarden in a new project.

## Usage

```bash
dbwarden init
```

## What It Does

1. Creates a `migrations/` directory in the current working directory
2. Sets up the directory structure for storing migration files
3. Does NOT create any database tables or modify the database

## Example

```bash
$ dbwarden init
DBWarden migrations directory created: /home/user/myproject/migrations

Next steps:
  1. Create a .env file with DBWARDEN_SQLALCHEMY_URL
  2. Run 'dbwarden make-migrations' to generate migrations from your models
```

## Directory Structure

After running `init`, your project structure will look like:

```
myproject/
├── migrations/          # Created by init command
│   └── .gitkeep        # Placeholder file
├── models/
│   └── user.py
├── .env
└── app.py
```

## Important Notes

- **No database changes**: This command only creates a local directory
- **Safe to run multiple times**: Running `init` again is safe; it won't overwrite existing migrations
- **Required before other commands**: Most DBWarden commands require the migrations directory to exist

## See Also

- [make-migrations](make-migrations.md): Generate migrations from models
- [new](new.md): Create manual migrations
