import tableauserverclient as TSC
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, TableDefinition, Inserter\
    , SqlType, TableName

server_url = 'https://10ax.online.tableau.com'
site = 'jharriscohdev372485'
pat = 'xNjZ7qg6QHW09lslrXUaTQ==:5Jjse8buJ7BwpzQffsilHbrSt7N7iZ0K'
pat_name = 'JeremyDevPAT'
tableau_auth = TSC.PersonalAccessTokenAuth(token_name=pat_name, personal_access_token=pat, site_id=site)
server = TSC.Server(server_url, use_server_version=True)

def getWorkbooks():
    server.auth.sign_in(tableau_auth)
    result = server.workbooks.get()
    server.auth.sign_out()

    wbs, pagination_item = result

    return wbs

def getUserInfo(uid):
    server.auth.sign_in(tableau_auth)
    result = server.users.get_by_id(uid)
    server.auth.sign_out()

    return result

def parseData():
    wbs = [{"workbook": wb, "owner": getUserInfo(wb.owner_id)} for wb in getWorkbooks()]
    dict = [{"workbook_id": wb['workbook'].id,
             "workbook_name": wb['workbook'].name,
             "project_name": wb['workbook'].project_name,
             "owner_id": wb['owner'].id,
             "owner_name": wb['owner'].name,
             "owner_full_name": wb['owner'].fullname} for wb in wbs]

    cols = list(dict[0].keys())
    data = [list(row.values()) for row in dict]

    return {"cols": cols, "data": data}

def createHyperFile():
    dict = parseData()
    file = "/Users/jharris/Desktop/workbookUsers.hyper"
    cols = dict['cols']
    data = dict['data']

    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(hyper.endpoint, file, CreateMode.CREATE_AND_REPLACE) as connection:
            connection.catalog.create_schema('Extract')

            table = TableDefinition(TableName('Extract', 'Extract'), [
                TableDefinition.Column(col, SqlType.text())
                for col in cols
            ])

            connection.catalog.create_table(table)

            with Inserter(connection, table) as inserter:
                inserter.add_rows(rows=data)
                inserter.execute()

def main():
    createHyperFile()

if __name__ == "__main__":
    main()
