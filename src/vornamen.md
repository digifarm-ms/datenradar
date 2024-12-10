---
theme: dashboard
title: Vornamen
toc: false
---

# Vornamenstatistik für Neugeborene

Zeigt die Top ${TOP_N_COUNT} Vornamen bei _Geburten in Münster_ über die letzten ${MONTHS_OF_DATA} Jahre.

```js
import {revive} from "./components/revive.js";
import {BumpChart} from "./components/BumpChart.js";
```

```js
//const {womens, mens, MONTHS_OF_DATA, TOP_N_COUNT} = await FileAttachment("data/top-ranked-players.json").json().then(revive);

const {womens, mens, MONTHS_OF_DATA, TOP_N_COUNT} = await FileAttachment("data/vornamen-geburten-topliste.json").json().then(revive);

console.log("WOMENS", womens);

```

<div class="grid">
  <div class="card">
    <h2>Top Mädchen Vornamen</h2>
    ${resize((width) => BumpChart(womens, {width}))}
  </div>
  <div class="card">
    <h2>Top Jungen Vornamen</h2>
    ${resize((width) => BumpChart(mens, {width}))}
  </div>
</div>

Daten: [Open-Data-Portal Münster](https://opendata.stadt-muenster.de/dataset/vornamenstatistik-f%C3%BCr-neugeborene-nach-geburtsjahr-m%C3%BCnster)