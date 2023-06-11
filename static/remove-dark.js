const fs = require("fs");

// Read the HTML file
fs.readFile("templates/wheater-aus.html", "utf8", (err, htmlString) => {
  if (err) {
    console.error("Error reading the file:", err);
    return;
  }

  // Use the regular expression to remove the "dark:" class
  const updatedHtmlString = htmlString.replace(/\bdark:([\w-]+\s?)/g, "");

  // Write the updated HTML back to the file
  fs.writeFile("templates/wheater-aus.html", updatedHtmlString, "utf8", (err) => {
    if (err) {
      console.error("Error writing to the file:", err);
      return;
    }
    console.log("File successfully updated!");
  });
});