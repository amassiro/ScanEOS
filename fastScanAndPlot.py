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
import html
import datetime



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
  print (" WARNING: no Treesize from eos fileinfo for ", path, ", using du (slow) ...")
  result = subprocess.run(["du", "-sb", path], capture_output=True, text=True)
  return int(result.stdout.split()[0])



#
# nicer html page: pie chart + full legend (sorted by size, with TB), on more columns
#
nicePageTemplate = '''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Space on EOS</title>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<style>
  :root { --bg: #ffffff; --fg: #1f2328; --muted: #656d76; --line: #d0d7de; --hover: #f3f4f6; }
  @media (prefers-color-scheme: dark) {
    :root { --bg: #0d1117; --fg: #e6edf3; --muted: #8d96a0; --line: #30363d; --hover: #161b22; }
  }
  body { background: var(--bg); color: var(--fg); margin: 0; padding: 24px 16px;
         font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
  .wrap { max-width: 1400px; margin: 0 auto; }
  h1 { font-size: 22px; margin: 0 0 4px 0; }
  .sub { color: var(--muted); font-size: 14px; margin-bottom: 16px; word-break: break-all; }
  .sub b { color: var(--fg); }
  #piechart { width: 100%; height: 520px; }
  .legend { column-width: 280px; column-gap: 24px; border-top: 1px solid var(--line);
            padding-top: 12px; margin-top: 8px; font-size: 13px; }
  .item { display: flex; align-items: center; gap: 8px; padding: 3px 6px; border-radius: 4px;
          break-inside: avoid; cursor: default; }
  .item:hover { background: var(--hover); }
  .sw { width: 12px; height: 12px; border-radius: 2px; flex: none; }
  .rank { color: var(--muted); width: 2.2em; text-align: right; flex: none; font-variant-numeric: tabular-nums; }
  .name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .tb { font-variant-numeric: tabular-nums; flex: none; }
  .pc { color: var(--muted); width: 3.8em; text-align: right; flex: none; font-variant-numeric: tabular-nums; }
</style>
<script type="text/javascript">
  // [folder, TB], already sorted by size
  var rows = __ROWS__;
  var total = rows.reduce(function (s, r) { return s + r[1]; }, 0);

  // well separated colours, as many as needed
  // (google charts wants hex colours, hsl -> hex)
  function color(i) {
    var h = (i * 137.508) % 360, s = 0.65, l = (i % 2 ? 0.42 : 0.56);
    var f = function (n) {
      var k = (n + h / 30) % 12;
      var c = l - s * Math.min(l, 1 - l) * Math.max(-1, Math.min(k - 3, 9 - k, 1));
      return Math.round(255 * c).toString(16).padStart(2, '0');
    };
    return '#' + f(0) + f(8) + f(4);
  }
  function fmtTB(x) { return x >= 0.01 ? x.toFixed(2) + " TB" : (x > 0 ? "< 0.01 TB" : "0 TB"); }

  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(draw);

  var chart;
  function draw() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'folder');
    data.addColumn('number', 'TB');
    rows.forEach(function (r) { data.addRow([r[0], {v: r[1], f: fmtTB(r[1])}]); });

    var fg = getComputedStyle(document.body).color;
    var options = {
      legend: 'none',
      colors: rows.map(function (r, i) { return color(i); }),
      sliceVisibilityThreshold: 0,
      pieSliceText: 'percentage',
      pieSliceTextStyle: { fontSize: 11 },
      backgroundColor: 'transparent',
      chartArea: { width: '94%', height: '94%' },
      titleTextStyle: { color: fg },
      pieSliceBorderColor: getComputedStyle(document.body).backgroundColor
    };
    chart = new google.visualization.PieChart(document.getElementById('piechart'));
    chart.draw(data, options);

    var legend = document.getElementById('legend');
    rows.forEach(function (r, i) {
      var d = document.createElement('div');
      d.className = 'item';
      d.title = r[0];
      d.innerHTML = '<span class="rank">' + (i + 1) + '</span><span class="sw" style="background:' + color(i) + '"></span>' +
                    '<span class="name"></span><span class="tb">' + fmtTB(r[1]) + '</span>' +
                    '<span class="pc">' + (total > 0 ? (100 * r[1] / total).toFixed(1) : '0.0') + '%</span>';
      d.querySelector('.name').textContent = r[0];
      d.onmouseenter = function () { chart.setSelection([{row: i}]); };
      d.onmouseleave = function () { chart.setSelection([]); };
      legend.appendChild(d);
    });
  }
  window.addEventListener('resize', function () { if (chart) { document.getElementById('legend').innerHTML = ''; draw(); } });
</script>
</head>
<body>
<div class="wrap">
  <h1>Space on EOS</h1>
  <div class="sub"><b>__FOLDER__</b> &nbsp;&middot;&nbsp; total <b>__TOTAL__ TB</b> in __NUM__ entries &nbsp;&middot;&nbsp; __DATE__</div>
  <div id="piechart"></div>
  <div id="legend" class="legend"></div>
</div>
</body>
</html>
'''

def writeNicePage(information, inputFolder, fileName) :
  rows = sorted(information.items(), key=lambda x: x[1], reverse=True)
  page = nicePageTemplate
  page = page.replace("__ROWS__", json.dumps([ [name, value] for name, value in rows ]))
  page = page.replace("__FOLDER__", html.escape(inputFolder))
  page = page.replace("__TOTAL__", "{0:.2f}".format(sum(information.values())))
  page = page.replace("__NUM__", str(len(rows)))
  page = page.replace("__DATE__", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
  oFile = open(fileName, 'w')
  oFile.write(page)
  oFile.close()



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
    parser.add_option('--outputFileNice'   , dest='outputFileNice'   , help='nicer output file (default: outputFile with _nice)' , default='')
          
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




     

    
   
   


  
    oFile.close()

    #
    # nicer page, in parallel
    #
    if opt.outputFileNice == "" :
      opt.outputFileNice = opt.outputFile.replace(".html", "") + "_nice.html"
    writeNicePage(information, inputFolder, opt.outputFileNice)

    print (" outputFile       = ", opt.outputFile)
    print (" outputFileNice   = ", opt.outputFileNice)


