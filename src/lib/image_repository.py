from dataclasses import dataclass
from typing import Sequence
# import requests
# import threading
# import concurrent.futures
# from PIL import Image
# import os

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


    # def retrieve(self, name: str) -> np.ndarray:
    #     filepath = os.path.join('./', name + ".png")
    #     image_url_binary = self._characters[name]
    #     with open(filepath, mode="wb") as f:
    #         f.write(image_url_binary)

    #     retrived_image = Image.open(filepath)
    #     return np.asanyarray(retrived_image)

# def download_and_save_pokemon(session, pokemon):
#     """Download and save a single pokemon."""
#     content = None
#     with session.get(pokemon.url) as response:
#         content = response.content
#     return content

# def dowload_and_save_all_pokemons(pokemons):
#     """Download and save all pokemons using a sequentially."""
#     pokemon_image = {}
#     with requests.Session() as session:
#         for p in pokemons:
#             pokemon_image[p.name] = download_and_save_pokemon(session, p)
#     return pokemon_image


# pokemnos = [DownloadableCharacter(name='Bulbasaur', url='https://play.pokemonshowdown.com/sprites/bw/bulbasaur.png'),
#             DownloadableCharacter(name='Ivysaur', url='https://play.pokemonshowdown.com/sprites/bw/ivysaur.png'),
#             DownloadableCharacter(name='Venusaur', url='https://play.pokemonshowdown.com/sprites/bw/venusaur.png'),
#             DownloadableCharacter(name='Charmander', url='https://play.pokemonshowdown.com/sprites/bw/charmander.png'),
#             DownloadableCharacter(name='Charmeleon', url='https://play.pokemonshowdown.com/sprites/bw/charmeleon.png'),
#             DownloadableCharacter(name='Charizard', url='https://play.pokemonshowdown.com/sprites/bw/charizard.png')]

# a = dowload_and_save_all_pokemons(pokemnos)
############### Thread
# thread_local =  threading.local()

# def get_session():
#     if not hasattr(thread_local, "thread_session"):
#         thread_local.thread_session = requests.Session()
#     return thread_local.thread_session

# def download_and_save_pokemon(pokemon):
#     """Download and save pokemon using threading process."""
#     session = get_session()
#     with session.get(pokemon.url) as response:
#         if response.status_code == 200:
#             yield [pokemon.name,response.content]
#         else:
#             yield [pokemon.name,"not found"]

# def dowload_and_save_all_pokemons(self):
#     """Download and save all pokemons using a threading."""
#     map_iterable = ((pokemon) for pokemon in self)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         future = executor.map(download_and_save_pokemon,map_iterable)

#     return future