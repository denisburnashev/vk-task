import requests
from pprint import pprint

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

class User_link:

    def __init__(self, ID):
        self.ID = ID

    def __str__(self):
        return 'https://vk.com/id' + self.ID



class VK_user:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def get_followers(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        followers_url = self.url + 'users.getFollowers'
        followers_param = {
            'count': 500,
            'user_id': user_id,
            'fields': 'first_name'
        }
        res = requests.get(followers_url, params={**self.params, **followers_param})
        res = res.json()
        followers_list = res['response']['items']
        print('Всего подписчиков:', res['response']['count'])
        for follower in followers_list:
            print('Имя Фамилия:', follower['first_name'], follower['last_name'], 'ID:', follower['id'])

    def get_friends(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        friends_url = self.url + 'friends.get'
        friends_param = {
            'count': 500,
            'user_id': user_id,
            'fields': 'nickname'
        }
        res = requests.get(friends_url, params={**self.params, **friends_param})
        res = res.json()
        friends_list = res['response']['items']
        return friends_list

    def both_friends(self, user1, user2):
        friends = []
        for friend1 in user1:
            for friend2 in user2:
                if friend1['id'] == friend2['id']:
                    both_friend = friend1['last_name'], friend1['first_name'], friend1['id']
                    friends.append(both_friend)
        for person in friends:
            print(f'Фамилия Имя: {person[0]} {person[1]}, ID пользователя: {person[2]}')


def main():
    while True:
        vk_client = VK_user(token, '5.126')
        user_input = input('Введите:\nboth_friends для поиска общих друзей\nfollowers для получения списка подписчиков\nlink для получения ссылки на профиль\n')
        if user_input == 'both_friends':
            user_input = input('Введите id 1 пользователя:\n')
            user1 = vk_client.get_friends(user_input)
            user_input = input('Введите id 2 пользователя:\n')
            user2 = vk_client.get_friends(user_input)
            vk_client.both_friends(user1, user2)
        elif user_input == 'followers':
            user_input = input('Введите id пользователя для просмотра его подписчиков:\n')
            vk_client.get_followers(user_input)
        elif user_input == 'link':
            user_input = input('Введите id пользователя:\n')
            link_user = User_link(user_input)
            print(link_user)
        elif user_input == 'stop':
            break

print(main())
