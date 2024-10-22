from   utils      import decrypt, date_log_event, get_last_log
from   sqlalchemy import create_engine
from   datetime   import datetime
from   flask      import Flask, request, jsonify, url_for
import pandas     as     pd
import requests
import math
import json

app = Flask(__name__)

COLUMN_DATE_MODIFY  = 'data_cadastro'
ENCRYPTED_FILE_NAME = 'credentials_PostgreSQL.enc'
PRIVATE_KEY_NAME    = 'private.pem'
EXTERNAL_LOGIN_URL  = 'http://200.235.135.49:413/api/login'
EXTERNAL_AUTH_URL   = 'http://200.235.135.49:413/api/authenticate'

PAGE_SIZE = 50  # Número de registros por página

def connect_pg(cred):
    """
    Create a connection to the PostgreSQL database using the provided credentials.
    Args:
        cred (dict): A dictionary containing database connection credentials.
    Returns:
        sqlalchemy.engine.base.Engine: The database engine object.
    """
    engine = create_engine(
        f"postgresql+psycopg2://{cred['username']}:{cred['password']}"
        f"@{cred['host']}:{cred['port']}"
        f"/{cred['database']}"
    )
    
    if not engine:
        raise ConnectionError("The connection to the database is not open.")
    
    return engine

def get_next_page_url(endpoint, page, date_str=None, inscricao=None, **kwargs):
    """
    Generate the URL for the next page of results.
    """
    if date_str:
        return url_for(endpoint, date_str=date_str, page=page + 1, _external=True, **kwargs)
    elif inscricao:
        return url_for(endpoint, inscricao=inscricao, page=page + 1, _external=True, **kwargs)
    else:
        return url_for(endpoint, page=page + 1, _external=True)

@app.route('/get_view/data/<date_str>', methods=['GET'])
def get_date_view(date_str):
    """
    Fetch views of a table for a specific date with pagination.
    """
    page = int(request.args.get('page', 1))
    offset = (page - 1) * PAGE_SIZE

    credential = decrypt(ENCRYPTED_FILE_NAME, PRIVATE_KEY_NAME)
    engine     = connect_pg(credential)

    date_datetime = datetime.strptime(date_str, "%d%m%Y")
    data_formatada = date_datetime.strftime('%Y-%m-%d')

    query_total =(f"SELECT COUNT(*) "
             f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_imoveis\" "
             f"WHERE \"{COLUMN_DATE_MODIFY}\"::date = '{data_formatada}' ")

    # Execute a consulta para obter o total de itens
    total_result = pd.read_sql(query_total, engine)
    print (total_result)
    # Extrair o valor de tot do resultado
    tot = total_result.iloc[0, 0]   

    query = (f"SELECT * "
             f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_imoveis\" "
             f"WHERE \"{COLUMN_DATE_MODIFY}\"::date = '{data_formatada}' "
             f"LIMIT {PAGE_SIZE} OFFSET {offset}")

    data = pd.read_sql(query, engine)

    imoveis = data.to_dict(orient='records')
    for imovel in imoveis:
        codigo_logradouro = imovel['codigo_logradouro']
        if codigo_logradouro is not None and not math.isnan(codigo_logradouro):
            query_logradouro = (f"SELECT * "
                                f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_logradouros\" "
                                f"WHERE \"id\" = {codigo_logradouro}")
            logradouro_data = pd.read_sql(query_logradouro, engine)
            if not logradouro_data.empty:
                logradouro_info = logradouro_data.to_dict(orient='records')[0]
                imovel['logradouro_info'] = logradouro_info

    engine.dispose()

    # Verificar se há uma próxima página
    next_page_url = None
    if int(tot) >= PAGE_SIZE * page:
        next_page_url = get_next_page_url('get_date_view', page, date_str=date_str)

    return jsonify({
        "imoveis": imoveis,
        "next_page": next_page_url
    }), 200

@app.route('/get_view/inscricao/<inscricao>', methods=['GET'])
def get_inscricao_view(inscricao):
    """
    Fetch views of a table for a specific inscricao with pagination.
    """
    page = int(request.args.get('page', 1))
    offset = (page - 1) * PAGE_SIZE

    credential = decrypt(ENCRYPTED_FILE_NAME, PRIVATE_KEY_NAME)
    engine     = connect_pg(credential)

    query_total = (f"SELECT COUNT(*) "
             f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_imoveis\" "
             f"WHERE \"inscricao\" = '{inscricao}' ")

    # Execute a consulta para obter o total de itens
    total_result = pd.read_sql(query_total, engine)

    # Extrair o valor de tot do resultado
    tot = total_result.iloc[0, 0]

    query = (f"SELECT * "
             f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_imoveis\" "
             f"WHERE \"inscricao\" = '{inscricao}' "
             f"LIMIT {PAGE_SIZE} OFFSET {offset}")

    data = pd.read_sql(query, engine)

    imoveis = data.to_dict(orient='records')
    for imovel in imoveis:
        codigo_logradouro = imovel['codigo_logradouro']
        if codigo_logradouro is not None and not math.isnan(codigo_logradouro):
            query_logradouro = (f"SELECT * "
                                f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_logradouros\" "
                                f"WHERE \"id\" = {codigo_logradouro}")
            logradouro_data = pd.read_sql(query_logradouro, engine)
            if not logradouro_data.empty:
                logradouro_info = logradouro_data.to_dict(orient='records')[0]
                imovel['logradouro_info'] = logradouro_info

    engine.dispose()

    # Verificar se há uma próxima página
    next_page_url = None
    if int(tot) >= PAGE_SIZE * page:
        next_page_url = get_next_page_url('get_inscricao_view', page, inscricao=inscricao)

    return jsonify({
        "imoveis": imoveis,
        "next_page": next_page_url
    }), 200

@app.route('/get_view/all', methods=['GET'])
def get_all_view():
    """
    Fetch views of all data with pagination.
    """
    page = int(request.args.get('page', 1))
    offset = (page - 1) * PAGE_SIZE

    credential = decrypt(ENCRYPTED_FILE_NAME, PRIVATE_KEY_NAME)
    engine     = connect_pg(credential)

    query_total = (f"SELECT COUNT(*) "
             f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_imoveis\" ")

    # Execute a consulta para obter o total de itens
    total_result = pd.read_sql(query_total, engine)

    # Extrair o valor de tot do resultado
    tot = total_result.iloc[0, 0]

    query = (f"SELECT * "
             f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_imoveis\" "
             f"LIMIT {PAGE_SIZE} OFFSET {offset}")

    data = pd.read_sql(query, engine)

    imoveis = data.to_dict(orient='records')
    for imovel in imoveis:
        codigo_logradouro = imovel['codigo_logradouro']
        if codigo_logradouro is not None and not math.isnan(codigo_logradouro):
            query_logradouro = (f"SELECT * "
                                f"FROM {credential['database']}.{credential['schema']}.\"wbs_dados_logradouros\" "
                                f"WHERE \"id\" = {codigo_logradouro}")
            logradouro_data = pd.read_sql(query_logradouro, engine)
            if not logradouro_data.empty:
                logradouro_info = logradouro_data.to_dict(orient='records')[0]
                imovel['logradouro_info'] = logradouro_info

    engine.dispose()

    # Verificar se há uma próxima página
    next_page_url = None
    if int(tot) >= PAGE_SIZE * page:
        next_page_url = get_next_page_url('get_all_view', page)

    return jsonify({
        "imoveis": imoveis,
        "next_page": next_page_url
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=3610)
