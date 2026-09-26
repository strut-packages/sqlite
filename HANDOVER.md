# SQLite package handover

This repository is the official `strut-packages/sqlite` package boundary.

The current Strut bootstrap compiler already owns the native SQLite runtime hooks and links the external/system SQLite library when SQLite APIs are used. The package intentionally does **not** vendor SQLite.

Current public usage:

```strut
include <sqlite>;

db := sqlite_open("app.db");
```

Maintain the package manifest, user-facing docs, examples and package-flow tests here. As Strut's package/native-library model matures, SQLite implementation details should move behind this package boundary without requiring applications to change their `include <sqlite>` usage.

Run:

```bash
python3 tests/run.py --strut /path/to/strut
```

before release changes.
