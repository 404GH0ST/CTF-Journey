const PDFExtract = require('pdf.js-extract').PDFExtract;
const pdfExtract = new PDFExtract();
const fs = require('fs');
const buffer = fs.readFileSync("flag_protected.pdf");
const options = {"password": "makanapel"}; /* see below */
pdfExtract.extractBuffer(buffer, options, (err, data) => {
  if (err) return console.log(err);
  console.log(data);
});
