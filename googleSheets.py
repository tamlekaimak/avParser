
def main(listname,gmail,df):
    import httplib2
    from googleapiclient import discovery


    from oauth2client.service_account import ServiceAccountCredentials

    CREDENTIALS_FILE = 'token.json'  # Имя файла с закрытым ключом, вы должны подставить свое

    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    serviceSheets = discovery.build('sheets', 'v4', credentials=credentials)
    serviceDrive=discovery.build('drive','v3',credentials=credentials)
    spreadsheet = serviceSheets.spreadsheets().create(body = {
        'properties': {'title': listname, 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист номер один',
                                   'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
    }).execute()
    spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
    access = serviceDrive.permissions().create(
        fileId = spreadsheetId,
        body = {'type': 'user', 'role': 'reader', 'emailAddress': gmail},  # Открываем доступ на чтение
    ).execute()
    print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
    serviceSheets.spreadsheets().values().append(
        spreadsheetId=spreadsheetId,
        valueInputOption='RAW',
        range='AB:A1',
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()
    return 'https://docs.google.com/spreadsheets/d/' + spreadsheetId