# Satellite Tracker — self-hosted

Στατική σελίδα (`index.html`) που διαβάζει τοπικά `data/tle_data.json` και
προπαγανδίζει τις τροχιές με SGP4 (`satellite.js`). Ένα GitHub Action
ανανεώνει το JSON αυτόματα από το space-track.org.

## Βήματα εγκατάστασης

1. **Δημιούργησε ένα νέο repo στο GitHub** και ανέβασε όλα τα αρχεία αυτού
   του φακέλου (διατήρησε τη δομή, ειδικά το `.github/workflows/`).

2. **Πρόσθεσε τα διαπιστευτήριά σου ως GitHub Secrets**
   (Settings → Secrets and variables → Actions → New repository secret):
   - `SPACETRACK_USER` — το email σου στο space-track.org
   - `SPACETRACK_PASS` — ο κωδικός σου

   Ποτέ μην τα βάζεις απευθείας σε αρχείο μέσα στο repo.

3. **Ενεργοποίησε το GitHub Pages**
   (Settings → Pages → Source: "Deploy from branch", branch: `main`, folder `/`).

4. **Τρέξε το Action μία φορά χειροκίνητα** (tab Actions → "Update TLE data" →
   Run workflow), ώστε να δημιουργηθεί το πρώτο `data/tle_data.json`.
   Μετά θα τρέχει μόνο του κάθε 6 ώρες (ρυθμίζεται στο
   `.github/workflows/update-tle.yml`, πεδίο `cron`).

5. Άνοιξε το `https://<username>.github.io/<repo>/` — η σελίδα θα δείχνει
   την ημερομηνία τελευταίας ενημέρωσης πάνω-πάνω.

## Τοπική δοκιμή χωρίς GitHub

```bash
pip install -r requirements.txt
export SPACETRACK_USER="..."
export SPACETRACK_PASS="..."
python3 spacetrack_fetch.py
python3 -m http.server 8000
# άνοιξε http://localhost:8000
```

## Προσθήκη/αφαίρεση δορυφόρων

Άλλαξε τη λίστα `DEFAULT_NORAD_IDS` στο `spacetrack_fetch.py`, ή πέρασε τα
NORAD IDs ως ορίσματα: `python3 spacetrack_fetch.py 25544 41747 67899`.

## Σημειώσεις

- Το space-track.org έχει όριο αιτημάτων (~300/ώρα) — το cron των 6 ωρών
  μένει πολύ μέσα στα όρια.
- Αν δεν υπάρχει ακόμα `data/tle_data.json` (πρώτη φόρτωση πριν τρέξει το
  Action), η σελίδα δείχνει ενδεικτικά δεδομένα με προειδοποίηση.
- Η διάδοση SGP4 είναι ακριβής για μέρες γύρω από το epoch κάθε TLE· γι'
  αυτό θέλουμε τακτική ανανέωση.
