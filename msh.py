import mysql.connector
import requests
import time


db = mysql.connector.connect(
        host='103.160.62.181',
        user='roiputra',
        password='Oj0dum3h**',
        database='bot'
)
cursor = db.cursor()

def send(id,bot_message):
    
   bot_token = '5349581892:AAHAvB8ruYWlRaaHrbvgmJ4MW2g0D6agE50'
   bot_chatID = id
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()
 


def user_log(id, id_user, nama, massage):
    sql = "SELECT id FROM `user_log` WHERE id_user = %s ORDER BY id DESC LIMIT 1"
    adr = (id_user,)
    cursor.execute(sql, adr)
    id_chat = cursor.fetchall()
    if id_chat == []:
        sql = "INSERT INTO `user_log` (`id`, `id_user`, `nama`, `massage`) VALUES (%s, %s, %s, %s)"
        val = id, id_user, nama, massage
        cursor.execute(sql, val)
        db.commit()
        user_log.chat_status = False
    else:
        if id_chat[0][0] == id:
            time.sleep(1)
            user_log.chat_status = True
        else:
            sql = "INSERT INTO `user_log` (`id`, `id_user`, `nama`, `massage`) VALUES (%s, %s, %s, %s)"
            val = id, id_user, nama, massage
            cursor.execute(sql, val)
            db.commit()
            user_log.chat_status = False




def get_massage():
    reg = requests.get('https://api.telegram.org/bot5349581892:AAHAvB8ruYWlRaaHrbvgmJ4MW2g0D6agE50/getUpdates')
    raw_data = reg.json()
    if raw_data['result'] == []:
        get_massage.chat_status = True
        time.sleep(10)
    else:
        max = len(raw_data['result'])
        data = raw_data['result'][max-1]['message']
        get_massage.id_massage = data['message_id']
        get_massage.id = data['from']['id']
        if 'last_name' in data:
            get_massage.name =  data['from']['first_name']+ ' '+data['from']['last_name']
        else:
            get_massage.name = data['from']['first_name']
        get_massage.chat = data['text']
        user_log(get_massage.id_massage, get_massage.id, get_massage.name, get_massage.chat)
        get_massage.chat_status = user_log.chat_status
        



def register(id_user, nama):
    sql = "SELECT id_user FROM `user` WHERE id_user = %s"
    adr = (id_user,)
    cursor.execute(sql, adr)
    user = cursor.fetchall()
    if user == []:
        get_massage()
        sql = "INSERT INTO `user` (`nama`, `id_user`) VALUES (%s,%s);"
        val = nama, id_user
        cursor.execute(sql, val)
        db.commit()
        send(id_user, 'selamat anda berhasil mendaftar')
    else:
        if user[0][0] == id_user:
            time.sleep(1)
        else:
            sql = "INSERT INTO `user` (`nama`, `id_user`) VALUES (%s,%s);"
            val = nama, id_user
            cursor.execute(sql, val)
            db.commit() 
            send(id_user, 'selamat {} berhasil mendaftar'.format(nama))
            
            
def list_url(id):
    sql = "SELECT `url` FROM `url`"
    cursor.execute(sql)
    url = cursor.fetchall()
    s = ''
    for u in url:
        s += '{} \n \n'.format(u[0])
    send(id, s)
    

def sta(id):
    sql = "SELECT `status` FROM `status`"
    cursor.execute(sql)
    status = cursor.fetchall()
    for st in status:
        text = st[0]
    send(id, text)
    
def userList(id):
    sql = "SELECT nama FROM `user`"
    cursor.execute(sql)
    user = cursor.fetchall()
    s = ''
    for u in user:
        s += '{} \n'.format(u[0])
    send(id, s)

    
           
while True:
    try:
        time.sleep(1)
        get_massage()
        status = False
        
        if get_massage.chat_status == True:
            continue
        else:
            if get_massage.chat == '/start' or  get_massage.chat == '/menu':
                if get_massage.id == 1270328028 or get_massage.id == 1952593695:
                    menu = """
                    halo selamat datang {}
                    /menu
                    /status
                    /userList
                    /urlList
                    """.format(get_massage.name)
                    send('{}'.format(get_massage.id), menu)
                else:
                    menu = """
                    halo selamat datang {}
                            
                    bila ada yang ingin ditanya
                    silahkan hubungi no di bawah ini 
                    0895600904600
                            
                    bila bot tidak membalas tunggu 5 menit 
                    karena bot akan tertidur,
                    jika tidak di gunakan dalam waktu yang lama.
                            """.format(get_massage.name)
                    send('{}'.format(get_massage.id), menu)
                    
            elif get_massage.chat == '/register':
                
                register("{}".format(get_massage.id) , get_massage.name)
            
            elif get_massage.chat == '/urlList':
                
                list_url('{}'.format(get_massage.id),)
            
            elif get_massage.chat == '/status':
                
                sta('{}'.format(get_massage.id))
            
            elif get_massage.chat == '/userList':
                
                userList('{}'.format(get_massage.id))
                
            else:
                send('{}'.format(get_massage.id), 'input tidak di ketahui')
    
    except:
        time.sleep(3)
        continue            
    
                