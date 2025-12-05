import { useState } from 'react';
import { Presentation, Sparkles, LogOut, FileText, Layers, Download, Loader2 } from 'lucide-react';
import { api } from '../api';

interface GeneratePPTPageProps {
  onLogout: () => void;
  authToken: string;
}

export function GeneratePPTPage({ onLogout, authToken }: GeneratePPTPageProps) {
  const [topic, setTopic] = useState('');
  const [slideCount, setSlideCount] = useState(10);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedFile, setGeneratedFile] = useState<string | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [error, setError] = useState('');

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    setGeneratedFile(null);
    setDownloadUrl(null);
    setError('');

    try {
      const blob = await api.generatePPT({ topic, slide: slideCount }, authToken);
      const url = URL.createObjectURL(blob);
      const filename = `${topic.replace(/\s+/g, '_')}_presentation.pptx`;
      setGeneratedFile(filename);
      setDownloadUrl(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Generation failed');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = () => {
    if (downloadUrl && generatedFile) {
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = generatedFile;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  const handleNewPresentation = () => {
    setTopic('');
    setSlideCount(10);
    setGeneratedFile(null);
    setDownloadUrl(null);
    setError('');
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center">
                <Presentation className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-gray-900">PPT Generator</h1>
                <p className="text-gray-600">Create presentations with AI</p>
              </div>
            </div>
            <button
              onClick={onLogout}
              className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <LogOut className="w-5 h-5" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-3xl mb-6">
            <Sparkles className="w-10 h-10 text-indigo-600" />
          </div>
          <h2 className="text-gray-900 mb-4">Create Your Presentation</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Enter a topic and let our AI generate a professional PowerPoint presentation for you in seconds
          </p>
        </div>

        {/* Generation Form */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 mb-8">
          <form onSubmit={handleGenerate} className="space-y-6">
            {/* Topic Input */}
            <div>
              <label htmlFor="topic" className="flex items-center gap-2 text-gray-700 mb-3">
                <FileText className="w-5 h-5 text-indigo-600" />
                <span>Presentation Topic</span>
              </label>
              <input
                id="topic"
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., Introduction to Machine Learning"
                required
                disabled={isGenerating}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all disabled:bg-gray-50 disabled:cursor-not-allowed"
              />
              <p className="mt-2 text-gray-500">
                Be specific for better results
              </p>
            </div>

            {/* Slide Count */}
            <div>
              <label htmlFor="slideCount" className="flex items-center gap-2 text-gray-700 mb-3">
                <Layers className="w-5 h-5 text-indigo-600" />
                <span>Number of Slides</span>
              </label>
              <div className="flex items-center gap-4">
                <input
                  id="slideCount"
                  type="range"
                  min="5"
                  max="30"
                  step="1"
                  value={slideCount}
                  onChange={(e) => setSlideCount(Number(e.target.value))}
                  disabled={isGenerating}
                  className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                />
                <div className="w-16 text-center px-3 py-2 bg-indigo-50 text-indigo-700 rounded-lg">
                  {slideCount}
                </div>
              </div>
              <p className="mt-2 text-gray-500">
                Recommended: 10-15 slides for optimal presentation length
              </p>
            </div>

            {/* Generate Button */}
            <button
              type="submit"
              disabled={isGenerating}
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Generating your presentation...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  <span>Generate Presentation</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-8">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
                <FileText className="w-6 h-6 text-red-600" />
              </div>
              <div className="flex-1">
                <h3 className="text-gray-900 mb-2">Generation Failed</h3>
                <p className="text-gray-600">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Generation Progress */}
        {isGenerating && (
          <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-6">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Loader2 className="w-6 h-6 text-indigo-600 animate-spin" />
              </div>
              <div className="flex-1">
                <h3 className="text-gray-900 mb-2">Creating your presentation</h3>
                <p className="text-gray-600 mb-4">
                  Our AI is generating {slideCount} slides about "{topic}". This may take a few moments...
                </p>
                <div className="w-full bg-indigo-200 rounded-full h-2 overflow-hidden">
                  <div className="h-full bg-indigo-600 rounded-full animate-pulse" style={{ width: '70%' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Success State */}
        {generatedFile && !isGenerating && (
          <div className="bg-green-50 border border-green-200 rounded-xl p-6">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <FileText className="w-6 h-6 text-green-600" />
              </div>
              <div className="flex-1">
                <h3 className="text-gray-900 mb-2">Presentation Ready!</h3>
                <p className="text-gray-600 mb-4">
                  Your presentation "{generatedFile}" has been generated successfully with {slideCount} slides.
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={handleDownload}
                    className="flex items-center gap-2 px-5 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-md hover:shadow-lg"
                  >
                    <Download className="w-5 h-5" />
                    <span>Download PPTX</span>
                  </button>
                  <button
                    onClick={handleNewPresentation}
                    className="flex items-center gap-2 px-5 py-2.5 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <Sparkles className="w-5 h-5" />
                    <span>Create Another</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Features Grid */}
        {!isGenerating && !generatedFile && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
              <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                <Sparkles className="w-6 h-6 text-indigo-600" />
              </div>
              <h3 className="text-gray-900 mb-2">AI-Powered</h3>
              <p className="text-gray-600">
                Advanced AI generates relevant content for your topic
              </p>
            </div>
            <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <Layers className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="text-gray-900 mb-2">Customizable</h3>
              <p className="text-gray-600">
                Choose the number of slides that fit your needs
              </p>
            </div>
            <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
              <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
                <Download className="w-6 h-6 text-pink-600" />
              </div>
              <h3 className="text-gray-900 mb-2">Instant Download</h3>
              <p className="text-gray-600">
                Get your PPTX file ready to use immediately
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
