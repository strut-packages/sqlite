#!/usr/bin/env python3
import argparse, json, os, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

SOURCE=r'''include <sqlite>;

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
'''

def run(cmd,cwd,env):
    return subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--strut",default=os.environ.get("STRUT_BIN","strut"))
    args=ap.parse_args()
    compiler=str(Path(args.strut).resolve()) if Path(args.strut).exists() else args.strut
    with tempfile.TemporaryDirectory(prefix="strut-sqlite-test-") as td:
        td=Path(td)
        env=os.environ.copy()
        env["STRUT_HOME"]=str(td/"strut-home")
        app=td/"app"
        app.mkdir()
        (app/"main.p").write_text(SOURCE)
        (app/"strut.json").write_text(json.dumps({
            "name":"sqlite-package-test","version":"0.1.0",
            "entry":"main.p","dependencies":{}
        })+"\n")
        for cmd in (
            [compiler,"init"],
            [compiler,"add",str(ROOT)],
            [compiler,"install"],
        ):
            p=run(cmd,app,env)
            if p.returncode:
                print(p.stdout,end="")
                print(p.stderr,end="",file=os.sys.stderr)
                return p.returncode
        out=app/("sqlite-test.exe" if os.name=="nt" else "sqlite-test")
        p=run([compiler,"main.p","-o",str(out)],app,env)
        if p.returncode:
            print(p.stdout,end="")
            print(p.stderr,end="",file=os.sys.stderr)
            return p.returncode
        p=run([str(out)],app,env)
        expected='[{"id":7,"value":"strut"}]\n'
        if p.returncode or p.stdout != expected:
            print("unexpected result",file=os.sys.stderr)
            print("stdout:",repr(p.stdout),file=os.sys.stderr)
            print("stderr:",repr(p.stderr),file=os.sys.stderr)
            return 1
    print("sqlite package test: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
