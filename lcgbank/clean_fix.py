#!/usr/bin/env python3

from collections import defaultdict
import re
import typing as T
import xml.etree.ElementTree as ET

id_split = re.compile(r'wsj_(\d+).(\d+)')
idx = re.compile(r'\d+')
tree = ET.parse('included_in_ccgbank.lcgbank.lcg')
root = tree.getroot()
root2 = ET.parse('left_out_from_ccgbank.lcgbank.lcg').getroot()
for sentence in root2:
    root.append(sentence)

def numid(e: ET.Element):
    return [int(s) for s in id_split.match(e.attrib['id']).groups()]

sent_sort = sorted(root, key=numid)
sent_idx_maps = {}
sections = defaultdict(lambda: ET.SubElement(root, 'section'))
for sentence in sent_sort:
    sent_id = sentence.get('id')
    sentence.text += '\t'
    sentence.tail += '\t'
    for e in sentence:
        if e.text is not None:
            e.text += '\t'
        e.tail += '\t'
        for f in e:
            f.tail += '\t'

    sent_idxs = {}
    i = 0
    for word in [*sentence[1], sentence[0]]:
        if 'cat' in word.attrib:
            cat = word.get('cat')
            if sent_id == 'wsj_0290.16' and word.get('text') == 'on':
                assert cat == 'S_41\\NP_42\\(S_43\\NP_44)'
                cat = 'S_41\\NP_42/PP_74\\(S_43\\NP_44/PP_75)'
                del sentence[2][16]
                m = ET.SubElement(sentence[2], 'match')
                m.tail = sentence[2][0].tail
                m.set('first', '40')
                m.set('second', '75')
                m = ET.SubElement(sentence[2], 'match')
                m.tail = sentence[2][0].tail
                m.set('first', '74')
                m.set('second', '45')
            cat_idxs = [(m[0], str(i + j))
                        for j, m in enumerate(idx.finditer(cat))]
            i += len(cat_idxs)
            sent_idxs.update(cat_idxs)
            word.set('cat', idx.sub(lambda m: sent_idxs[m[0]], cat))
    matching = ET.SubElement(sentence, 'matching')
    matching.text = sentence[2].text
    matching.tail = sentence[2].tail
    last_tail = sentence[2][-1].tail
    reg_tail = sentence[2][0].tail
    for match in sorted(sentence[2],
                        key=lambda m: int(sent_idxs[m.get('first')])):
        f, s = match.get('first'), match.get('second')
        if f == s:
            continue
            sentence[2].remove(match)
        else:
            match.set('first', sent_idxs[match.get('first')])
            match.set('second', sent_idxs[match.get('second')])
            match.tail = reg_tail
            matching.append(match)
    match.tail = last_tail
    del sentence[2]

    sec_id = sent_id[4:6]
    sections[sec_id].set('id', sec_id)
    sections[sec_id].text = '\n\t'
    sections[sec_id].tail = '\n'
    root.remove(sentence)
    if sent_id in ['wsj_0162.10', 'wsj_0439.24', 'wsj_0465.39', 'wsj_0530.2',
                   'wsj_0560.13', 'wsj_0576.50', 'wsj_0693.11', 'wsj_0794.19',
                   'wsj_0984.4', 'wsj_0992.6', 'wsj_0996.38', 'wsj_1121.14',
                   'wsj_1146.132', 'wsj_1312.19', 'wsj_1312.27', 'wsj_1646.21',
                   'wsj_1676.22', 'wsj_1678.3', 'wsj_2162.11', 'wsj_2227.32',
                   'wsj_2376.63', 'wsj_2419.4']:
        sentence = ET.Comment(ET.tostring(sentence, 'unicode'))
        sentence.text = f'noparse\n\t{sentence.text}'
        sentence.tail = '\n\t'
    elif sent_id in ['wsj_0209.40', 'wsj_0224.4', 'wsj_0278.18', 'wsj_0439.45',
                     'wsj_0633.26', 'wsj_0795.9', 'wsj_0810.26', 'wsj_0922.12',
                     'wsj_1092.2', 'wsj_1316.3', 'wsj_1387.33', 'wsj_1618.37',
                     'wsj_1778.87', 'wsj_1915.49', 'wsj_1986.23',
                     'wsj_2110.12', 'wsj_2136.29', 'wsj_2398.11']:
        sentence = ET.Comment(ET.tostring(sentence, 'unicode'))
        sentence.text = f'badmatch\n\t{sentence.text}'
        sentence.tail = '\n\t'
    sections[sec_id].append(sentence)

for s in sections:
    sections[s][-1].tail = '\n'

tree.write('LCGbank.xml', encoding='UTF-8', xml_declaration=True)
