#!/usr/bin/env python

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




if __name__ == '__main__':
    print '''
--------------------------------------------------------------------------------------------------

    Scan resources on EOS
 
--------------------------------------------------------------------------------------------------
'''    

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputFolder'      , dest='inputFolder'      , help='input folder to scan'           , default='example.txt')
    parser.add_option('--outputFile'       , dest='outputFile'       , help='output file'                    , default='out_example.html')
          
    # read default parsing options as well
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()


    print " inputFolder      = ", opt.inputFolder
    print " outputFile       = ", opt.outputFile

    toExec = "ls " + opt.inputFolder
    os.system(toExec)

    cwd = os.getcwd()
    print "cwd  = ", cwd
    
    os.chdir(opt.inputFolder)

    toExec = "du -hs *  >  " + cwd + "/temp.txt" 
    os.system(toExec)

    os.chdir(cwd)




    iFile = open ("temp.txt")

    information = {}
     
    with iFile:
      for line in iFile:
        #print "line = ", line
        if len(line.split()) > 1 :
          ### 77T     archival
          space, name  = line.rstrip().split()
          space = space.replace("T","000000")
          space = space.replace("G","000")
          space = space.replace("K","")
          information[ name  ] = float(space) / 1000000.
            
    print " information = ", information

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




     

    
   
   


  
    print " outputFile       = ", opt.outputFile


