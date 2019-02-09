# -*- coding: utf-8 -*-
import re
from text_preprocessing import emoji, hashtag, char, word


def preprocess_text(text):
    text = word.word_replace(text)
    text = char.char_replacing(text)

    text = emoji.emoticon_to_emoji(text)
    text = word.word_expanding(text)
    text = word.word_negation(text)

    text = char.char_escape(text)
    text = char.char_removing(text)
    text = char.currency_replace(text)

    text = emoji.emoji_categorization(text)
    text = emoji.emoji_gender(text)
    text = emoji.escape_emoji(text)

    text = hashtag.process_hashtags(text)

    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
    text = re.sub(r"\s+", " ", text)

    return text


def preprocessing(x):
    max_len = 0
    for i in range(len(x)):
        x[i] = preprocess_text(x[i])

        if len(x[i].split()) > max_len:
            max_len = len(x[i].split())

    return x, max_len


def preprocessing_pipeline(train_x, trial_x, test_x):
    print('Train preprocessing')
    train_x, max_len_train = preprocessing(train_x)

    print('Trial preprocessing')
    trial_x, max_len_trial = preprocessing(trial_x)

    print('Test preprocessing')
    test_x, max_len_test = preprocessing(test_x)

    return train_x, trial_x, test_x, max(max_len_train, max_len_trial, max_len_test)
