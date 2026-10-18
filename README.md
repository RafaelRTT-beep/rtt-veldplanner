# RTT Veldplanner

Het speelveld van Running the Target (Smeetsweg 8, Zoeterwoude) tekenen, tellen en delen met de bouwers.

- **Planner:** https://rafaelrtt-beep.github.io/rtt-veldplanner/
- **Bouwerweergave (alleen kijken, zonder account):** https://rafaelrtt-beep.github.io/rtt-veldplanner/?bouwer
- **Eén veld voor de bouwers:** `…/?bouwer&veld=<veld-id>`

## Inloggen

Alleen beheerders kunnen tekenen en opslaan. Bouwers hoeven niet in te loggen.

- **Met wachtwoord (dagelijks):** klik rechtsboven op **Inloggen**; je sleutelhanger vult e-mail en wachtwoord in met Face ID of Touch ID.
- **Met mailcode (eerste keer of wachtwoord vergeten):** kies **Mail met code**. Je krijgt een mail met een code van 6 cijfers
  en een inloglink. Typ de code in de planner (op iPad en iPhone in de beginscherm-app altijd de code gebruiken).
- **Wachtwoord instellen:** ingelogd → klik op je naam rechtsboven → **Wachtwoord instellen of wijzigen**. Safari stelt een sterk
  wachtwoord voor en bewaart het in de sleutelhanger.

Daarna blijf je op dat apparaat ingelogd. Zet de planner als app op je beginscherm (Safari: deelknop → Zet op beginscherm)
of in je Dock (Mac: Archief → Voeg toe aan Dock).

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
