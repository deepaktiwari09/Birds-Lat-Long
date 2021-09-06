from calendar import Calendar
import string as st

#In Progress
class __Converter():
    def __init__(self):
        pass
    
    def sentence_to_group_list(self,sentence:str,word:str):
        list_object = []
        f_in = 0
        l_in = len(word)
        for x in range(0,int(len(sentence)/len(word))):
            list_object.append(sentence[f_in:l_in])
            f_in = f_in + len(word)
            l_in = l_in + len(word)
        if len(word) != 1:
            gap = len(sentence)-(len(list_object)*len(word))
            list_object.append(sentence[-gap:])
        return list_object

    def sentence_to_simple_list(self,sentence:str):
        result = []
        for x in range(0,len(sentence)):
            result.append(sentence[x])
        return result
    
    def sentence_to_simple_index_list(self,sentence_list:list):
        result = []
        for x in range(0,len(sentence_list)):
            result.append(x)
        return result

    
class Remover(__Converter):
    
    def __init__(self):
        pass

    def remove_Latter(self,sentence:str,latter_to_remove:str):
        result = ""
        for x in range(0,len(sentence)):
            if sentence[x] != latter_to_remove:
                result = result + str(sentence[x])
            else:
                continue
        return result

    def remove_word(self,sentence:str,word_to_remove:str):
        sent = sentence
        index = sentence.find(word_to_remove)
        re_len = [x+1 for x in range(0,len(word_to_remove))]
        result = ""
        if len(word_to_remove) != 1:
            loop_val = True
            while loop_val :
                if index != -1: # founded
                    a = []
                    for x in range(0,len(sent)):
                        if x != index and x not in [index + re_len[x] for x in range(0,len(re_len)-1)]:
                            a.append(sent[x])
                    sent = ""
                    for y in range(0,len(a)):
                        sent = sent + str(a[y])
                     
                    index = sent.find(word_to_remove)
                    
                    if index == -1: # not founded
                        result = sent
                        
                        break
                if index == -1:
                    result = ""
                    break
            return result
        if len(word_to_remove) == 1:
            return ""


class Finder(Remover,__Converter):
    def __init__(self):
        pass
    #work in progress
    def word_finder(self,sentence,word_to_find):
        removed_sent = super().sentence_to_simple_list( super().remove_word(sentence, word_to_find))
        main_list = super().sentence_to_simple_list(sentence)
        main_index_list = super().sentence_to_simple_index_list(main_list)
        sub_result = []
        result = []
        if len(removed_sent) != 0 :
            for x in range(0,len(main_list)):
                if main_list[x] in removed_sent:
                    sub_result.append(x)
            print(main_index_list)
            print(sub_result)
            for x in range(0,len(main_index_list)):
                if main_index_list[x] not in sub_result:
                    result.append(main_index_list[x])
            
            send_data = []
            a = 0
            print(result)
            for x in range(0,int(len(result)/len(word_to_find))):
                send_data.append((result[a],result[a+len(word_to_find)-1]))
                a = a + len(word_to_find)
            return send_data
        if len(removed_sent) == 0:
            send_data = []
        
            return send_data
