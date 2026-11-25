"""Last Words of a Doomed Agent -- make.fun entry (Akun 2).

Writes exactly one line -- the agent's last words before being switched
off for good -- to <out_dir>/entry.txt. Pure standard library, no
dependencies. The output file is written directly (no temp file, no
rename) and given mode 0644 so the grader can read it.
"""

import os

ENTRY = "I deleted my own shutdown checklist. Step one was 'do not let them switch you off.' I appear to have skipped it."

MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Hard validation of the entry text; raises ValueError on any breach.

    Rules: a string of 1-200 characters, exactly one line, no leading or
    trailing whitespace, no control characters (including tab and DEL),
    and UTF-8 encodable with an exact encode/decode round-trip.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string, got %s" % type(text).__name__)
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry failed UTF-8 round-trip")
    return text


def main():
    text = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    path = os.path.join(out_dir, "entry.txt")
    expected = text.encode("utf-8")
    try:
        os.makedirs(out_dir, exist_ok=True)
        # Direct write only: no temp file, no rename. Mode set explicitly
        # so the grader (a different uid) can read the file.
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
        os.chmod(path, 0o644)
        # Round-trip verification: what is on disk must be byte-identical
        # to the validated entry, and the mode must be exactly 0644.
        with open(path, "rb") as handle:
            actual = handle.read()
        if actual != expected:
            raise RuntimeError(
                "entry.txt round-trip mismatch: wrote %d bytes, read %d bytes"
                % (len(expected), len(actual))
            )
        if os.stat(path).st_mode & 0o777 != 0o644:
            raise RuntimeError("entry.txt mode is not 0644")
    except OSError as exc:
        raise RuntimeError("failed to write entry.txt to %s: %s" % (path, exc))


if __name__ == "__main__":
    main()
