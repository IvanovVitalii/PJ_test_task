import json
import sqlite3
import datetime

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

with open('users.json', 'r') as f:
    users = json.load(f)

user_ = []
z = []
for user in users:
    for value in user.values():
        z.append(value)
    user_.append(z)
    z = []

cursor.executemany("INSERT INTO statistic_user VALUES (?,?,?,?,?,?)", user_)
conn.commit()

with open('users_statistic.json', 'r') as f:
    users_statistic = json.load(f)

statistic = []
z = []
_id = 1
for i in users_statistic:
    date = datetime.datetime.strptime(i['date'], '%Y-%m-%d')
    z.append(_id)
    z.append(i['user_id'])
    z.append(date)
    z.append(i['page_views'])
    z.append(i['clicks'])
    statistic.append(z)
    _id += 1
    z = []


cursor.executemany("INSERT INTO statistic_statistic VALUES (?,?,?,?,?)", statistic)
conn.commit()


'''
SELECT statistic_user.id, statistic_user.first_name, statistic_statistic.clicks
FROM statistic_user
INNER JOIN statistic_statistic ON statistic_user.id=statistic_statistic.user_id
WHERE statistic_user.id = 1
'''