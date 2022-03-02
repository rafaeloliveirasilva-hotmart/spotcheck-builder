import pandas as pd
import datetime
from datetime import date
import json
from types import new_class
import requests

DATE_INTERVAL_DAYS = 7

opinion_box_url = 'https://api-cx.opinionbox.com/'

date_begin = datetime.date.today() - datetime.timedelta(days=DATE_INTERVAL_DAYS+1)
date_end = datetime.date.today() - datetime.timedelta(days=1)

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

    return ob_data

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

origin_file = pd.read_csv("QLT ASSURANCE - SPOTCHECK - Q1 2022 - CSVS/Tag Pendente - Query - Tag Pendente - 31_01_2022.csv", sep=',')

origin_file.columns = ['ticket_id', 'subject', 'createdAt', 'updatedAt', 'status', 'user_id', 'team_id', 'channel', 'satisfactionScore','satisfactionComment', 'createdAtMonth', 'isSolved','solvedAt','solvedAtMonth','comment','analyzed','requester_id','followUps','satisfactionReason','type','priority','wrongSorting','sortingAgent','userProfile','userEmail','productId','contactReason','otherReasonDetail','transactionNumber','contactReasonForm','isInternal','extensions','privacyContactReason']

# def create_ticket_audit_csv(opinionbox_data, pending_tickets_data):
#     print(f'processing {len(opinionbox_data)} data from Opinionbox...')

#     for ticket_id in pending_tickets_data.items():

#         opinionbox_ticket = opinionbox_data.get(str(ticket_id), {})

#         evaluation_grade = opinionbox_ticket.get('evaluation_grade')

#         try:
#             evaluation_grade = int(evaluation_grade)
#         except (ValueError, TypeError):
#             evaluation_grade = evaluation_map.get(evaluation_grade, evaluation_grade)

# CSV Read

origin_file.to_csv("QLT ASSURANCE - SPOTCHECK - Q1 2022 - CSVS/Tag Pending - OPB Grades.csv", index=False, columns=['ticket_id'])

target_file = pd.read_csv("QLT ASSURANCE - SPOTCHECK - Q1 2022 - CSVS/Tag Pending - OPB Grades.csv")
print('\nModified file:')
print(target_file)
        