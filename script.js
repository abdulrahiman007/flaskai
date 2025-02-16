document.getElementById("fileInput").addEventListener("change", function() {
    if (this.files.length > 0) {
        alert("File selected: " + this.files[0].name);
    }
});
