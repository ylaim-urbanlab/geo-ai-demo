# Default Arguments

Default arguments are fallback values a function uses when you do not pass that input yourself.

They make functions easier to call for common cases while still allowing customization when needed.

Why this matters here: `plot_points_by_category` defaults to `column="CONDITION"` and `figsize=(10, 10)` if you do not provide those.
