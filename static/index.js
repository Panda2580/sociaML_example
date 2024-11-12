// Funktion zur Aktualisierung der Statusmeldung
function addStatusMessage(message) {
    const statusMessage = document.getElementById('status-message');
    statusMessage.textContent = message;
}

// Funktion zum Anzeigen des Ladeindikators
function toggleLoadingSpinner(show) {
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = show ? 'block' : 'none';
}

// Hauptfunktion zum Hochladen der Datei
function handleUpload(event) {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file');

    // Überprüfen, ob eine Datei ausgewählt wurde
    if (fileInput.files.length === 0) {
        addStatusMessage("Please select a file to upload.");
        event.preventDefault();
        return;
    }

    // Statusmeldung und Spinner anzeigen
    addStatusMessage("Uploading file...");
    toggleLoadingSpinner(true);
}

// Event-Listener für das Formular
document.getElementById('upload-form').addEventListener('submit', handleUpload);


