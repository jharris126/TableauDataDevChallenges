import tableauserverclient as TSC

server_url = 'https://10ax.online.tableau.com'
site = 'jharriscohdev372485'
pat = ''
pat_name = 'JeremyDevPAT'
tableau_auth = TSC.PersonalAccessTokenAuth(token_name=pat_name, personal_access_token=pat, site_id=site)
server = TSC.Server(server_url, use_server_version=True)

wbh = TSC.WebhookItem()
wbh.name = "EmailCreatedWorkbookShort"
wbh.url = "https://hooks.zapier.com/hooks/catch/2363885/os02i9x/"
wbh.event = "workbook-created"

with server.auth.sign_in(tableau_auth):
    result = server.webhooks.create(wbh)
    print(result)
