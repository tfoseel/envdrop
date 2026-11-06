"""Run: python3 test_envdrop.py  (no deps; the window itself is stubbed)"""
import importlib.machinery, importlib.util, io, os, subprocess, tempfile
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("envdrop", os.path.join(HERE, "envdrop"))
spec = importlib.util.spec_from_loader("envdrop", loader)
ed = importlib.util.module_from_spec(spec); loader.exec_module(ed)

SECRET = "sk-proj-" + "a1B2c3" * 8

with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    subprocess.run(["git", "init", "-q"], check=True)
    open(".env.example", "w").write("OPENAI_API_KEY=\nPORT=3000\nDB_URL=\n")
    open(".env", "w").write("PORT=3000\nDB_URL=\n")

    # Names come from the project: declared in .env.example or left empty in .env, not yet set.
    assert ed.missing(d) == ["DB_URL", "OPENAI_API_KEY"], ed.missing(d)

    # ask with no names -> one window for the missing keys; one left blank -> skipped, exit 1.
    seen = []
    ed.window = lambda names, where: seen.append(names) or {"DB_URL": " postgres://u:p w@h/db ", "OPENAI_API_KEY": ""}
    out = io.StringIO()
    with redirect_stdout(out):
        rc = ed.cmd_ask([])
    assert seen == [["DB_URL", "OPENAI_API_KEY"]] and rc == 1
    o = out.getvalue()
    assert "saved DB_URL to" in o and "Skipped: OPENAI_API_KEY." in o and "Do not read" in o, o
    assert SECRET not in out.getvalue()

    # explicit name -> saved, quoted value with space preserved, file 0600, .env gitignored.
    ed.window = lambda names, where: {"OPENAI_API_KEY": SECRET}
    with redirect_stdout(io.StringIO()):
        assert ed.cmd_ask(["OPENAI_API_KEY"]) == 0
    assert open(".env").read() == f'PORT=3000\nDB_URL="postgres://u:p w@h/db"\nOPENAI_API_KEY={SECRET}\n'
    assert ed.read_env(".env")["DB_URL"] == "postgres://u:p w@h/db"
    assert oct(os.stat(".env").st_mode & 0o777) == "0o600"
    assert ".env" in open(".gitignore").read()
    assert ed.missing(d) == []

    # all blank -> nothing written.
    ed.window = lambda names, where: {"NEW_KEY": "  "}
    with redirect_stdout(io.StringIO()):
        assert ed.cmd_ask(["NEW_KEY"]) == 1
    # cancel -> nothing written, exit 1.
    ed.window = lambda names, where: None
    with redirect_stdout(io.StringIO()):
        assert ed.cmd_ask(["NEW_KEY"]) == 1
    assert "NEW_KEY" not in open(".env").read()

print("ok")
