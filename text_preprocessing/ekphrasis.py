from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons

def preprocess_through_ekphrasis(train_file_path, test_file_path, trial_file_path):
    text_processor = TextPreProcessor(
        normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
                   'time', 'url', 'date', 'number'],
        annotate={"hashtag", "allcaps", "elongated", "repeated",
                  'emphasis', 'censored'},
        fix_html=True,
        segmenter="twitter",
        corrector="twitter",
        unpack_hashtags=True,
        unpack_contractions=True,
        spell_correct_elong=True,
        spell_correction=True,
        all_caps_tag="wrap",
        fix_bad_unicode=True,
        tokenizer=SocialTokenizer(lowercase=True).tokenize,
        dicts=[emoticons]
    )

    for file_path in [train_file_path, test_file_path, trial_file_path]:
        with open(file_path, 'r', newline='') as file:
            new_sentences = list()
            labels = list()
            for line in file:
                labels.append(line.split('\t')[0])
                new_sentences.append(" ".join(text_processor.pre_process_doc(line.split('\t')[1])))
        with open(file_path[:-4] + "_ekphrasis.csv", 'w', newline='') as new_file:
            for label, sentence in zip(labels, new_sentences):
                new_file.write("{}\t{}\n".format(label, sentence.replace("[ <hashtag> triggerword </hashtag> #]", "[#TRIGGERWORD#]").replace("[ <allcaps> newline </allcaps> ]", "[NEWLINE]")))