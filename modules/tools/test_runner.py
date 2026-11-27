from pathlib import Path
import subprocess, sys

ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"codepilot_outputs"

def run_unittest(filename):
    name=Path(filename).name
    target=(OUTPUT/name).resolve()
    if target.parent != OUTPUT.resolve() or not target.is_file() or target.suffix != ".py":
        raise ValueError("Choose an existing Python test file in codepilot_outputs.")
    if target.stat().st_size>100_000: raise ValueError("Test file exceeds 100 KB.")
    result=subprocess.run([sys.executable,"-m","unittest","-v",target.stem],
        cwd=str(OUTPUT),capture_output=True,text=True,timeout=20)
    return (result.stdout+"\n"+result.stderr).strip(), result.returncode
