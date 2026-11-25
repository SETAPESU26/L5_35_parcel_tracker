# Lab 5: Reflection

**Name:** Mohammed Sahil S
**SRN:** PES2UG24CS281

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The Flake8 issues were the easiest. Each message gave the exact line and column, and fixing it meant adding spaces or blank lines. Docstrings and snake_case names were also simple, but every reference had to be renamed together. The longer names also pushed some lines out of alignment, so Flake8 had to be rerun after the Pylint fixes.

The `shell=True` issue (B602) was the hardest. Removing `shell=True` alone was not enough. The command had to become a list of arguments, `ping` needed an absolute path, and an address starting with `-` could still have been read as an option. The mutable default argument also needed some thought, because the fix had to keep working for callers who pass their own history list.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes, in a limited sense. Bandit's B404 flags the line `import subprocess` whatever the module is used for. After the fix, the call uses a fixed program path, a list of arguments and no shell, but Bandit still reports B404 and B603 (both Low) because it cannot tell that the call is safe. I marked these two lines with `# nosec` and the specific code, so any new finding is still reported.

B311 was not a false positive here. `random` is fine in many programs, but this one used it for a delivery OTP, which must not be predictable.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **In the editor:** show Flake8 and Pylint warnings while writing code.
- **Before each commit:** run the three tools on changed files with a pre-commit hook.
- **In CI:** run them on every pull request and fail the build if Pylint drops below 9.5, Flake8 reports anything, or Bandit reports a Medium or High issue.
- **For suppressions:** allow `# nosec` only with a specific code and a reason, and check it during code review.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Quality:** Pylint went from 4.91 to 10.00, Bandit from 4 reported issues to 0 (2 Low findings suppressed after review), and Flake8 from 4 issues to 0.
- **Security:** passing `127.0.0.1; touch <file>` to `ping_hub` now fails as an unknown host and the second command does not run. The OTP and the label file are also created safely.
- **Robustness:** bookings no longer share a hidden history list, and an unexpected error in `track_parcel` is no longer reported as an unknown id.
- **Readability:** names are consistent, every function has a docstring, and importing the file no longer runs the demo.

Static analysis does not find everything. None of the tools noticed that `is_with_courier` returns `False` for "Out for Delivery". Tests and code review are still needed for logic like this.
