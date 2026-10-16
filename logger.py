import sys
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: python logger.py <logfile>", file=sys.stderr)
    sys.exit(1)

with open(sys.argv[1], "a") as f:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        action = parts[0]
        if action == "QUIT":
            break
        msg = parts[1] if len(parts) > 1 else ""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"{ts} [{action}] {msg}\n")
        f.flush()