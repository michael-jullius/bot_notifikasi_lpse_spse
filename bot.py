import mysql.connector
from bs4 import BeautifulSoup
import requests
import time
import smtplib

# stated program
print('start')

# function send telegram


def send(id, bot_message):
    bot_token = ''
    bot_chatID = id
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def send_pu(id, bot_message):
    bot_token = ''
    bot_chatID = id
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


# define base db
# db defaut
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='bot',
)


# db for status
def status():
    db_status = db
    cursor_status = db_status.cursor()
    cursor_status.execute("INSERT INTO `status` (`status`) VALUES ('sukses')")
    db_status.commit()
    cursor_status.close()


# db for error log
def error_log(error):
    db_error_log = db
    cursor_error_log = db_error_log.cursor()
    cursor_error_log.execute(
        "INSERT INTO `error_log` (`name_error`, `create_at`) VALUES ('{}', CURRENT_TIME())".format(error))
    db_error_log.commit()
    cursor_error_log.close()


# db for list url
def url():
    db_url = db
    cursor_url = db_url.cursor()
    cursor_url.execute("SELECT url FROM url")
    url.link = cursor_url.fetchall()
    cursor_url.close()


# get last loop id from db
cursor = db.cursor()
sql = "SELECT loop_id FROM data ORDER BY id DESC LIMIT 1"
cursor.execute(sql)
now = cursor.fetchall()
cursor.close()


# set default value index
i = 0
for i in now:
    i = i[0]
i = int(i)


def fetch_data(data, uri):
    # check data Pekerjaan_Kontruksi null or not
    if data != []:

        # get all data from table data
        cursor = db.cursor()
        sql = "SELECT * FROM data"
        cursor.execute(sql)
        cek = cursor.fetchall()
        cursor.close()

        # logging
        error_log('cek data error')

        # check before data from db null or not
        if cek == []:

            # logging
            error_log('insert data first time error')

            # looping
            for d in data:
                # find specific data from resource page
                nama = d.find('a').text
                biaya = d.find('td', class_='table-hps').text
                waktu = d.find('td', class_='center').text
                loop = i
                # insert data to db
                cursor = db.cursor()
                sql = "INSERT INTO data (loop_id, nama, harga, tanggal, url, create_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIME())"
                val = (loop, nama, biaya, waktu, uri)
                cursor.execute(sql, val)

                # submit/push
                db.commit()
                cursor.close()

                # send massage to telegram
                cursor = db.cursor()
                sql = "SELECT id_user FROM `user`"
                cursor.execute(sql)
                user = cursor.fetchall()
                cursor.close()
                if user == []:
                    time.sleep(1)
                else:
                    for us in user:
                        send('{}'.format(us[0]), 'ada perubahan di lpse {} dengan pekerjaan {} {}'.format(
                            uri, nama, biaya))

        else:
            # logging
            error_log('insert data error')

            # looping
            for d in data:
                # find specific data from resource page
                nama = d.find('a').text
                biaya = d.find('td', class_='table-hps').text
                waktu = d.find('td', class_='center').text
                loop = i

                # insert data to db
                cursor = db.cursor()
                sql = "INSERT INTO data (loop_id, nama, harga, tanggal, url, create_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIME())"
                val = (loop, nama, biaya, waktu, uri)
                cursor.execute(sql, val)

                db.commit()
                cursor.close()

    time.sleep(1)


# main function
def bot_notif(uri, i):
    # logging
    error_log('page request error')

    # get page resource
    page = requests.get("{}".format(uri), verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')

    # check status running or not and insert to db status
    status()

    # find all div like Pekerjaan_Kontruksi
    data_konsultan = soup.find_all(
        'tr', class_='Jasa_Konsultansi_Badan_Usaha_Non_Konstruksi')
    data = soup.find_all('tr', class_='Pekerjaan_Konstruksi')

    # logging
    error_log('find data error')

    data_list = [data, data_konsultan]
    # check data Pekerjaan_Kontruksi null or not
    for open_data in data_list:
        fetch_data(open_data, uri)

    time.sleep(5)


# infinity loop
while True:

    # call db url
    url()

    # declare index in loop with + 1
    i += 1

    # loop link and call function bot_notif
    link = url.link
    for index in range(len(link)):
        try:
            bot_notif('{}'.format(link[index][0]), i)
        except:
            print('An exception occurred')

    # logging
    error_log('get new data error')

    # get new data from db
    cursor = db.cursor()
    sql = "SELECT nama, harga, url FROM data WHERE loop_id = %s"
    adr = (i,)
    cursor.execute(sql, adr)
    now = cursor.fetchall()
    cursor.close()

    # logging
    error_log('get last data error')

    # get before data from db
    l = i-1
    cursor = db.cursor()
    sql = "SELECT nama,harga,url FROM data WHERE loop_id = %s"
    adr = (l,)
    cursor.execute(sql, adr)
    last = cursor.fetchall()
    cursor.close()

    # logging
    error_log('delete data error')

    # delete data result from looping 3
    cursor = db.cursor()
    de = i-2
    sql = "DELETE FROM data WHERE loop_id = %s"
    adr = (de,)
    cursor.execute(sql, adr)
    db.commit()
    cursor.close()

    # logging
    error_log('cek same data error')

    # checking data same or not
    # declare variable last and new
    a = now
    b = last

    # loop data and check where data not same and send to telegram
    for last in a:
        dt = False
        for new in b:
            if last != new:
                continue
            else:
                if last == new:
                    dt = True

                else:
                    dt = False
        if dt == True:
            continue
        else:
            cursor = db.cursor()
            sql = "SELECT id_user FROM `user`"
            cursor.execute(sql)
            user = cursor.fetchall()
            cursor.close()
            if user == []:
                time.sleep(1)
            else:
                if last[2] == 'https://lpse.lampungtengahkab.go.id/eproc4' or last[2] == 'http://lpse.metrokota.go.id/eproc4':
                    for us in user:
                        send('{}'.format(
                            us[0]), 'ada perubahan di lpse dengan pekerjaan {}'.format(last))
                elif last[2] == 'https://lpse.pu.go.id/':
                    cursor = db.cursor()
                    sql = "SELECT id_user FROM `user`"
                    cursor.execute(sql)
                    user_pu = cursor.fetchall()
                    cursor.close()
                    if user == []:
                        time.sleep(1)
                    else:
                        for us in user_pu:
                            send_pu('{}'.format(
                                us[0]), 'ada perubahan di lpse dengan pekerjaan {}'.format(last))
                else:
                    for us in user:
                        if us[0] == 1249554282:
                            time.sleep(1)
                        else:
                            send('{}'.format(
                                us[0]), 'ada perubahan di lpse dengan pekerjaan {}'.format(last))
    cursor.close()
    # logging
    error_log('while error')
    # delay per loop
    time.sleep(120)

    # delay per loop
    time.sleep(120)
    continue
