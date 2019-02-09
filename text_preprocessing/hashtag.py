import re

dictionary = [line.rstrip('\n') for line in open('files/dict.txt', encoding='UTF-8')]


def process_hashtags(text):
    hashtags = re.findall(r" (#\w+)", text)

    for hashtag in hashtags:
        processed_hashtag = hashtag[1:]
        if processed_hashtag in dictionary:
            text = text.replace(hashtag, processed_hashtag)

    return text
