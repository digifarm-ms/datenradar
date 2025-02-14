---
toc: false
title: Stromspeicher
theme: [wide]
---

# Stromspeicher in Münster

```js
import {DonutChart} from "./components/donutChart.js";
import {Swatches} from "./components/swatches.js";
// import {bigNumber} from "./components/bigNumber.js";

const rawInputData = FileAttachment("data/marktstammdatenregister-speicher.csv").csv({typed: true});
```

```js
// Define Radio Button Input "Auswertungstyp" 
const userAuswertungstypInput = Inputs.radio(
    new Map([
      ['Nutzbare Speicherkapaz. (kWh)', "NutzbareSpeicherkapazitaet",],
      ['Bruttoleistung (kW)', "Bruttoleistung"],
      ['Anzahl Anlagen', "Anzahl"]
    ]),
  {
    label: "Auswertungstyp:",
    value: "NutzbareSpeicherkapazitaet",
    unique: true
  }
);
const userAuswertungstyp = Generators.input(userAuswertungstypInput);
```

```js
// Define Radio Button Input "Natürliche Person" 
const userNatuerlichepersonInput = Inputs.radio(
    new Map([
      ["Nur natürliche Personen anzeigen", 'Ja'],
      ["Nur Unternehmen", 'Nein'],
      ["Beides anzeigen", 'egal']
    ]),
    {label: 'Einschränkung:', 
    value: 'egal'}
);
const userNatuerlicheperson = Generators.input(userNatuerlichepersonInput);
```


```js
// Extract Earliest and Latest Date from CSV File
const dateColumn = rawInputData.map(function(d) { return d.EinheitRegistrierungsdatum });
const beginDate = dateColumn.sort(d3.ascending)[0];
const endDate = dateColumn.sort(d3.descending)[0];


// Define Date Inputs
const nthDayInput = Inputs.date({label: "Startdatum:", value: beginDate});
const endDayInput = Inputs.date({label: "Enddatum:", value: endDate});
const appStartDay = Generators.input(nthDayInput);
const appEndDay = Generators.input(endDayInput);
```

```js
// Batterie Typ Mapping & helper function
const batterieMapping = {
  	727: 'Lithium-Batterie',
    728: 'Blei-Batterie',
    729: 'Redox-Flow-Batterie',
    730: 'Hochtemperaturbatt.',
    731: 'NiMh/NiCd-Batt.', //Nickel-Cadmium- / Nickel-Metallhydridbatterie
    732: 'Sonstige Batterie',
}
function getBatterieTech(x) {
  return batterieMapping[x] ? batterieMapping[x] : x;
}

function set(input, value) {
  input.value = value;
  input.dispatchEvent(new Event("input", {bubbles: true}));
}
```

```js
const yearbuttons = Inputs.button([
  ["2022", () => {set(nthDayInput, '2022-01-01');set(endDayInput,  '2022-12-31');}],
  ["2023", () => {set(nthDayInput, '2023-01-01');set(endDayInput,  '2023-12-31');}],
  ["2024", () => {set(nthDayInput, '2024-01-01');set(endDayInput,  '2024-12-31');}],
  ["2025", () => {set(nthDayInput, '2025-01-01');set(endDayInput,  '2025-12-31');}],
])
```


```js
// Filtere die Daten entsprechend der User Filter Auswahl
// und stelle sie reactive für alle anderen Widgets zur Verfügung
// (reactiveness geht wohl automatisch wenn diese Methode in einem eigenen JS Block ist..?)
const anlagenListeGefiltert = rawInputData.filter(function(i) {
    if (i.EinheitRegistrierungsdatum < appStartDay) { return false;   }
    if (i.EinheitRegistrierungsdatum > appEndDay) { return false;   }

    if (userNatuerlicheperson=="egal") {
      return true
    }  else if (i.AnlagenbetreiberPersonenArt==518 && userNatuerlicheperson == 'Ja') {
      return true;
    }  else if (i.AnlagenbetreiberPersonenArt!=518 && userNatuerlicheperson == 'Nein') {
      return true;
    }
    return false;
}
);
```

