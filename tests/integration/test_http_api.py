import json


def test__on_post_create_pereval(client, pereval, pereval_info):
    body = pereval_info.dict()
    body.pop('status')
    body['add_time'] = pereval_info.add_time.isoformat()

    response = client.post(
        "/submitData",
        json=body,
    )

    assert response.status_code == 201
    assert json.loads(response.content)['id'] == pereval.id


def test__on_get_all(client, pereval_info_response):

    pereval_info_response.add_time = pereval_info_response.add_time.isoformat()
    user_email = 'qwerty@mail.ru'

    response = client.get(
        "/submitData",
        params='user_email=%s' % user_email,
    )

    assert response.status_code == 200
    assert json.loads(response.content)['pereval_data'] == [pereval_info_response.dict()]


def test__on_get(client, pereval_info):

    pereval_info.add_time = pereval_info.add_time.isoformat()

    response = client.get("/submitData/1")
    result = json.loads(response.content)['pereval_data']
    assert response.status_code == 200
    assert result['user'] == pereval_info.user
    assert result['title'] == pereval_info.title


def test__on_patch(client, pereval_info):

    body = pereval_info.dict()
    body.pop('status')
    body['add_time'] = pereval_info.add_time.isoformat()

    response = client.patch(
        "/submitData/1",
        json=body,
    )

    result = json.loads(response.content)['state']

    assert response.status_code == 202
    assert result == 1
