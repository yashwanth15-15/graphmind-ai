import { useState, useEffect } from 'react'
import { checkHealth, uploadDocument } from './api/client'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState<'loading' | 'connected' | 'disconnected'>('loading')
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  useEffect(() => {
    const verifyBackend = async () => {
      const isConnected = await checkHealth();
      setBackendStatus(isConnected ? 'connected' : 'disconnected');
    };
    verifyBackend();
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
      setUploadResult(null);
      setUploadError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setUploadError(null);
    try {
      const result = await uploadDocument(selectedFile);
      setUploadResult(result);
    } catch (err: any) {
      setUploadError(err.message || 'Failed to upload document');
    } finally {
      setUploading(false);
    }
  };

  return (
    <>
      <section id="center" style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
        <div className="hero" style={{ marginBottom: '2rem' }}>
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        
        <div>
          <h1>GraphMind AI - Milestone 3</h1>
          <p>Document Upload & Text Extraction</p>
          
          <div style={{ marginTop: '20px', padding: '10px', borderRadius: '8px', backgroundColor: backendStatus === 'connected' ? '#d4edda' : backendStatus === 'disconnected' ? '#f8d7da' : '#e2e3e5', color: backendStatus === 'connected' ? '#155724' : backendStatus === 'disconnected' ? '#721c24' : '#383d41', fontWeight: 'bold', marginBottom: '2rem' }}>
            {backendStatus === 'loading' && "Checking Backend..."}
            {backendStatus === 'connected' && "Backend Connected ✓"}
            {backendStatus === 'disconnected' && "Backend Disconnected"}
          </div>
        </div>

        <div style={{ backgroundColor: '#1a1a1a', padding: '2rem', borderRadius: '12px', border: '1px solid #333' }}>
          <h2>Upload Document</h2>
          <p style={{ color: '#888', marginBottom: '1rem' }}>Supported formats: PDF, PPTX, TXT</p>
          
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
            <input 
              type="file" 
              accept=".pdf,.pptx,.txt" 
              onChange={handleFileChange}
              style={{ padding: '0.5rem' }}
            />
            <button 
              onClick={handleUpload} 
              disabled={!selectedFile || uploading || backendStatus !== 'connected'}
              style={{ padding: '0.5rem 1.5rem', backgroundColor: '#646cff', color: 'white', border: 'none', borderRadius: '4px', cursor: (!selectedFile || uploading || backendStatus !== 'connected') ? 'not-allowed' : 'pointer', opacity: (!selectedFile || uploading || backendStatus !== 'connected') ? 0.5 : 1 }}
            >
              {uploading ? 'Uploading...' : 'Upload & Extract'}
            </button>
          </div>

          {uploadError && (
            <div style={{ color: '#ff4a4a', marginTop: '1rem', padding: '1rem', backgroundColor: 'rgba(255, 74, 74, 0.1)', borderRadius: '4px' }}>
              Error: {uploadError}
            </div>
          )}

          {uploadResult && (
            <div style={{ marginTop: '2rem', textAlign: 'left' }}>
              <h3 style={{ color: '#4ade80' }}>Extraction Successful!</h3>
              <p><strong>Filename:</strong> {uploadResult.filename}</p>
              <p><strong>Type:</strong> {uploadResult.document_type}</p>
              <p><strong>Total Pages/Slides:</strong> {uploadResult.total_pages}</p>
              
              <div style={{ marginTop: '1rem' }}>
                <h4>Extracted Content:</h4>
                <div style={{ maxHeight: '400px', overflowY: 'auto', backgroundColor: '#0f0f0f', padding: '1rem', borderRadius: '8px', border: '1px solid #333' }}>
                  {uploadResult.pages.map((page: any, index: number) => (
                    <div key={index} style={{ marginBottom: '1.5rem', paddingBottom: '1.5rem', borderBottom: index < uploadResult.pages.length - 1 ? '1px solid #333' : 'none' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', color: '#888', fontSize: '0.9rem' }}>
                        <span>Page/Slide {page.page_number}</span>
                        <span>Type: {page.metadata.type}</span>
                      </div>
                      <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', margin: 0, fontSize: '0.95rem', color: '#e5e5e5' }}>
                        {page.text || <em style={{ color: '#666' }}>(No text extracted)</em>}
                      </pre>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </section>
    </>
  )
}

export default App
