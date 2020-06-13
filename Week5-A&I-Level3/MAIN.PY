import tableauserverclient as TSC
import twitter

def getDatasource(request):
data = request.get_json()

    ds_id = data['resource_luid']
    
    server_url = 'https://10ax.online.tableau.com'
    site = 'jharriscohdev372485'
    pat = ''
    pat_name = 'JeremyDevPAT'
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=pat_name, personal_access_token=pat, site_id=site)
    server = TSC.Server(server_url, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
            ds = server.datasources.get_by_id(ds_id)
            ds_name = ds.name
            proj = ds.project_name

            server.datasources.populate_connections(ds)
            conn_type_ls = [conn.connection_type for conn in ds.connections]
            conn_types = ', '.join(conn_type_ls)
            conn_count = len(conn_type_ls)
            conn_server_ls = [conn.server_address for conn in ds.connections]
            conn_servers = ', '.join(conn_server_ls)

    vals = {'project': proj, 'conn_types': conn_types, 'conn_servers': conn_servers, 'conn_count': conn_count, 'datasource': ds_name}

    tweet = f'A Tableau data source named "{ds_name}" within the "{proj}" project on my Tableau Online developer site failed to refresh.'
    tweet += f' This data source has {conn_count} connection(s) to the following technologies: {conn_types}. #DataDev'

    api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

    api.PostUpdate(tweet)

    return str(tweet)
