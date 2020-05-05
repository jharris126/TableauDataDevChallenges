import tableauserverclient as TSC
import requests
import json

server_url = 'https://10ax.online.tableau.com'
site = 'jharriscohdev372485'
pat = 'xNjZ7qg6QHW09lslrXUaTQ==:5Jjse8buJ7BwpzQffsilHbrSt7N7iZ0K'
pat_name = 'JeremyDevPAT'
tableau_auth = TSC.PersonalAccessTokenAuth(token_name=pat_name, personal_access_token=pat, site_id=site)
server = TSC.Server(server_url, use_server_version=True)

def makeQuery():
    filtersls = []
    for x in range(1, 10):
        calc = '"' + 'Calculation' + str(x) + '"'
        test = '"' + 'Test' + str(x) + '"'
        field = '"' + 'Field' + str(x) + '"'
        ls = [calc, test, field]
        filtersls.extend(ls)

    filters = str.join(",", filtersls)

    query = """{
      calculatedFields (filter: {nameWithin: [""" + filters + """]}){
        id
        name
        formula
        downstreamWorkbooks {
          name
          projectName
          owner {
            id
            name
            email
          }
        }
      }
    }"""

    return query

def getData():
    server.auth.sign_in(tableau_auth)
    result = server.metadata.query(query=makeQuery())
    server.auth.sign_out()

    return result['data']['calculatedFields']

def prepBody(emp, wb, prj, fld, frmla):
    body = f"""Hello {emp}, 
            You are receiving this email because you are the owner of a workbook that contains a """
    body += f"""field we've flagged as having a potentially malformed name. Please review the name for {fld} on """
    body += f"""workbook {wb} within the project {prj}. The formula for this field can be found below. Thank you!
            
            Calculation Formula: {frmla}"""

    return body

def sendEmails(email, wbname, body):
    subj = f"Calculation Issue On {wbname} Tableau Workbook"
    dict = {"email": email, "subject": subj, "body": body, "from": "TableauFieldNamePolice@coh.org"}
    jstr = json.dumps(dict)

    #send to zapier webhook to parse and send data, do not want to include an actual smtp
    url = "https://hooks.zapier.com/hooks/catch/2363885/o5smet2/"
    requests.post(url, data=jstr)

    return

def prepEmails(data):
    for field in data:
        for wb in field['downstreamWorkbooks']:
            email = wb['owner']['email']
            emp = wb['owner']['name']
            wbnm = wb['name']
            prj = wb['projectName']
            fld = field['name']
            frmla = field['formula']
            body = prepBody(emp, wbnm, prj, fld, frmla)
            sendEmails(email, wbnm, body)

def main():
    data = getData()
    prepEmails(data)

if __name__ == "__main__":
    main()
