# -*- coding: utf-8 -*-
import ast
import re


def clean_up(FILE):
    lemmata = []
    with open(FILE, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n')
    for line in lines:
        try:
            if line:
                # pre-clean
                if "Tokenliste:" in line:
                    lemma_terms = {"Lemmaliste:", "Lemma:", "Lemmata:",
                                   "Lemma-Liste:"}
                    if any(lt in line for lt in lemma_terms):
                        line = line.split("Lemma")[1].split(':')[1]
                    else:
                        line = line.replace("Tokenliste: ", "")
                arrow_terms = {"=>", "->", "→"}  # ['-', 'Ja'] --> ['-', 'Ja']
                if any(a in line for a in arrow_terms):
                    for a in arrow_terms:
                        if a in line:
                            line = line.split(a)[1].strip()
                            break
                # read list
                if "[" in line or "(" in line:
                    if not ('"' in line or '\'' in line):
                        # list notation without quotation marks "/'
                        sentlemmata = [lemma.strip("()[]\n") for lemma in
                                       line.split(", ")]
                    else:  # list notation
                        sentlemmata = ast.literal_eval(line)
                elif "|" in line:  # Legen|sie|er|auf|mein|Schreibtisch|.
                    sentlemmata = map(str.strip, line.split('|'))
                else:  # white space or comma tokenization
                    if line.count(",") >= (len(line.split())-1):
                        sentlemmata = line.split(', ')
                    else:
                        sentlemmata = line.split()
                sentlemmata = list(map(str.strip, sentlemmata))
                punct = set('?!,.')
                for i, s in enumerate(sentlemmata):
                    if any(s.endswith(p) and s[:-1].isalnum() for p in punct):
                        word, p_mark, empty = re.split('([^a-zA-Z0-9])', s)
                        sentlemmata[i] = word
                        sentlemmata.insert(i+1, p_mark)
                if sentlemmata:
                    lemmata.append(sentlemmata)
        except Exception as e:
            print(line, e)
    return lemmata


clean_up('../../nbs/chatgpt-rub2019-opensubtitles.txt')
