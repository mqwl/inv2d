import sqlite3
import sql
from ui.app import App

con = sqlite3.connect("inv2d.db")
sql.init_db(con)

app = App(con)
app.mainloop()

con.commit()
con.close()
