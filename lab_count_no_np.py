#код не склеян с похожим кодом, который ищет ошибки в согласовании,если подлежащее явялется частью именной группы
#здесь программа ходит по папкам корпуса(скачаны на компьютер - это такие "тестовые тексты", на которых проверяется работа кода)
#если все хорошо, то код отправяется для работы на сайт: http://realec.org

import re, os

import pandas as pd
from os import listdir
from os.path import isfile, join

# open files
def open_file(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
        t = re.sub(r'\n', '', text)
        t = t.split('@')
    return t

#find mistakes in agreement
def find_errors(filename):
    errors = []
    errors_sentences = []
    t = open_file(filename)

    #many|few|fewer|several|both + noun in Sg
    many_few_fewer_several_both = r'(?:<[^>]+\s...>){0,40}<(?:many|few|fewer|several|both) DT0><\S*? NN1>(?:<[^>]+\s...>){0,40}' 
    #great/good deal of/a bit of/ amount of + noun in Pl
    bit_amount_deal= r'(?:(<(?:bit|amount) \S*?>)|(<(?:great|good) AJ0><deal NN1>))<of PRF><\S*? NN2>(?:<[^>]+\s...>){0,40}'
    #number of/couple of + noun in Sg
    number_couple_of= r'(?:<[^>]+\s...>){1,40}<(?:number(s)?|couple) NN1><of PRF><\S*? NN1>(?:<[^>]+\s...>){0,40}'
    
    h_thous_mil_s = r'(?:<[^>]+\s...>){1,40}<(?:hundred(s)?|thousand(s)?|million(s)?|billion(s)?) CRD><of PRF><\S*? NN1>(?:<[^>]+\s...>){0,40}'

    numbers = r'(?:<[^>]+\s...>){1,40}<\w*? CRD><\S*? NN1>(?:<[^>]+\s...>){0,40}'

    little_much = r'(?:<[^>]+\s...>){1,40}<(?:little|much) DT0><\S*? NN2>(?:<[^>]+\s...>){0,40}'

    two_hundreds ='<\S*? CRD><(?:hundreds|thousands|millions|billions) \S*?>'
    one = r'(?:<[^>]+\s...>){0,40}<one CRD><\S*? NN2>(?:<[^>]+\s...>){0,40}'
    the_rich = r'<the AT0><\S*? AJ0>'
    for index in range(len(t)):
        sent_and_mark = re.split(r'(?<=[.!?…])> ', t[index])
        s_and_m = ' '.join(sent_and_mark)
        marking = re.findall(r'<.*>', s_and_m)
        sentence = re.sub('\n', '',re.split(r'<.*>', s_and_m)[0])
        q = ' '.join(marking)

        speople = r'<((sports)?people) \S*?>'
        sfind = re.findall(speople, q)
        if sfind:
            if 'sports' in sfind[0]:
                q = re.sub(r'<sportspeople (\S*?)>', r'<sportspeople NN2>', q)
            else:
                q = re.sub(r'<people (\S*?)>', r'<people NN2>', q)
                

        if re.findall(one, q):
            if re.findall(r'<(?:first|second|third|former|latter|last) \S*?><one \S*?>', q):
                pass
            else:
                errors.append(q)
                errors_sentences.append(sentence)

        if re.findall(two_hundreds, q):
            errors.append(q)
            errors_sentences.append(sentence)


        if re.findall(many_few_fewer_several_both, q):
            if re.findall(r'<(?:many|few|fewer|several|both) DT0><\S*? NN1><\S*? NN2>',q):
                pass
            elif re.findall(r'<both DT0><\S*? [A-Z]{2}[0-9]{1}><and CJC>', q):
                pass
            else:
                errors.append(q)
                errors_sentences.append(sentence)
                
        elif re.findall(number_couple_of, q):
            if re.findall(r'<(?:number(s)?|couple) NN1><of PRF><\S*? NN1><\S*? NN2>',q):
                pass
            elif re.findall(r'<percentage NN[0-9]><number(s)? NN1><of PRF><\S*? NN1><\S*? NN2>',q):д
                pass
            else:
                errors.append(q)
                errors_sentences.append(sentence)


        
        elif re.findall(h_thous_mil_s, q):
            if re.findall(r'<(?:hundred(s)?|thousand(s)?|million(s)?|billion(s)?) CRD><of PRF><\S*? NN1><\S*? NN2>',q):
                pass
            else:
                errors.append(q)
                errors_sentences.append(sentence)

        elif re.findall(bit_amount_deal, q):
            #pass if we find correct phrases such as 'amount of gases/substances'
            if re.findall(r'<amount \S*?><of PRF><(?:gases|substances) NN[0-9]>', q):
                pass
            else:
                errors.append(q)
                errors_sentences.append(sentence)   
            
        elif re.findall(little_much, q):
            errors.append(q)
            errors_sentences.append(sentence)

        elif re.findall(numbers,q):
            if re.findall('<\S*? CRD><\S*? NN1><\S*? NN2>',q):
                pass
            else:
                num = re.findall('<(\S*?) CRD><\S*? NN1>', q)
                for n in num:
                    #pass if '%'
                    if re.findall('{0}%'.format(n), sentence):
                        pass
                    elif n == '1':
                        pass
                    elif n == 'one':
                        pass
                    #pass if a 'procent' or a 'precent'
                    #(the same word, but with spelling mistake) is mentioned
                    elif re.findall('{0} pr(?:e|o)cent'.format(n), sentence):
                        pass
                    #pass if a date is mentioned
                    elif re.findall('{0} year'.format(n), sentence):
                        pass
                    #pass if a date is mentioned (like 'in 2000 there was..')
                    elif re.findall('(?:I|i)n {0}'.format(n), sentence):
                        pass
                    else:
                        errors.append(q)
                        errors_sentences.append(sentence)


    return errors_sentences
