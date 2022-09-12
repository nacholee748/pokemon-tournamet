from pathlib import Path
from typing import Dict, Iterator, Protocol, Tuple

import pandas as pd  # type: ignore
import streamlit as st

from lib.pokemon import Pokemon
from lib.summary import Summary
from lib.tournament import Tournament
from lib.image_repository import ImageRepository, DownloadableCharacter
from lib.reporting import Reporter


def main(workdir) -> None:
    st.markdown("<h1 style='text-align: center; color: white;font-size:90px'>"+ 'pokemon final tournament'.upper() +"</h1>", unsafe_allow_html=True)
    st.subheader('All generations are considered in this outstanding event')

    st.write("Upload the files with all Pokemon data")

    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("http://vignette1.wikia.nocookie.net/yuyuhakusho/images/f/fe/Vlcsnap-2011-03-27-20h49m55s57.jpg/revision/latest?cb=20110328015036");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

    files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    if files:
        matches_section = st.container()
        matches_section.markdown("<h2 style='color: black;font-size:60px'>"+ "Tournament's matches" +"</h2>", unsafe_allow_html=True)
        summary_section = st.container()
        summary_section.markdown("<h2 style='color: black;font-size:60px'>"+ "Tournament Summary" +"</h2>", unsafe_allow_html=True)

        participants, download_data = zip(*_load_participants_and_download_data(files))
        tournament = Tournament(participants=participants, num_arenas=4)
        image_repository = ImageRepository(download_data)
        reporter = Reporter(workdir)

        stage = 0
        while tournament.next_matches:
            stage += 1
            expander = matches_section.expander(f"Matches at stage {stage}")
            expander.write(
                f"There were {len(tournament.next_matches)} matches at this stage"
            )
            tabs = expander.tabs(
                [f"Match {i}" for i in range(len(tournament.next_matches))]
            )
            for t, m in zip(tabs, tournament.next_matches):
                with t:
                    t.header(f"Match between {m[0].name} and {m[1].name}")
                    col1, col2 = t.columns(2)
                    with col1:
                        if m[0].generation=="gen1":
                            st.header(f"{m[0].name}: This Pokemon belongs to Gen1")
                            st.image(image_repository.retrieve(m[0].name))
                        elif m[0].generation=="gen2":
                            st.header(f"{m[0].name}: This Pokemon belongs to Gen2")
                            st.image(image_repository.retrieve(m[0].name))
                        elif m[0].generation=="gen3":
                            st.header(f"{m[0].name}: This Pokemon belongs to Gen3")
                            st.image(image_repository.retrieve(m[0].name))
                        elif m[0].generation=="gen4":
                            st.header(f"{m[0].name}: This Pokemon belongs to Gen4")
                            st.image(image_repository.retrieve(m[0].name))
                        elif m[0].generation=="gen5":
                            st.header(f"{m[0].name}: This Pokemon belongs to Gen5")
                            st.image(image_repository.retrieve(m[0].name))
                        else:
                            st.header(f"{m[0].name}: This Pokemon belongs to Gen6")
                            st.image(image_repository.retrieve(m[0].name))
                    with col2:
                        if m[1].generation=="gen1":
                            st.header(f"{m[1].name}: This Pokemon belongs to Gen1")
                            st.image(image_repository.retrieve(m[1].name))
                        elif m[1].generation=="gen2":
                            st.header(f"{m[1].name}: This Pokemon belongs to Gen2")
                            st.image(image_repository.retrieve(m[1].name))
                        elif m[1].generation=="gen3":
                            st.header(f"{m[1].name}: This Pokemon belongs to Gen3")
                            st.image(image_repository.retrieve(m[1].name))
                        elif m[1].generation=="gen4":
                            st.header(f"{m[1].name}: This Pokemon belongs to Gen4")
                            st.image(image_repository.retrieve(m[1].name))
                        elif m[1].generation=="gen5":
                            st.header(f"{m[1].name}: This Pokemon belongs to Gen5")
                            st.image(image_repository.retrieve(m[1].name))
                        else:
                            st.header(f"{m[1].name}: This Pokemon belongs to Gen6")
                            st.image(image_repository.retrieve(m[1].name))
            with st.spinner(f"Running stage {stage}"):
                results = tournament.run_stage()
            reporter.update(stage=stage, results=results)
        summary = Summary(participants, reporter)
        with summary_section.container():
            st.write("End result")
            col1, col2, col3 = st.columns(3)
            col1.metric("Number of participants", summary.num_paticipants)
            col3.image(
                image_repository.retrieve(summary.most_endurance),
                caption=f"Most endurance: {summary.most_endurance}",
            )
            col2.image(
                image_repository.retrieve(summary.champion),
                caption=f"Champion: {summary.champion}",
            )

        with summary_section.container():
            st.write("High level summary")
            col1, col2, col3, col4 = summary_section.columns(4)
            col1.write(f"Top ability: {summary.most_common_ability_used_in_battle}")
            col2.write(f"Top type: {summary.strongest_type}")
            col3.write(f"Top generation: {summary.strongest_generation}")
            col4.write(f"Max rounds: {summary.max_rounds_in_tournament}")

        with summary_section.container():
            st.markdown("<h2 style='color: white;font-size:40px'>"+ "Statistics per type" +"</h2>", unsafe_allow_html=True)
            st.bar_chart(
                _prepare_for_barplot(summary.participants_per_type, "Num participants")
            )
            st.markdown("<h2 style='color: white;font-size:40px'>"+ "Best 50 participants per type" +"</h2>", unsafe_allow_html=True)
            st.bar_chart(
                _prepare_for_barplot(summary.in_top_fifty_per_type, "Amount in top 50")
            )

        with summary_section.container():
            st.markdown("<h2 style='color: white;font-size:40px'>"+ "Statistics per generation" +"</h2>", unsafe_allow_html=True)
            st.bar_chart(
                _prepare_for_barplot(
                    summary.in_top_fifty_per_generation, "Amount in top 50"
                )
            )

def _prepare_for_barplot(input: Dict[str, int], name_for_values: str) -> pd.DataFrame:
    index, values = zip(*input.items())
    return pd.DataFrame({name_for_values: values}, index=index)

class _File(Protocol):
    name: str

    def read(self) -> bytes:
        ...


def _load_participants_and_download_data(
    files,
) -> Iterator[Tuple[Pokemon, DownloadableCharacter]]:
    for f in files:
        generation = f.name.split("-")[1]
        df = pd.read_csv(f)
        for row in df.itertuples():
            abilities = {row.Ability1, row.Ability2, row.Ability3}
            if "none" in abilities:
                abilities.remove("none")
            p = Pokemon(
                name=row.Pokemon,
                type=row.Type1,
                generation=generation,
                abilities=tuple(abilities),
                health_points=row.HP,
                attack=row.Attack,
                defense=row.Defense,
                speed=row.Speed,
            )
            c = DownloadableCharacter(name=row.Pokemon, url=row.Sprite)
            yield p, c


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="This app lists animals")

    parser.add_argument(
        "--workdir",
        type=Path,
        default="./pokemon-tournament",
        help="Working directory for the application",
    )

    args = parser.parse_args()
    main(args.workdir)
