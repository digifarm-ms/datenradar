---
toc: false
title: Stromspeicher (vis.)
theme: [air, ocean-floor, wide]
---

# Stromspeicher in Münster

```js
import {DonutChart} from "./components/donutChart.js";
import {Swatches} from "./components/swatches.js";
import {bigNumber} from "./components/bigNumber.js";

const hotelData = FileAttachment("data/marktstammdatenregister-speicher.csv").csv({typed: true});
```

```js
// Radio button input to choose 
const pickMarketSegmentInput = Inputs.radio(
  ["NutzbareSpeicherkapazitaet", "Anzahl"],
  {
    label: "Auswertungstyp:",
    value: "NutzbareSpeicherkapazitaet",
    unique: true
  }
);
const pickMarketSegment = Generators.input(pickMarketSegmentInput);
```

${pickMarketSegmentInput}

## Stromspeicher nach ${pickMarketSegment}

```js

// Anleitung für d3.rollups: https://observablehq.com/@d3/d3-group
function calcDonutSum(field) {
    return d3.rollups(
        hotelData, 
        v => (pickMarketSegment == "Anzahl")? v.length : d3.sum(v, d => d['NutzbareSpeicherkapazitaet']), 
        d => d[field]
    ).map(([name, value]) => ({name, value}));
}

function myDonut(data, name, cols) {
    const ress= data.map((d) => ([d.name + ' ('+Math.floor(d.value)+')']));
    return html`
    ${resize(width => DonutChart(data, {centerText: name, width, colorDomain: cols, colorRange: cols}))}
    ${Swatches(d3.scaleOrdinal(ress, cols))}
    `;
}
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
```

<div class="grid grid-cols-4">
  <div class="card ">${myDonut(calcDonutSum('BetriebsStatusName'), "Betriebsstatus", d3.schemeSet2)}</div>
  <div class="card ">${myDonut(calcDonutSum('NetzbetreiberNamen'), "Netzbetreiber", d3.schemeSet1)}</div>
  <div class="card ">${myDonut(calcDonutSum('Batterietechnologie'), "Batterietechnologie", d3.schemeObservable10)}</div>
  <div class="card ">${myDonut(calcDonutSum('Ort'), "Ort", d3.schemeSet3)}</div>
  <div class="card ">${myDonut(calcDonutSum('Plz'), "Plz", d3.schemePaired)}</div>
  <div class="card ">${myDonut(calcDonutSum('StromspeichertechnologieBezeichnung'), "Stromspeichertechnologie", d3.schemeDark2)}</div>
  <div class="card ">${myDonut(calcDonutSum('SpannungsebenenNamen'), "Spannungsebene", d3.schemeTableau10)}</div>
  <div class="card ">${myDonut(calcDonutSum('VollTeilEinspeisungBezeichnung'), "Einspeisung", d3.schemeCategory10)}</div>
</div>
<!--div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => bigNumber(`Number of bookings, ${pickMarketSegment}`, datesExtent, `${d3.format(",")(hotelData.length)}`, `${d3.format(".1%")(bookingsByMarketSegment.length / bookingsAll.length)} of all bookings`, width))}
  </div>
  <div class="card">
    ${resize((width) => bigNumber(`Average daily rate`, datesExtent, `$${d3.mean(bookingsByMarketSegment.map((d) => d.ADR)).toFixed(2)}`, `${pickMarketSegment == "All" ? `` : d3.format("$.2f")(Math.abs(rateDiffFromAverage))} ${rateDiffFromAverage > 0 ? `greater than average rate` : rateDiffFromAverage === 0 ? `` : `less than average rate`}`, width))}
  </div>
</div -->

<div class="grid card" style="height: 250px">
    ${resize((width, height) => arrivalLineChart(width, height))}
</div>

<!-- div class="grid grid-cols-2"">
  <div class="card grid-colspan-1">
    <h2>Bookings by room type and season</h2>
    <h3>Market segment: ${pickMarketSegment}</h3>
    ${resize((width) => typeSeasonChart(width))}
  </div>
  <div class="card grid-colspan-1">
    <h2>${pickMarketSegment} reservations: rate distribution by season</h2>
    ${resize((width, height) => dailyRateChart(width, height))}
  </div>
</div -->

