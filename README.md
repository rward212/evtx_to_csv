This little python script takes an .evtx file and spits out a .csv file that allows users to see the following fields:
1. DateTime
2. Severity
3. Message
4. Source

You can either run the Convert_evtx_to_csv.exe in a command prompt or download Chocolaty and Make and use the 
makefile to run the Convert_evtx_to_csv.py file.

Follow the following instructions to run:
1. Install Python
2. Install [Chocolaty](https://chocolatey.org/install)
3. Install [Make](https://gnuwin32.sourceforge.net/packages/make.htm)
4. Clone this repo
5. Open your terminal, navigate to the evtx_to_csv directory, and then run `make setup`
6. Run `python evtx_to_csv.py "<path to .evtx file>"`
5. The resulting file (Logs.txt) will be output in the same directory as the Convert_evtx_to_csv.py