---INSTALATION GUIDE----
We hebben twee manieren om het project te installeren, voor mensen die helemaal geen besef hebben van code kan simpelweg de executable file downloaden, en deze kan direct gelanceerd worden met een simpele klik. Hiervoor zijn ook geen dependencies nodig, dus ook heeft de machine geen behoefte aan Python.
Het nadeel van dit is dat door een applicatie executable te maken het iets minder performant wordt. Dit heeft toch wel een invloed op “Manomap2.0”, aangezien programma relatief lange laadtijd al heeft als de gedetecteerde contracties getekend worden op de line plot. Het verlengen van dit proces is niet echt gewenst.

De andere optie houd wel wat kennis van Python in. Voor deze installatie moet vooraf al geïnstalleerd zijn: Git, Python.
clone de repository met dit commando
git clone https://github.com/Wout-Vanherf/ManoMapV2.git

hiervoor zijn deze libraries nodig:
pip install openpyxl
pip install scipy
pip install tkinter
pip install mpldatacursor
pip install RangeSlider
pip install matplotlib

hiermee zijn alle dependencies gedownload, je kan het programma laten draaien door
python .\Python\main.py 