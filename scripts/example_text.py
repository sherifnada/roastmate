import requests

print(requests.post(
    "http://127.0.0.1:8000/receive_message",
    json={'accountEmail': 'snadalive@gmail.com', 'content': 'Testing 124', 'is_outbound': False, 'status': 'RECEIVED', 'error_code': None,
          'error_message': None, 'message_handle': '101603', 'date_sent': '2023-08-29T03:18:43.000Z',
          'date_updated': '2023-08-29T03:18:43.131Z', 'from_number': '+18023494963', 'number': '+18023494963', 'to_number': '+15615466689',
          'was_downgraded': None, 'plan': 'sapphire', 'media_url': '', 'message_type': 'group',
          'group_id': 'bbf5f88e-7205-415a-9e2b-bd1d89b71d70', 'participants': ['+18023494963', '+19144006238'], 'send_style': '',
          'opted_out': False, 'error_detail': None}
).text)

