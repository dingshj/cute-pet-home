# -*- coding: utf-8 -*-
from app import create_app
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.first()
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)

    for path in ['/dashboard', '/pets', '/services', '/adoption', '/shop', '/recognize']:
        r = client.get(path, follow_redirects=False)
        if r.status_code in (200, 308):
            loc = r.headers.get('Location', '')
            print(f'{path}: {r.status_code} -> {loc}')
        else:
            print(f'{path}: {r.status_code}')
