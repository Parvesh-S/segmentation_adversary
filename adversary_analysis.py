from adversary_preprocessing import get_paragraphs,create_triplet_list,segment_dataset, get_masterlist
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize
import math
'''
I/O Specification...

1. TF-IDF...
I: Master list with paragraph, category, score triplets for each category
   (in this case, we only care about tokenizing each paragraph and feeding that to the algorithm to see word statistics, but I want to keep the category that each paragraph(and thereby words) came from for later analysis)

O: Aggregated list of words and tf-idf score pairs, along with each umbrella category (sort these by tf-idf score inside each category)


2. Word Probability Calculation...
I: List of all words present in each category (pass in master list for later use)
O: Probability a given word is a part of a given category 

(This should be run on every category and then all outputs should 
be compared to see which words are most predictive for each respective category
across the board)
|
|
V
Mergesort resulting pairs by probability

3. Merge tf-idf and word_category_probability results for each category

'''

#Run tf_idf() on each category's data tuple list
def tf_idf(category_data_list):
    document_count = len(category_data_list)
    copied_list = []
    for item in category_data_list:
        #tmp_list = [item[0].lower,item[1],item[2]]
        copied_list.append(item[0].lower())
    vectorizer = TfidfVectorizer(norm='l2', ngram_range=(1,4))

    fit = vectorizer.fit_transform(copied_list)
    idf = vectorizer.idf_
    data = list(zip(vectorizer.get_feature_names(),idf))
    data.sort(key=lambda tup: tup[1])
    return data

#Run word_category_counts on each category's data tuple list
def word_category_counts(document_category_list):
    unique_word_dict = {}
    do_not_add = ["'/'","./.",",/,"]
    for document in document_category_list:
        doc_tokenized = word_tokenize(document[0])
        for word in doc_tokenized:
            word_tagged = nltk.tag.pos_tag([word.lower()])
            #print(word_tagged)
            word_with_pos = '/'.join(str(i) for i in word_tagged[0])
            if word_with_pos not in unique_word_dict and word_with_pos not in do_not_add:
                unique_word_dict[word_with_pos] = 1
            elif word_with_pos not in do_not_add:
                unique_word_dict[word_with_pos] += 1
    
    word_keys = list(unique_word_dict.keys())
    word_values = list(unique_word_dict.values())

    #OUTPUT: Each unique word and the corresponding number of
    #occurrences (list of tuples)
    cat_final_list =  zip(word_keys,word_values)
    return unique_word_dict

#Run corpus_word_counts on master list of all categories
#NOTE: Give this function the list of all paragraphs
def corpus_word_counts(total_list):
    total_counts_dict = {}
    for l in total_list:
        for word in word_tokenize(l):
            word_tagged = nltk.tag.pos_tag([word.lower()])
            word_with_pos = '/'.join(str(i) for i in word_tagged[0])
            if word_with_pos not in total_counts_dict:
                total_counts_dict[word_with_pos] = 1
            else:
                total_counts_dict[word_with_pos] += 1
    return total_counts_dict
 
#feed output of corpus_word_counts (master_list) to word_category_probs()
def word_category_probs(merged_counts_dict,cat_dict,cat_name):
    #Want: to return a list of probabilities that a given word 
    #will be attached to a given category
    #returns a list with sorted probabilities
    total_keys = list(merged_counts_dict.keys())
    total_values = list(merged_counts_dict.keys())
    probs_list = []
    for word,count in cat_dict.items():
        if merged_counts_dict[word] == 0:
            #raise Exception('Zero count item encountered in total dictionary.')
            continue
        else:
            prob = float(count / merged_counts_dict[word])
            word_prob_tuple = (word,prob)
            probs_list.append(word_prob_tuple)
    probs_list.sort(key=lambda tup: tup[1])
    return probs_list

'''
TODO:
Currently get_candidates only will return intersected single words because 
the probability count scripts do not take into account n-grams of 
size greater than 1.
So, we want to add support for n-grams there in order to allow
the get_candidates results to be stronger. 
'''
def get_candidates(cat_name,probs_list,tfidf_list):
    #take in the prob list and tfidf list, do pruning by some metrics,
    # and then do a union
    # Return the intersected set
    tfidf_cpy = []
    for item in tfidf_list:
        tfidf_cpy.append(item[0])
    probs_cpy = []
    for item in probs_list:
        separator = "/"
        word = item[0].split(separator,1)[0]
        probs_cpy.append(word)
    
    tfidf_split = math.floor(len(tfidf_list) / 2)
    tfidf_words = tfidf_cpy[tfidf_split:]
    tfidf_set = set(tfidf_words)
    
    probs_split = math.floor(len(probs_list)* .65)
    probs_words = probs_cpy[probs_split:]
    probs_set = set(probs_words)
    
    intersect_set = tfidf_set.intersection(probs_set)
    

    '''
    #further prune and add common n-grams to final set
    #this is not the most elegant thing but it's an ok stop-gap 
    #until I add better n-gram support within the prob functions
    n_gram_set = []
    for item in tfidf_words:
        if len(item[0].split(" ")) > 1:
            n_gram_set.append(item)
    n_gram_set.sort(key=lambda tup: tup[1])
    n_gram_cutoff = math.floor(len(n_gram_set) * .85)
    n_gram_final = []
    for item in n_gram_set[n_gram_cutoff:]:
        n_gram_final.append(item[0])
    n_gram_final_set = set(n_gram_final)
    print(n_gram_final_set)
    final_set = n_gram_final_set.union(intersect_set)
    ''' 
    return [cat_name,list(intersect_set)]




