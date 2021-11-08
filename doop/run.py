#!/usr/bin/env python
import os
import shutil
import sys
from datetime import datetime, timedelta

ARTIFACT_ROOT = sys.path[0] # sys.path[0] is the directory containing this script
DOOP_HOME = os.path.join(ARTIFACT_ROOT, 'doop')
DOOP_CACHE = os.path.join(DOOP_HOME, 'cache')



ANALYSES=['1callH+SL','1callH+S','1objH+T','2objH','1callH+T', '1callH+SL_', '1callH+S_', 'S1objH+T','DecisionTree','1callH+T_new']

ANALYSIS_MAP={
'1callH+SL' : '1-tunneled-call-site-sensitive+heap',
'1objH+T' : '1-tunneled-object-sensitive+heap',
'2objH' : '2-object-sensitive+heap',
'1callH+T' : '1-tunneled-call-site-sensitive+heap+old', 
'1callH+SL_' : '1-tunneled-call-site-sensitive+heap+Sobj', 
'S1objH+T' : 'selective-1-tunneled-object-sensitive+heap',
'1callH+T_new' : '1-tunneled-call-site-sensitive+heap+T_new',
'DecisionTree' : 'simulated-1-tunneled-call-site-sensitive+heap',
}

USE_SIMULATION=['1callH+S', '1callH+S_']

PROGRAM=[
    'luindex', 'lusearch', 'antlr', 'pmd', 'chart', 'eclipse', 'jython', 'fop', 'checkstyle', 'jpc', 'bloat', 'xalan'
]

DACAPO=[
    'luindex', 'lusearch', 'antlr', 'pmd', 'chart', 'eclipse', 'jython','fop','bloat','xalan'
]
ALLOW_PHANTOM=['jpc', 'checkstyle']

UNSCALABLE={
    '2objH':['jython'],
    '1objH+T':['jython'],
    '1callH+S':['jython'],
}

CP={
    'jpc':'jars/JPC/JPCApplication.jar',
    'checkstyle':'jars/checkstyle/checkstyle-5.7-all.jar',
}


def getCP(app):
    if CP.has_key(app):
        return CP[app]
    elif app in DACAPO:
        return 'jars/dacapo/%s.jar' % app
    else:
        raise Exception('Unknown application: %s' % app)


def runPTA(pta,app):
  if not pta in ANALYSES:
    raise Exception('Unknown analysis: {}'.format(pta))

    
  # Use Simulation
  if pta in USE_SIMULATION:
    cmd = "./run -jre1.6 -simulation "
    if app in ALLOW_PHANTOM:
      cmd = cmd + "-phantom "
    
    if pta == '1callH+S':
      cmd = cmd + ANALYSIS_MAP['1objH+T'] + ' ' + getCP(app)
      os.system(cmd)
      cmd = 'bloxbatch -db last-analysis -query TunnelingInvo | sort > tmp_TunnelingAbstraction.facts'

    elif pta == '1callH+S_': # 1callHS'
      cmd = cmd + ANALYSIS_MAP['S1objH+T'] + ' ' + getCP(app)
      os.system(cmd)
      cmd = 'bloxbatch -db last-analysis -query CandidateInvocation | sort > tmp_TunnelingAbstraction.facts'
    else:
      raise Exception('Unknown analysis: {}'.format(pta))
    
    
    os.system(cmd)
    cmd = 'python process.py > TunnelingAbstraction.facts'
    os.system(cmd)
    cmd = 'rm tmp_TunnelingAbstraction.facts'
    os.system(cmd)

    cmd = './run -jre1.6 '
    if app in ALLOW_PHANTOM:
      cmd = cmd + "-phantom "
    cmd = cmd + 'simulated-1-tunneled-call-site-sensitive+heap' + ' ' + getCP(app)
    os.system(cmd)
  
  # Do not use Simulation
  else : 
    if pta == 'DecisionTree':
      cmd = 'cp decision_tree.facts TunnelingAbstraction.facts'
      os.system(cmd)
    cmd = "./run -jre1.6 "
    if app in ALLOW_PHANTOM:
      cmd = cmd + "-phantom "
    cmd = cmd + ANALYSIS_MAP[pta] + ' ' + getCP(app)
    os.system(cmd)
  
  cmd = 'rm -r cache/*'
  os.system(cmd)


def run(args):
  pta = args[0]
  app = args[1]
  if UNSCALABLE.has_key(pta) and app in UNSCALABLE[pta]:
    raise Exception('Unscalble : %s' % app)

  if args[1] == '-all':
    for app in PROGRAM:
      if not UNSCALABLE.has_key(pta) or app not in UNSCALABLE[pta]:
        runPTA(pta, app)
  else:
    runPTA(pta,args[1])

if __name__ == '__main__':
    run(sys.argv[1:])
