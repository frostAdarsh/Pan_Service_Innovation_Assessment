import React, { useState } from 'react';
import FileUpload from '../components/FileUpload'; 
import MediaChat from '../components/MediaChat';   

export default function Home() {
  const [currentDocument, setCurrentDocument] = useState(null);
  const [localFileUrl, setLocalFileUrl] = useState(null);

  const handleUploadSuccess = (docData, fileUrl) => {
    setCurrentDocument(docData);
    setLocalFileUrl(fileUrl);
  };

  const handleReset = () => {
    setCurrentDocument(null);
    setLocalFileUrl(null);
  };

  return (
    <div>
      {!currentDocument ? (
        <FileUpload onUploadSuccess={handleUploadSuccess} />
      ) : (
        <div className="max-w-6xl mx-auto bg-white p-8 rounded-xl shadow-lg border">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Analysis Complete: {currentDocument.filename}</h2>
            <button 
              onClick={handleReset}
              className="text-sm font-medium bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded transition"
            >
              Upload New File
            </button>
          </div>
          
          {currentDocument.file_type === 'media' && (
            <div className="mb-6 p-4 bg-gray-100 rounded-lg border">
              <h3 className="font-semibold text-gray-700 mb-2"> AI Summary:</h3>
              <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
                {currentDocument.summary}
              </p>
            </div>
          )}
          
          <MediaChat document={currentDocument} fileUrl={localFileUrl} />
        </div>
      )}
    </div>
  );
}