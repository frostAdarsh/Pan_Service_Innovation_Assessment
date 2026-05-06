import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import Home from './pages/Home';
import MetadataDashboard from './pages/MetadataDashboard';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
      <header className="bg-white shadow-sm border-b px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-6">
          <h1 className="text-xl font-bold text-blue-700 flex items-center gap-2"> DataTrack</h1>
          <SignedIn>
            <nav className="flex gap-4 ml-6 border-l pl-6 border-gray-200">
              <Link to="/" className="text-gray-600 hover:text-blue-600 font-medium transition">Upload & Chat</Link>
              <Link to="/metadata" className="text-gray-600 hover:text-blue-600 font-medium transition">Dashboard</Link>
            </nav>
          </SignedIn>
        </div>
        <div>
          <SignedOut>
            <div className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition font-medium">
              <SignInButton mode="modal" />
            </div>
          </SignedOut>
          <SignedIn>
            <UserButton afterSignOutUrl="/" />
          </SignedIn>
        </div>
      </header>

      <main className="p-6">
        <SignedOut>
          <div className="flex flex-col items-center justify-center mt-20 text-center">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Welcome to DataTrack</h2>
            <p className="text-gray-500 mb-6">Please sign in to upload documents and chat with the AI.</p>
            <div className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg hover:bg-blue-700 transition font-medium cursor-pointer">
              <SignInButton mode="modal" />
            </div>
          </div>
        </SignedOut>

        <SignedIn>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/metadata" element={<MetadataDashboard />} />
            <Route path="*" element={<div className="text-center mt-20 font-bold text-xl">404 - Page Not Found</div>} />
          </Routes>
        </SignedIn>
      </main>
    </div>
  );
}