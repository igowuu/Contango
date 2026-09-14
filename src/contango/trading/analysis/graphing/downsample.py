from __future__ import annotations


def downsample_curve(
    curve: tuple[tuple[int, float], ...],
    max_points: int = 1500,
) -> tuple[tuple[int, float], ...]:
    """
    Reduces a  curve to at most `max_points` points via
    fixed stride sampling, always keeping the final point.

    Args:
        curve: The raw (timestamp, value) points, in order.
        max_points: The maximum number of points to keep.

    Returns:
        The downsampled curve. Returned unchanged if already within max_points.
    """
    if len(curve) <= max_points:
        return curve

    step = len(curve) / max_points
    indices = [int(i * step) for i in range(max_points)]
    if indices[-1] != len(curve) - 1:
        indices.append(len(curve) - 1)

    return tuple(curve[i] for i in indices)
