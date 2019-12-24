#!/usr/bin/env python

import sys
import json
sys.path.append('scripts')

from data_convert.convert_common_qa import *
from data_convert.convert_common import *

def readingFunctionNQ(input):
  finp = FileWrapper(input)

  seenIds = set()

  for line in finp:
    root = json.loads(line)
    doc = root['document_html'].encode(DEFAULT_ENCODING)
    questionText = root["question_text"]
    answerList = []
    qid = root['example_id']
    if qid in seenIds:
      raise Exception('Data inconsistency, repeating example/question ID' + qid)

    seenIds.add(qid)
    for oneAnnot in root['annotations']:
      for shortAnsw in oneAnnot['short_answers']:
        answerList.append(doc[shortAnsw['start_byte']:shortAnsw['end_byte']].decode(DEFAULT_ENCODING))

    if answerList:
      yield qid, questionText, answerList


convertAndSaveQueries(readingFunctionNQ)