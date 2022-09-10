from dataclasses import dataclass
from typing import Sequence

import numpy as np

@dataclass
class DownloadableCharacter:
    name: str
    url: str

class ImageRepository:
    def __init__(self, characters: Sequence[DownloadableCharacter]) -> None:
        raise NotImplementedError

    def retrieve(self, name: str) -> np.ndarray:
        raise NotImplementedError