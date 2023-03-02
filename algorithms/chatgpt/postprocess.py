# -*- coding: utf-8 -*-
import ast
import re


def clean_up(FILE):
    lemmata = []
    # count different formats
    formats = {'list-notation': 0,
               'list-notation-without-quot': 0,
               ':-notation': 0,
               'comma-separated': 0,
               'whitespace-separated': 0,
               '+-separated': 0,
               '|-separated': 0,
               '_-separated': 0,
               'other': [],
               'error': []}
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
                    formats['|-separated'] += 1
                elif "+" in line and (line.count("+") >= 3):
                    sentlemmata = map(str.strip, line.split('+'))
                    formats['+-separated'] += 1
                elif "_" in line and (line.count("_") >= 3):
                    sentlemmata = map(str.strip, line.split('_'))
                    formats['_-separated'] += 1
                elif line.count(':') == line.count('\n') != 0:
                    # token : lemma\n
                    sentlemmata = [x.split(':')[1].strip() for x in
                                   line.split('\n')]
                    formats[':-notation'] += 1
                elif line.strip().startswith("[") or \
                        line.strip().startswith("("):
                    if not ('"' in line or '\'' in line):
                        # list notation without quotation marks "/'
                        sentlemmata = [lemma.strip("()[]\n") for lemma in
                                       line.split(", ")]
                        formats['list-notation-without-quot'] += 1
                    else:  # list notation
                        sentlemmata = ast.literal_eval(line)
                        formats['list-notation'] += 1
                else:  # white space or comma tokenization
                    if line.count(",") >= (len(line.split())-1):
                        sentlemmata = line.split(', ')
                        formats['comma-separated'] += 1
                    else:
                        sentlemmata = line.split()
                        formats['whitespace-separated'] += 1
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
                else:  # other format?
                    formats['other'].append(line)
        except Exception:
            formats['error'].append(line)
    return lemmata, formats


if __name__ == '__main__':
    # short demo, glance into lemma list
    # path = '../../nbs/chatgpt_outputs/chatgpt-ud-gsd.txt'
    path = '../../nbs/chatgpt_outputs/chatgpt-nosta-d-bematac-norm.txt'
    lems, forms = clean_up(path)
    print(lems[:10], forms)
