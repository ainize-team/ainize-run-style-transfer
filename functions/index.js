const fs = require("fs");
global.XMLHttpRequest = require("xhr2");
const { PythonShell } = require("python-shell");

exports.transfer = async (req, res) => {
  const baseId = req.query.base;
  const styleId = req.query.style;
  const baseImage = getImagePath(baseId);
  const styleImage = getImagePath(styleId);
  const { basePath, stylePath, outputPath } = await runPython(baseImage, styleImage);
  const fileNames = [basePath, stylePath, outputPath];
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write('<html><body>');
  const files = fileNames.map((filename) => {
    fs.readFile(filename, (err, data) => {
      if (err) throw err;
      res.write('<img src="data:image/jpeg;base64,');
      res.write(Buffer.from(data).toString('base64'));
      res.write('" width="300" height="300" />');
    });
  });
  Promise.all(files, async () => {
    res.end('</body></html>');
  });
};

getImagePath = imageId => {
  return `https://drive.google.com/uc?export=download&id=${imageId}`;
};

runPython = (baseHash, styleHash) => {
  return new Promise((resolve, reject) => {
    PythonShell.run(
      "/workspace/functions/style-transfer.py",
      { args: [baseHash, styleHash] },
      async (err, result) => {
        if (err) {
          if (err.traceback === undefined) {
            console.log(err.message);
          } else {
            console.log(err.traceback);
          }
        }
        const basePath = await result[result.length - 3];
        const stylePath = await result[result.length - 2];
        const outputPath = await result[result.length - 1];
        console.log(basePath, stylePath, outputPath);
        resolve({basePath, stylePath, outputPath});
      }
    );
  });
};
