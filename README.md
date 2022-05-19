### Disclaimer:
- I build this script for my personal use, in order to do ONE single appointment for NIE, because the manual process it is difficult, repetitive and takes a long time (because of the Spanish authorities, *&%!@# )
- There is no intent to develop this script further 
- It supports only NIE appointment request in Barcelona province 
- This script was inspired by [cita-bot](https://github.com/cita-bot/cita-bot) - but this one wasn't working anymore

Requirements: chrome web browser, python 3.x

### Installation 

1. git clone this repo
2. (optional step) create a virtual environment:
```
python -m venv .venv
source .venv/bin/activate
```
3. `pip install -r requirements.txt` 
4. install espeak, say OR wsay, 
eg, on linux: `sudo apt-get install espeak`

5. Open cita_information.py and replace the `FILL_PASSPORT_NUMBER` and `FILL_THE_NAME` with the passport number, respectively with the full name (in caps lock) - exactly how it is in the passport - for the person for which you need to do the appointment.

Example:
```
PASSPORT_NUMBER = "672343451"
PERSON_NAME = "JOSEPH BIDEN"
```

5. run the script as `python cita.py`

Good luck!
