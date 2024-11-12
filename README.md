This little python script ingests a .evtx file and spits out a .csv file that allows users to see the following fields:
1. DateTime
2. Severity
3. Message
4. Source

Follow the following instructions to run:
1. Install Python
2. Clone this repo
3. Run `Make setup`
4. run `python evtx_to_csv.py "<path to .evtx file>"`
5. The resulting file (Logs.txt) will be output in the same directory as the convert_vtx_to_csv.py