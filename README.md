# sqlite

Official SQLite package for Strut.

The package uses the **external/system SQLite library**; SQLite itself is not vendored into this repository or into Strut.

## Requirements

Install SQLite development headers/libraries for the target platform so the native linker can resolve SQLite.

Typical Linux development packages expose `sqlite3.h` and `libsqlite3`.

## Add the package

From a local checkout while the remote package resolver is still evolving:

```bash
strut add /path/to/strut-packages/sqlite
```

Then:

```strut
include <sqlite>;
```

## Open a database

```strut
include <sqlite>;

function main() -> void : SqliteError {
    sqlite_db db := sqlite_open("app.db");

    db.exec("CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT)");

    db.close();
    return;
}
```

`sqlite_db` is reference-backed by the bootstrap runtime and closes its native connection when its shared state is destroyed. Calling `.close()` explicitly is still recommended when the lifetime should be obvious.

## Prepared parameters

Parameters are supplied as a JSON array and bound rather than interpolated into SQL:

```strut
db.exec(
    "INSERT INTO users VALUES (?, ?)",
    json.parse("[1,\\"Nick\\"]")
);
```

Queries use the same binding mechanism:

```strut
rows := db.query(
    "SELECT id, name FROM users WHERE id = ?",
    json.parse("[1]")
);

print(json.stringify(rows));
```

The returned rows are JSON arrays of objects.

## Transactions

The underlying SQLite surface supports scoped transactions. A transaction commits if its callable completes and rolls back if it throws.

## API

### `sqlite_open`

```strut
sqlite_db db := sqlite_open(path);
```

May throw `SqliteError`.

### `db.exec`

```strut
db.exec(sql);
db.exec(sql, params);
```

Executes a prepared statement. `params` is a JSON array.

### `db.query`

```strut
rows := db.query(sql);
rows := db.query(sql, params);
```

Returns query rows as `json`.

### `db.transaction`

```strut
db.transaction(() => {
    db.exec("...");
    db.exec("...");
});
```

Commits on success and rolls back when the body throws.

### `db.close`

```strut
db.close();
```

Closes the database deterministically.

## Test

```bash
python3 tests/run.py --strut /path/to/strut
```

or:

```bash
STRUT_BIN=/path/to/strut python3 tests/run.py
```

The test uses an in-memory database and leaves no database file behind.

## Current implementation note

The first Strut compiler implements the SQLite ABI/runtime hooks in its bootstrap backend. This package is the public package boundary so applications declare SQLite as a dependency rather than treating database support as part of the minimal standard library. As the package/runtime boundary matures, implementation details can move out of the bootstrap compiler without changing application-level package usage.
