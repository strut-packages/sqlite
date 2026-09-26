include "../sqlite.h";

function main() -> void : SqliteError {
    sqlite_db db := sqlite_open(":memory:");
    db.exec("CREATE TABLE values_table(id INTEGER, value TEXT)");
    db.exec(
        "INSERT INTO values_table VALUES (?, ?)",
        json.parse("[7,\"strut\"]")
    );

    rows := db.query(
        "SELECT id, value FROM values_table WHERE id = ?",
        json.parse("[7]")
    );

    print(json.stringify(rows));
    db.close();
    return;
}
