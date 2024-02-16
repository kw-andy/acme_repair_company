"""Creating 5 unitests for repairs_parts.py
"""

import os

import repairs_parts

os.environ["URL_TO_FETCH"] = 'https://www.vroomly.com/backend_challenge/labour_times'
os.environ["JSON_INPUT"] = 'data.json'
os.environ["JSON_OUTPUT"] = 'quotations.json'

def test_exp():
    url_to_fetch,json_input,json_output = repairs_parts.exp_variables_from_bash()    
    assert url_to_fetch == 'https://www.vroomly.com/backend_challenge/labour_times'
    assert json_input == 'data.json'
    assert json_output == 'quotations.json'

