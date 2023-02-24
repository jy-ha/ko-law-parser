import json
import re
import os

from collections import OrderedDict

def parse_law(law_file):
    # define pointers and keys
    pointer_contents = 0
    key_part = None  # n편
    key_chapter = None  # n장
    key_section = None  # n절
    key_sub_section = None  # n관
    key_sub_sub_section = None  # n항: 가끔 있다
    key_article = None  # n조

    # define regex
    regex_part = re.compile(r'^제[\d]+편')              # 편
    regex_chapter = re.compile(r'^제[\d]+장')           # 장
    regex_section = re.compile(r'^제[\d]+절')           # 절
    regex_sub_section = re.compile(r'^제[\d]+관')       # 관
    regex_sub_sub_section = re.compile(r'^제[\d]+항')   # 항: 가끔 있다
    regex_article = re.compile(r'^제[\d]+조')           # 조
    regex_paragraph = re.compile(r'^[\d]+항')           # 항
    regex_subparagraph = re.compile(r'^[\d의]+호')      # 호
    regex_detail_1 = re.compile(r'^(?:([가-히]))\.')    # 목
    regex_detail_2 = re.compile(r'^[\d]+\)')
    regex_detail_3 = re.compile(r'^[가-히]\)')

    # index 파싱
    law_dict = OrderedDict()
    with open(law_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            
            if pointer_contents == 0:  # nothing
                if regex_part.match(line): # start part
                    pointer_contents = 1
                elif regex_chapter.match(line): # start chapter
                    pointer_contents = 1
                else:
                    continue
            
            if pointer_contents == 1:  # index
                if regex_part.match(line): # start part
                    key_part = line
                    key_chapter = None
                    key_section = None
                    key_sub_section = None
                    key_sub_sub_section = None
                    law_dict[key_part] = OrderedDict()
                    continue
                elif regex_chapter.match(line): # start chapter
                    key_chapter = line
                    key_section = None
                    key_sub_section = None
                    key_sub_sub_section = None
                    if key_part:
                        law_dict[key_part][key_chapter] = OrderedDict()
                    else:
                        law_dict[key_chapter] = OrderedDict()
                    continue
                elif regex_section.match(line): # start section
                    key_section = line
                    key_sub_section = None
                    key_sub_sub_section = None
                    if key_part:
                        law_dict[key_part][key_chapter][key_section] = OrderedDict()
                    else:
                        law_dict[key_chapter][key_section] = OrderedDict()
                    continue
                elif regex_sub_section.match(line): # start sub section
                    key_sub_section = line
                    key_sub_sub_section = None
                    if key_part:
                        law_dict[key_part][key_chapter][key_section][key_sub_section] = OrderedDict()
                    else:
                        law_dict[key_chapter][key_section][key_sub_section] = OrderedDict()
                    continue
                elif regex_sub_sub_section.match(line): # start sub sub section
                    key_sub_sub_section = line
                    if key_part:
                        if key_section:
                            if key_sub_section:
                                law_dict[key_part][key_chapter][key_section][key_sub_section][key_sub_sub_section] = OrderedDict()
                            else:
                                law_dict[key_part][key_chapter][key_section][key_sub_sub_section] = OrderedDict()
                        else:
                            law_dict[key_part][key_chapter][key_sub_sub_section] = OrderedDict()
                    else:
                        if key_section:
                            if key_sub_section:
                                law_dict[key_chapter][key_section][key_sub_section][key_sub_sub_section] = OrderedDict()
                            else:
                                law_dict[key_chapter][key_section][key_sub_sub_section] = OrderedDict()
                        else:
                            law_dict[key_chapter][key_sub_sub_section] = OrderedDict()
                elif regex_article.match(line): # start article
                    key_article = line
                    if key_part:
                        if key_section:
                            if key_sub_section:
                                if key_sub_sub_section:
                                    law_dict[key_part][key_chapter][key_section][key_sub_section][key_sub_sub_section][key_article] = OrderedDict()
                                else:
                                    law_dict[key_part][key_chapter][key_section][key_sub_section][key_article] = OrderedDict()
                            else:
                                law_dict[key_part][key_chapter][key_section][key_article] = OrderedDict()
                        else:
                            law_dict[key_part][key_chapter][key_article] = OrderedDict()
                    else:
                        if key_section:
                            if key_sub_section:
                                if key_sub_sub_section:
                                    law_dict[key_chapter][key_section][key_sub_section][key_sub_sub_section][key_article] = OrderedDict()
                                else:
                                    law_dict[key_chapter][key_section][key_sub_section][key_article] = OrderedDict()
                            else:
                                law_dict[key_chapter][key_section][key_article] = OrderedDict()
                        else:
                            law_dict[key_chapter][key_article] = OrderedDict()
                    continue
                else:
                    break

    # contents 파싱
    def call_get_article(key, node):
        if node[key]:
            for k, v in node[key].items():
                call_get_article(k, node[key])
        else:
            node[key] = get_article(law_file, key)

    for k1, v1 in law_dict.items():
        call_get_article(k1, law_dict)
    return law_dict


def get_article(law_file, article):
    is_contents = False
    is_target = False
    target_articles = []
    filename = os.path.basename(law_file)[:os.path.basename(law_file).rfind('.')]
    regex_date = re.compile(r'\<.*\d{4}\. \d{1,2}\. \d{1,2}\..*\>')

    with open(law_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if not is_contents:
                if line == filename:
                    is_contents = True
                continue

            if not is_target:
                if line.startswith(article):
                    is_target = True
                else:
                    continue
            
            if (line == "") or (line[0] == "["):  # end of article
                break

            target_articles.append(line)

    target_article = '\n'.join(target_articles)
    target_article = regex_date.sub('', target_article)
    target_article = target_article[len(article):].strip()
    target_article = parse_article(target_article)
    return target_article


def parse_article(article):
    # 항 표현, 호 표현 치환
    paragraphs_circle = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳"]
    for i, circle_num in enumerate(paragraphs_circle):
        article = article.replace(circle_num, f"{i+1}항 ")
    for i in range(1, 100):
        article = article.replace(f"<{i}>", f"{i}항 ")
    regex_subparagraph = re.compile(r'\n(?:([\d의]+))\.')
    article = regex_subparagraph.sub(r'\n\1호 ', article)
    article = article.replace('  ', ' ')
    article = article.split('\n')

    key_paragraph = None  # n항
    key_subparagraph = None  # n호
    key_detail_1 = None  # 가.
    key_detail_2 = None  # n)
    key_detail_3 = None  # 가)

    regex_paragraph = re.compile(r'^[\d]+항')
    regex_subparagraph = re.compile(r'^[\d의]+호')
    regex_detail_1 = re.compile(r'^(?:([가-히]))\.')  # 목
    regex_detail_2 = re.compile(r'^[\d]+\)')
    regex_detail_3 = re.compile(r'^[가-히]\)')

    target_article = OrderedDict()
    for row in article:
        if row == '':
            continue
        if regex_paragraph.match(row):
            key_paragraph = row
            key_subparagraph = None
            key_detail_1 = None
            key_detail_2 = None
            key_detail_3 = None
            target_article[key_paragraph] = OrderedDict()
        elif regex_subparagraph.match(row):
            key_subparagraph = row
            key_detail_1 = None
            key_detail_2 = None
            key_detail_3 = None
            if key_paragraph:
                target_article[key_paragraph][key_subparagraph] = OrderedDict()
            else:
                # 항 없이 호 표현만 있는 경우 > 호를 항으로 치환
                key_subparagraph = key_subparagraph.replace('호', '항')
                target_article[key_subparagraph] = OrderedDict()
        elif regex_detail_1.match(row):
            key_detail_1 = regex_detail_1.sub(r'\1목.', row)
            key_detail_2 = None
            key_detail_3 = None
            if key_paragraph:
                target_article[key_paragraph][key_subparagraph][key_detail_1] = OrderedDict()
            else:
                target_article[key_subparagraph][key_detail_1] = OrderedDict()
        elif regex_detail_2.match(row):
            key_detail_2 = row
            key_detail_3 = None
            if key_paragraph:
                target_article[key_paragraph][key_subparagraph][key_detail_1][key_detail_2] = OrderedDict()
            else:
                target_article[key_subparagraph][key_detail_1][key_detail_2] = OrderedDict()
        elif regex_detail_3.match(row):
            key_detail_3 = row
            if key_paragraph:
                target_article[key_paragraph][key_subparagraph][key_detail_1][key_detail_2][key_detail_3] = OrderedDict()
            else:
                target_article[key_subparagraph][key_detail_1][key_detail_2][key_detail_3] = OrderedDict()

        else:
            if key_paragraph:
                if key_subparagraph:
                    if key_detail_1:
                        if key_detail_2:
                            if key_detail_3:
                                target_article[key_paragraph][key_subparagraph][key_detail_1][key_detail_2][key_detail_3][row] = OrderedDict()
                            else:
                                target_article[key_paragraph][key_subparagraph][key_detail_1][key_detail_2][row] = OrderedDict()
                        else:
                            target_article[key_paragraph][key_subparagraph][key_detail_1][row] = OrderedDict()
                    else:
                        target_article[key_paragraph][key_subparagraph][row] = OrderedDict()
                else:
                    target_article[key_paragraph][row] = OrderedDict()
            else:
                target_article[row] = OrderedDict()
    return target_article


def delete_deleted_laws(law_dict: dict):
    regex_delete = re.compile(r'.*삭제.*')
    regex_delete_section = re.compile(r'^제[\d]+조(의\d)*$')
    kill_list = []
    for k, v in law_dict.items():
        if regex_delete.match(k):
            kill_list.append(k)
        elif isinstance(v, dict):
            delete_deleted_laws(v)
    for kill in kill_list:
        del(law_dict[kill])
    
    kill_list = []
    for k, v in law_dict.items():
        if regex_delete_section.match(k):
            kill_list.append(k)
    for kill in kill_list:
        del(law_dict[kill])
    return law_dict


def save_json(law_dict, law_file):
    with open(law_file, 'w', encoding='utf-8') as f:
        json.dump(law_dict, f, ensure_ascii=False, indent=4)
