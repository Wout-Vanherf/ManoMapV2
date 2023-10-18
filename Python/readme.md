# INSTALLATION GUIDE
We hebben twee manieren om het project te installeren, voor mensen die helemaal geen besef hebben van code kan simpelweg de executable file downloaden, en deze kan direct gelanceerd worden met een simpele klik. Hiervoor zijn ook geen dependencies nodig, dus ook heeft de machine geen behoefte aan Python.
Het nadeel van dit is dat door een applicatie executable te maken het iets minder performant wordt. Dit heeft toch wel een invloed op “Manomap2.0”, aangezien programma relatief lange laadtijd al heeft als de gedetecteerde contracties getekend worden op de line plot. Het verlengen van dit proces is niet echt gewenst.

De andere optie houd wel wat kennis van Python in. Voor deze installatie moet vooraf al geïnstalleerd zijn: Git, Python.
Clone de repository met het volgende commando:

``
git clone https://github.com/Wout-Vanherf/ManoMapV2.git
``

**Om het project uit code te runnen zijn deze libraries nodig**:

``
pip install openpyxl
``

``
pip install scipy
``

``
pip install tkinter
``

``
pip install mpldatacursor
``

``
pip install RangeSlider
``

``
pip install matplotlib
``

Hiermee zijn alle dependencies gedownload, je kan het programma laten draaien door
``python .\Python\main.py ``

# MODULE DOCS
Het project bestaat uit de volgende modules:
## Detection.py
Een module die een determenistisch detecttie algorithme op de data runt.

Er worden hier 2 methoden van extern gebruikt:

**find_patterns_from_values_dict**:

De volgende inputs zijn vereist:
- valuedict: een dictionary waarbij de keys de tijdstippen zijn (op regelmatige intervallen) en de values lijsten van de numerieke meetwaarden. Elke lijst moet dezelfde dimensies hebben.
- first_sensor: de eerste sensor van de range die beschouwt moet worden
- last_sensor: de laatste sensor van de range die beschouwt moet worden 
- threshold: de minimumwaarde van een meting om gemarkeerd te worden

Keyword vars:
- amount_of_sensors (default 3): het aantal sensors er consecutief boven de threshold moet zitten om deze sensoren te markeren als contractie
- amount_overlapped (default 2): het aantal sensoren er gemeenschappelijk moeten zijn met vorige meting om deze te markeren als contractie

**find_contractions_from_patterns**

Deze functie roep je op om een bruikbare structuur te bekomen voor de andere modules.
De functie neemt 2 parameters:
- pattern_results: hier geef je de output van de find_patterns_from_values mee
- contraction_length: de minimale lengte van een contractie, als er minder metingen dan deze waarde aanwezig zijn, wordt de contraction gedropt.

De output van deze functie is een lijst met contractions, contractions worden weergegeven als dictionary en bevatten:
- length: hoeveel metingen lang de contractie zich heeft voorgedaan
- measure_number: op welke meting de contractie is gestart
- sequences: een twee-dimensionale lijst met de opeenvolgende sensoren die boven de threshold liggen binnen de contractie, de values zijn tuples met zowel het sensornummer als de amplitude
    

