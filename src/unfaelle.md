---
theme: dashboard
title: Unfälle
toc: false
---


```js
// Import deck.gl components for interactive map
import deck from "npm:deck.gl";

const {DeckGL, AmbientLight, PointCloudLayer, PointCloudLayerProps, LASLoader, GeoJsonLayer, TextLayer, HexagonLayer, LightingEffect, PointLight, ScatterplotLayer, COORDINATE_SYSTEM} = deck;

```


```js
// County-level data for US
const states = await fetch("https://gist.githubusercontent.com/fegoa89/d33514a5e59eb5af812b909915bcb3da/raw/05ddd9064028f1218cf6a1efb797a1d903508ad5/germany-states.geojson").then((r) => r.json());

// State polygons
// const states = topojson.feature(us, us.objects.states);

// Find state centroids (for text label)
const stateCentroid = states.features.map(d => ({name: d.properties.NAME_1, longitude: d3.geoCentroid(d.geometry)[0], latitude: d3.geoCentroid(d.geometry)[1]}));

// NID dams data:
const dams = FileAttachment("data/unfaelle-muenster.csv").csv({typed: true});
```
# Unfälle im Regierungsbezirk Münster


<div class="grid grid-cols-3">
    <div class="card grid-colspan-2" style="padding: 0px;">
        <div style="padding: 1rem;">
            <h2>Test einer 3D-Darstellung</h2>
            <h3>Mit der Maus zoomen und scrollen, oder SHIFT halten und drehen.</h3>
            ${colorLegend}
        </div>
        <div>
            <figure style="max-width: none; position: relative;">
            <div id="container" style="border-radius: 8px; overflow: hidden; height: 620px; margin: 0rem 0;">
            </div>
            </figure>
        </div>
    </div>
</div>


Stichworte: KFZ, Autos, Fahrzeuge, Verkehrsunfälle, Kraftfahrzeuge


```js
const colorRange = [
  [59, 82, 139],
  [33, 145, 140],
  [94, 201, 98],
  [253, 231, 37]
];

const colorLegend = Plot.plot({
  margin: 0,
  marginTop: 30,
  marginRight: 20,
  width: 450,
  height: 50,
  style: "color: 'currentColor';",
  x: {padding: 0, axis: null},
  marks: [
    Plot.cellX(colorRange, {fill: ([r, g, b]) => `rgb(${r},${g},${b})`, inset: 2}),
    Plot.text(["Wenig Unfälle"], {frameAnchor: "top-left", dy: -12}),
    Plot.text(["Viele Unfälle"], {frameAnchor: "top-right", dy: -12})
  ]
});

const effects = [
  new LightingEffect({
    ambientLight: new AmbientLight({color: [255, 255, 255], intensity: 1}),
    pointLight: new PointLight({color: [255, 255, 255], intensity: 0.8, position: [-0.144528, 49.739968, 80000]}),
    pointLight2: new PointLight({color: [255, 255, 255], intensity: 0.8, position: [-3.807751, 54.104682, 8000]})
  })
];
```


```js
const deckInstance = new DeckGL({
  container,
  initialViewState,
  controller: true,
  effects
});

// clean up if this code re-runs
invalidation.then(() => {
  deckInstance.finalize();
  container.innerHTML = "";
});
```

```js
const initialViewState = {
  longitude: 7.628202,
  latitude: 51.961563,
  zoom: 7.5,
  minZoom: 1,
  maxZoom: 70,
  pitch: 45,
  bearing: 20
};
```

```js
deckInstance.setProps({
  controller: true,
  layers: [
    new GeoJsonLayer({
      id: "base-map",
      data: states,
      lineWidthMinPixels: 1.5,
      getLineColor: [255, 255,255, 100],
      getFillColor: [10, 10, 100]
    }),
    new HexagonLayer({
      id: 'hexbin-plot',
      data: dams,
      coverage: 0.3,
      radius: 600,
      upperPercentile: 99,
      colorRange,
      elevationScale: 20,
      elevationRange: [50, 5000],
      extruded: true,
      getPosition: d => [d.XGCSWGS84,d.YGCSWGS84],
      opacity: 1,
      material: {
        ambient: 1,
        specularColor: [51, 51, 51]
      }
    }),
    new TextLayer({
        id: "text-layer",
        data: stateCentroid,
        getPosition: d => [d.longitude, d.latitude],
        getText: d => d.name,
        fontFamily: 'Helvetica',
        fontWeight: 700,
        background: false,
        fontSettings: ({
          sdf: true,
          }),
        outlineWidth: 4,
        getSize: 14,
        getColor: [247,248,243, 255],
        getTextAnchor: 'middle',
        getAlignmentBaseline: 'center',
        getPixelOffset: [0, -10]
    }),
    new PointCloudLayer({
        id: 'PointCloudLayer',
//        data: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/pointcloud.json',
        data: 'data/3dm_32_405_5757_1_nw.laz',
        loaders: [LASLoader],
coordinateSystem: COORDINATE_SYSTEM.LNGLAT,
getNormal: [0, 1, 0],
getColor: [255, 55, 55],
opacity: 1,
pointSize: 5
      })
  ]
});
```