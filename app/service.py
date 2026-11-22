"""Affärslogik för Servicekoll: när behöver en brandsläckare nästa service?

Serviceintervallen är EXEMPELVÄRDEN för kursprojektet, inte branschregler.
"""

import calendar
from datetime import date

# Exempelvärden: antal månader mellan servicetillfällen per släckartyp
SERVICE_INTERVALS_MONTHS = {
    "pulver": 12,
    "skum": 12,
    "vatten": 12,
    "kolsyra": 24,
}

# Så här många dagar innan förfallodatum räknas släckaren som "snart"
DUE_SOON_DAYS = 10


def add_months(start: date, months: int) -> date:
    """Lägg till hela månader. 31 jan + 1 mån blir sista feb (28 eller 29)."""
    month_index = start.month - 1 + months
    year = start.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(start.day, last_day))


def service_status(extinguisher_type: str, last_service: date, today: date) -> dict:
    """Räkna ut nästa servicedatum och status (ok, snart eller forsenad)."""
    extinguisher_type = extinguisher_type.strip().lower()

    if extinguisher_type not in SERVICE_INTERVALS_MONTHS:
        raise ValueError(f"Okänd släckartyp: {extinguisher_type}")
    if last_service > today:
        raise ValueError("Senaste service kan inte ligga i framtiden")

    next_service = add_months(last_service, SERVICE_INTERVALS_MONTHS[extinguisher_type])
    days_left = (next_service - today).days

    if days_left < 0:
        status = "forsenad"
    elif days_left <= DUE_SOON_DAYS:
        status = "snart"
    else:
        status = "ok"

    return {
        "type": extinguisher_type,
        "last_service": last_service.isoformat(),
        "next_service": next_service.isoformat(),
        "days_left": days_left,
        "status": status,
    }