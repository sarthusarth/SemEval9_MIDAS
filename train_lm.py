from fastai.text import *
from sklearn.model_selection import train_test_split


BOS = 'xbos'  # beginning-of-sentence tag
FLD = 'xfld'
max_vocab = 60000
min_freq = 1
em_sz,nh,nl = 400,1150,3  #Embedding size,num_hidden,num_layers

wd=1e-7
bptt=70
bs=48
lrs=1e-3
drops = np.array([0.25, 0.1, 0.2, 0.02, 0.15])*0.9
opt_fn = partial(optim.Adam, betas=(0.8, 0.99))

def read(path): # Reading csv files
  ds=pd.read_csv(path,header=None)
  ds=pd.DataFrame({0:ds[3],1:ds[2]})
  return ds
def rm_space(x): # To remove space that appears after pre-processing
  if (x[0]==' '): 
    return x[1:] 
  else :
    return x
def get_texts(df, n_lbls=1):
    labels = df.iloc[:,range(n_lbls)].values.astype(np.int64)
    texts = f'\n{BOS} {FLD} 1 ' + df[n_lbls].astype(str)
    for i in range(n_lbls+1, len(df.columns)): texts += f' {FLD} {i-n_lbls} ' + df[i].astype(str)
    texts = list(texts.values)

    tok = Tokenizer().proc_all_mp(partition_by_cores(texts))
    return tok, list(labels)


def train(trn_texts,val_texts):
	tok_trn, trn_labels = get_texts(trn_texts, 1)
	tok_val, val_labels = get_texts(val_texts, 1)
	freq = Counter(p for o in tok_trn for p in o)
	itos = [o for o,c in freq.most_common(max_vocab) if c>min_freq]
	itos.insert(0, '_pad_')
	itos.insert(0, '_unk_')
	stoi = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})
	trn_lm = np.array([[stoi[o] for o in p] for p in tok_trn])
	val_lm = np.array([[stoi[o] for o in p] for p in tok_val])
	
	#Using pre-trained weights
	PRE_PATH =Path('./wt103')
	PRE_LM_PATH = Path(f'{PRE_PATH}/fwd_wt103.h5')
	wgts = torch.load(PRE_LM_PATH, map_location=lambda storage, loc: storage)
	enc_wgts = to_np(wgts['0.encoder.weight'])
	row_m = enc_wgts.mean(0)
	itos2 = pickle.load((PRE_PATH/'itos_wt103.pkl').open('rb'))
	stoi2 = collections.defaultdict(lambda:-1, {v:k for k,v in enumerate(itos2)})
	new_w = np.zeros((max_vocab, em_sz), dtype=np.float32)
	for i,w in enumerate(itos):
    r = stoi2[w]
    new_w[i] = enc_wgts[r] if r>=0 else row_m
    wgts['0.encoder.weight'] = T(new_w)
	wgts['0.encoder_with_dropout.embed.weight'] = T(np.copy(new_w))
	wgts['1.decoder.weight'] = T(np.copy(new_w))
	
	trn_dl = LanguageModelLoader(np.concatenate(trn_lm), bs, bptt)
	val_dl = LanguageModelLoader(np.concatenate(val_lm), bs, bptt)
	md = LanguageModelData(PATH, 1, max_vocab, trn_dl, val_dl, bs=bs, bptt=bptt)
	learner= md.get_model(opt_fn, em_sz, nh, nl, 
    dropouti=drops[0], dropout=drops[1], wdrop=drops[2], dropoute=drops[3], dropouth=drops[4])

	learner.metrics = [accuracy]
	learner.freeze_to(-1)
	learner.model.load_state_dict(wgts)
	learner.fit(lrs, 2, wds=wd, use_clr=(32,2), cycle_len=1)
	learner.unfreeze()
	learner.fit(lrs, 5, wds=wd, use_clr=(20,10), cycle_len=1)
	return learner,itos

ds_train=read('./data/V1.4_Training_processed.csv')
ds_val=read('./data/SubtaskA_Trial_Test_Labeled_processed.csv')
ds_scrap=read('./data/scraped_reviews_microsoft_processed.csv')
ds_eval=read('./data/SubtaskA_EvaluationData_final_processed.csv')

ds_lm=pd.concat([ds_train,ds_val,ds_scrap,ds_eval]).reset_index(drop=True)
ds_lm[1]=ds_lm[1].apply(lambda x: rm_space(x))
ds_lm=ds_lm[ds_lm[1]!=''].reset_index(drop=True)

trn_texts,val_texts = sklearn.model_selection.train_test_split(
    ds_lm, test_size=0.1,random_state=42)


language_model,itos=train(trn_texts,val_texts)
language_model.save_encoder('./trained/language_model')
itos=np.save('./trained/itos.npy',itos)