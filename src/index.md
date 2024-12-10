


<div class="hero">
    <img src="assets/logo/internet-cafe-svgrepo-com.svg" width="200">
    <h1>Datenradar</h1>
</div>

  <h2>Open Data Datenvisualisierungen</h2>


<!-- img src="assets/logo/internet-cafe-svgrepo-com.svg" width="400" -->

Visualisierungen von Open-Data-Datensätzen der Stadt Münster.\
Bitte Datensatz auswählen:



```js
const dashboards = await FileAttachment("data/index-observable-notebooks.json").json();

// display(dashboards)

```



```html

<div class="topborder grid grid-cols-2">
    ${dashboards.map(item => html`<a class="listcard card" href="${item.file}">
    <div class="fl1">
        <img class="listimg" src="_file/assets/logo/computerscreen.svg" height="100">
        <div class="fl2">
            <h1>${item.title}</h1>
            ${item.desc}
        </div>
    </div>
    </a>

    `)}

</div>
```



<style>
.topborder {margin-top:2rem}
.hero img {
    float:left;
    margin-right:-20px
}
.listimg {float:left;margin-right:1rem}

a.listcard:hover{text-decoration:none}
.listcard:hover {border:3px solid black;background-color:#ddd}
.card.listcard {border:3px solid transparent;min-height:100px;margin: 0}
a.card.listcard {display:block}
.listcard .fl1 {display:flex}
.hero {
  font-family: var(--sans-serif);
  margin: 3rem 0 6rem;
  text-wrap: balance;
}

.hero h1 {
  margin: 1rem 0;
  padding: 2rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
  .hero {}
}


</style>

