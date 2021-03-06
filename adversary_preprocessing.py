import requests
import json
from collections import OrderedDict
from termcolor import colored

paragraph_list = []
paragraph_category_score_list = []

'''
TODO:
Add text corpus reading and then iterate through the resulting paragraphs in the triplet_create function below
'''

'''
I/O Information...

I: Text Corpus File
O: List of Paragraph, Category, Category_Score Triplets

'''

def get_paragraphs(file):
    paragraph_list = []
    para = []
    with open(file, 'r') as f:
        for line in f:
            if line.isspace() == False:
                para.append(line)
            else:
                #zip para and append to overall paragraph list
                joined = "".join(para)
                paragraph_list.append(joined)
                para = []
    
    return paragraph_list  

def create_triplet_list(paragraph_list):
    paragraph_category_score_list = []
    for para in paragraph_list:
        r1 = requests.post('https://pribot.org/api/getCategories',
                   json={'key': 'xXaJt4QsteETBAa8UY4G4QZeMHRK7upUdf2XrFQZQpN', 'texts': [para]},
                       headers={'Content-Type': 'application/json'},
                       cookies={},
        )
    
        resp = r1.json()

        #Saving category labels (in order of confidence 0 is most, etc...)
        cat_strs = resp['category_classes']
        cat_strs_list = cat_strs.split(",")
        cat_strs_list_cleaned = []
        for item in cat_strs_list:
            clean = item.replace(" ","")
            cleaner = clean.replace("[[","")
            cleanest = cleaner.replace("'","")
            ultra_clean = cleanest.replace("]]","")
            cat_strs_list_cleaned.append(ultra_clean)
    
        #Saving category confidence scores (in same order as above...)
        cat_scores = resp['category_scores']
        cat_scores_list = cat_scores.split(",")
        cat_scores_list_cleaned = []
        for item in cat_scores_list:
            clean = item.replace(" ","")
            cleaner = clean.replace("[[","")
            cleanest = cleaner.replace("'","")
            ultra_clean = cleanest.replace("]]","")
            cat_scores_list_cleaned.append(ultra_clean)
        
        #Want: [ (paragraph, list of every cat and score over .7), ditto, ditto, ]
        over_70pct_cats = []
        over_70pct_scores = []
        for item in range(len(cat_scores_list_cleaned)):
            if float(cat_scores_list_cleaned[item]) >= .70:
                over_70pct_cats.append(cat_strs_list_cleaned[item])
                over_70pct_scores.append(cat_scores_list_cleaned[item])
        
        #Create paragraph, classification, and confidence score triplets
        triplet = [para,over_70pct_cats,over_70pct_scores] #changed this to a list- needs to be mutable
        #print (triplet)
        #append triplet to paragraph_category_score_list 
        paragraph_category_score_list.append(triplet) #paragraph, category, score
       
    
    return paragraph_category_score_list



'''
Cleans dataset of unclassified elements (for some reason the classifier didn't mark every
piece of text that I gave it), and segments each paragraph by the first-most confident data
category

'''

def segment_dataset(corpus_triplet_list,desired_index):
    #Make a list for each type of classification 
    #and place each instance in the corresponding list
    privacy_contact_information = [] #index 0
    third_party_sharing_collection = [] #index 1
    user_choice_control = [] #index 2
    introductory_generic = [] #index 3
    data_security = [] #index 4
    first_party_collection_use = [] #index 5
    international_and_specific_audiences = [] #index 6
    policy_change = [] #index 7
    do_not_track = [] #index 8 
    user_access_edit_and_deletion = [] #index 9
    practice_not_covered = [] #index 10
    data_retention = [] #index 11

    master_list = [privacy_contact_information,third_party_sharing_collection,user_choice_control,introductory_generic,data_security,first_party_collection_use,international_and_specific_audiences,policy_change,do_not_track, user_access_edit_and_deletion,practice_not_covered,data_retention]
        
    


    #Rid corpus_triplet_list of unclassified items...
    cleaned_list = []
    for i in corpus_triplet_list:
        if len(i[1]) >= 1:
            cleaned_list.append(i)
    
    #print("---------------")
    #print(cleaned_list)
    #Iterate through the triplet list and do necessary additions 
    for item in cleaned_list:
        if item[1][0] == "privacy-contact-information":
            privacy_contact_information.append(item)
        if item[1][0] == "third-party-sharing-collection":
            third_party_sharing_collection.append(item)
        if item[1][0] == "user-choice-control":
            user_choice_control.append(item)
        if item[1][0] == "introductory-generic":
            introductory_generic.append(item)
        if item[1][0] == "data-security":
            data_security.append(item)
        if item[1][0] == "first-party-collection-use":
            first_party_collection_use.append(item)
        if item[1][0] == "international-and-specific-audiences":
            international_and_specific_audiences.append(item)
        if item[1][0] == "policy-change":
            policy_change.append(item)
        if item[1][0] == "do-not-track":
            do_not_track.append(item)
        if item[1][0] == "user-access-edit-and-deletion":
            user_access_edit_and_deletion.append(item)
        if item[1][0] == "practice-not-covered":
            practice_not_covered.append(item)
        if item[1][0] == "data-retention":
            data_retention.append(item)
    
    return master_list[desired_index]

