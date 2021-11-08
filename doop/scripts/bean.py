#!/usr/bin/python
import os, sys

BEAN_CP = 'bean.jar'

def splitArgs(args):
 analysis = args[0]
 i = 1
 while i < len(args):
  if args[i] == analysis:
   break
  i += 1
 opts = args[1:i]
 jars = args[i+1:]
 argMap = { 'analysis':analysis, 'opts':opts, 'jars':jars }
 return argMap
 
# use the name of first jar as program name
def getProgramName(argMap):
 basename = os.path.basename(argMap['jars'][0])
 return os.path.splitext(basename)[0]
 
def runCIanalysis(argMap):
 print
 print 'Running pre-analysis (context-insensitive analysis) ...'
 cmd = './run %s context-insensitive %s' % (' '.join(argMap['opts']), ' '.join(argMap['jars']))
 os.system(cmd)

def getReflectionString(dbDir, programName):
 def removeSpace(filepath):
  f = open(filepath)
  lines = f.readlines()
  f.close()
  f = open(filepath, 'w')
  for line in lines:
   f.write(line.strip() + '\n')
  f.close()
 
 filepath = os.path.join('tmp', programName + '.refstr')
 cmd = 'bloxbatch -db %s -query ReflectionStringConstant > %s' % (dbDir, filepath)
 os.system(cmd)
 removeSpace(filepath)
 return filepath
 
def runBean(dbDir, programName):
 print
 print 'Running BEAN ...'
 contextfile = os.path.join('tmp', programName + '-BeanContext.facts')
 cmd = 'java -cp %s bean.main.DoopMain %s %s' % (BEAN_CP, dbDir, contextfile)
 os.system(cmd)
 return contextfile
 
def readLines(filepath):
 f = open(filepath)
 lines = f.readlines()
 f.close()
 return lines
 
def merge(ctxfile, strFile):
 strconsts = set([line.strip() for line in open(strFile)])
 beanhctx = [line.strip() for line in readLines(ctxfile)]
 out = open(ctxfile, 'w')
 for line in beanhctx:
  [heap1, heap2, heap, hctx] = line.split('\t')
  if heap1 in strconsts: heap1 = '<<string-constant>>'
  if hctx in strconsts: hctx = '<<string-constant>>'
  out.write('\t'.join([heap1,heap2,heap,hctx]) + '\n')
 out.close()

def run(args):
 argMap = splitArgs(args)
 programName = getProgramName(argMap)
 runCIanalysis(argMap)
 dbDir = 'last-analysis'
 strfile = getReflectionString(dbDir, programName)
 contextfile = runBean(dbDir, programName)
 merge(contextfile, strfile)
 print 'Ready for running BEAN-directed analysis\n'
 
if __name__ == '__main__':
 args = sys.argv[1:]
 run(args)
 