<style type="text/css">
@media (min-width: calc(640px + 6rem + 272px)) {
    .stickyTop {
        background-color: var(--theme-background);
        position: sticky;
        top: 50px;
        z-index: 2000;
        border-bottom: 5px solid var(--theme-background);
    }
    .stickyTop .card { 
        margin: 0;
        border: solid 1px var(--theme-foreground);
    }
}
</style>

<!-- Show user inputs -->
<div class="stickyTop">
<div class="card">
${userAuswertungstypInput}
${userNatuerlichepersonInput}
<div style="width:40%;float:right">${yearbuttons}</div> 
${nthDayInput}
${endDayInput}
</div>
</div>

## Stromspeicher nach ${userAuswertungstyp}

```js
// Hilfsfunktionen für die Pie Charts

function calcDonutSum(field) {
    // Berechnung der Prozentualen Anteile in den Pie Charts bzw Donuts
    // Anleitung für d3.rollups: https://observablehq.com/@d3/d3-group
    return d3.rollups(
        anlagenListeGefiltert, 
        v => (userAuswertungstyp == "Anzahl")? v.length : d3.sum(v, d => d[userAuswertungstyp]), 
        d => d[field]
    ).map(([name, value]) => ({name, value}));
}

function myDonut(data, name, cols) {
    if (name == 'Batterietechnologie') {
      data = data.map(function (d) { d.name = getBatterieTech(d.name); return d;});
    }
    const ress= data.map(function (d) {
        var einheit ="";
        if (userAuswertungstyp=="NutzbareSpeicherkapazitaet") einheit = " kWh";
        else if (userAuswertungstyp=="Bruttoleistung") einheit = " kW";
        return [d.name + ' ('+Math.floor(d.value)+einheit+')']});
    return html`
    ${resize(width => DonutChart(data, {centerText: name, width, colorDomain: cols, colorRange: cols}))}
    ${Swatches(d3.scaleOrdinal(ress, cols))}
    `;
}
```

<div class="card" style="height: 350px;overflow:hidden">
${userColorcodeInput}
${resize((width, height) => arrivalLineChart(width, height))}
</div>

```js
const userColorcodeInput = Inputs.select( new Map([
      ["Betriebsstatus", 'BetriebsStatusName'],
      ["AnlagenbetreiberPersonenArt", 'AnlagenbetreiberPersonenArt'],
      ["Stromspeichertechnologie", 'StromspeichertechnologieBezeichnung'],
      ["Spannungsebene", 'SpannungsebenenNamen'],
      ["Batterietechnologie", 'Batterietechnologie'],
      ["Plz", 'Plz']
    ]), {value: "Betriebsstatus", label: "Farbcodierung"});
const userColorcode = Generators.input(userColorcodeInput);
```

