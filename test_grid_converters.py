import pytest
from game import pixels_to_grid, grid_to_pixels

H = 10
W = 10
GRID_SIZE = 10


@pytest.mark.parametrize(
    "coords,expected",
    [[(0, 0), (0, 1)], [(W, 0), (1, 1)], [(0, H), (0, 0)], [(W, H), (1, 0)]],
)
def test_it_converts_from_pixels_to_grid(coords, expected):
    assert pixels_to_grid(*coords, max_y=H, grid_size=GRID_SIZE) == expected


@pytest.mark.parametrize(
    "coords,expected",
    [[(0, 0), (0, H)], [(1, 0), (W, H)], [(0, 1), (0, 0)], [(1, 1), (W, 0)],],
)
def test_it_converts_from_grid_to_pixels(coords, expected):
    assert grid_to_pixels(*coords, max_y=H, grid_size=GRID_SIZE) == expected


@pytest.mark.parametrize("coords", [(0, 0), (0, H), (W, 0), (W, H)])
def test_conversions_are_stable(coords):
    assert (
        grid_to_pixels(
            *pixels_to_grid(*coords, max_y=H, grid_size=GRID_SIZE),
            max_y=H,
            grid_size=GRID_SIZE
        )
        == coords
    )
