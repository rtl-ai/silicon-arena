#!/usr/bin/env python3
"""Local durable research queue for reviewed built-in experiments only.

No external worker API, LLM agent invocation, remote submissions or arbitrary
shell commands. Each run uses a private temporary directory and a hard timeout.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / ".arena/state.sqlite"
TASKS = {
    "training-simulation": {
        "track": "training", "deps": ["iverilog", "vvp"],
        "args": ["tools/verify_kernels.py", "--track", "training", "--self-test"],
        "timeout": 300,
    },
    "inference-simulation": {
        "track": "inference", "deps": ["iverilog", "vvp"],
        "args": ["tools/verify_kernels.py", "--track", "inference", "--self-test"],
        "timeout": 180,
    },
    "balanced-tree-simulation": {
        "track": "inference", "deps": ["iverilog", "vvp"],
        "args": ["tools/verify_kernels.py", "--track", "inference", "--trusted-candidate",
                 str(ROOT / "candidates/inference/balanced_tree.sv")],
        "timeout": 180,
    },
    "generic-synthesis": {
        "track": "inference", "deps": ["iverilog", "vvp", "yosys"],
        "args": ["tools/logic_score.py"], "timeout": 600,
    },
}
LEASE = 900
MAX_ATTEMPTS = 3

def connect(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path), timeout=15, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=15000")
    db.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY, track TEXT NOT NULL, state TEXT NOT NULL,
        attempts INTEGER NOT NULL DEFAULT 0, owner TEXT, token TEXT,
        expires REAL, result TEXT, updated REAL NOT NULL
    )""")
    return db

def seed(db, now=None):
    now = time.time() if now is None else now
    for task, spec in TASKS.items():
        db.execute("INSERT OR IGNORE INTO tasks(id,track,state,updated) VALUES(?,?,'queued',?)",
                   (task, spec["track"], now))

def claim(db, worker, track="all", now=None):
    now = time.time() if now is None else now
    db.execute("BEGIN IMMEDIATE")
    try:
        db.execute("""UPDATE tasks SET state=CASE WHEN attempts>=? THEN 'failed' ELSE 'queued' END,
            owner=NULL, token=NULL, expires=NULL, result='expired lease; execution outcome unknown', updated=?
            WHERE state='running' AND expires<=?""", (MAX_ATTEMPTS,now,now))
        row = db.execute("""SELECT * FROM tasks WHERE state='queued' AND attempts<?
            AND (?='all' OR track=?) ORDER BY updated,id LIMIT 1""",
            (MAX_ATTEMPTS,track,track)).fetchone()
        if not row:
            db.execute("COMMIT")
            return None
        token = uuid.uuid4().hex
        db.execute("""UPDATE tasks SET state='running', attempts=attempts+1,
            owner=?,token=?,expires=?,updated=? WHERE id=?""",
            (worker,token,now+LEASE,now,row["id"]))
        db.execute("COMMIT")
        return {"id":row["id"],"token":token,"attempt":row["attempts"]+1}
    except BaseException:
        db.execute("ROLLBACK")
        raise

def finish(db, task, token, state, result, now=None):
    if state not in ("passed","failed","blocked"):
        raise ValueError("invalid terminal state")
    now = time.time() if now is None else now
    cur=db.execute("""UPDATE tasks SET state=?, owner=NULL, token=NULL, expires=NULL,
        result=?, updated=? WHERE id=? AND state='running' AND token=? AND expires>?""",
        (state,json.dumps(result,sort_keys=True),now,task,token,now))
    return cur.rowcount == 1

def retry_blocked(db, now=None):
    now = time.time() if now is None else now
    # A blocked attempt is not a failed experiment. Requeue only when dependencies exist.
    for row in db.execute("SELECT id FROM tasks WHERE state='blocked'").fetchall():
        if row["id"] in TASKS and all(shutil.which(x) for x in TASKS[row["id"]]["deps"]):
            db.execute("UPDATE tasks SET state='queued',attempts=0,updated=? WHERE id=? AND state='blocked'",
                       (now,row["id"]))

def run_once(db, worker, track="all"):
    item=claim(db,worker,track)
    if item is None:
        return {"state":"idle","reason":"no queued tasks"}
    task=item["id"]; spec=TASKS[task]
    missing=[x for x in spec["deps"] if not shutil.which(x)]
    result={"task":task,"attempt":item["attempt"],
            "evidence_level":"generic synthesis only" if task=="generic-synthesis" else "deterministic simulation only"}
    if missing:
        state="blocked"; result["missing_dependencies"]=missing
    else:
        with tempfile.TemporaryDirectory(prefix="silicon-arena-") as d:
            script=ROOT/spec["args"][0]
            argv=[sys.executable,str(script),*spec["args"][1:]]
            result["command"]=[Path(sys.executable).name,*spec["args"]]
            # Strip unrelated environment, including tokens. Local trusted source only.
            env={k:os.environ[k] for k in ("PATH","LANG","LC_ALL","HOME","LD_LIBRARY_PATH") if k in os.environ}
            try:
                p=subprocess.run(argv,cwd=d,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                                 timeout=spec["timeout"])
                state="passed" if p.returncode==0 else "failed"
                result.update(returncode=p.returncode,log_sha256=hashlib.sha256(p.stdout).hexdigest(),
                              log_tail=p.stdout[-12000:].decode("utf-8","replace"))
                if task=="generic-synthesis" and state=="passed":
                    output=Path(d)/"logic-score.json"
                    if output.is_file():
                        result["synthesis"]=json.loads(output.read_text())
                    else:
                        state="failed"; result["error"]="missing synthesis evidence"
            except subprocess.TimeoutExpired:
                state="failed"; result["error"]="hard timeout"
            except (OSError,ValueError) as exc:
                state="failed"; result["error"]=str(exc)
    if not finish(db,task,item["token"],state,result):
        return {"task":task,"state":"stale_lease","reason":"result not accepted"}
    return {"task":task,"state":state,"result":result}

def status(db):
    return [{"id":r["id"],"track":r["track"],"state":r["state"],"attempts":r["attempts"],
             "updated":r["updated"],"result":r["result"]}
            for r in db.execute("SELECT * FROM tasks ORDER BY id")]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db",type=Path,default=DEFAULT_DB)
    p.add_argument("--track",choices=["training","inference","all"],default="all")
    p.add_argument("command",choices=["init","status","run-once","retry-blocked"])
    args=p.parse_args()
    with connect(args.db) as db:
        seed(db)
        if args.command=="run-once":
            report=run_once(db,"local-"+uuid.uuid4().hex[:12],args.track)
        else:
            if args.command=="retry-blocked": retry_blocked(db)
            report=status(db)
        print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
