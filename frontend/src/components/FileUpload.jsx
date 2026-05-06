import React, { useState } from 'react';
import axios from 'axios';
import { UploadCloud, Loader2 } from 'lucide-react';
import { useAuth } from '@clerk/clerk-react';

export default function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const { userId } = useAuth();

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId); 

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/upload/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      const fileUrl = URL.createObjectURL(file);
      onUploadSuccess(response.data, fileUrl);
    } catch (error) {
      console.error("Upload failed:", error);
      
      if (error.response && error.response.data && error.response.data.detail) {
        alert(error.response.data.detail);
      } else {
        alert("Failed to upload file. Make sure your backend is running!");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-20 p-8 bg-white rounded-xl shadow-lg border border-gray-100">
      <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Upload Document or Media</h2>
      <form onSubmit={handleUpload} className="space-y-6">
        <div className="border-2 border-dashed border-gray-300 rounded-xl p-10 text-center hover:bg-gray-50 transition cursor-pointer relative">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            accept="audio/*,video/*,.pdf"
            required
          />
          <div className="flex flex-col items-center justify-center space-y-3 pointer-events-none">
            <UploadCloud className="w-12 h-12 text-blue-500" />
            {file ? (
              <span className="text-gray-800 font-medium bg-blue-100 px-3 py-1 rounded-full">{file.name}</span>
            ) : (
              <>
                <span className="text-gray-600 font-medium">Click to browse or drag and drop</span>
                <span className="text-sm text-gray-400">Supports PDF, MP3, MP4, WAV</span>
              </>
            )}
          </div>
        </div>
        <button
          type="submit"
          disabled={!file || loading}
          className="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition flex justify-center items-center gap-2"
        >
          {loading ? <><Loader2 className="w-5 h-5 animate-spin" /> Processing AI Analysis...</> : 'Analyze File'}
        </button>
      </form>
    </div>
  );
}