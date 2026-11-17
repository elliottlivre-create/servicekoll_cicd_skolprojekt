# servicekoll_cicd_skolprojekt
Skolprojekt för sista kurs i devops utbildning. 



Servicekoll – CI/CD-skolprojekt

Ett litet API som räknar ut när en brandsläckare behöver nästa service. Appen är medvetet liten: fokus ligger på CI/CD-kedjan runt den.

Slutprojekt i kursen Continuous Integration och Continuous Delivery, DevOps Engineer, Nackademin.

Endpoints
Endpoint	Beskrivning
GET /health	Hälsokontroll
GET /version	Vilken version som körs
GET /types	Släckartyper och serviceintervall
GET /service-status?type=pulver&last_service=2026-03-01	Nästa service och status (ok, snart, forsenad)
Serviceintervallen är exempelvärden för projektet, inte branschregler.

Kör lokalt
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
Tester
python -m pytest -v
ruff check .