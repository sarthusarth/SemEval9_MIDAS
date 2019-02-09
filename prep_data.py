from modules import preprocessing
import numpy as np
import pandas as pd
import csv
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons,emoticon_groups,exp

TRN_DATA='./data/V1.4_Training.csv'
VAL_DATA='./data/SubtaskA_Trial_Test_Labeled.csv'
TEST_DATA='./data/SubtaskA_EvaluationData_final.csv'
SCRAP_DATA='./data/scraped_reviews_microsoft.csv'
emoticons={x:f'em{emoticons[x][1:-1]}' for x in emoticons} # unique tokens to emoticons
text_processor = TextPreProcessor(
    # terms that will be normalized
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
        'time', 'url', 'date'],
    # terms that will be annotated
    annotate={"hashtag", 'censored'},
    fix_html=True,  # fix HTML tokens
    
    # corpus from which the word statistics are going to be used 
    # for word segmentation 
    segmenter="english", 
    
    # corpus from which the word statistics are going to be used 
    # for spell correction
    corrector="english", 
    
    unpack_hashtags=True,  # perform word segmentation on hashtags
    unpack_contractions=True,  # Unpack contractions (can't -> can not)
    spell_correct_elong=False,  # spell correction for elongated words
    
    # select a tokenizer. You can use SocialTokenizer, or pass your own
    # the tokenizer, should take as input a string and return a list of tokens
    tokenizer=SocialTokenizer(lowercase=False).tokenize,
    
    # list of dictionaries, for replacing tokens extracted from the text,
    # with other expressions. You can pass more than one dictionaries.
    dicts=[emoticons]
)

def fixup(x):
    x = x.replace('U ', "you ").replace('Im ', 'i am ').replace(' r ', " are ").replace(
        ' u ', ' you ').replace('Plz','please').replace('plz','please').replace('pc ','computer ').replace('PC','computer').replace(
        'I\'m','i am').replace('i\'m','i am').replace("' s",'is').replace("' d",'would').replace(' e g',' example').replace(
        "doesn t",'does not').replace("</hashtag>",'').replace(" i e",' ie').replace(" e . g",' example').replace("i . e .","ie")
    
    return x


def read_csv(data_path):
    file_reader = csv.reader(open(data_path,"rt", errors="ignore",encoding="utf-8"), delimiter=',')
    sent_list = []

    for row in file_reader:
        id = row[0]
        sent = row[1]
        lab=row[2]
        sent_list.append(np.array([id,sent,lab]))
    return np.stack(sent_list)


def prepare_text(txt): # input is string 
	txt=' '.join(text_processor.pre_process_doc(txt))
	return preprocessing.preprocess_text(fixup(txt))  # cleans are returns txt


def prepare_dataset(Path):
	ds=read_csv(Path)
	rm=0 # to check removed rows
	cln_ds=[]
	for ix in range(len(ds)):
		idx,txt,lb=ds[ix]
		txt=prepare_text(txt)
		if len(txt)>0:
			cln_ds.append([idx,txt,lb])
		else:
			rm+=1
	print (f'{Path} : removed lines = {rm}')
	cln_ds=np.array(cln_ds)
	cln_ds=pd.DataFrame({0:cln_ds[:,0],1:cln_ds[:,1],2:cln_ds[:,2]})
	cln_ds.to_csv(f'{Path[:-4]}_processed.csv',header=None)



prepare_dataset(TRN_DATA)
prepare_dataset(VAL_DATA)
prepare_dataset(SCRAP_DATA)




