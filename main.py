import os
import time
import MySQLdb

tables = ('tbl_without_index', 'tbl_with_index')

db = MySQLdb.connect(
    host=os.environ['MYSQL_HOST'],
    port=int(os.environ['MYSQL_PORT']),
    user=os.environ['MYSQL_USER'],
    passwd=os.environ['MYSQL_PASS'],
    db=os.environ['MYSQL_DB']
)
db.autocommit(True)
cursor = db.cursor()

# insert initial data
for table in tables:
    sql = f'INSERT INTO {table} (id, done) VALUES (%s, %s)'
    
    # 10000 * 1000 = 10000000
    for i in range(1000):
        start = 10000 * i + 1
        end = 10000 * (i + 1)
        print(f"{start} .. {end}")

        values = [(x, 0) for x in range(start, end + 1)]
        cursor.executemany(sql, values)

# exam
for table in tables:
    with open(f'result.{table}.txt', 'wt') as f:
        for i in range(1001):
            start = 10000 * i + 1
            end = 10000 * (i + 1)
            num_of_done = 10000 * i

            sql = f'SELECT * FROM {table} WHERE done = FALSE ORDER BY id ASC LIMIT 50'
            t_start = time.time_ns()
            cursor.execute(sql)
            t_finish = time.time_ns()
            
            t_elapsed = (t_finish - t_start) / 10**9

            sql = 'EXPLAIN ' + sql
            cursor.execute(sql)
            explain_row = cursor.fetchone()

            print(f'{num_of_done}\t{t_elapsed}\t{explain_row[9]}')
            print(f'{num_of_done}\t{t_elapsed}\t{explain_row[9]}', file=f)

            sql = f'UPDATE {table} SET done = TRUE WHERE id IN ({",".join([str(x) for x in range(start, end + 1)])})'
            cursor.execute(sql)

for table in tables:
    cursor.execute(f'TRUNCATE {table}')
