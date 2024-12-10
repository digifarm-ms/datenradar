---
theme: dashboard
title: Erneuerbare Energien
toc: false
---

# Windräder und Photovoltaikanlagen in Münster

<!-- Load and transform the data -->

```js
const facilities = FileAttachment("data/erneuerbare-energien-muenster.csv").csv({typed: true});
```


<!--
Columns of the CSV files
========================

facilities =
"Id";"AnlagenbetreiberId";"AnlagenbetreiberMaStRNummer";"AnlagenbetreiberName";"BetriebsStatusId";"BetriebsStatusName";"DatumLetzteAktualisierung";"EinheitMeldeDatum";"EinheitName";"InbetriebnahmeDatum";"MaStRNummer";"PersonenArtId";"Typ";"Ort";"Plz";"AnzahlSolarModule";"Bruttoleistung";"EnergietraegerName";"Flurstueck";"IsAnonymisiert";"IsPilotwindanlage";"LokationId";"Nettonennleistung"
9113162;5821904;"ABR948361155505";"(natürliche Person)";35;"In Betrieb";"2024-11-19";"2024-11-19";"Balkonkraftwerk";"2024-11-01";"SEE952076174508";518;1;"Münster";"48163";2;0.8;"Solare Strahlungsenergie";"";True;"";8342795;0.8

launches =
date,state,stateId,family
1957-10-04,Soviet Union,SU,R-7
 -->

```js
// Prepare colors for PLZ Gebiete
const color = Plot.scale({
  color: {
    type: "categorical",
    domain: d3.groupSort(facilities, (D) => -D.length, (d) => d.Plz),
    unknown: "var(--theme-foreground-muted)"
  }
});
```

```js
// Prepare colors for EnergietraegerName
const colorEnergietyp = Plot.scale({
  color: {
    type: "categorical",
    domain: d3.groupSort(facilities, (D) => -D.length, (d) => d.EnergietraegerName),
    unknown: "var(--theme-foreground-muted)"
  }
});
```

Hier betrachten wir den Ausbau von Sonnenenergie und Windenergie in Münster. Diese erneuerbaren Energiequellen gelten als wichtigste Säule einer nachhaltigen Energiepolitik. Als erneuerbare bzw. regenerative Energien werden Energiequellen bezeichnet, die für nachhaltige Energieversorgung praktisch unerschöpflich zur Verfügung stehen. Damit grenzen sie sich von fossilen Energiequellen ab, die endlich sind oder sich erst über den Zeitraum von Millionen Jahren regenerieren.

<!-- Cards with big numbers -->

<div class="grid grid-cols-4">
  <div class="card">
    <h2>Anzahl Anlagen Gesamt</h2>
    <span class="big">${facilities.length.toLocaleString("de-DE")}</span>
  </div>
  <div class="card">
    <h2>Windkraft <span class="muted">(Anzahl Anlagen)</span></h2>
    <span class="big">${facilities.filter((d) => d.EnergietraegerName === "Wind").length.toLocaleString("de-DE")}</span>
  </div>
  <div class="card">
    <h2>In Planung <span class="muted">(Anzahl Anlagen)</span></h2>
    <span class="big">${facilities.filter((d) => d.BetriebsStatusName === "In Planung").length.toLocaleString("de-DE")}</span>
  </div>
  <div class="card">
    <h2>Vorübergehend stillgelegt <span class="muted">(Anzahl Anlagen)</span></h2>
    <span class="big">${facilities.filter((d) => d.BetriebsStatusName === "Vorübergehend stillgelegt").length.toLocaleString("de-DE")}</span>
  </div>

</div>

<!-- Plot of Solaranlagen installation history -->

## Anlagen sortiert nach Installationsjahr


```js
function timelineOfInstallations(data, {width} = {}) {
  return Plot.plot({
    title: "Anzahl pro Jahr installierter Anlagen",
    width,
    height: 300,
    y: {grid: true, label: "Launches"},
    color: {...color, legend: true},
    marks: [
      Plot.rectY(data, Plot.binX({y: "count"}, {x: "InbetriebnahmeDatum", fill: "Plz", interval: "year", tip: true})),
      Plot.ruleY([0])
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => timelineOfInstallations(facilities, {width}))}
  </div>
</div>


## Anzahl Anlagen nach Postleitzahl
```js

let topfacilities = facilities.filter((d) => top_names.includes(d.AnlagenbetreiberMaStRNummer));

