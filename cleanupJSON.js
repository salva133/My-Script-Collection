const fs = require('fs');

// Lesen Sie die JSON-Datei
let data = JSON.parse(fs.readFileSync('apotheken.json'));

// Entfernen Sie die unerwünschten Eigenschaften aus allen Objekten
data = data.map(item => {
  const newItem = { ...item }; // Erstellen Sie eine Kopie des aktuellen Objekts

  // Entfernen Sie die unerwünschten Eigenschaften
  delete newItem['Debitor ID'];
  delete newItem['Apo Nr.'];
  delete newItem['State'];
  delete newItem['Email'];
  delete newItem['Inhabername'];
  delete newItem['Stadt'];
  delete newItem['Straße'];
  delete newItem['Hausnummer'];
  delete newItem['Land'];

  return newItem; // Geben Sie das bereinigte Objekt zurück
});

// Schreiben Sie die bereinigten Daten zurück in die Datei
fs.writeFileSync('apotheken.json', JSON.stringify(data, null, 2));
