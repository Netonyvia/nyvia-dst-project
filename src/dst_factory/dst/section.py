from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DSTSection:
    name: str
    prompt_path: Path
    output_path: Path