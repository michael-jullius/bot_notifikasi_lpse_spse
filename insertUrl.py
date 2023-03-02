import mysql.connector

input_url = ''
url = ''


db_url = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='bot'
)
cursor_url = db_url.cursor()

while input_url != 'quit':
    print("""
          0.Menu
          1.input url
          2.keluar
          """)
    input_url = input("pilih nomor menu: ")
    
    if input_url == '0':
        print("""
          0.Menu
          1.input url
          2.keluar
          """)
    elif input_url == '1':
        url = input("masukan url: ")
        cursor_url.execute("INSERT INTO `url` (`url`) VALUES ('{}')".format(url))
        db_url.commit()
        
    elif input_url == '2':
        break
    else:
        print('masukan input yang benar')