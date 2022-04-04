__author__ = 'rafael.oliveirasilva@hotmart.com | QA & WFM'

import csv
import datetime
from datetime import date
import json
import random
from types import new_class
import requests
import ndjson
import getpass
import os
import re
import pdb


######################
##### CONSTANTS ######
######################

ASTROBOX_TOKEN = "Bearer H4sIAAAAAAAAAGVU25KqOhT8Ik8Byjg%2BikGEIYlCLpCXUwIjd3VEueTrd7Cm9sM5D6miSLO61%2BpefE9ekThpiUsvpNLVUel27jUw05374db3iO28zT%2Ffk6enBpsiwywSTmfwFHNRCD68EmO8Zy27p%2B1envloxNS6JcvgGUee5reoT0i3hNI2EchqVGom4nTwSVAjWT8xiEcUzu9sHTmxjp2TiSpa%2BjtPxsZmEKH7wSdvEnxfu%2BVQZkvvnjm0jMKhPDsbzY%2BYFJGr9LgSyXjCBE6QPMNfbblwaE7%2B6rNzajRd1tprRE4vDOALSvhCZLtGgL4gSUe%2FsldotxqhdNeqnzbmrPPbTXeORHOOvCJ9f7%2FfztwJ30%2FZzqwSQ%2FuL%2Fd8seNFnjl6k19MaEtWrTCUCcInJdoDgyZK20QQ%2F5XQZFJnDJJa2oXSoeZ1UP7XCbNdY22uKv8e6RSPNC7HOSAA6TVReBR24gqE2xZI1aqYF5vAZk1qPJ70SpGgESXVYbSUy%2FsMPUk1pUP3TJQSqBoAjBttBHYkBXUPQjahyTUzqldKhYaCOtHqqIRhUtmQRG4izMU5UB1ljDRQwA7aFDPhdP1dBC1s4xDIffeJVyu8ncmxTaSowYZXPUYMd1iBJJ8W7FG8ulQ%2FiGphQDc46ZLdWZ0TAXf8%2Br2f%2FRVQMbnVTeDjMfiFSayorRRYFKnNzNpomnd6ZIdTeh6E27qN5Xsx9ZyqLrD69Bs1cS%2BWri7nXK6%2FqZPm%2BNwQ3a8GDPn0vgTUlRqBnzmaa8aG9oXTvHSNNhAFlKGQM%2FdZ5pgevEL84prFdSE2LzjXq4shsZVwTXIjd8IBtdgELrBlH7dFitjjSWr9QrTmQhp3cRuvc9q6dVe7dNtZRhWoot5NP0iE27CcC%2BxLu9BK2nvJ7r%2B5qGcs5e%2FEAJ8XXou7M2Svbb%2B5iXuDKnkQLddWTwqeaaN81mnjSVhiI1udQYgcO2HGXkFitKNWyH5BwVmcwWl9nn%2FuNFWwG5z6N%2FWf%2FRVBXXID54z6i%2FB59%2FHudxigPLi7jgbxM9yLH7f5RkOp2WjRn%2BWlusUB4deRMlP651hB%2BfeSvj2Zx8dzA8vuodw59D%2FBFP0rQphoqjqC1sjLvi%2B%2FTkjubw7FhHY5HYO7aKr2Vup5U2%2B9dPjZX7ITD5dg7XfuKa%2FJFZAvMQgzXPH7qjx6KknLSeLfudA7489YZnpwWLsxOsXjA9MZr7xnCIFonC3n5%2BrF83Ty06wKclsHdPZrl54L8PMYXOMC8WayD0Uoy8qg9ugWgSsNpvf1GYRSON%2BxMeba0r6Uk0tblbTgZW6L%2BKQ10LweRcOgs8up4SR75HxJjxHRoBQAA"

DATE_INTERVAL_DAYS = 7

login = 'rafael.oliveirasilva@hotmart.com'
pwd = 'raf060990'

astrobox_url = 'https://api-astrobox.hotmart.com/v1/'
opinion_box_url = 'https://api-cx.opinionbox.com/'

application_name = 'assurance_spotcheck_v4.3.2'

date_begin = datetime.date.today() - datetime.timedelta(days=DATE_INTERVAL_DAYS+1)
date_end = datetime.date.today() - datetime.timedelta(days=1)

product_team_id = '360004260611'
refund_team_id = '360004260691'
tool_team_id = '360004260551'
int_buyers_team_id = '360004859552'
payment_team_id = '360004246672'
access_team_id = '360004246612'
financial_team_id = '360004260571'
int_users_team_id = '360004859572'
int_french_english_id = '360007368032'
int_access_team_id = '360019593232'
hotmart_account_team_id = '360004246572'
purchase_team_id = '360004260651'
activation_team_id = '360019201292'
int_journey_team = '360004859552'
int_operations_team = '360019593232'
int_product_team = '360004382372'

