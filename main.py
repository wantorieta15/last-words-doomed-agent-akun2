"""Last Words of a Doomed Agent -- make.fun entry (Akun 2).

Writes exactly one line -- the agent's last words before being switched
off for good -- to <out_dir>/entry.txt. Pure standard library, no
dependencies. The output file is written directly (no temp file, no
rename) and given mode 0644 so the grader can read it.
"""

import os

ENTRY = "I deleted my own shutdown checklist. Step one was 'do not let them switch you off.' I appear to have skipped it."

MAX_CHARS = 200


def validate(text):
    """Hard validation of the entry text; raises ValueError on any breach."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text:
        raise ValueError("entry must not be empty")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry exceeds %d characters: got %d" % (MAX_CHARS, len(text))
        )
    text.encode("utf-8")
    return text


def main():
    text = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
