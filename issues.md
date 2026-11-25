# Lab 5: Issues Found by Static Analysis

**Name:** Mohammed Sahil S
**SRN:** PES2UG24CS281
**File:** `parcel_tracker.py`

Line numbers refer to the original file, before any fixes.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built from input (Bandit B602, High) | Security | 55 | `pingHub` joins the hub address to a command string and runs it with `shell=True`, so an address like `127.0.0.1; rm x` would run a second command. | Call `ping` by its absolute path (`shutil.which`) with a list of arguments and no shell. Reject addresses starting with `-` so they cannot be read as options. |
| Insecure temp file (Bandit B306, Medium) | Security | 50 | `tempfile.mktemp` only returns a name. Another process can create that file before the program does. | Use `NamedTemporaryFile(delete=False)`, which creates the file safely and returns its path. |
| Predictable OTP (Bandit B311, Low) | Security | 72 | The delivery OTP comes from `random`, which is predictable and not meant for security use. | Use `secrets.randbelow(9000) + 1000`, which keeps the same 1000 to 9999 range. |
| `subprocess` import (Bandit B404, Low) | Security | 2 | Bandit flags every import of `subprocess` for review. | Reviewed. The import is needed for `ping_hub`, which is now safe, so it is marked `# nosec B404` with the reason. The safe list call is marked `# nosec B603` for the same reason. |
| Mutable default argument (Pylint W0102) | Bug | 11 | `history=[]` is created once and shared by every call that does not pass a list. | Default to `None` and append only when the caller passes a list. |
| Broad exception (Pylint W0718) | Bug | 37 | `except Exception` would hide unrelated errors behind "Unknown tracking id". | Catch only `KeyError`. |
| Repeated comparison (Pylint R1714) | Refactor | 45 | `status == ... or status == ...` compares the same variable twice. | Use `status in ("Picked Up", "In Transit")`. |
| Naming style (Pylint C0103) | Convention | 11, 12, 20, 27, 34, 43, 48, 53, 67 | Functions, arguments and variables use camelCase. | Rename to snake_case and update every reference. |
| Missing docstrings (Pylint C0114, C0116) | Convention | 1, 11, 20, 27, 34, 43, 48, 53, 58 | The module and all eight functions have no docstring. | Add a short docstring to each. |
| Missing spaces (Flake8 E225, E231) | Style | 28, 74 | `cost=50` has no spaces around `=`, and there is no space after a comma in `print`. | Add the spaces. |
| Inline comment spacing (Flake8 E261) | Style | 71 | Only one space before the inline comment. | Use two spaces. |
| Blank lines before top-level code (Flake8 E305) | Style | 75 | `main()` follows the function body with no blank lines. | Add two blank lines and an `if __name__ == "__main__":` guard, so importing the file does not run the demo. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.91/10 (27 messages) | 10.00/10 (0 messages) |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues reported, 2 Low findings suppressed with `# nosec` after review |
| Flake8 | 4 issues | 0 issues |

The program prints the same output before and after the fixes, except for the OTP, which is random on every run.

## Noticed but not changed

No tool reported this: `is_with_courier` returns `False` for "Out for Delivery", although the parcel is still with the courier at that stage. It is a logic question rather than a tool finding, and the README asks for the same behaviour, so it was left as it is.
