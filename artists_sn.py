import requests
from bs4 import BeautifulSoup as BS


def sn_get(url_artist: list):
    all_list = []
    insta_list = []
    twitter_list = []
    foundation = []
    for artist in url_artist:
        print('-' * 20)
        print(f'{url_artist.index(artist) + 1}/{(len(url_artist))}')
        print(f'Working with {artist}')
        request = requests.get(artist).text
        soup = BS(request, 'html.parser')

        if 'Collected by' in request:
            print('* Invite detected, adding to main list *'.upper())
            foundation.append(artist)
            social_plate = soup.find('div', class_='st--c-PJLV st--c-bQzyIt st--c-PJLV-iddxAmI-css')

            try:
                social_plate = social_plate.find_all('a', href=True)
                for plate in social_plate:
                    all_list.append(plate['href'])
            except:
                continue

    for link in all_list:
        if 'instagram' in link:
            insta_list.append(link)
        elif 'twitter' in link:
            twitter_list.append(link)

    return insta_list, twitter_list, foundation


if __name__ == '__main__':

    url_artist = ['https://foundation.app/@sahandamani', 'https://foundation.app/@NTV', 'https://foundation.app/@mattecho', 'https://foundation.app/@Snow_W']
    print(sn_get(url_artist))