def segment_dataset(corpus_triplet_list,desired_index):
    #Make a list for each type of classification 
    #and place each instance in the corresponding list
    privacy_contact_information = [] #index 0
    third_party_sharing_collection = [] #index 1
    user_choice_control = [] #index 2
    introductory_generic = [] #index 3
    data_security = [] #index 4
    first_party_collection_use = [] #index 5
    international_and_specific_audiences = [] #index 6
    policy_change = [] #index 7
    do_not_track = [] #index 8 
    user_access_edit_and_deletion = [] #index 9
    practice_not_covered = [] #index 10
    data_retention = [] #index 11

    master_list = [privacy_contact_information,third_party_sharing_collection,user_choice_control,introductory_generic,data_security,first_party_collection_use,international_and_specific_audiences,policy_change,do_not_track, user_access_edit_and_deletion,practice_not_covered,data_retention]
        
    


    #Rid corpus_triplet_list of unclassified items...
    cleaned_list = []
    for i in corpus_triplet_list:
        if len(i[1]) >= 1:
            cleaned_list.append(i)
    
    #print("---------------")
    #print(cleaned_list)
    #Iterate through the triplet list and do necessary additions 
    for item in cleaned_list:
        if item[1][0] == "privacy-contact-information":
            privacy_contact_information.append(item)
        if item[1][0] == "third-party-sharing-collection":
            third_party_sharing_collection.append(item)
        if item[1][0] == "user-choice-control":
            user_choice_control.append(item)
        if item[1][0] == "introductory-generic":
            introductory_generic.append(item)
        if item[1][0] == "data-security":
            data_security.append(item)
        if item[1][0] == "first-party-collection-use":
            first_party_collection_use.append(item)
        if item[1][0] == "international-and-specific-audiences":
            international_and_specific_audiences.append(item)
        if item[1][0] == "policy-change":
            policy_change.append(item)
        if item[1][0] == "do-not-track":
            do_not_track.append(item)
        if item[1][0] == "user-access-edit-and-deletion":
            user_access_edit_and_deletion.append(item)
        if item[1][0] == "practice-not-covered":
            practice_not_covered.append(item)
        if item[1][0] == "data-retention":
            data_retention.append(item)
    
    return master_list[desired_index]

def get_masterlist(corpus_triplet_list):
    #Make a list for each type of classification 
    #and place each instance in the corresponding list
    privacy_contact_information = [] #index 0
    third_party_sharing_collection = [] #index 1
    user_choice_control = [] #index 2
    introductory_generic = [] #index 3
    data_security = [] #index 4
    first_party_collection_use = [] #index 5
    international_and_specific_audiences = [] #index 6
    policy_change = [] #index 7
    do_not_track = [] #index 8 
    user_access_edit_and_deletion = [] #index 9
    practice_not_covered = [] #index 10
    data_retention = [] #index 11

    master_list = [privacy_contact_information,third_party_sharing_collection,user_choice_control,introductory_generic,data_security,first_party_collection_use,international_and_specific_audiences,policy_change,do_not_track, user_access_edit_and_deletion,practice_not_covered,data_retention]
     

    #Rid corpus_triplet_list of unclassified items...
    cleaned_list = []
    for i in corpus_triplet_list:
        if len(i[1]) >= 1:
            cleaned_list.append(i)
    
    #print("---------------")
    #print(cleaned_list)
    #Iterate through the triplet list and do necessary additions 
    for item in cleaned_list:
        if item[1][0] == "privacy-contact-information":
            privacy_contact_information.append(item)
        if item[1][0] == "third-party-sharing-collection":
            third_party_sharing_collection.append(item)
        if item[1][0] == "user-choice-control":
            user_choice_control.append(item)
        if item[1][0] == "introductory-generic":
            introductory_generic.append(item)
        if item[1][0] == "data-security":
            data_security.append(item)
        if item[1][0] == "first-party-collection-use":
            first_party_collection_use.append(item)
        if item[1][0] == "international-and-specific-audiences":
            international_and_specific_audiences.append(item)
        if item[1][0] == "policy-change":
            policy_change.append(item)
        if item[1][0] == "do-not-track":
            do_not_track.append(item)
        if item[1][0] == "user-access-edit-and-deletion":
            user_access_edit_and_deletion.append(item)
        if item[1][0] == "practice-not-covered":
            practice_not_covered.append(item)
        if item[1][0] == "data-retention":
            data_retention.append(item)
    
    return master_list

def main():
    '''
    f = "policy_corpus_partial_cleaned_part.txt"
    para_list = get_paragraphs(f)
    print ("================")
    print (para_list)
    print ("================")
    dataset_list = create_triplet_list(para_list)
    print ("================")
    print (dataset_list)
    print ("================")
    '''
main()
