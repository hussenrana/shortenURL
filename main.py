import mysql.connector
import hashlib
map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#function to convert id to short url using map we define with base 62
def idToShortURL(id):

    shortURL = ""
    if id == 0 :
        return "a"
    # for each digit find the base 62
    while (id > 0):
        shortURL += map[id % 62]
        id //= 62
    return shortURL[::-1]



#function to convert url to id by using algorithm until we move all over the characters till get the id
def URLToId(shortURL):
    id = 0
    for i in shortURL:
        val_i = ord(i)
        if (val_i >= ord('a') and val_i <= ord('z')):
            id = id * 62 + val_i - ord('a')
        elif (val_i >= ord('A') and val_i <= ord('Z')):
            id = id * 62 + val_i - ord('A') + 26
        else:
            id = id * 62 + val_i - ord('0') + 52
    return id
#function to handle all over the connection in data base
def ConnectToDB():
    try:
        connection=mysql.connector.connect(
            host="b39pjqvxy6ddkgcf5qwu-mysql.services.clever-cloud.com",
            user="uecz3fzsqf8nap2g",
            password="0E0c7SI3aemdP0iZdryd",
            database="b39pjqvxy6ddkgcf5qwu")

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
    return connection

def CheckIdinDB(connection,id):
    cursor = connection.cursor()
    sql_select_query = """select * from websites where id = %s"""
    # set variable in query
    cursor.execute(sql_select_query, (id,))
    # fetch result
    record = cursor.fetchall()
    if len(record)==0:
        return False
    return record

def SaveIdinDB(connection,id):
    cursor = connection.cursor()
    mySql_insert_query = "INSERT INTO websites (id,originalURL,shortURL) VALUES (%s,%s, %s)"
    shortURL=idToShortURL(int(id))
    val = (str(id), URL,"http://"+shortURL+".com")
    cursor.execute(mySql_insert_query, val)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into Laptop table")
    cursor.close()
    return shortURL
#two options to convert that user can choose betweem two cases
def LongURLToShort(URL):
    connection=ConnectToDB()
    id=str(hash(URL))[1:13]
    result=CheckIdinDB(connection,id)
    print(result)
    if result==False:
        shortURL=SaveIdinDB(connection,id)
    else:
        shortURL=result[0][2]
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
    return "http://"+shortURL+".com"

def sanity_check(loops=1):
    import random
    import cowsay
    rand_url = ""
    for i in range(loops):
        for char in range(random.randint(1, 10)):
            rand_url += random.choice(map)
        #rand_url = "1"
        print("generated URL is {0}".format(rand_url))
        expected_id = URLToId(rand_url)
        print("expected id is {0}".format(expected_id))
        actual_url = idToShortURL(expected_id)
        print("actual is {0}".format(actual_url))
        if rand_url != actual_url:
            cowsay.daemon("fail !!!! check following URL {0}, id is {1} , actual URL is {2}".format(rand_url, expected_id, actual_url))
        else:
            cowsay.daemon("passed!! {0} == {1}".format(rand_url, actual_url))





Descision=input("To short URL: Click 1\nTo reach for existing URL Click 2\n")
URL=input("Please Enter your URL: ")
if len(URL)>500:
    print("Your URL is length is out of range")
    exit(1)
if URL[0:7]!="http://":
    print("URL must start with http://")
    exit(1)
if Descision=='1':
   print("Your Short URL is: "+LongURLToShort(URL))
elif Descision=='2':
    connection = ConnectToDB()
    result = CheckIdinDB(connection, URLToId(URL[7:len(URL)-4]))
    if result == False:
        print("404: Page not found")
    else:
        print("You have reached to page: " + result[0][0])
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
#In case you want to see the test cases you can run the sanity check below:
#sanity_check(10)




