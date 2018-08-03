import requests 
import json

def return_category(para):
  r1 = requests.post('https://pribot.org/api/getCategories',
                  json={'key': 'xXaJt4QsteETBAa8UY4G4QZeMHRK7upUdf2XrFQZQpN', 'texts': [para]},
                      headers={'Content-Type': 'application/json'},
                      cookies={},)
   
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
  #print type(cat_scores_list_cleaned[0])

  cat_score_over = []
  cat_over = []

  for i in range(len(cat_strs_list_cleaned)):
    if float(str(cat_scores_list_cleaned[i])) >= .7:
      cat_over.append(cat_strs_list_cleaned[i])
      #print(cat_scores_list_cleaned[i])
      #print("---------------------------")
      #print(cat_strs_list_cleaned[i])
      #print("---------------------------")
      cat_score_over.append(cat_scores_list_cleaned[i])

  to_return = (para, zip(cat_over, cat_score_over), cat_over)

  #print("------------------------------------------")
  #print(to_return[2])
  results = list(zip(cat_over,cat_score_over))
  return results
'''
total_count = 100
success_count = 0
test_results = []
for i in range(total_count):
  orig_text = raw_input("What piece of text would you like to test?... \n")
  orig_result = return_category(orig_text)

  adv_text = raw_input("What piece of adversarial text would you like to test... \n")
  adv_result = return_category(adv_text)

  test_results.append((orig_result, adv_result))

  to_compare = orig_result[2]
  to_compare2 = adv_result[2]

  results_add = set(to_compare + to_compare2)

  if len(results_add) == (len(to_compare2) + len(to_compare)):
    success_count+=1

success_rate = (success_count/total_count) * 100

#print success_rate
'''

