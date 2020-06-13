import tableauserverclient as TSC

server_url = 'https://10ax.online.tableau.com'
site = 'jharriscohdev372485'
pat = ''
pat_name = 'JeremyDevPAT'
tableau_auth = TSC.PersonalAccessTokenAuth(token_name=pat_name, personal_access_token=pat, site_id=site)
server = TSC.Server(server_url, use_server_version=True)

wbh = TSC.WebhookItem()
wbh.name = "ExtractFailedToTwitter"
wbh.url = "https://us-central1-datatest-270319.cloudfunctions.net/datasource-get-info"
wbh.event = "datasource-refresh-failed"

with server.auth.sign_in(tableau_auth):
    print(server.webhooks.create(wbh))