<div class="card" style="padding: 0">
  <div style="padding: 1em">
    ${display(tableSearch)}
  </div>
  ${display(Inputs.table(tableSearchValue, {
      columns: [
        "Id", 
        "AnlagenbetreiberName", 
        "BetriebsStatusName", 
        "EinheitRegistrierungsdatum", 
        "InbetriebnahmeDatum", 
        "NetzbetreiberNamen", 
        "Ort",
        "Plz", 
        "StromspeichertechnologieBezeichnung",
        "Batterietechnologie", 
        "Bruttoleistung",
        "NutzbareSpeicherkapazitaet",
        "SpannungsebenenNamen"
      ],
      header: 
        {
          BetriebsStatusName: "Status", 
          EinheitRegistrierungsdatum: "Registr.", 
          InbetriebnahmeDatum: "Inbetr.", 
          Batterietechnologie: "Batt.-Techn.", 
          Bruttoleistung: "Leistung",
          NutzbareSpeicherkapazitaet: "Speicherkapazität",
          StromspeichertechnologieBezeichnung: "Art"
          },
        width: {arrivalDate: 100},
        format: {
            Id: x => x.toString(), 
            EinheitRegistrierungsdatum: d3.utcFormat("%d.%m.%Y"),
            NutzbareSpeicherkapazitaet: sparkbar(d3.max(tableSearch, d => d.NutzbareSpeicherkapazitaet))
        }
    }
  ))}
</div>


```js
// Filtered data for selected market segment
const bookingsByMarketSegment =
  pickMarketSegment == "All"
    ? hotelData.filter((d) => d.MarketSegment != "Complementary")
    : hotelData.filter((d) => d.MarketSegment == pickMarketSegment && d.MarketSegment != "Complementary");

// All bookings data (except complementary)
const bookingsAll = hotelData.filter((d) => d.MarketSegment != "Complementary");

// Bookings by nationality
const bookingCountry = d3
  .rollups(
    bookingsByMarketSegment,
    (d) => d.length,
    (v) => v.Country
  )
  .map(([name, value]) => ({name, value}))
  .sort((a, b) => d3.descending(a.value, b.value));

// Limit to top 5
const bookingCountryTopN = bookingCountry.slice(0, 5);

// Bin the rest as "Other"
const bookingCountryOther = {
  name: "Other",
  value: d3.sum(bookingCountry.slice(5 - bookingCountry.length), (d) => d.value)
};

// Combine top 5 countries and "other" for donut chart
const byCountry = bookingCountryTopN.concat(bookingCountryOther);

//Booking status (cancelled or not cancelled)
const byBookingOutcome = d3
  .rollups(
    bookingsByMarketSegment,
    (d) => d.length,
    (d) => d.IsCanceled
  )
  .map(([name, value]) => ({name, value}))
  .sort((a, b) => d3.descending(a.value, b.value));

// Bookings by room type
const byRoomType = d3
  .rollups(
    bookingsByMarketSegment,
    (d) => d.length,
    (d) => d.ReservedRoomType
  )
  .map(([name, value]) => ({name, value}))
  .sort((a, b) => d3.descending(a.value, b.value));

// Bookings by season
const bookingSeason = d3
  .rollups(
    bookingsByMarketSegment,
    (d) => d.length,
    (v) => v.season
  )
  .map(([name, value]) => ({name, value}));

// Find & format arrival date extent for big number
const arrivalDates = d3.extent(bookingsAll, (d) => d.arrivalDate);

const datesExtent = [
  d3.timeFormat("%b %d, %Y")(new Date(arrivalDates[0])),
  d3.timeFormat("%b %d, %Y")(new Date(arrivalDates[1]))
];

// Calculate rate difference from total average for big number
const rateDiffFromAverage = d3.mean(bookingsByMarketSegment, (d) => d.ADR) - d3.mean(bookingsAll, (d) => d.ADR);
```

```js
// Create search input (for searchable table)
const tableSearch = Inputs.search(bookingsAll);

const tableSearchValue = view(tableSearch);
```

