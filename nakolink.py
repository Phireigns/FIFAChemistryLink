import tkinter as tk
import json

def calculate_chemistry(nation1, nation2, league1, league2, club1, club2):
    chemistry = 0

    # Check if players have the same nation
    if nation1 == nation2:
        chemistry += 1

    # Check if players have the same league
    if league1 == league2:
        chemistry += 1

    # Check if players have the same club
    if club1 == club2:
        chemistry += 1

    return chemistry

def calculate_button_click():
    players.clear()

    for i in range(num_players):
        player_name = player_entries[i].get().strip()
        player_nation = nation_entries[i].get().strip()
        player_league = league_entries[i].get().strip()
        player_club = club_entries[i].get().strip()

        if not player_name or not player_nation or not player_league or not player_club:
            result_label.config(text=f"Invalid data for Player {i+1}.")
            return

        players.append((player_name, player_nation, player_league, player_club))

    total_chemistry = 0
    chemistry_results = []

    for i in range(num_players):
        for j in range(i + 1, num_players):
            player1 = players[i]
            player2 = players[j]
            chemistry = calculate_chemistry(player1[1], player2[1], player1[2], player2[2], player1[3], player2[3])
            total_chemistry += chemistry
            chemistry_results.append(f"{player1[0]} and {player2[0]}: {chemistry}")

    result_label.config(text="\n".join(chemistry_results))

    green_players = 0
    yellow_players = 0
    player_marks = []

    for player in players:
        player_name = player[0]
        player_points = sum(
            calculate_chemistry(player[1], p[1], player[2], p[2], player[3], p[3]) for p in players if p != player
        )

        if player_points >= 5:
            player_marks.append(f"{player_name}: Green")
            green_players += 1
        elif player_points == 4:
            player_marks.append(f"{player_name}: Yellow")
            yellow_players += 1
        else:
            player_marks.append(f"{player_name}: Red")

    player_marks.append("")

    if (
        green_players >= 9
        or (green_players == 8 and yellow_players >= 2)
        or (green_players == 7 and yellow_players >= 3)
        or (green_players == 6 and yellow_players >= 4)
        or (green_players == 5 and yellow_players == 6)
        or (green_players == 4 and yellow_players == 7)
    ):
        player_marks.append("Perfect team chemistry!")
    else:
        player_marks.append("Bad team chemistry!")
    result_label.config(text="\n".join(player_marks))

def clear_button_click():
    for i in range(num_players):
        player_entries[i].delete(0, tk.END)
        nation_entries[i].delete(0, tk.END)
        league_entries[i].delete(0, tk.END)
        club_entries[i].delete(0, tk.END)
    result_label.config(text="")

# Load saved data (if any)
def load_data():
    try:
        with open("player_data.json", "r") as file:
            data = json.load(file)
            for i in range(num_players):
                player_entries[i].insert(0, data[i]["name"])
                nation_entries[i].insert(0, data[i]["nation"])
                league_entries[i].insert(0, data[i]["league"])
                club_entries[i].insert(0, data[i]["club"])
    except FileNotFoundError:
        pass

# Save data before closing the program
def save_data():
    data = []
    for i in range(num_players):
        player_data = {
            "name": player_entries[i].get().strip(),
            "nation": nation_entries[i].get().strip(),
            "league": league_entries[i].get().strip(),
            "club": club_entries[i].get().strip()
        }
        data.append(player_data)

    with open("player_data.json", "w") as file:
        json.dump(data, file)


# GUI setup
window = tk.Tk()
window.title("NakoLink")
window.iconbitmap("nakolink.ico")

num_players = 11
players = []

player_entries = []
nation_entries = []
league_entries = []
club_entries = []

playerNames_label = tk.Label(window, text="Player Name:")
playerNames_label.grid(row=0, column=0, padx=5, pady=5)
nationNames_label = tk.Label(window, text="Nation:")
nationNames_label.grid(row=0, column=1, padx=5, pady=5)
leagueNames_label = tk.Label(window, text="League:")
leagueNames_label.grid(row=0, column=2, padx=5, pady=5)
clubNames_label = tk.Label(window, text="Club:")
clubNames_label.grid(row=0, column=3, padx=5, pady=5)

for i in range(num_players):

    player_entry = tk.Entry(window)
    player_entry.grid(row=i+1, column=0)
    player_entries.append(player_entry)

    nation_entry = tk.Entry(window)
    nation_entry.grid(row=i+1, column=1)
    nation_entries.append(nation_entry)

    league_entry = tk.Entry(window)
    league_entry.grid(row=i+1, column=2)
    league_entries.append(league_entry)

    club_entry = tk.Entry(window)
    club_entry.grid(row=i+1, column=3)
    club_entries.append(club_entry)

calculate_button = tk.Button(window, text="Calculate",bg='#006600', fg='#FFF', command=calculate_button_click)
calculate_button.grid(row=num_players + 1,column=0, columnspan=2, pady=0)

clear_button = tk.Button(window, text="Clear",bg='#FF6633', fg='#FFF', command=clear_button_click)
clear_button.grid(row=num_players + 1, column=2, columnspan=2, pady=10)

result_label = tk.Label(window, text="")
result_label.grid(row=num_players + 2, column=0, columnspan=8)

# Load data when the program starts
load_data()

def save_data_and_close_window():
    save_data()
    window.destroy()

# Bind the event handler to the window close event
window.protocol("WM_DELETE_WINDOW", save_data_and_close_window)

window.mainloop()