f = "policy_corpus_partial_cleaned_part.txt"
para_list = get_paragraphs(f)
dataset_list = create_triplet_list(para_list)
master_list = get_masterlist(dataset_list)
#Segmenting the dataset
pci_list = segment_dataset(dataset_list,0)
tpsc_list = segment_dataset(dataset_list,1)
ucc_list = segment_dataset(dataset_list,2)
ig_list = segment_dataset(dataset_list,3)
ds_list = segment_dataset(dataset_list,4)
fpcu_list = segment_dataset(dataset_list,5)
iasa_list = segment_dataset(dataset_list,6)
pc_list = segment_dataset(dataset_list,7)
dnt_list = segment_dataset(dataset_list,8)
uaead_list = segment_dataset(dataset_list,9)
pnc_list = segment_dataset(dataset_list,10)
dr_list = segment_dataset(dataset_list,11)

#Total unique word occurrences across each category
total_counts_dict = corpus_word_counts(para_list)

#Getting word occurrences for each cat (Dicts), probs for each cat,
# tfidf for each cat, and adv options for each cat (in that order)

if len(pci_list) > 0:
    pci_counts_dict = word_category_counts(pci_list)
    pci_probs = word_category_probs(total_counts_dict,pci_counts_dict,"privacy-contact-information")
    pci_tfidf = tf_idf(pci_list)
    pci_options = get_candidates("privacy-contact-information",pci_probs,pci_tfidf)
    
if len(tpsc_list) > 0:
    tpsc_counts_dict = word_category_counts(tpsc_list)
    tpsc_probs = word_category_probs(total_counts_dict,tpsc_counts_dict,"third-party-sharing-collection")
    tpsc_tfidf = tf_idf(tpsc_list)
    tpsc_options = get_candidates("third-party-sharing-collection",tpsc_probs,tpsc_tfidf)
    
if len(ucc_list) > 0:
    ucc_counts_dict = word_category_counts(ucc_list)
    ucc_probs = word_category_probs(total_counts_dict,ucc_counts_dict,"user-choice-control")
    ucc_tfidf = tf_idf(ucc_list)
    ucc_options = get_candidates("user-choice-control",ucc_probs,ucc_tfidf)

if len(ig_list) > 0:
    ig_counts_dict = word_category_counts(ig_list)
    ig_probs = word_category_probs(total_counts_dict,ig_counts_dict,"introductory-generic")
    ig_tfidf = tf_idf(ig_list)
    ig_options = get_candidates("introductory-generic",ig_probs, ig_tfidf)

if len(ds_list) > 0:
    ds_counts_dict = word_category_counts(ds_list)
    ds_probs = word_category_probs(total_counts_dict,ds_counts_dict,"data-security")
    ds_tfidf = tf_idf(ds_list)
    ds_options = get_candidates("data-security",ds_probs,ds_tfidf)
    
if len(fpcu_list) > 0:
    fpcu_counts_dict = word_category_counts(fpcu_list)
    fpcu_probs = word_category_probs(total_counts_dict,fpcu_counts_dict,"first-party-collection-use")
    fpcu_tfidf = tf_idf(fpcu_list)
    fpcu_options = get_candidates("first-party-collection-use",fpcu_probs,fpcu_tfidf)

if len(iasa_list) > 0:
    iasa_counts_dict = word_category_counts(iasa_list)
    iasa_probs = word_category_probs(total_counts_dict,iasa_counts_dict,"international-and-specific-audiences")
    iasa_tfidf = tf_idf(iasa_list)
    iasa_options = get_candidates("international-and-specific-audiences",iasa_probs,iasa_tfidf)

if len(pc_list) > 0:
    pc_counts_dict = word_category_counts(pc_list)
    pc_probs = word_category_probs(total_counts_dict,pc_counts_dict,"policy-change")
    pc_tfidf = tf_idf(pc_list)
    pc_options = get_candidates("policy-change",pc_probs,pc_tfidf)

if len(dnt_list) > 0:
    dnt_counts_dict = word_category_counts(dnt_list)
    dnt_probs = word_category_probs(total_counts_dict,dnt_counts_dict,"do-not-track")
    dnt_tfidf = tf_idf(dnt_list)
    dnt_options = get_candidates("do-not-track",dnt_probs,dnt_tfidf)

if len(uaead_list) > 0:
    uaead_counts_dict = word_category_counts(uaead_list)
    uaead_probs = word_category_probs(total_counts_dict,uaead_counts_dict,"user-access-edit-and-deletion")
    uaead_tfidf = tf_idf(uaead_list)
    uaead_options = get_candidates("user-access-edit-and-delection",uaead_probs,uaead_tfidf)

if len(pnc_list) > 0:
    pnc_counts_dict = word_category_counts(pnc_list)
    pnc_probs = word_category_probs(total_counts_dict,pnc_counts_dict,"practice-not-covered")
    pnc_tfidf = tf_idf(pnc_list)
    pnc_options = get_candidates("policy-not-covered",pnc_probs,pnc_tfidf)

if len(dr_list) > 0:
    dr_counts_dict = word_category_counts(dr_list)
    dr_probs = word_category_probs(total_counts_dict,dr_counts_dict,"data-retention")
    dr_tfidf = tf_idf(dr_list)
    dr_options = get_candidates("data-retention",dr_probs,dr_tfidf)

