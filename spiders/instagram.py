import scrapy
import re
import json
from pprint import pprint
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from instaparser.items import InstaparserItem
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_link = 'https://www.instagram.com/accounts/login/ajax/'
    user_login = 'king.of.maggots96@gmail.com'
    username = 'tarzan_master_pars'
    password = '#PWD_INSTAGRAM_BROWSER:10:1638903870:AeZQAA6fome76Cje26urBoRFzH3dQ6PzjME66bqFzH12PElLlfKMV/EPuttQwbLMs3hr2Od3iIpSZf6eVkemKKVCGrlXj8zFCFu6wd2Zlmtu/SRY0TkWXBFzdxqwiuaYrV0VWNYyqY/LwrnqQv3w6nDqZQ=='
    follower = 'maxmir__'
    following = 'kyliejenner'
    followers_api_url = 'https://i.instagram.com/api/v1/friendships/7622748212/followers/?count=12&search_surface=follow_list_page'
    following_api_url = 'https://i.instagram.com/api/v1/friendships/7622748212/following/?count=12'
    max_id = 0

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.user_login, 'enc_password': self.password},
                                 headers={'X-CSRFToken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            while True:
                x = input("Для просмотра информации подписчика нажмите 1. Для подписавшегося - нажмите 2")
                if x == '1':
                    yield response.follow(
                        f"/{self.follower}",
                        callback=self.parse_follower,
                        cb_kwargs={'x': x, 'follower': self.follower})
                    break
                elif x == '2':
                    yield response.follow(
                        f'/{self.username}',
                        callback=self.parse_follower,
                        cb_kwargs={'x': x, 'follower': self.following})
                    break
                else:
                    print("Ошибка. Попробуйте снова")

    def parse_follower(self, response: HtmlResponse, x, follower):
        while True:
            new_x = input(f"Собрать информацию подписчиков пользователя: {follower} - 1. Подписок - 2")
            if new_x == '1':
                yield scrapy.Request(self.followers_api_url,
                                     callback=self.parse_info,
                                     cb_kwargs={'x': new_x, 'follower': follower})
                break
            elif new_x == '2':
                yield scrapy.Request(self.following_api_url,
                                     callback=self.parse_info,
                                     cb_kwargs={'x': new_x, 'follower': follower})
                break
            else:
                print("Error. Try again")
                continue

    def parse_info(self, response: HtmlResponse, x, follower):
        followings = response.json()
        for user in followings['users']:
            yield InstaparserItem(
                main_user=follower,
                follower_id=user['pk'],
                username=user['username'],
                photo=user['profile_pic_url'])
        if self.max_id < 400:
            self.max_id += 12
            if x == '1':
                if scrapy.Request(self.followers_api_url[:-32] + f'&max_id={self.max_id}' + self.followers_api_url[-32:],
                                  callback=self.parse_info):
                    yield scrapy.Request(self.following_api_url + f'&max_id={self.max_id}',
                                         callback=self.parse_info,
                                         cb_kwargs={'x': x})
            if x == '2':
                if self.max_id < 400:
                    if scrapy.Request(self.following_api_url+f'&max_id={self.max_id}',
                                             callback=self.parse_info):
                        yield scrapy.Request(self.following_api_url+f'&max_id={self.max_id}',
                                             callback=self.parse_info,
                                             cb_kwargs={'x': x})


    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

