import pandas as pd
from twilio.rest import Client
import numpy as np

account_sid = "sid_twillio"
auth_token  = "token_twillio"
client = Client(account_sid, auth_token)
phoneNumbers = ['22222222']

relatorio = pd.read_excel("SALDO.xlsx")

relatorio = relatorio.drop(['SALDO', 'Unnamed: 2','Unnamed: 3','Unnamed: 4', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], axis=1)
relatorio = relatorio.drop(0)
relatorio = relatorio.drop(1)
relatorio.columns = relatorio.columns.str.lower().str.replace(': ', '_')
relatorio.columns = relatorio.columns.str.lower().str.replace('unnamed: 1', 'conta')
relatorio.columns = relatorio.columns.str.lower().str.replace('unnamed: 5', 'saldo')
relatorio.columns = relatorio.columns.str.lower().str.replace('unnamed: 6', 'diaria')
relatorio = relatorio.replace({'--': np.nan})
relatorio = relatorio.replace({'R$': ''})
relatorio['diaria'] = pd.to_numeric(relatorio['diaria'], errors='coerce')
relatorio = relatorio.dropna(how='any', axis=0)

relatorio.to_excel('new_saldo.xlsx')

tabela = pd.read_excel("new_saldo.xlsx")

for i, conta in enumerate(tabela['conta']):
    saldo = tabela.loc[i, 'saldo']
    diaria = tabela.loc[i, 'diaria']
    custo_semanal = saldo/diaria

    if custo_semanal < 7:
        for tel in phoneNumbers:
            message = client.messages.create(
                to=tel,
                from_="+11111111",
                body=f'\n\n--------------\n\nRELATÓRIO SEMANAL\n\n{conta}, Saldo insuficiente para 7 dias.')
            print(message.sid)