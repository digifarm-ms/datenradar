---
theme: dashboard
title: Spielplätze
toc: false
---

# Kinderspielplätze in Münster


```js
import * as L from "npm:leaflet";

const plz = FileAttachment("data/spielplaetze.json").json();
```

```js
const div = display(document.createElement("div"));
div.style = "height: 800px;";

const map = L.map(div)
  .setView([51.96236, 7.62571], 14);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
})
  .addTo(map);

let grandCentralLayer = L.geoJson(plz, {
    onEachFeature: function (feature, layer) {
        layer.bindPopup('<b>'+feature.properties.Name+'</b><p>Fläche: '+feature.properties.Fl\u00e4che +'m²</p>');
    },
    weight: 2,
    color: '#33f'
}).addTo(map);

// map.fitBounds(grandCentralLayer.getBounds());

```
