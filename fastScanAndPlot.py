#!/usr/bin/env python3

import json
import sys
from sys import exit
import ROOT
import optparse
import os.path
import string
import logging
import traceback
from array import array
from collections import OrderedDict
import math

import os
import subprocess



#
# size of a file or folder, in bytes
# on EOS use the recursive "Treesize" kept by the MGM (fast),
# otherwise fallback to du (slow, it goes through all the files)
#
def getSize(path) :
  if not os.path.isdir(path) :
    return os.path.getsize(path)
  try :
    result = subprocess.run(["eos", "fileinfo", path + "/"], capture_output=True, text=True)
    if result.returncode == 0 and "Treesize:" in result.stdout :
      return int(result.stdout.split("Treesize:")[1].split()[0])
  except FileNotFoundError :
    # no eos command available
    pass
  result = subprocess.run(["du", "-sb", path], capture_output=True, text=True)
  return int(result.stdout.split()[0])



if __name__ == '__main__':
    print ('''
--------------------------------------------------------------------------------------------------

    Scan resources on EOS
 
--------------------------------------------------------------------------------------------------
''')

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputFolder'      , dest='inputFolder'      , help='input folder to scan'           , default='example.txt')
    parser.add_option('--outputFile'       , dest='outputFile'       , help='output file'                    , default='out_example.html')
          
    # read default parsing options as well
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()


    print (" inputFolder      = ", opt.inputFolder)
    print (" outputFile       = ", opt.outputFile)

    #
    # size of each sub-folder (in bytes), see getSize
    #
    inputFolder = opt.inputFolder.rstrip("/")

    information = {}

    for name in sorted(os.listdir(inputFolder)) :
      if name.startswith(".") :
        continue
      size = getSize(inputFolder + "/" + name)
      print (" >> ", name, " : ", size, " bytes")
      information[ name ] = float(size) / 1000000000000.

    # ---- old (slow) way, with du on all the tree ----
    #cwd = os.getcwd()
    #os.chdir(opt.inputFolder)
    #toExec = "LC_ALL=C du -hs *  >  " + cwd + "/temp" + opt.outputFile + ".txt"
    #os.system(toExec)
    #os.chdir(cwd)

    print (" information = ", information)

    oFile = open(opt.outputFile, 'w')
    #oFile.write('// to copy\n')

     
     
    oFile.write(' <html>                                                                                               \n')
    oFile.write('   <head>                                                                                             \n')
    oFile.write('     <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>          \n')
    oFile.write('     <script type="text/javascript">                                                                  \n')
    oFile.write('       google.charts.load(\'current\', {\'packages\':[\'corechart\']});                               \n')
    oFile.write('       google.charts.setOnLoadCallback(drawChart);                                                    \n')
    oFile.write('       function drawChart() {                                                                         \n')
    oFile.write('                                                                                                      \n')
    oFile.write('               var data = google.visualization.arrayToDataTable([                                     \n')
    oFile.write('                  [\'folder\', \'TB\'],                                                               \n')
    oFile.write('                                                                                                      \n')
    
    
    for key, value in information.items() :
      oFile.write( ' [\'%s\' , ' % key)  
      oFile.write( ' {0:.2f}  ] , \n '.format(float(value))  )   
      #[  'archival     '  ,      77             ]  ,
      
    
    oFile.write('                                                                                                      \n')
    oFile.write('                                                                                                      \n')
    oFile.write('          ]);                                                                                         \n')
    oFile.write('                                                                                                      \n')
    oFile.write('           var options = {                                                                            \n')
    oFile.write('             title: \'Space on EOS\'                                                                  \n')
    oFile.write('           };                                                                                         \n')
    oFile.write('                                                                                                      \n')
    oFile.write('           var chart = new google.visualization.PieChart(document.getElementById(\'piechart\'));      \n')
    oFile.write('                                                                                                      \n')
    oFile.write('           chart.draw(data, options);                                                                 \n')
    oFile.write('         }                                                                                            \n')
    oFile.write('       </script>                                                                                      \n')
    oFile.write('     </head>                                                                                          \n')
    oFile.write('     <body>                                                                                           \n')
    oFile.write('       <div id="piechart" style="width: 900px; height: 500px;"></div>                                 \n')
    oFile.write('     </body>                                                                                          \n')
    oFile.write('   </html>                                                                                            \n')
    oFile.write('                                                                                                      \n')
    oFile.write('                                                                                                      \n')




     

    
   
   


  
    print (" outputFile       = ", opt.outputFile)


