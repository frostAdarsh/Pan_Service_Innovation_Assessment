import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Play, MessageSquare, Send, Loader2, Clock, FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function MediaChat({ document, fileUrl }) {
  const [messages, setMessages] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  
  const mediaRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleJumpToTime = (timeInSeconds) => {
    if (mediaRef.current) {
      const seconds = Number(timeInSeconds); 
      if (!isNaN(seconds)) {
        mediaRef.current.currentTime = seconds;
        mediaRef.current.play();
      }
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!currentQuestion.trim()) return;

    const newMessages = [...messages, { role: 'user', content: currentQuestion }];
    setMessages(newMessages);
    setCurrentQuestion("");
    setIsTyping(true);

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/chat/`, {
        document_id: document.id,
        question: currentQuestion
      });

      setMessages([...newMessages, { role: 'ai', content: response.data.answer }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages([...newMessages, { role: 'ai', content: "⚠️ Sorry, I encountered an error trying to answer that." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="mt-8 flex flex-col lg:flex-row gap-6 h-[600px]">
      
      {/* Left Column: Media Player OR Document Key Points */}
      <div className="w-full lg:w-1/2 flex flex-col bg-white border rounded-xl p-4 shadow-sm overflow-y-auto">
        <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
          {document.file_type === 'media' 
            ? <><Play className="w-5 h-5 text-blue-600" /> Media Viewer</>
            : <><FileText className="w-5 h-5 text-blue-600" /> Document Analysis</>}
        </h3>

        {document.file_type === 'media' ? (
          <video 
            ref={mediaRef} 
            controls 
            className="w-full rounded-lg bg-black mb-4 max-h-[300px]"
            src={fileUrl}
          >
            Your browser does not support the video tag.
          </video>
        ) : (
          /* --- UPDATED PDF VIEWER AREA --- */
          <div className="w-full flex-1 bg-blue-50/50 rounded-lg p-6 mb-4 border border-blue-100 overflow-y-auto">
            <div className="flex items-center gap-3 mb-4 border-b border-blue-200 pb-3">
              <FileText className="w-6 h-6 text-blue-600" />
              <h3 className="font-bold text-gray-800 text-lg">📄 Key Document Points</h3>
            </div>
            
            {/* Render the Key Points right inside the left panel */}
            <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
              {document.summary}
            </p>
          </div>
        )}

        {/* Timestamps (Only renders if they exist, which they won't for PDFs) */}
        {document.timestamps && document.timestamps.length > 0 && (
          <div className="mt-2">
            <h4 className="font-semibold text-gray-700 flex items-center gap-2 mb-3">
              <Clock className="w-4 h-4" /> Key Topics & Timestamps
            </h4>
            <div className="flex flex-wrap gap-2">
              {document.timestamps.map((ts, index) => (
                <button
                  key={index}
                  onClick={() => handleJumpToTime(ts.time)}
                  className="flex items-center gap-1 bg-blue-50 text-blue-700 hover:bg-blue-100 px-3 py-1.5 rounded-full text-sm font-medium transition-colors border border-blue-200"
                >
                  <Play className="w-3 h-3" /> {ts.topic} ({ts.time}s)
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Right Column: Chat Interface */}
      <div className="w-full lg:w-1/2 flex flex-col bg-white border rounded-xl shadow-sm overflow-hidden">
        <div className="bg-gray-50 border-b px-4 py-3 flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-green-600" />
          <h3 className="text-lg font-bold text-gray-800">Chat with AI</h3>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-400">
              <MessageSquare className="w-10 h-10 mb-2 opacity-50" />
              <p>Ask a question about the uploaded file!</p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div 
                key={index} 
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div 
                  className={`max-w-[85%] rounded-2xl px-4 py-2 ${
                    msg.role === 'user' 
                      ? 'bg-blue-600 text-white rounded-br-none' 
                      : 'bg-white border text-gray-800 rounded-bl-none shadow-sm'
                  }`}
                >
                  {msg.role === 'ai' ? (
                    <div className="prose prose-sm max-w-none">
                      <ReactMarkdown>
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            ))
          )}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-white border text-gray-500 rounded-2xl rounded-bl-none px-4 py-3 shadow-sm flex items-center gap-2 text-sm">
                <Loader2 className="w-4 h-4 animate-spin" /> AI is thinking...
              </div>
            </div>
          )}
          <div ref={chatEndRef} /> 
        </div>

        <form onSubmit={handleSendMessage} className="p-4 bg-white border-t flex gap-2">
          <input
            type="text"
            value={currentQuestion}
            onChange={(e) => setCurrentQuestion(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isTyping}
          />
          <button
            type="submit"
            disabled={isTyping || !currentQuestion.trim()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition flex items-center gap-2 font-medium"
          >
            <Send className="w-4 h-4" /> Send
          </button>
        </form>
      </div>

    </div>
  );
}