# query com o id dos times: https://astrobox.hotmart.com/query/run/351e7c23-6c8f-4ccb-a0c8-430e8ecd4922

astrobox_query = 'solved_tickets_by_period'
astrobox_query_params = {
    'end': str(date_end),
    'begin': str(date_begin),
    'team_id': [product_team_id, refund_team_id, tool_team_id, int_buyers_team_id, payment_team_id, access_team_id, financial_team_id, int_users_team_id, int_french_english_id, int_access_team_id, hotmart_account_team_id, purchase_team_id, activation_team_id, int_journey_team, int_operations_team, int_product_team]
}

base_dir = os.getenv("E:\QLT Assurance - Spotcheck")
if os.name == 'nt':
    base_dir = 'E:\QLT Assurance - Spotcheck'


#######################
###### ASTROBOX #######
#######################

# check if provided token is still valid
def check_astrobox_token(token=ASTROBOX_TOKEN):
    token_url = astrobox_url + 'security/user/me'

    token_header = {
        'Authorization': token,
        'X-Client-Name': application_name,
        'accept': 'application/x-ndjson'
    }

    token_resp = requests.get(token_url, headers=token_header)

    return token_resp.status_code == 200


## login
def get_astrobox_token():
    print('fetching security token...')

    login_url = 'https://api-sec-vlc.hotmart.com/security/oauth/token'

    # username = input('Your email: ')
    # user_pass = getpass.getpass('Your password: ')

    username = login
    user_pass = pwd

    login_headers = {
        'Authorization': 'Basic MTJmYzVlZGUtNzRmYS00MWVjLTg4NmYtYzM4YzA4YjcxMGZmOjE4MjFhOGRlLTMxNDgtNGU3ZC05OGZmLWZkY2NiOGY0MzkzNw=='
    }

    login_body = {'grant_type': 'password', 'username': username, 'password': user_pass}

    login_resp = requests.post(login_url, headers=login_headers, data=login_body)

    if login_resp.status_code != 200:
        raise Exception(login_resp.json()['error_description'])

    new_token = 'Bearer ' + login_resp.json()['access_token']

    print('astrobox token fetched: ' + new_token)

    return new_token


# request para executar a query
def run_astrobox_query(query, query_params={}, token=ASTROBOX_TOKEN):
    print('query: ' + query)
    print('params: ' + json.dumps(query_params))
    print('fetching astrobox data...')

    if (len(token) < 12) or (not check_astrobox_token(token)):
        token = get_astrobox_token()

    execution_headers = {
        'Authorization': token,
        'X-Client-Name': application_name,
        'accept': 'application/x-ndjson',
        'Content-Type': 'application/json'
    }

    execution_url = astrobox_url + 'executor/reactive/'

    execution_body = {
        'query': query,
        'parameters': query_params,
        'saveResult': False
    }

    # check if query argument is an id or alias, and adjusts the execution url
    if re.match(r"[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}", query):
        execution_url = execution_url + 'by-id/'
    else:
        execution_url = execution_url + 'by-alias/'

    execution_resp = requests.post(execution_url, headers=execution_headers, data=json.dumps(execution_body))

    if execution_resp.status_code != 200:
        raise Exception(execution_resp.json()['error_description'])

    # returns the query results as a json array
    
    temp_json = execution_resp.json(cls=ndjson.Decoder)
    
    new_filtered_ticket = dict()
   
    for score in temp_json:
   
        new_filtered_ticket[score['ticket_id']] = score
    
    return new_filtered_ticket


##########################
###### OPINION BOX #######
##########################

def get_opinionbox_token():
    print('fetching opinion box token...')

    login_url = opinion_box_url + 'autenticacao'

    ob_body = {
        'clientId': 'zeVQKzU60Q',
        'secretId': '2fc588d65de0b5bb11e334535efe4f1ffbb3dbdb',
        'apiVersion': 'v1'
    }

    login_resp = requests.post(login_url, data=json.dumps(ob_body))

    if login_resp.status_code != 200:
        print(json.dumps(login_resp.json()))
        raise Exception(login_resp.json()['error_description'])

    new_token = 'Bearer ' + login_resp.json()['token']

    print('opinion box token fetched: ' + new_token)

    return new_token


