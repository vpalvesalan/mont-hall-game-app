import streamlit as st
import random
from PIL import Image

# Load door images
door_closed = Image.open("door_closed.png")
door_open_goat = Image.open("door_open_goat.png")
door_open_car = Image.open("door_open_car.png")

# Title of the app
st.title("Jogo de Monty Hall")

# Instructions
st.write("""
Bem-vindo ao Problema de Monty Hall!

1. Existem 3 portas: Porta 1, Porta 2 e Porta 3.
2. Atrás de uma das portas há um carro e, atrás das outras duas, há bodes.
3. Escolha uma porta e decida se quer trocar de porta depois que uma cabra for revelada.
""")

# Player selects a door using clickable images
st.write("Escolha uma porta:")
col1, col2, col3 = st.columns(3)

# Placeholder to track player's choice
door_choice = None

with col1:
    if st.image(door_closed, caption="Porta 1", use_column_width=True, output_format="PNG"):
        door_choice = 1
with col2:
    if st.image(door_closed, caption="Porta 2", use_column_width=True, output_format="PNG"):
        door_choice = 2
with col3:
    if st.image(door_closed, caption="Porta 3", use_column_width=True, output_format="PNG"):
        door_choice = 3

# Player decides whether to switch
switch = st.radio("Você quer trocar de porta depois que uma for revelada?", ["Sim", "Não"])

# Button to play the game
if st.button("Play"):
    if door_choice is None:
        st.warning("Você precisa escolher uma porta antes de jogar!")
    else:
        # Set up the game
        doors = ["bode", "bode", "carro"]
        random.shuffle(doors)  # Randomly place the carro behind one door

        # Player's initial choice (0-based index)
        player_choice_index = door_choice - 1

        # Host opens a door that is not the player's choice and has a bode
        host_opens_index = next(i for i in range(3) if i != player_choice_index and doors[i] == "bode")

        # If the player chooses to switch, update their choice
        if switch == "Sim":
            player_choice_index = next(i for i in range(3) if i != player_choice_index and i != host_opens_index)

        # Determine the result
        result = doors[player_choice_index]

        # Display the results
        st.write(f"Você escolheu a porta {door_choice}.")
        st.write(f"O apresentador abriu a Porta {host_opens_index + 1}, que tem um bode.")
        st.write(f"Você {'trocou para' if switch == 'Sim' else 'ficou com a'} Porta {player_choice_index + 1}.")

        # Display the doors with the revealed content
        st.write("Resultado final:")
        col1, col2, col3 = st.columns(3)
        for i in range(3):
            if i == host_opens_index:
                with col1 if i == 0 else col2 if i == 1 else col3:
                    st.image(door_open_goat, caption=f"Porta {i + 1} (Bode)")
            elif i == player_choice_index:
                with col1 if i == 0 else col2 if i == 1 else col3:
                    if result == "carro":
                        st.image(door_open_car, caption=f"Porta {i + 1} (Carro)")
                    else:
                        st.image(door_open_goat, caption=f"Porta {i + 1} (Bode)")
            else:
                with col1 if i == 0 else col2 if i == 1 else col3:
                    st.image(door_closed, caption=f"Porta {i + 1}")

        if result == "carro":
            st.success("Parabéns, você ganhou um carro! 🎉")
        else:
            st.error("Não foi dessa vez, você ganhou um bode. 🐐")
