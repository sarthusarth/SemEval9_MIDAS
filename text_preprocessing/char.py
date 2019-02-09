import re


def currency_replace(text):
    text = re.sub(r"\$", " dollar ", text)
    text = re.sub(r"£", " pound ", text)
    text = re.sub(r"€", " euro ", text)
    text = re.sub(r"¥", " yen ", text)
    text = re.sub(r"[¢₡₱₭₦]", " currency ", text)

    return text


def char_removing(text):
    text = text.replace("http://url.removed", "")
    text = re.sub(r"[ं-ో̇]", "", text)
    text = re.sub(r"[•]", "", text)
    text = re.sub(r"[】【]", "", text)
    text = re.sub(r"[0-9]+", " ", text)
    text = re.sub(r"[\{\}\(\)\[\]]+", " ", text)
    text = re.sub(r"[*/\&|_<>~\+=\-\^™\\\%\"]+", " ", text)
    text = re.sub(r"[‼.,;:?!…]+", " ", text)

    return text


def char_replacing(text):
    text = re.sub(r"[‘´’̇]+", "\'", text)
    text = re.sub(r"[#̇]+", "#", text)
    text = re.sub(r"[”“❝„\"]", "\"", text)

    return text


def char_escape(text):
    text = re.sub(r'\'\b', '\' \1', text)
    text = re.sub(r'\b\'', '\1 \'', text)
    text = re.sub(r'\(\b', '\( \1', text)
    text = re.sub(r'\b\)', '\1 \)', text)
    text = re.sub(r':\b', ': \1', text)
    text = re.sub(r'\b:', '\1 :', text)
    text = re.sub(r'\-\b', '- \1', text)
    text = re.sub(r'\b\-', '\1 -', text)
    text = re.sub(r'—\b', '- \1', text)
    text = re.sub(r'\b—', '\1 -', text)
    text = re.sub(r'\b\^', '\1 \^', text)
    text = re.sub(r'\^\b', '\^ \1', text)

    return text
