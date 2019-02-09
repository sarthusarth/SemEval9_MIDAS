import re

emoji_list = [line.rstrip('\n') for line in open('files/emoji.txt', encoding='UTF-8')]


def escape_emoji(text):
    for emoji in emoji_list:
        text = text.replace(emoji, ' ' + emoji + ' ')
    return text


# def process_emoji(text):
#     for e in emoji.emoji_dict:
#         text = text.replace(e, emoji.emoji_dict[e])
#     # return re.sub("\xf0...", '', str(text))
#     return text


def emoji_gender(text):
    text = re.sub(r"🏻️", "", text)
    text = re.sub(r"🏼‍️", "", text)
    text = re.sub(r"🏽‍️", "", text)
    text = re.sub(r"🏾‍️", "", text)
    text = re.sub(r"🏿️‍", "", text)
    text = re.sub(r"🏻", "", text)
    text = re.sub(r"🏼", "", text)
    text = re.sub(r"🏽", "", text)
    text = re.sub(r"🏾", "", text)
    text = re.sub(r"🏿", "", text)
    text = re.sub(r"♂️", "", text)
    text = re.sub(r"♀️", "", text)
    text = re.sub(r"️", "", text)
    return text


def emoji_categorization(text):
    text = re.sub(r"[☺☻😊😌🙂]+", "🙂", text)
    text = re.sub(r"[😀😁😆😄😃😸😺]+", "😀", text)
    text = re.sub(r"[☹😞😔🙁]+", "🙁", text)
    text = re.sub(r"[♥❤♡💟💝💜💛💚💙🖤💘💗💖💕💓💞💌]+", "💜", text)
    text = re.sub(r"[😗😙😚😍😽😻😘]+", "😘", text)
    text = re.sub(r"[😮😯😲🙀]+", "😮", text)
    text = re.sub(r"[😨😧😦]+", "😦", text)
    text = re.sub(r"[😏]+", "😏", text)
    text = re.sub(r"[😜😝😛]+", "😛", text)
    text = re.sub(r"[🤣😹😂]+", "😂", text)
    text = re.sub(r"[😿😢😭😥😪😢]+", "😢", text)
    text = re.sub(r"[😠😾😤👿😡]+", "😡", text)
    text = re.sub(r"[👬👭👫]+", "👫", text)
    text = re.sub(r"[✔]+", "✅", text)
    text = re.sub(r"[🌞]+", "☀", text)
    text = re.sub(r"[🎊🎉🎈🎂🎆🎇]+", "🎉", text)

    text = re.sub(r"[⚽⚾🏀🏐🏈🏉🎾🎳🏏🏑🏒🏓🏸🥊⛳🏊🏌🏃🏄🎿]+", " :sport: ", text)
    text = re.sub(r"[🌑🌓🌕🌙🌜🌛🌝]+", " :moon: ", text)
    text = re.sub(r"[🌍🌎🌏]+", " :earth: ", text)
    text = re.sub(r"[🐂🐄🐅🐇🐈🐉🐊🐋🐍🐎🐐🐑🐒🐓🐔🐕🐖🐗🐘🐚🐛🐝🐞🐟🐠🐢🐣🐥🐦🐨🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼]+", " :animal: ", text)
    text = re.sub(r"[🍄🍅🍆🍇🍉🍊🍌🍍🍎🍏🍑🍒🍓]+", " :fruit: ", text)
    text = re.sub(r"[🍔🍕🍖🍗🍛🍜🍝🍞🍟🍣🍥🍦🍧🍨🍩🍪🍫🍬🍭🍯🍰]+", " :food: ", text)
    text = re.sub(r"[🇦-🇿]{2}", " :flag: ", text)
    text = re.sub(r"[♩♪♫♬🎵🎶🎷🎸🎹🎺🎼🎤🎧🎻]+", " :music: ", text)
    text = re.sub(r"[🌷🌸🌹🌺🌻🌼]+", " :flower: ", text)
    text = re.sub(r"[🌱🌲🌳🌴🌵🌾🌿🍀🍁🍂🍃]+", " :plant: ", text)
    text = re.sub(r"[🍷🍸🍹🍺🍻🍼🍾]+", " :drink: ", text)
    text = re.sub(r"[👕👗👙👚👛👜👠]+", " :dress: ", text)
    text = re.sub(r"[💰💳💵💷💸]+", " :money: ", text)

    return text


def emoticon_to_emoji(text):
    text = re.sub(r":-*\)+", "🙂", text)
    text = re.sub(r"\(+-*:", "🙂", text)
    text = re.sub(r":-*(d|D)+", "😀", text)
    text = re.sub(r"x-*(d|D)+", "😀", text)
    text = re.sub(r":-*(p|P)+", "😛", text)
    text = re.sub(r":-*\(+", "🙁", text)
    text = re.sub(r";-*\)+", "😉", text)
    text = re.sub(r":-*<+", "😠", text)
    text = re.sub(r":-*/+", "😕", text)
    text = re.sub(r":-*\*+", "😘", text)
    text = re.sub(r":-*(o|O)+", "😮", text)
    text = re.sub(r":'+-*\)+", "😂", text)
    text = re.sub(r":'+-*\(+", "😢", text)
    text = re.sub(r">_<", "😣", text)
    text = re.sub(r"\(-_-\)zzz", "😴", text)
    text = re.sub(r"-_+-", "😑", text)
    text = re.sub(r"\^_+\^", "😊", text)
    text = re.sub(r"\*_+\*", "😍", text)
    text = re.sub(r">_+>", "😒", text)
    text = re.sub(r"<_+<", "😒", text)
    text = re.sub(r"\(⌣́_⌣̀\)", "😌", text)
    text = re.sub(r";_+;", "😢", text)
    text = re.sub(r"3:-+\)", "😈", text)
    text = re.sub(r"<+3+", "💜", text)
    text = re.sub(r">\.<", "🤔", text)
    text = re.sub(r"\._+\.", "😔", text)
    text = re.sub(r"¯\\_\(ツ\)_/¯", "🤷", text)
    text = re.sub(r"¯_\(ツ\)_/¯", "💁", text)
    text = re.sub(r"(o|O)+_+(o|O)+", "😐", text)
    text = re.sub(r"(o|O)+\.+(o|O)+", "😮", text)

    return text
