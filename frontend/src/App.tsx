import { useState } from "react";
import axios from "axios";
import "./App.css";

type VerificationField = {
  expected: string | null;
  actual: string | null;
  score: number;
  status: string;
};

type ApiResponse = {
  filename: string;
  ocr_text: string[];
  parsed: {
    brand: string | null;
    class: string | null;
    alcohol: string | null;
    net_contents: string | null;
    government_warning: boolean;
  };
  verification: {
    overall: string;
    results: {
      brand: VerificationField;
      class: VerificationField;
      alcohol: VerificationField;
      net_contents: VerificationField;
      government_warning: VerificationField;
    };
  };
};

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [brand, setBrand] = useState("OLD TOM DISTILLERY");
  const [className, setClassName] = useState("Kentucky Straight Bourbon Whiskey");
  const [alcohol, setAlcohol] = useState("45%");
  const [netContents, setNetContents] = useState("750 mL");
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (selectedFile: File | null) => {
    setFile(selectedFile);
    setResult(null);

    if (selectedFile) {
      setPreviewUrl(URL.createObjectURL(selectedFile));
    } else {
      setPreviewUrl("");
    }
  };

  const handleVerify = async () => {
    if (!file) {
      setError("Please upload a label image.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("brand", brand);
    formData.append("class_name", className);
    formData.append("alcohol", alcohol);
    formData.append("net_contents", netContents);

    try {
      const response = await axios.post<ApiResponse>(
        "https://ai-alcohol-label-verification-4j54.onrender.com/api/verify",
        formData
      );

      setResult(response.data);
    } catch {
      setError("Unable to verify label. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const statusLabel = (status: string) => {
    return status === "PASS" ? "✅ Pass" : "⚠ Review Recommended";
  };

  const overallText =
  result?.verification.overall === "PASS"
    ? "Verified"
    : "Manual Review Recommended";

  return (
    <div className="page">
      <div className="container">
        <header className="hero">
          <p className="eyebrow">AI-Powered Alcohol Label Verification Prototype</p>
          <h1>AI-Powered Alcohol Label Verification</h1>
          <p>
            Upload a label image, extract text using OCR, and compare it against
            expected application values.
          </p>
        </header>

        <div className="layout">
          <main className="card">
            <h2>Upload Label</h2>

            <input
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              onChange={(e) => handleFileChange(e.target.files?.[0] || null)}
            />

            {previewUrl && (
              <div className="preview-box">
                <img src={previewUrl} alt="Uploaded label preview" />
              </div>
            )}

            {file && (
              <p className="file-name">
                Selected file: <strong>{file.name}</strong>
              </p>
            )}

            <h2>Expected Application Values</h2>

            <label>Brand Name</label>
            <input value={brand} onChange={(e) => setBrand(e.target.value)} />

            <label>Class / Type</label>
            <input
              value={className}
              onChange={(e) => setClassName(e.target.value)}
            />

            <label>Alcohol Content</label>
            <input
              value={alcohol}
              onChange={(e) => setAlcohol(e.target.value)}
            />

            <label>Net Contents</label>
            <input
              value={netContents}
              onChange={(e) => setNetContents(e.target.value)}
            />

            {error && <div className="error">{error}</div>}

            <button onClick={handleVerify} disabled={loading}>
              {loading ? "Verifying..." : "Verify Label"}
            </button>
          </main>

          {result && (
            <aside className="card summary-card">
              <h2>Verification Summary</h2>

              <div
                className={
                  result.verification.overall === "PASS"
                    ? "overall pass"
                    : "overall fail"
                }
              >
                {overallText}
              </div>

              <p>
                The system extracted text from the uploaded image and compared
                it against the expected values.
              </p>
            </aside>
          )}
        </div>

        {result && (
          <section className="card">
            <h2>Field-Level Results</h2>

            <div className="results-grid">
              {Object.entries(result.verification.results).map(
                ([field, value]) => (
                  <div
                    key={field}
                    className={
                      value.status === "PASS"
                        ? "result-card pass-card"
                        : "result-card fail-card"
                    }
                  >
                    <h3>{field.replace("_", " ").toUpperCase()}</h3>
                    <p>
                      <strong>Expected:</strong> {value.expected || "N/A"}
                    </p>
                    <p>
                      <strong>Extracted:</strong> {value.actual || "Not found"}
                    </p>
                    <p>
                      <strong>Match Score:</strong> {Math.round(value.score)}%
                    </p>
                    <p>
                      <strong>Status:</strong> {statusLabel(value.status)}
                    </p>
                  </div>
                )
              )}
            </div>

            <h2>OCR Text Extracted</h2>
            <pre>{JSON.stringify(result.ocr_text, null, 2)}</pre>
          </section>
        )}
      </div>
    </div>
  );
}

export default App;