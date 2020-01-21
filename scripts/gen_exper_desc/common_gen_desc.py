import os
import sys
import argparse
import json

# These parameter names must match parameter names in config.sh
EXTR_TYPE_PARAM="extrType"
EXPER_SUBDIR_PARAM="experSubdir"
TEST_ONLY_PARAM="testOnly"

FEAT_EXPER_SUBDIR="feat_exper"

class BaseParser:
  def initAddArgs(self):
    pass

  def __init__(self, progName):
    self.parser = argparse.ArgumentParser(description=progName)
    self.parser.add_argument('--outdir', metavar='output directory',
                        help='output directory',
                        type=str, required=True)
    self.parser.add_argument('--rel_desc_path', metavar='relative descriptor path',
                        help='relative descriptor path',
                        type=str, required=True)
    self.parser.add_argument('--exper_subdir', metavar='exper. results subdir.',
                        help='top-level sub-directory to store experimental results',
                        type=str, default=FEAT_EXPER_SUBDIR)
    self.initAddArgs()

  def getArgs(self):
    """
    :return: argument objects, to be used
    """
    return self.args

  def parseArgs(self):
    """This is deliberately implemented with a delayed optimization,
    so that a user can add new parameter definitions before arguments
    are parsed.
    """
    self.args = self.parser.parse_args()
    print(self.args)


class ParserWithBM25Coeff(BaseParser):
  def initAddArgs(self):
    self.parser.add_argument('--b', metavar='BM25 b',
                        help='BM25 parameter b',
                        type=int, required=True)
    self.parser.add_argument('--k1', metavar='BM25 k1',
                             help='BM25 parameter b',
                             type=int, required=True)

  def __init__(self, progName):
    super().__init__(progName)


def genRerankDescriptors(args, extrJsonGenFunc, jsonDescName, jsonSubDir):
  """
  A generic function to write a bunch of experimental descrptors (for the re-ranking only scenario).

  :param args:              arguments previously produce by the class inherited from BaseParser
  :param extrJsonGenFunc:   generator of extractor JSON and its file ID.
  :param jsonDescName:      the name of the top-level descriptor file that reference individual extractor JSONs.
  :param jsonSubDir:        a sub-directory to store extractor JSONs.

  """
  descDataJSON = []

  outJsonSubDir = os.path.join(args.outdir, jsonSubDir)
  if not os.path.exists(outJsonSubDir):
    os.makedirs(outJsonSubDir)

  for fileId, jsonDesc, testOnly in extrJsonGenFunc():
    jsonFileName = fileId + '.json'

    descDataJSON.append({EXPER_SUBDIR_PARAM: os.path.join(args.exper_subdir, jsonSubDir, fileId),
                         EXTR_TYPE_PARAM: os.path.join(args.rel_desc_path, jsonSubDir, jsonFileName),
                         TEST_ONLY_PARAM: int(testOnly)})

    with open(os.path.join(outJsonSubDir, jsonFileName), 'w') as of:
      json.dump(jsonDesc, of, indent=2)

  with open(os.path.join(args.outdir, jsonDescName), 'w') as of:
    json.dump(descDataJSON, of, indent=2)



