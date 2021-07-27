import requests


request = requests.post('/logging/write/',
                        json={
                            'project_name': 'ClientServerWUNU',
                            'log': {
                                'level': 'INFO',
                                'level_number': 20,

                                'func_name': '',
                                'path_to_file': 'src/testlog.py',
                                'filename': 'testlog.py',
                                'line': 465,

                                'message': 'hello from testlog.py',
                                'created': '25-06-2021',

                                'additional_info': {
                                    'language': 'python',
                                    'framework': 'django'
                                }
                            }
                        })

print(request.json())