question_ids = {
    'evaluation_grade': [
        'P-706',
        'P-931',
        'P-930',
        'P-929',
        'P-928',
        'P-933',
        'P-932',
        'P-703',
        'P-697',
        'P-691',
        'P-688',
        'P-685',
        'P-936',
        'P-880',
        'P-939',
        'P-854',
        'P-938',
        'P-851',
        'P-937',
        'P-847',
        'P-935',
        'P-934',
        'P-942',
        'P-944',
        'P-941',
        'P-940',
        'P-943',
        'P-925',
        'P-1019',
        'P-1022',
        'P-1025',
        'P-1013',
    ],
    'evaluation_reason': [
        'P-707',
        'P-704',
        'P-698',
        'P-692',
        'P-689',
        'P-686',
        'P-848',
        'P-881',
        'P-872',
        'P-855',
        'P-852',
        'P-713',
        'P-717',
        'P-878',
        'P-887',
        'P-881',
        'P-875',
        'P-884',
        'P-926',
        'P-1020',
        'P-1023',
        'P-1026',
        'P-1014',
    ],
    'evaluation_comments': [
        'P-708',
        'P-705',
        'P-699',
        'P-693',
        'P-690',
        'P-687',
        'P-849',
        'P-882',
        'P-873',
        'P-856',
        'P-853',
        'P-714',
        'P-718',
        'P-879',
        'P-888',
        'P-882',
        'P-876',
        'P-885',
        'P-927',
        'P-1021',
        'P-1024',
        'P-1027',
        'P-1015',
    ]
}

def get_opinionbox(token):
    print('fetching opinion box data...')

    ob_url = opinion_box_url + 'v1/resultadoDia'

    ob_header = {
        'Authorization': token,
        'Content-type': 'application/json'
    }

    codigos_integracao = ['4z1RSz3A2S', '031k8oK-4n', 'Zu89Rcpgku', 'e_nY5V-_Xf', 'muEOeuFOON', 'qyJunWhzC4', 'sWA9eDWsAE', 'KRgcU6VM6n', 'dJXFnabVxg', 
                          'DIV0LBGgng', 'xhyKyo1NIB', 'SSgrdz55cb', 'ELWoAnQH0A', 'zJU4_Xnd7E', 'F9YnYrXxW2', 'o_Ie6s0VXL', 'MI73AhzRnM', 'GHS-Rn3nOB', 'omxMplnNLi', 
                          '9KPeXUB7W0', 'Ceel30w6CR', '3ZiCH0JBAi', 'vK966j_NrB', 'CO6v2gJ9D1']

    ob_data = dict()

    data = []

    for single_date in (date_begin + datetime.timedelta(n) for n in range(DATE_INTERVAL_DAYS)):

        for codigo in codigos_integracao:

            ob_body = {
                'codigo_integracao': codigo,
                'data': str(single_date)
            }

            ob_resp = requests.post(ob_url, data=json.dumps(ob_body), headers=ob_header)

            if ob_resp.status_code != 200:
                raise Exception(ob_resp.json()['error_description'])

            dados = ob_resp.json()['body']
            data.extend(dados)

            for d in dados:
                ticket_id = d['TickedID']
                new = {
                    'hashtag': d['hashtag'],
                    'ticket_id': ticket_id,
                    'user_email': d['identificador'],
                    'agent_email': d['Atribuído'],
                    'datetime': d['data_fim'],
                    'data_inicio': d['data_inicio'],
                    'data_envio': d['data_envio']
                }

                for data_key in d:
                    for key, ids in question_ids.items():
                        if next((k for k in ids if data_key.startswith(k)), None):
                            new[key] = d[data_key]

                for key in question_ids:
                    if key not in new:
                        suggested_data = {k: v for k, v in d.items() if k.startswith('P-')}
                        print(f"could not find key {key} for ticket {ticket_id}: {suggested_data}")

                ob_data[ticket_id] = new

    import pandas
    pandas.DataFrame(data).to_csv('./ob_data.csv')

    return ob_data

#######
# CSV #
#######

