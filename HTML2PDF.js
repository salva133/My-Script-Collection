const puppeteer = require('puppeteer');
const path = require('path');

async function printPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const htmlPath = path.join(process.env.HOME, 'Downloads/new woko/index.html');
    await page.goto('file://' + htmlPath, {waitUntil: 'networkidle0'});
    const pdf = await page.pdf({ format: 'A4' });

    await browser.close();
    return pdf;
}

printPDF().then(pdf => {
    const outputPath = path.join(process.env.HOME, 'Downloads/new woko/output.pdf');
    require('fs').writeFileSync(outputPath, pdf);
});