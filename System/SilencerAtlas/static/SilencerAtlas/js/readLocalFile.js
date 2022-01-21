// store a reference to our file handle
let fileHandle;

async function getLocalFile() {
  // open file picker
  [fileHandle] = await window.showOpenFilePicker();
  console.log(fileHandle.kind, fileHandle.name);
  if (fileHandle.kind === "file") {
    // run file code
    await myFunction(await readTextFile(fileHandle));
  } else if (fileHandle.kind === "directory") {
    // run directory code
  }
}

async function readTextFile(fileHandle) {
  const file = await fileHandle.getFile();
  const contents = await file.text();
  console.log(contents);
  return contents;
}

async function myFunction(contents) {

}