```js
// Line chart (arrival dates)
let mem;
function firstOrRecent(values) {
  return values.length ? (mem = values[0]) : mem;
}
function arrivalLineChart(width, height) {
  return Plot.plot({
    height: height - 50,
    marginBottom: 35,
    width,
    x: {label: "Reg.-Datum"},
    y: {label: "Anz.Anlagen", grid: true},
    color: {domain: seasonDomain, range: seasonColors, label: "Season"},
    title: `Neu registrierte ${pickMarketSegment} nach Datum`,
    subtitle: `Daily counts (gray area) and 28-day moving average (solid line).`,
    marks: [
      () => htl.svg`<defs>
      <linearGradient id="gradient" gradientTransform="rotate(90)">
        <stop offset="60%" stop-color="#B5B5B5" stop-opacity="0.7" />
        <stop offset="100%" stop-color="#B5B5B5" stop-opacity="0.1" />
      </linearGradient>
      </defs>`,
      Plot.areaY(
        hotelData,
        Plot.binX(
          {y: "count", thresholds: "day", filter: null},
          {
            x: "EinheitRegistrierungsdatum",
            curve: "step",
            fill: "url(#gradient)"
          }
        )
      ),
      Plot.lineY(
        hotelData,
        Plot.windowY(
          {k: 28},
          Plot.binX(
            {y: "count", interval: "day", filter: null},
            {
              x: "EinheitRegistrierungsdatum",
              z: null,
              tip: {
                format: {
                  EinheitRegistrierungsdatum: true,
                  bookings: true,
                  x: "%d. %b %Y"
                }
              }
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

```js
//Create faceted histograms of daily rate

// Season color scheme
const seasonColors = ["#959C00", "#9C5A00", "#465C9C", "#109F73"];
const seasonDomain = ["Summer", "Fall", "Winter", "Spring"];

// Calculate mean daily rate by season (for rule mark)
const meanRateBySeason = d3
  .rollups(
    hotelData,
    (v) => d3.mean(v, (d) => d.ADR),
    (d) => d.season
  )
  .map(([season, value]) => ({season, value}));

// Build daily rate faceted histograms
const dollarFormat = d3.format("$.2f");
const defaultFormat = d3.format(",");
function dailyRateChart(width, height) {
  return Plot.plot({
    width,
    height: height - 20,
    marginLeft: 30,
    marginRight: 0,
    marginTop: 10,
    marginBottom: 30,
    x: {label: "Average rate($)", grid: true},
    y: {nice: true, label: null},
    axis: null,
    fy: {label: "Season", domain: seasonDomain},
    color: {domain: seasonDomain, range: seasonColors, label: "Season"},
    marks: [
      Plot.axisX({ticks: 4}),
      Plot.axisY({ticks: 2}),
      Plot.rectY(
        hotelData,
        Plot.binX({y: "count"}, {x: "ADR", interval: 10, fill: "season", fy: "season", tip: true})
      ),
      Plot.text(
        hotelData,
        Plot.groupZ(
          {text: (v) => `${v[0].season} (n = ${defaultFormat(v.length)})`},
          {
            fy: "season",
            frameAnchor: "top-right",
            dx: -6,
            dy: 6
          }
        )
      ),
      Plot.ruleX(meanRateBySeason, {x: "value", fy: "season", stroke: "currentColor"}),
      Plot.text(meanRateBySeason, {
        x: "value",
        fy: "season",
        text: (d) => `${d.season} mean rate: ${dollarFormat(d.value)}`,
        dx: 5,
        dy: -20,
        textAnchor: "start"
      }),
      Plot.frame({opacity: 0.4})
    ]
  });
}
```

```js
// Faceted bar charts of bookings by room type
function typeSeasonChart(width, height) {
  return Plot.plot({
    marginTop: 20,
    marginBottom: 30,
    marginLeft: 40,
    width,
    height: 270,
    x: {domain: seasonDomain, tickSize: 0, axis: null, label: "Season"},
    y: {label: "Count", fontSize: 0, grid: true, insetTop: 5},
    fx: {label: "Room type"},
    color: {legend: true, domain: seasonDomain, range: seasonColors, label: "Season"},
    marks: [
      Plot.text("ABCDEFGHLP", {fx: Plot.identity, text: null}),
      Plot.frame({opacity: 0.4}),
      Plot.barY(
        bookingsByMarketSegment,
        Plot.groupX(
          {y: "count"},
          {
            x: "season",
            fx: "ReservedRoomType",
            fill: "season",
            tip: true
          }
        )
      )
    ]
  });
}
```