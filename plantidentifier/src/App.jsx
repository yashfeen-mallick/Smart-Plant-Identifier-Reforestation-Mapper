import React, { useState } from "react";
import './app.css';

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (selectedFile) {
      const imageUrl = URL.createObjectURL(selectedFile);
      setPreview(imageUrl);
      setPrediction(null);  // Reset previous result
      setError(null);       // Reset error
    } else {
      setPreview(null);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data);  // Set the prediction data
        setError(null);
      } else {
        setPrediction(null);
        setError(data.error || "Prediction failed.");
      }
    } catch (error) {
      console.error("Error sending image to ML model:", error);
      setError("Prediction failed.");
      setPrediction(null);
    }
  };

  return (
    <div className="maindiv">
      <div>PLANT IDENTIFIER</div>

      <div className="innerdiv">
        <h2 className="heading">Upload plant image</h2>
        <input type="file" className="inputbox" accept="image/*" onChange={handleFileChange} />
        {preview && <img src={preview} alt="Preview" className="preview-img" />}
        <button className="submitbutton" onClick={handleSubmit}>Predict</button>

      <div className="resultdiv">
        {error && <div className="error">❌ {error}</div>}
        {prediction && (
          <div className="result">
            <h3>✅ Prediction Result</h3>
            <p><strong>Label:</strong> {prediction.label}</p>
            <p><strong>Confidence:</strong> {prediction.confidence}%</p>
          </div>
        )}
      </div>
        </div>
    </div>
  );
}
