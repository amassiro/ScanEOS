# ScanEOS

where:

    /afs/cern.ch/user/a/amassiro/work/Utils/ScanEOS

how:


    python3 scanAndPlot.py --inputFolder /eos/cms/store/group/   --outputFile mytest_full.html


    python3 scanAndPlot.py --inputFolder /tmp/amassiro/eos/cms/store/group/phys_higgs/
    python3 scanAndPlot.py --inputFolder /tmp/amassiro/eos/cms/store/group/phys_higgs/    --outputFile mytest.html
    python3 scanAndPlot.py --inputFolder /tmp/amassiro/eos/cms/store/group/phys_higgs/cmshww/    --outputFile mytest_cmshww.html
    python3 scanAndPlot.py --inputFolder    /eos/cms/store/group/phys_higgs/cmshww/   --outputFile mytest_cmshww.html
    python3 scanAndPlot.py --inputFolder    /eos/cms/store/group/phys_higgs/cmshww/amassiro/   --outputFile mytest_cmshww_amassiro.html    
    
    
    /store/group/dpg_ecal/comm_ecal
    
    python3 scanAndPlot.py --inputFolder   /tmp/amassiro/eos/cms/store/group/dpg_ecal/                 --outputFile mytest_ecal.html
    python3 scanAndPlot.py --inputFolder   /tmp/amassiro/eos/cms/store/group/dpg_ecal/comm_ecal/       --outputFile mytest_common_ecal.html
    python3 scanAndPlot.py --inputFolder   /tmp/amassiro/eos/cms/store/group/dpg_ecal/alca_ecalcalib   --outputFile mytest_alca_ecallib.html


    python3 scanAndPlot.py --inputFolder   /eos/cms/store/group/dpg_ecal/                 --outputFile mytest_ecal.html
    python3 scanAndPlot.py --inputFolder   /eos/cms/store/group/dpg_ecal/comm_ecal/       --outputFile mytest_common_ecal.html
    python3 scanAndPlot.py --inputFolder   /eos/cms/store/group/dpg_ecal/alca_ecalcalib   --outputFile mytest_alca_ecallib.html

    
    
    

NB: python2 version (old, not maintained):

    python scanAndPlotPy2.py --inputFolder /eos/cms/store/group/   --outputFile mytest_full.html

