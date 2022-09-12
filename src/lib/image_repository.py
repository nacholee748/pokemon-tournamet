from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd

@dataclass
class DownloadableCharacter:
    name: str
    url: str

class ImageRepository:
    def __init__(self, characters: Sequence[DownloadableCharacter]) -> None:
        # self._characters = dowload_and_save_all_pokemons(characters)
        self._characters = characters

    def retrieve(self, name: str) -> np.ndarray:
        df_images = pd.DataFrame(self._characters)
        return df_images[df_images['name']==name]['url'].values[0]
