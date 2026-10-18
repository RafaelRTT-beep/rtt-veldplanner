# RTT Veldplanner

Het speelveld van Running the Target (Smeetsweg 8, Zoeterwoude) tekenen, tellen en delen met de bouwers.

- **Planner:** https://rafaelrtt-beep.github.io/rtt-veldplanner/
- **Bouwerweergave (alleen kijken, zonder account):** https://rafaelrtt-beep.github.io/rtt-veldplanner/?bouwer
- **Eén veld voor de bouwers:** `…/?bouwer&veld=<veld-id>`

## Inloggen

Alleen beheerders kunnen tekenen en opslaan. Klik rechtsboven op **Inloggen** en vul je e-mailadres in.
Je krijgt een mail met een inloglink en een code van 6 cijfers: tik op de link, of typ de code in de planner.
Daarna blijf je op dat apparaat ingelogd. Bouwers hoeven niet in te loggen.

Beheerders staan in Supabase (project RTT APP), tabel `public.rtt_veld_beheerder` (e-mailadres in kleine letters).

## Opslag (Supabase-project RTT APP)

| Tabel | Inhoud | Lezen | Schrijven |
|---|---|---|---|
| `rtt_veld` | velden (`design` = de tekening als JSON) | iedereen | beheerders |
| `rtt_veld_instellingen` | raster, paneelhoogte, voorraad, veld voor de bouwers | iedereen | beheerders |
| `rtt_veld_beheerder` | wie mag schrijven | alleen je eigen regel | niemand via de app |
| `rtt_bouwtekening` | de online gezette bouwtekening (PNG) | via de edge function `bouwtekening` | beheerders |

De QR-code op de print wijst naar `https://wrkoeoharqyjjjnlihgu.supabase.co/functions/v1/bouwtekening?id=<veld-id>`.

De sleutel in de code is de openbare *publishable key*. Wat iemand mag, staat in de RLS-regels van de tabellen.

## Bouwen

`src/app.html` is de bron. `python3 build.py` maakt `index.html` en bouwt jsPDF en qrcode-generator in
(uit `vendor/`, gecontroleerd tegen de hashes van cdnjs), zodat PDF en QR ook zonder internet werken.
`python3 build.py --icloud` werkt ook de offline-kopie in iCloud bij
("RtT files/05 Locaties & Plattegronden/RTT Veldplanner/RTT Veldplanner (offline).html").

`sw.js` zorgt dat de planner ook zonder internet opent als je hem op het beginscherm van de iPad of telefoon zet.
