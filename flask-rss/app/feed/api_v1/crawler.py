import requests
from app.shared.logger import Logger
from config import settings

def get_site_data(url, method='GET', requests_params={}, expected_status=200, 
                  output='text'):
    """
        Get site data, process and logger the result.
    """
    if output not in ['text', 'json']:
        raise ValueError('Output expect `text` or `json` values')

    method = method.lower()
    try:
        method = getattr(requests, method)
        response = method(url, **requests_params)
        
        status = response.status_code == expected_status
        data = response.text if output == 'text' else response.json

        if not status:
            Logger.error(f'Error URL: `{url}` response status: '+
                         f'{response.status_code} | output: {output} | '+
                         f'data: {data}')

        Logger.info(f'RSS Response ok')
        return status, data
    
    except Exception as err:
        Logger.error(f'Error URL: `{url}` | {err}')
        return False, None