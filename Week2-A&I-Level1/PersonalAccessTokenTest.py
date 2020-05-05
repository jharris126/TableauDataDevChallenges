import tableauserverclient as TSC

server_url = 'https://10ax.online.tableau.com'
site = 'jharriscohdev372485'
pat = 'xNjZ7qg6QHW09lslrXUaTQ==:5Jjse8buJ7BwpzQffsilHbrSt7N7iZ0K'
pat_name = 'JeremyDevPAT'
tableau_auth = TSC.PersonalAccessTokenAuth(token_name=pat_name, personal_access_token=pat, site_id=site)
server = TSC.Server(server_url, use_server_version=True)

server.auth.sign_in(tableau_auth)

print(server.sites.get_by_content_url(site).name)

server.auth.sign_out()
