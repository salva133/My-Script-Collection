const fs = require("fs");

// Lesen Sie die JSON-Datei
let data = JSON.parse(fs.readFileSync("list-pharmacies.json"));

// Gruppieren Sie die Daten nach den ersten beiden Ziffern der PLZ
let groups = {};
for (let item of data) {
  let groupKey = Math.floor(item["PLZ"] / 10000) * 10;
  if (!groups[groupKey]) {
    groups[groupKey] = [];
  }
  groups[groupKey].push(item);
}

// Schreiben Sie jede Gruppe in eine separate Datei
for (let groupKey in groups) {
  fs.writeFileSync(
    `list-pharmacies_${groupKey}.json`,
    JSON.stringify(groups[groupKey], null, 2)
  );
}
