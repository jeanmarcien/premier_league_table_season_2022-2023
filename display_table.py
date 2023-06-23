import sqlite3
import tkinter as tk
from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title('Premier League Table')

# Create a Treeview widget
table = ttk.Treeview(window)

# Define columns for the table
table['columns'] = ('name', 'gamesPlayed', 'wins', 'ties', 'losses', 'goalsFor', 'goalsAgainst', 'goalDifference',
                    'points')

# Format column headers
table.heading('#0', text='Rank')
table.heading('name', text='CLUB')
table.heading('gamesPlayed', text='MP')
table.heading('wins', text='W')
table.heading('ties', text='D')
table.heading('losses', text='L')
table.heading('goalsFor', text='GF')
table.heading('goalsAgainst', text='GA')
table.heading('goalDifference', text='GD')
table.heading('points', text='PTS')

# Connect to the SQLite database
conn = sqlite3.connect('results.db')
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT teams.id, teams.name, stats.gamesPlayed, stats.wins, stats.ties, stats.losses, stats.goalsFor, "
               "stats.goalsAgainst, stats.goalDifference, stats.points "
               "FROM teams "
               "INNER JOIN stats ON teams.id = stats.id")

# Fetch all the rows from the query result
rows = cursor.fetchall()

# Iterate over the rows and insert into the table
for row in rows:
    table.insert(parent='', index='end', text=row[0], values=row[1:])

# Define column widths and alignment
columns = ['#0', 'gamesPlayed', 'wins', 'ties', 'losses', 'goalsFor', 'goalsAgainst', 'goalDifference', 'points']
for column in columns:
    table.column(column, width=75, anchor='center')

# Configure the style of the table
style = ttk.Style()
style.configure('Treeview.Heading', font=('Arial', 12, 'bold'), foreground='black')
style.configure('Treeview', font=('Arial', 11), foreground='black', background='white')
table.tag_configure('top_four', background='lightblue')
table.tag_configure('top_six', background='purple')
table.tag_configure('top_seven', background='lightgray')
table.tag_configure('relegation', background='red')

# Apply tags to rows based on their position in the table
for i, item in enumerate(table.get_children()):
    if i < 4:
        table.item(item, tags=('top_four',))
    elif i < 6:
        table.item(item, tags=('top_six',))
    elif i < 7:
        table.item(item, tags=('top_seven',))
    elif i > 16:
        table.item(item, tags=('relegation',))

# Bind events to the tags
table.tag_bind('top_four', '<B1-Motion>', lambda event: table.selection_set(table.identify_row(event.y)))
table.tag_bind('top_six', '<B1-Motion>', lambda event: table.selection_set(table.identify_row(event.y)))
table.tag_bind('top_seven', '<B1-Motion>', lambda event: table.selection_set(table.identify_row(event.y)))

# Close the cursor and the database connection
cursor.close()
conn.close()

# Adjust the height of the Treeview to display all rows
table_height = len(rows) + 1  # +1 to account for the header row
table.configure(height=table_height)

# Display the table
table.pack()

# Start the GUI event loop
window.mainloop()
