"""Display a headerless 16-bit detector frame."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


DEFAULT_FILE = Path(__file__).with_name(
    "frame_00000003_id_3_20260810T070644_484673874Z(1).raw"
)
DEFAULT_FILE_2 = Path(__file__).with_name("frame_00000004_id_4_20260810T070645_484487615Z.raw")
DEFAULT_WIDTH = 4024
DEFAULT_HEIGHT = 3036


def load_raw_frame(path: Path, width: int, height: int) -> np.ndarray:
    """Load a little-endian uint16 frame from a headerless raw file."""
    frame = np.fromfile(path, dtype="<u2")
    expected_samples = width * height
    if frame.size != expected_samples:
        raise ValueError(
            f"{path} contains {frame.size} uint16 samples, but "
            f"{width} x {height} requires {expected_samples}. "
            "Pass the correct --width and --height."
        )
    return frame.reshape((height, width))


def sortFile(pFile, pWidth, pHeight) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        default= pFile,
        help=f"headerless uint16 frame (default: {pFile.name})",
    )
    parser.add_argument("--width", type=int, default=pWidth)
    parser.add_argument("--height", type=int, default=pHeight)
    args = parser.parse_args()

    if not args.file.is_file():
        parser.error(f"file does not exist: {args.file}")
    if args.width <= 0 or args.height <= 0:
        parser.error("--width and --height must be positive")

    return args


def plotGraph(args):
    fig, ax = plt.subplots()
    image = ax.imshow(frame, cmap="gray", vmin=low, vmax=high)
    ax.set_title(args.file.name)
    ax.set_xlabel(f"{args.width} x {args.height} pixels, uint16")
    fig.colorbar(image, ax=ax, label="Pixel value")
    fig.tight_layout()
    plt.show()

args1 = sortFile(DEFAULT_FILE, DEFAULT_WIDTH, DEFAULT_HEIGHT)
args2 = sortFile(DEFAULT_FILE_2, DEFAULT_WIDTH, DEFAULT_HEIGHT)
frame = load_raw_frame(args1.file, args1.width, args1.height)
frame2 = load_raw_frame(args2.file, args2.width, args2.height)
low, high = np.percentile(frame, (1, 99))

plotGraph(args1)
plotGraph(args2)




