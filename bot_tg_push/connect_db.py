import pymysql
from pymysql.cursors import DictCursor

DOMAIN = 'https://lucky-spb.online/'

def execute_target():
    connection = pymysql.connect(
        host='localhost',
        user='django',
        password='djangoPass',
        db='SellBuildKRD',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT * FROM Sell_sell WHERE published_tg=0;')
        q_data = cur.fetchall()
        # print('q_data', q_data)
        if q_data != ():
            update_published_tg(q_data)
    return q_data


def update_published_tg(q):
    connection = pymysql.connect(
        host='localhost',
        user='django',
        password='djangoPass',
        db='SellBuildKRD',
        charset='utf8mb4',
        cursorclass=DictCursor
    )

    id_list = []
    for id in q:
        id_list.append(id['id'])
    with connection:
        cur = connection.cursor()
        ids = ''
        for id in id_list:
            ids += f'{id},'
        cur.execute(f'UPDATE Sell_sell SET published_tg = TRUE WHERE id in ({ids[:-1]});')
        connection.commit()


def parse_data():
    q = execute_target()
    target_dict = {}
    for target in q:
        connection = pymysql.connect(
            host='localhost',
            user='django',
            password='djangoPass',
            db='SellBuildKRD',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        with connection:
            cur = connection.cursor()
            cur.execute(f'SELECT * FROM Sell_image WHERE sellId_id = {target["id"]};')
            q_image = cur.fetchall()
        target_dict[target['id']] = {}
        image_list = []
        for image in q_image:
            image_list.append(DOMAIN + f"{image['imageSell']}")
            # print(image['imageSell'])
        target_dict[target['id']]['image_list'] = image_list
        target_dict[target['id']]['headerImage'] = DOMAIN + f'{target["headerImage"]}'
        target_dict[target['id']]['nameSell'] = target["nameSell"]
        target_dict[target['id']]['address'] = target["address"]
        target_dict[target['id']]['furnish'] = target["furnish"]
        target_dict[target['id']]['specifications'] = target["specifications"]
        target_dict[target['id']]['price'] = target["price"]
        target_dict[target['id']]['telephone'] = target["telephone"]

    # print(target_dict)
    # print('target_dict', target_dict)
    return target_dict


if __name__ == '__main__':
    # execute_target()
    parse_data()