```js
// Line chart (installation dates)
function arrivalLineChart(width, height) {
  return Plot.plot({
    height: height - 100,
    marginBottom: 35,
    width,
    x: {label: "Reg.-Datum"},
    y: ((userAuswertungstyp == "Anzahl")
       ? {label: userAuswertungstyp, grid: true}
       : {label: userAuswertungstyp, grid: true, type: "log", base: 2, domain: [1e0, 1e4], ticks: 20}),
//    color: {domain: seasonDomain, range: seasonColors, label: "Season"},
   
    subtitle: ((userAuswertungstyp == "Anzahl")
       ? `Darstellung als Anzahl pro Tag (Balken) sowie gleitender Mittelwert (Linie)`
       : `Darstellung einzelner Anlagen (Punkte) sowie gleitender Mittelwert (Linie) `),
    marks: [
      () => htl.svg`<defs>
      <linearGradient id="gradient" gradientTransform="rotate(90)">
        <stop offset="60%" stop-color="#B5B5B5" stop-opacity="0.7" />
        <stop offset="100%" stop-color="#B5B5B5" stop-opacity="0.1" />
      </linearGradient>
      </defs>`,
      Plot.dotY(
        anlagenListeGefiltert,
          {y: userAuswertungstyp, 
            x: "EinheitRegistrierungsdatum",
            r: 2,
            stroke: {value: userColorcode},
            channels: {
                AnlagenbetreiberName: {
                    value: "AnlagenbetreiberName",
                    label: ""
                },
                Plz: "Plz",
                BetriebsStatusName:  {
                    value: "BetriebsStatusName",
                    label: "Betriebsstatus"
                },
                NutzbareSpeicherkapazitaet:  {
                    value: "NutzbareSpeicherkapazitaet",
                    label: "Speicherkapazität"
                },
            },
            tip: {
                format: {
                    EinheitRegistrierungsdatum: true,
                    x: "%d. %b %Y",
                    AnlagenbetreiberName: true,
                    BetriebsStatusName: true,
                    Plz: d => d.toString(), 
                    NutzbareSpeicherkapazitaet: d => d.toString() + " kWh", 
                }
            }
          }
      ),
      Plot.areaY(
        anlagenListeGefiltert,
        Plot.binX(
          {y: ((userAuswertungstyp == "Anzahl")? "count" : "sum"), thresholds: "day", filter: null},
          {
            x: "EinheitRegistrierungsdatum",
            y: userAuswertungstyp,
            curve: "step",
            fill: "url(#gradient)",
            tip: {
                format: {
                    EinheitRegistrierungsdatum: true,
                    x: "%d. %b %Y",
                }
            }

          }
        )
      ),
      Plot.lineY(
        anlagenListeGefiltert,
        Plot.windowY(
          {k: 60},
          Plot.binX(
            {y: ((userAuswertungstyp == "Anzahl")? "count" : "sum"), interval: "day", filter: null},
            {
              x: "EinheitRegistrierungsdatum",
              y: userAuswertungstyp,
              z: null,
            }
          )
        )
      ),
      Plot.ruleY([0]),
      Plot.axisX({ticks: 5}),
      Plot.axisY({ticks: 5})
    ]
  });
}
```

## Kategorien

<div class="grid grid-cols-4">
  <div class="card ">${myDonut(calcDonutSum('Plz'), "Plz", d3.schemePaired)}</div>
  <div class="card ">${myDonut(calcDonutSum('Batterietechnologie'), "Batterietechnologie", d3.schemeObservable10)}</div>
  <div class="card ">${myDonut(calcDonutSum('SpannungsebenenNamen'), "Spannungsebene", d3.schemeTableau10)}</div>
  <div class="card ">${myDonut(calcDonutSum('VollTeilEinspeisungBezeichnung'), "Einspeisung", d3.schemeCategory10)}</div>
  <div class="card ">${myDonut(calcDonutSum('BetriebsStatusName'), "Betriebsstatus", d3.schemeSet2)}</div>
  <div class="card ">${myDonut(calcDonutSum('NetzbetreiberNamen'), "Netzbetreiber", d3.schemeSet1)}</div>
  <div class="card ">${myDonut(calcDonutSum('StromspeichertechnologieBezeichnung'), "Stromspeichertechnologie", d3.schemeDark2)}</div>
  <div class="card ">${myDonut(calcDonutSum('Ort'), "Ort", d3.schemeSet3)}</div>

</div>




## Datentabelle

```js
// Visuelle Darstellung in der Tabellenspalte "Leistung"

function sparkbar(max) { 
   // logarithmic sparkbar
  return (x) => htl.html`<div style="
    background: var(--theme-green);
    color: black;
    font: 10px/1.6 var(--sans-serif);
    width: ${100 * Math.log(x+1)/Math.log(max+1)}%;
    float: right;
    padding-right: 3px;
    box-sizing: border-box;
    overflow: visible;
    display: flex;
    justify-content: end;">${Math.floor(x).toLocaleString("de-DE")}kWh`
}

