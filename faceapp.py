import pynotify
from facepy import GraphAPI
# making connection
graph = GraphAPI('access_token')  # replace with your access token
# switch type menu
choice = input(
    'What you want? \n1.status \n2.feed \n3.posts \n4.inbox \n5.post a status update \n6.notifications \n enter your choice: \n')
# func to filter the recieved json/dictionary object and extract required data


def filter(res, type):
    data = res.get('data')
    if type == 'notifs':
        result = data[0]['title']
        return result
    elif type == 'status':
        result = data[0]['message']
        return result
    elif type == 'feed':
        result = data[0]['message']+'\n'+data[0]['description']
        return result
    elif type == 'inbox':
        msg = data[0]['comments']['data'][0]['message']
        sender = data[0]['comments']['data'][0]['from']['name']
        result = {'data': msg, 'from': sender}
        return result
# func to create a popup using pynotify


def create_popup(text, type_val):
    pynotify.init('test app')
    n = pynotify.Notification(type_val, text)
    n.show()
# main function


def main_func():
        # limit of objects recieved by the GraphAPI
    limit = 1
    if choice == 1:
        res = graph.get('me/statuses', limit=limit)
        data = filter(res, 'status')
        create_popup(data, 'status')
    elif choice == 2:
        res = graph.get('me/feed', limit=limit)
        data = filter(res, 'feed')
        create_popup(data, 'feed')
    elif choice == 3:
        res = graph.get('me/posts', limit=limit)
        data = filter(res, 'posts')
        create_popup(data, 'posts')
    elif choice == 4:
        res = graph.get('me/inbox', limit=limit)
        data = filter(res, 'inbox')
        text = 'From : '+data['from']+'\t'+data['data']
        create_popup(text, 'inbox')
    elif choice == 5:
        msg = raw_input('enter your message \n')
        graph.post('me/feed', message=msg)
    elif choice == 6:
        res = graph.get('me/notifications', limit=limit)
        data = filter(res, 'notifs')
        create_popup(data, 'notifs')
    else:
        print 'invalid'

if choice:
    main_func()
