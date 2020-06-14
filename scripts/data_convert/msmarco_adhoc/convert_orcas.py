#!/usr/bin/env python
# A file to generate queries & qrels from the ORCAS data collection
#
import sys
import os
import json
import argparse
import pytorch_pretrained_bert

sys.path.append('scripts')
from data_convert.text_proc import *
from data_convert.convert_common import *
from config import *
from common_eval import *

parser = argparse.ArgumentParser(description='Convert MSMARCO-adhoc queries.')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--out_dir', metavar='output directory', help='output directory',
                    type=str, required=True)
parser.add_argument('--min_query_token_qty', type=int, default=0,
                    metavar='min # of query tokens', help='ignore queries that have smaller # of tokens')
parser.add_argument('--' + BERT_TOK_OPT, action='store_true', help=BERT_TOK_OPT_HELP)

args = parser.parse_args()
print(args)
arg_vars = vars(args)

inpFile = FileWrapper(args.input)

outFileQueries = FileWrapper(os.path.join(args.out_dir, QUESTION_FILE_JSON), 'w')
outFileQrelsName = os.path.join(args.out_dir, QREL_FILE)

minQueryTokQty = args.min_query_token_qty

stopWords = readStopWords(STOPWORD_FILE, lowerCase=True)
print(stopWords)
nlp = SpacyTextParser(SPACY_MODEL, stopWords, keepOnlyAlphaNum=True, lowerCase=True)

if BERT_TOK_OPT in arg_vars:
    print('BERT-tokenizing input into the field: ' + TEXT_BERT_TOKENIZED_NAME)
    bertTokenizer = pytorch_pretrained_bert.BertTokenizer.from_pretrained(BERT_BASE_MODEL)

qrelList = []

# Input file is a TSV file
ln = 0

prevQid = ''

for line in inpFile:
    ln += 1
    line = line.strip()
    if not line:
        continue
    fields = line.split('\t')
    if len(fields) != 4:
        print('Misformated line %d ignoring:' % ln)
        print(line.replace('\t', '<field delimiter>'))
        continue

    qid, query, did, _  = fields

    query_lemmas, query_unlemm = nlp.procText(query)

    query_toks = query_lemmas.split()
    if len(query_toks) >= minQueryTokQty:

        qrelList.append(QrelEntry(queryId=qid, docId=did, relGrade=1))

        # Entries are sorted by the query ID
        if prevQid != qid:
            doc = {DOCID_FIELD: qid,
                   TEXT_FIELD_NAME: query_lemmas,
                   TEXT_UNLEMM_FIELD_NAME: query_unlemm,
                   TEXT_RAW_FIELD_NAME: query.lower()}
            addRetokenizedField(doc, TEXT_RAW_FIELD_NAME, TEXT_BERT_TOKENIZED_NAME, bertTokenizer)

            docStr = json.dumps(doc) + '\n'
            outFileQueries.write(docStr)

    prevQid = qid

    if ln % REPORT_QTY == 0:
        print('Processed %d input line' % ln)

print('Processed %d input lines' % ln)

writeQrels(qrelList, outFileQrelsName)

inpFile.close()
outFileQueries.close()

