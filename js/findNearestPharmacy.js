const DEBUG_MODE = true;

let arrJson = [];
let arrPlz = [];

async function loadData() {
  const responseJson = await fetch(
    "/dam/jcr:f4fcfc72-3f6b-49f6-84a9-258af95424d5/pharmacies.json"
  );
  const dataJson = await responseJson.json();
  arrJson = dataJson;

  const responsePlz = await fetch(
    "/dam/jcr:941d9e94-7907-4981-b600-20e2252e6f8a/plz_germany.json"
  );
  const dataPlz = await responsePlz.json();
  arrPlz = dataPlz;
}

loadData().catch((error) => {
  console.error("Error:", error);
});

function debugVariableObj(variableObj) {
  // Usage: debugVariableObj({ <variablename> })
  if (DEBUG_MODE) {
    if (!variableObj || Object.keys(variableObj).length === 0) {
      console.log(
        "[DEBUG] No object provided. Please check your input. Correct usage: debugVariableObj({ variableName });"
      );
      return;
    }
    const variableName = Object.keys(variableObj)[0];
    const variableValue = variableObj[variableName];
    console.log(`[DEBUG] ${variableName}:`, variableValue);
  }
}

function debugLog(message) {
  if (DEBUG_MODE) {
    console.log(`[DEBUG] ${message}`);
  }
}

function deg2rad(deg) {
  return deg * (Math.PI / 180);
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
  const R = 6371; // Radius der Erde in km
  const dLat = deg2rad(lat2 - lat1);
  const dLon = deg2rad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) *
      Math.cos(deg2rad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const d = R * c; // Entfernung in km
  return d;
}

function decodeHtml(html) {
  var txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
}

function removeSpecialChars(str) {
  return str.replace(/[^a-zA-Z0-9 ]/g, "");
}

function addPlz() {
  let plz = document.querySelector("#plz");
  if (plz === null) {
    return;
  }
  plz = plz.value;
  if (plz.length <= 0) {
    return;
  }
  debugLog("1. PLZ given");

  let link = "";
  let plzGroup = parseInt(plz.charAt(0));

  let locations = arrJson.filter((item) => item["PLZ"] === plz);

  if (locations.length > 0) {
    let apotheke = locations
      .map((location) =>
        encodeURIComponent(
          removeSpecialChars(decodeHtml(location.Apothekenname))
        )
      )
      .join("|");
    link = `https://www.google.de/maps/search/${plz}+${apotheke}`;
    debugLog("5. Query returned");
  } else {
    let initialLocation = arrPlz.find((item) => item["plz"] === plz);
    let initialLat = initialLocation.lat;
    let initialLng = initialLocation.lng;

    let location = arrJson.reduce((prev, curr) => {
      const prevDistance = getDistanceFromLatLonInKm(
        initialLat,
        initialLng,
        prev.lat,
        prev.lng
      );
      const currDistance = getDistanceFromLatLonInKm(
        initialLat,
        initialLng,
        curr.lat,
        curr.lng
      );

      return currDistance < prevDistance ? curr : prev;
    });
    if (location) {
      let apotheke = encodeURIComponent(
        removeSpecialChars(decodeHtml(location.Apothekenname))
      );
      let correctedPlz = location.PLZ; // Use the PLZ from the found location
      link = `https://www.google.de/maps/search/${correctedPlz}+${apotheke}`; // Use the corrected PLZ here
      debugLog("5. Query returned");
    } else {
      link = `https://www.google.de/maps/search/${plz}+apotheke`;
      debugLog("5.1 Query not solvable, using fallback query");
    }
  }

  let xa = document.createElement("a");
  debugLog("6. create xa");
  xa.href = link;
  debugLog("7. handover link to href");
  xa.target = "_blank";
  xa.click();
  debugLog("8. clicking for xa");
}

document.addEventListener("DOMContentLoaded", () => {
  debugLog("9. Listening for Enter button");
  document.querySelector("#plz").addEventListener("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
      debugLog("10. Enter got hit");
      addPlz();
    }
  });
});
