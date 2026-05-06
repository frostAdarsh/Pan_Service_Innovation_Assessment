import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Database, FileText, Video, Calendar, Tag, Trash2 } from 'lucide-react';
import { useAuth } from '@clerk/clerk-react';

export default function MetadataDashboard() {
  const { userId } = useAuth();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!userId) return; 

    const fetchHistory = async () => {
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/documents/${userId}`);
        setDocuments(res.data);
      } catch (error) {
        console.error("Error fetching documents:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [userId]);

  const handleDelete = async (docId) => {
    if (!window.confirm("Are you sure you want to delete this document forever?")) return;

    try {
      await axios.delete(`${import.meta.env.VITE_API_URL}/api/v1/documents/${docId}`);
      setDocuments(documents.filter(doc => doc.id !== docId));
    } catch (error) {
      console.error("Error deleting document:", error);
      alert("Failed to delete document.");
    }
  };

  if (loading) {
    return <div className="text-center mt-20 text-gray-500 text-xl animate-pulse">Loading Metadata...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex items-center gap-3 mb-8">
        <Database className="w-8 h-8 text-blue-600" />
        <h2 className="text-3xl font-bold text-gray-800">Metadata & Keywords Dashboard</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {documents.map((doc) => (
          <div key={doc.id} className="bg-white rounded-xl shadow-sm border p-5 hover:shadow-md transition relative group">
            
            <button 
              onClick={() => handleDelete(doc.id)}
              className="absolute top-4 right-4 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full transition"
              title="Delete Document"
            >
              <Trash2 className="w-5 h-5" />
            </button>

            <div className="flex items-start mb-4 pr-10">
              <div className="flex items-center gap-2 overflow-hidden">
                {doc.file_type === 'pdf' ? (
                  <FileText className="text-red-500 w-5 h-5 flex-shrink-0"/>
                ) : (
                  <Video className="text-blue-500 w-5 h-5 flex-shrink-0"/>
                )}
                <h3 className="font-bold text-gray-800 truncate" title={doc.filename}>{doc.filename}</h3>
              </div>
            </div>

            <div className="flex justify-between items-center mb-4">
              <div className="text-sm text-gray-500 flex items-center gap-1">
                <Calendar className="w-4 h-4" /> 
                {new Date(doc.upload_date).toLocaleDateString()}
              </div>
              <span className="text-xs font-medium bg-gray-100 text-gray-600 px-2 py-1 rounded">
                {doc.file_type.toUpperCase()}
              </span>
            </div>

            <div>
              <h4 className="text-xs font-bold text-gray-400 uppercase mb-2 flex items-center gap-1">
                <Tag className="w-3 h-3" /> Extracted Keywords
              </h4>
              <div className="flex flex-wrap gap-2">
                {doc.keywords && doc.keywords.length > 0 ? (
                  doc.keywords.map((kw, i) => (
                    <span key={i} className="text-xs bg-blue-50 text-blue-700 border border-blue-200 px-2 py-1 rounded-full">{kw}</span>
                  ))
                ) : (
                  <span className="text-xs text-gray-400 italic">No keywords extracted</span>
                )}
              </div>
            </div>

          </div>
        ))}
        
        {documents.length === 0 && (
          <div className="col-span-full text-center py-10 text-gray-500 bg-white border border-dashed rounded-xl">
            You haven't uploaded any documents yet.
          </div>
        )}
      </div>
    </div>
  );
}