const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;

// Ensure the uploads directory exists
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

app.use(cors());
app.use(express.static(path.join(__dirname, "..", "frontend")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "..", "frontend", "index.html"));
});
app.use(express.json({ limit: "10mb" }));

// Multer config: saves image with a unique timestamped name
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    const uniqueName = `input_${Date.now()}.jpg`;
    cb(null, uniqueName);
  }
});
const upload = multer({ storage });

app.post("/detect", upload.single("image"), (req, res) => {
  const language = req.body.language || "english";
  const imagePath = req.file.path;
  const scriptPath = path.join(__dirname, "emotion.py");

  // Run the Python script with image path as an argument
  exec(`python "${scriptPath}" "${imagePath}"`, (err, stdout, stderr) => {
    // Delete the uploaded image after processing
    fs.unlink(imagePath, (unlinkErr) => {
      if (unlinkErr) console.warn("Could not delete uploaded image:", unlinkErr);
    });

    if (err) {
      console.error("Python error:", err);
      console.error("stderr:", stderr);
      return res.status(500).send("Emotion detection failed.");
    }

    const emotion = stdout.trim().toLowerCase();
  
   const songs = {
  english: {
    happy: "https://www.youtube.com/watch?v=OPf0YbXqDm0",
    sad: "https://www.youtube.com/watch?v=Xn676-fLq7I",
    angry: "https://www.youtube.com/watch?v=k4V3Mo61fJM",
    calm: "https://www.youtube.com/watch?v=QfgJQUiQFes",
    surprised: "https://www.youtube.com/watch?v=4NRXx6U8ABQ",
    neutral: "https://www.youtube.com/watch?v=liTfD88dbCo"
  },
  hindi: {
    happy: "https://www.youtube.com/watch?v=ph4i-C8UC1w",
    sad: "https://www.youtube.com/watch?v=bw7bVpI5VcM",     // Agar Tum Saath Ho
    angry: "https://www.youtube.com/watch?v=T94PHkuydcw",   // Zinda
    calm: "https://www.youtube.com/watch?v=vEe-UgJvUHE",    // Raabta
    surprised: "https://www.youtube.com/watch?v=BddP6PYo2gs",
    neutral: "https://www.youtube.com/watch?v=BddP6PYo2gs"
  },
  punjabi: {
    happy: "https://www.youtube.com/watch?v=dZ0fwJojhrs",   // High Rated Gabru
    sad: "https://www.youtube.com/watch?v=2eliQ_KR8yA",
    angry: "https://www.youtube.com/watch?v=E8rpY2FwKkY",
    calm: "https://www.youtube.com/watch?v=S-ezhTXPVGU",
    surprised: "https://www.youtube.com/watch?v=vX2cDW8LUWk",
    neutral: "https://www.youtube.com/watch?v=nqUN530Rgtw"
  }
};

    const langSongs = songs[language] || songs["english"];
const videoURL = langSongs[emotion] || langSongs["neutral"];


// Convert to EMBED + AUTOPLAY
const embedURL = videoURL
  .replace("watch?v=", "embed/")
  + "?autoplay=1&mute=1";
  res.json({ emotion, url: embedURL });
  });
});

app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
