import sql


db_name = input("Enter database name: ")
con = sql.sqlite3.connect(db_name)
sql.init_db(con)
while True:
    console = input('''
        Commands:
        Type 'p' to view DB structure
        Type 'q' to exit and save
        ''')
    if console == 'p':
        sql.print_db_info(con)
    elif console == 'q':
        con.close()
        break