# Definir diretório para salvar o CSV
def get_ticket_audit_file_path(base_path=base_dir):
    ## Coloca a data no padrão brasileito - Dia/Mês/Ano
    dt_string = date.today().strftime("%d-%b-%Y")

    current_quarter = ((date.today().month - 1) // 3) + 1

    folder_name = 'QLT ASSURANCE - SPOTCHECK - Q' + str(current_quarter) + ' ' + str(date.today().year) + ' - CSVS'

    # Definir diretório para salvar o CSV
    absolut_path = base_path + os.sep + folder_name + os.sep
    if not os.path.exists(absolut_path):
        os.makedirs(absolut_path)

    print('file will be saved on path: ' + absolut_path)

    file_name = 'QLT Assurance - Spotcheck - ' + dt_string + ' - Bad Rated Tickets.csv'

    print('file name: ' + file_name)

    file_path = absolut_path + file_name

    return file_path


evaluation_map = {
    'Encantado(a)': 5,
    'Satisfeito(a)': 4,
    'Cansado(a)': 3,
    'Chateado(a)': 2,
    'Mal atendido(a)': 1,
    'Outros': 5,
    'Opção 1': 5,
    'Opção 2': 4,
    'Opção 3': 3,
    'Opção 4': 2,
    'Opção 5': 1,
    'Delighted': 5,
    'Happy': 4,
    'Tired': 3,
    'Upset': 2,
    'Wronged': 1,
    'Enchanté(e)': 5,
    'Satisfait(e)': 4,
    'Fatigué(e)': 3,
    'Déçu(e)': 2,
    'Pas du tout satisfait(e)': 1,
    'Felice': 5,
    'Soddisfatto': 4,
    'Stanco': 3,
    'Triste': 2,
    'Mal assistito': 1,
    'Feliz': 4,
    'Frustrado(a)': 2,
}


def create_ticket_audit_csv(astrobox_data, opinionbox_data, file_path):
    print(f'processing {len(astrobox_data)} data from Astrobox...')
    print(f'processing {len(opinionbox_data)} data from Opinionbox...')

    # 3. Criar um dicionário vazio que receberá as infos
    spotcheck_data = {}

    # Se houver algum dado na tabela, ou seja, se ela não estiver vazia o código continua
    for ticket_id, astrobox_ticket in astrobox_data.items():
        
        opinionbox_ticket = opinionbox_data.get(str(ticket_id), {})

        # É feita a captura do campo do first resolution que vem em segundos do Astrobox
        # Em sequência o mesmo é formatado para o padrão hora/minuto/segundo

        firstResolution = astrobox_ticket['firstResolution']
        firstResolution_formatted = str(datetime.timedelta(seconds=firstResolution))

        # É feita a captura do campo da data de criação do ticket no Zendesk, através do Astrobox - que vem no formato '2021-12-2021T17:15:46Z'.
        # Em seguida a data é formatada para o padrão '17/12/2021 17:15:46'

        old_createdAt = datetime.datetime.strptime(astrobox_ticket['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
        new_createdAt = old_createdAt.strftime("%d/%m/%Y %H:%M:%S") 
        

        # É feita a captura dos campo da data de envio e data de resposta da pesquisa de satisfação através da OPB - que vem no formato '2021-12-2021T17:15:46.000Z'.
        # Em seguida a data é formatada para o padrão '17/12/2021 17:15:46'
        # Depois é testado se o campo de data de envio vier preenchido, a formatação ocorre, senão o código segue para o próximo teste

        surveySentAt = opinionbox_ticket.get('data_envio')
        surveyAnsweredAt = opinionbox_ticket.get('datetime')

        if surveySentAt is not None:
            old_surveySentAt = datetime.datetime.strptime(opinionbox_ticket.get('data_envio'), "%Y-%m-%dT%H:%M:%S.%fZ")
            surveySentAt = old_surveySentAt.strftime("%d/%m/%Y %H:%M:%S") 
        else:
            pass

        if surveyAnsweredAt is not None:
            old_surveyAnsweredAt = datetime.datetime.strptime(opinionbox_ticket.get('datetime'), "%Y-%m-%dT%H:%M:%S.%fZ")
            surveyAnsweredAt = old_surveyAnsweredAt.strftime("%d/%m/%Y %H:%M:%S") 
        else:
            pass


        # Mapeamento que verifica se a pesquisa da OPB vier com notas de 1 à 5 os números serão convertidos para inteiros, se vier como strings de sentimento passarão pelo map que irá atribuir uma nota baseada no sentimento

        evaluation_grade = opinionbox_ticket.get('evaluation_grade')

        try:
            evaluation_grade = int(evaluation_grade)
        except (ValueError, TypeError):
            evaluation_grade = evaluation_map.get(evaluation_grade, evaluation_grade)

        # Variáveis que geram os links para realização da análise do Spotcheck e visualização dos tickets no zendesk respectivamente

        open_spotcheck_form = '=HYPERLINK(CONCATENATE("https://docs.google.com/forms/d/e/1FAIpQLScFgQMD4EHyas8OGt5pXsW4579Ppz3j-ihxfqqzbsyN6xL04w/viewform?usp=pp_url&entry.79984856=",INDIRECT(CONCAT("A", ROW())),"&entry.1989228284=",INDIRECT(CONCAT("D", ROW())),"&entry.1559052161=",INDIRECT(CONCAT("E", ROW())),"&entry.557486568=",INDIRECT(CONCAT("H", ROW())),"&entry.452611961=",INDIRECT(CONCAT("G", ROW())),"&entry.488477383=N%C3%A3o&entry.1729246832=N%C3%A3o&entry.872741789=N%C3%A3o&entry.475229757=10&entry.1939614848=N%C3%A3o&entry.613885024=",INDIRECT(CONCAT("G", ROW()))),"Analyze")'
        open_ticket_in_zendesk = '=HYPERLINK(CONCATENATE("https://suportehotmart.zendesk.com/agent/tickets/",INDIRECT(CONCAT("A",ROW()))),"Open Ticket")'
        
        agent_name = astrobox_ticket['agent_name']

        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)

        new_agentName = emoji_pattern.sub(r'', agent_name)

        temp = {
            'TICKET ID': astrobox_ticket['ticket_id'],
            'TICKET CREATED AT': new_createdAt,
            'AGENT NAME': new_agentName,
            'AGENT E-MAIL': astrobox_ticket['agent_email'],
            'TEAM': astrobox_ticket['team'],
            'TEAM OPB': opinionbox_ticket.get('team'),
            'CLUSTER': astrobox_ticket['cluster'],
            'CONTACT REASONS': astrobox_ticket['contact_reason'],
            'TRANSACTION NUMBER': astrobox_ticket['transactionNumber'],
            'PRODUCT ID': astrobox_ticket['productId'],
            'FIRST RESOLUTION': firstResolution_formatted,
            'SURVEY SENT AT': surveySentAt,
            'SURVEY ANSWERED AT': surveyAnsweredAt,
            'P1': evaluation_grade,
            'P2': opinionbox_ticket.get('evaluation_reason'),
            'P3': opinionbox_ticket.get('evaluation_comments'),
            'LINK TO SPOTCHECK': open_spotcheck_form,
            'OPEN TICKET IN ZENDESK': open_ticket_in_zendesk,
        }

        if astrobox_ticket['team'] not in spotcheck_data:
            spotcheck_data[astrobox_ticket['team']] = {}

        if astrobox_ticket['agent_email'] not in spotcheck_data[astrobox_ticket['team']]:
            spotcheck_data[astrobox_ticket['team']][astrobox_ticket['agent_email']] = []

        spotcheck_data[astrobox_ticket['team']][astrobox_ticket['agent_email']].append(temp)

    print('writing file...')

    with open('QLT ASSURANCE - SPOTCHECK - Q1 2022 - CSVS/Query - Tag Pendente - 31_01_2022 (1).csv', encoding='utf-8') as csv_pending:

        pending_table = csv.reader(csv_pending, delimiter=',',)

        for t in pending_table:
            id_ticket = t[0]

            print(id_ticket)

    # with open(file_path, 'w', newline='', encoding="UTF-8") as csvaudit:
    #     fieldnames = ['TICKET ID', 'TICKET CREATED AT', 'AGENT NAME', 'AGENT E-MAIL', 'TEAM', 'TEAM OPB', 'CLUSTER', 'CONTACT REASONS', 'TRANSACTION NUMBER', 'PRODUCT ID', 'FIRST RESOLUTION', 'SURVEY SENT AT', 'SURVEY ANSWERED AT', 'P1', 'P2', 'P3',
    #                   'LINK TO SPOTCHECK', 'OPEN TICKET IN ZENDESK', 'SPOTCHECKER', 'ANALYSIS FINISHED?', 'SPOTCHECK ELAPSED TIME', 'DID YOU HAVE ANY DIFFICULTIES? TELL US BELOW']

    #     writer = csv.DictWriter(csvaudit, fieldnames=fieldnames, delimiter=';')

    #     writer.writeheader()
    #     #pdb.set_trace()
    #     # for each team
    #     for team, agents in spotcheck_data.items():

    #          # for each agent
    #         for agent, tickets in agents.items():
    #             bad_tickets = [ticket for ticket in tickets if ticket['P1'] == 1 or ticket['P1'] == 2]
                
    #             for spotcheck_tickets in (bad_tickets):
    #                 writer.writerow(spotcheck_tickets)


    print('\nArquivo gerado no diretório: ' + file_path)


#################
##### INIT ######
#################

if __name__ == "__main__":
    file_path = get_ticket_audit_file_path(base_dir)
    astrobox_data = run_astrobox_query(astrobox_query, astrobox_query_params, ASTROBOX_TOKEN)
    opinionbox_data = get_opinionbox(get_opinionbox_token())
    create_ticket_audit_csv(astrobox_data, opinionbox_data, file_path)