const fs = require("fs");
global.XMLHttpRequest = require("xhr2");
const { PythonShell } = require("python-shell");

exports.transfer = async (req, res) => {
  const baseId = req.query.base;
  const styleId = req.query.style;
  const baseImage = getImagePath(baseId);
  const styleImage = getImagePath(styleId);
  const outputPath = await runPython(baseImage, styleImage);
  res.status(200).sendFile(outputPath);
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
        const outputPath = await result[result.length - 1];
        console.log(outputPath);
        resolve(outputPath);
      }
    );
  });
};