for (let index = 0; index < topfacilities.length; ++index) {
    if (topfacilities[index]["AnlagenbetreiberName"]) {
        topfacilities[index]["AnlagenbetreiberMaStRNummer"] = topfacilities[index]["AnlagenbetreiberName"];
    }
}
```


<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => plzChart(topfacilities, "Anzahl", "Plz", {width}))}
  </div>
</div>


```js
function plzChart(data, name1, name2, {width}) {

  //data = data.group({x: "count"}, {y: "AnlagenbetreiberName", fill: "Plz", tip: true, sort: {y: "-x"}}).filter((D) => D.Betreiber > 2)

  return Plot.plot({
    width,
    height: 400,
    marginTop: 0,
    marginLeft: 200,
    x: {grid: true, label: name1},
    y: {label: null},
    color: {...colorEnergietyp, legend: true},
    marks: [
      Plot.rectX(data,
            Plot.groupY({x: "count"}, {y: name2, fill: "EnergietraegerName", tip: true, sort: {y: "-x"}})
      ),
      Plot.ruleX([0])
    ]
  });
}
```

## Betreiber mit den meisten Anlagen in Münster

```js
// Generate a list of the top Betreibers

const only_business = facilities.filter((d) => d.AnlagenbetreiberName !== "(natürliche Person)");
const grouped = d3.group(only_business, d => d.AnlagenbetreiberMaStRNummer);
const sorted = d3.reverse(d3.sort(grouped, (a, b) => d3.ascending(a[1].length, b[1].length)))
const toplist = sorted.slice(0,30)
var top_names = toplist.map(function(d){return d[0]})
```

```js
function vehicleChart(data, name1, name2, {width}) {

  //data = data.group({x: "count"}, {y: "AnlagenbetreiberName", fill: "Plz", tip: true, sort: {y: "-x"}}).filter((D) => D.Betreiber > 2)

  return Plot.plot({
    width,
    height: 400,
    marginTop: 0,
    marginLeft: 200,
    x: {grid: true, label: name1},
    y: {label: null},
    color: {...color, legend: true},
    marks: [
      Plot.rectX(data,
            Plot.groupY({x: "count"}, {y: name2, fill: "Plz", tip: true, sort: {y: "-x"}})
      ),
      Plot.ruleX([0])
    ]
  });
}


```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => vehicleChart(topfacilities, "Betreiber", "AnlagenbetreiberMaStRNummer", {width}))}
  </div>
</div>

```js

//display(Inputs.table(topfacilities));

```

## Anlagen der Stadtverwaltung Münster & Tochtergesellschaften




```js
const muensterfacilities = d3.filter(facilities, (d) => ((d.AnlagenbetreiberName)));
// const filteredfacilities = muensterfacilities;
```

<div class="grid grid-cols-2">
  <div class="card">

```js
const betreiberListe = [...new Set(d3.map(muensterfacilities,function(d){return d.AnlagenbetreiberName;}))];
const preselection = view(
    Inputs.select(
        betreiberListe,
        {multiple: true, label: "Betreiber Auswahl", value: betreiberListe}
    )
);
```
  </div>
  <div class="card">


```js

const filteredfacilities = view(
    Inputs.search(
        d3.filter(
            muensterfacilities,
            (d) => (preselection.includes(d.AnlagenbetreiberName))
        ),
        {placeholder: "Anlagen durchsuchen", label: "Stichwort Suche", format: (d) => `${d} Ergebnisse` }
    )
);
```
  </div>

</div>


<div class="grid grid-cols-1">
  <div class="card" style="padding: 0;">

```js
function sparkbar(max) {
  return (x) => htl.html`<div style="
    background: var(--theme-green);
    color: black;
    font: 10px/1.6 var(--sans-serif);
    width: ${100 * x / max}%;
    float: right;
    padding-right: 3px;
    box-sizing: border-box;
    overflow: visible;
    display: flex;
    justify-content: end;">${x.toLocaleString("en-US")}`
}
function displayAnlagen(anlagen) {
    display(Inputs.table(anlagen, {
        columns: [
            "AnlagenbetreiberName",
            "Plz",
            "EnergietraegerName",
            "EinheitName",
            "InbetriebnahmeDatum",
            "AnzahlSolarModule",
            "Bruttoleistung",
            "BetriebsStatusName",
            "MaStRNummer"
        ],
        width: {
            "Plz": 50
        },
        sort: "AnzahlSolarModule",
        reverse: true,
        rows: 30,
        format: {
            "AnzahlSolarModule": sparkbar(Math.min(1000, d3.max(anlagen, d => d.AnzahlSolarModule)))
        }
    }));
}

// display(Inputs.table(filteredfacilities))

displayAnlagen(filteredfacilities);

//const stadtwerkefacilites = d3.filter(facilities, (d) => (d.AnlagenbetreiberName || "").includes("Stadtwerke"));
//displayAnlagen(stadtwerkefacilites);


```

  </div>
</div>

<style>

blockquote, ol, ul, p, h1, h2 {
    max-width: 1200px;
}

</style>
