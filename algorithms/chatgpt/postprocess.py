# -*- coding: utf-8 -*-
import ast
import re


def clean_up(FILE):
    lemmata = []
    with open(FILE, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n')
    for line in lines:
        line = line.strip()  # remove whitespaces in beginning/end
        try:
            if line:
                # pre-clean
                if "Tokenliste:" in line:
                    line = line.replace("Tokenliste: ", "")
                lemma_terms = {"Lemmaliste:", "Lemma:", "Lemmata:",
                               "Lemma-Liste:", "lemmatisiert"}
                if any(lt.lower() in line.lower() for lt in lemma_terms):
                    line = line.split("emma")[1].split(':')[1]
                arrow_terms = {"=>", "->", "→"}  # ['-', 'Ja'] --> ['-', 'Ja']
                if any(a in line for a in arrow_terms):
                    for a in arrow_terms:
                        if a in line:
                            line = line.split(a)[1].strip()
                            break
                # read list
                if "|" in line and (line.count("|") >= 3):
                    # Legen|sie|er|.
                    sentlemmata = map(str.strip, line.split('|'))
                elif "+" in line and (line.count("+") >= 3):
                    sentlemmata = map(str.strip, line.split('+'))
                elif "_" in line and (line.count("_") >= 3):
                    sentlemmata = map(str.strip, line.split('_'))
                elif line.count(':') == line.count('\n') != 0:
                    # token : lemma\n
                    sentlemmata = [x.split(':')[1].strip() for x in
                                   line.split('\n')]
                elif line.strip().startswith("[") or \
                        line.strip().startswith("("):
                    if not ('"' in line or '\'' in line):
                        # list notation without quotation marks "/'
                        sentlemmata = [lemma.strip("()[]\n") for lemma in
                                       line.split(", ")]
                    else:  # list notation
                        sentlemmata = ast.literal_eval(line)
                else:  # white space or comma tokenization
                    if line.count(",") >= (len(line.split())-1):
                        sentlemmata = line.split(', ')
                    else:
                        sentlemmata = line.split()
                sentlemmata = list(map(str.strip, sentlemmata))
                sentlemmata = list(map(lambda s: s.strip('"\''), sentlemmata))
                # separate punctuation
                punct = set('?!,.')
                for i, s in enumerate(sentlemmata):
                    if len(s) >= 2:  # prevent index error
                        if any(s.endswith(p) and s[-2].isalnum()
                               for p in punct):
                            if len(re.split('([^a-zA-ZäöüßÄÖÜ0-9])', s)) == 3:
                                word, p_mark, empty = \
                                    re.split('([^a-zA-ZäöüßÄÖÜ0-9])', s)
                                sentlemmata[i] = word
                                sentlemmata.insert(i+1, p_mark)
                if sentlemmata:
                    lemmata.append(sentlemmata)
        except Exception as e:
            print(line, e)
    return lemmata


if __name__ == '__main__':
    # short demo, glance into lemma list
    path = '../../nbs/chatgpt_outputs/chatgpt-rub2019-opensubtitles.txt'
    print(clean_up(path)[:10])
