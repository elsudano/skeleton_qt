## Python Docstring Style Guide

This document defines the standard format for docstrings in the `skeleton_qt` project.

### Recommended Format: NumPy (DOCSTR) style

```
class ClassName:
    """Manage route design and route-related business logic."""

    def function_one(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> float:
        """Calculate the distance between two geographic points.

        Parameters
        ----------
        start : tuple[float, float]
            Latitude and longitude of the starting point.
        end : tuple[float, float]
            Latitude and longitude of the destination.

        Returns
        -------
        float
            Distance between the two points in kilometers.
        """
```

### Key Rules

* **First line**: Concise summary in imperative mood (no "This")
* **Blank lines** between sections (Parameters, Returns, Raises)
* **Use type hints** in docstrings when possible: `str`, `bool`, etc.
* **Avoid redundancy** - don't document what's already clear from function signature
* **Consistent with code style**: PEP 257 compliance

### Examples from project:
- `TextBinder`: Complete NumPy format ✓
- `HttpClient`: Complete NumPy format ✓
- Missing docstrings in tests: Will be fixed (D103)

These rules are enforced by Ruff (`--select D`), which automatically fixes violations.