// Create search input (for searchable table)
const tableSearch = Inputs.search(anlagenListeGefiltert);
const tableSearchValue = view(tableSearch);
```


<div class="card" style="padding: 0">
  <div style="padding: 1em">
    ${display(tableSearch)}
  </div>
  <div style="padding: 1em">
  ${display(Inputs.table(tableSearchValue, {
      sort: "NutzbareSpeicherkapazitaet",
      reverse: true,
      rows: 18,
      columns: [
        "Id",
        "AnlagenbetreiberPersonenArt",
        "AnlagenbetreiberName", 
        "Bruttoleistung",
        "NutzbareSpeicherkapazitaet",
        "BetriebsStatusName", 
        "EinheitRegistrierungsdatum", 
        "InbetriebnahmeDatum", 
        "NetzbetreiberNamen", 
        "Ort",
        "Plz", 
        "StromspeichertechnologieBezeichnung",
        "Batterietechnologie", 
        "SpannungsebenenNamen"
      ],
      header: 
        {
          BetriebsStatusName: "Status", 
          EinheitRegistrierungsdatum: "Registr.", 
          InbetriebnahmeDatum: "Inbetr.", 
          Batterietechnologie: "Batt.-Techn.", 
          Bruttoleistung: "Leistung",
          NutzbareSpeicherkapazitaet: "Sp.kapaz.",
          StromspeichertechnologieBezeichnung: "Art",
          AnlagenbetreiberPersonenArt: 'Nat.Pers.'
          },
        width: {arrivalDate: 100},
        format: {
//            Id: id => htl.html`<a href="https://www.marktstammdatenregister.de/MaStR/Einheit/Detail/EinheitDetailDrucken/${id}" target=_blank>${id}</a>`,
            Id: id => htl.html`<a href="https://www.marktstammdatenregister.de/MaStR/Einheit/Detail/IndexOeffentlich/${id}" target=_blank>${id}</a>`,
            Plz: d => d.toString(), 
            Bruttoleistung: (d) => (d + "kW"),
            EinheitRegistrierungsdatum: d3.utcFormat("%d.%m.%Y"),
            InbetriebnahmeDatum: d3.utcFormat("%d.%m.%Y"),
            NutzbareSpeicherkapazitaet: sparkbar(d3.max(tableSearchValue, d => d.NutzbareSpeicherkapazitaet)),
            AnlagenbetreiberPersonenArt: (d) => (d==517?'Nein':'Ja'),
            Batterietechnologie: getBatterieTech
        }
    }
  ))}
    </div>
</div>


<div class="small">Aktuell ausgewählter Datumsfilter:
${appStartDay.toLocaleDateString("de-DE")} - ${appEndDay.toLocaleDateString("de-DE")}  (${d3.timeDay.count(appStartDay, appEndDay)} Tage)</div>
<br><br><br><br>
<div class="card">
<table style="opacity:0.8">
<tr><th colspan="2">Information zu den dargestellten Daten</th></tr>
<tr><td>Datenstand:</td><td>${endDate.toLocaleDateString("de-DE")}</td></tr>
<tr><td>Datenquelle:</td><td><a href="https://www.marktstammdatenregister.de/MaStR/Einheit/Einheiten/OeffentlicheEinheitenuebersicht">Marktstammdatenregister</a></td></tr>
<tr><td>Lizenz:</td><td><a href="https://www.govdata.de/dl-de/by-2-0">Datenlizenz Deutschland – Namensnennung – Version 2.0</a></td></tr>
<tr><td>Datendownload:</td><td><a href="https://opendata.stadt-muenster.de/search?query=marktstammdaten">Marktstammdatenregister Datensätze auf dem Open Data Portal Münster</a></td></tr>
</table>

</div>