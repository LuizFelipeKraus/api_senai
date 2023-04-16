import requests
from flask import  jsonify


class SearchPostalCode():
    def get_cep(cep):
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({'error': 'CEP não encontrado'})

    def validated_cep(cep):
        cep = str(cep).replace('-', '').replace('.', '')
        return cep