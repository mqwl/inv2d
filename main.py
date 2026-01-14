import sql


db_name = input("Enter database name: ")
con = sql.sqlite3.connect(db_name)
sql.init_db(con)
sql.print_db_info(con)
con.close()
