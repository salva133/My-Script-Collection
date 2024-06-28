const axios = require("axios");
const fs = require("fs");
const XLSX = require("xlsx");
require('dotenv').config();  // Umgebungsvariablen laden

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Lesen Sie die Datei
const workbook = XLSX.readFile("pharmacy_master_list_Blue.xlsx");

// Holen Sie das erste Arbeitsblatt
const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];

// Konvertieren Sie das Arbeitsblatt in JSON
let data = XLSX.utils.sheet_to_json(worksheet);

// Definieren Sie die Basis-URL für die Geocoding API
const baseURL = "https://maps.googleapis.com/maps/api/geocode/json";

// API-Schlüssel aus Umgebungsvariablen laden
const apiKey = process.env.GOOGLE_API_KEY;

// Eine asynchrone Funktion, die die Geocoding API aufruft
async function getGeoData(address) {
  try {
    const response = await axios.get(baseURL, {
      params: {
        address: address,
        key: apiKey,
      },
    });

    // Überprüfen Sie, ob die Anfrage erfolgreich war und ob Ergebnisse zurückgegeben wurden
    if (
      response.data.status !== "OK" ||
      !response.data.results ||
      response.data.results.length === 0
    ) {
      throw new Error(`No results for ${address}`);
    }

    const location = response.data.results[0].geometry.location;
    return location;
  } catch (error) {
    const errorMessage = `Error getting geodata for ${address}: ${error.message}\n`;
    console.error(errorMessage);
    fs.appendFileSync("error.log", errorMessage);
    return null;
  }
}

// Eine asynchrone Funktion, die eine Warteschlange von Geocoding-Anfragen erstellt
async function addGeoData(data) {
  for (let i = 0; i < data.length; i++) {
    const address = `${data[i]["Straße"]} ${data[i]["Hausnummer"]}, ${data[i]["PLZ"]} ${data[i]["Stadt"]}, ${data[i]["Land"]}`;
    const location = await getGeoData(address);

    if (location) {
      data[i] = {
        ...data[i],
        lat: location.lat,
        lng: location.lng,
      };
    }

    // Warten Sie 50 Millisekunden vor dem nächsten Request
    await sleep(50);
  }
  return data;
}

// Rufen Sie die addGeoData Funktion auf und speichern Sie das Ergebnis in einer JSON-Datei
addGeoData(data)
  .then((dataWithGeoData) => {
    fs.writeFileSync(
      "apotheken_add.json",
      JSON.stringify(dataWithGeoData, null, 2)
    );
  })
  .catch((error) => {
    const errorMessage = `Error: ${error.message}\n`;
    console.error(errorMessage);
    fs.appendFileSync("error.log", errorMessage);
  });
