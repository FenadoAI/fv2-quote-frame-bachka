import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Download, RefreshCw, Quote, User } from "lucide-react";

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API = `${API_BASE}/api`;

const QuoteGenerator = () => {
  const [people, setPeople] = useState([]);
  const [selectedPersonId, setSelectedPersonId] = useState("");
  const [currentQuote, setCurrentQuote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const canvasRef = useRef(null);

  // Fetch famous people on component mount
  useEffect(() => {
    fetchPeople();
  }, []);

  // Generate a quote when person is selected
  useEffect(() => {
    if (selectedPersonId) {
      generateRandomQuote();
    }
  }, [selectedPersonId]);

  const fetchPeople = async () => {
    try {
      const response = await axios.get(`${API}/people`);
      setPeople(response.data);
    } catch (err) {
      console.error("Error fetching people:", err);
      setError("Failed to load famous people");
    }
  };

  const generateRandomQuote = async () => {
    if (!selectedPersonId) return;

    setLoading(true);
    setError("");

    try {
      const response = await axios.get(`${API}/quotes/random?person_id=${selectedPersonId}`);
      setCurrentQuote(response.data);
    } catch (err) {
      console.error("Error fetching quote:", err);
      setError("Failed to load quote");
    } finally {
      setLoading(false);
    }
  };

  const generateQuoteImage = () => {
    if (!currentQuote || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // Set canvas size
    canvas.width = 800;
    canvas.height = 600;

    // Create gradient background
    const gradient = ctx.createLinearGradient(0, 0, 800, 600);
    gradient.addColorStop(0, '#667eea');
    gradient.addColorStop(1, '#764ba2');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 800, 600);

    // Set text properties
    ctx.fillStyle = 'white';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Draw quote text
    ctx.font = 'bold 32px serif';
    const maxWidth = 700;
    const lineHeight = 45;
    const x = 400;
    let y = 250;

    // Wrap text
    const words = currentQuote.text.split(' ');
    let line = '';
    const lines = [];

    for (let n = 0; n < words.length; n++) {
      const testLine = line + words[n] + ' ';
      const metrics = ctx.measureText(testLine);
      const testWidth = metrics.width;
      if (testWidth > maxWidth && n > 0) {
        lines.push(line);
        line = words[n] + ' ';
      } else {
        line = testLine;
      }
    }
    lines.push(line);

    // Draw each line
    lines.forEach((line, index) => {
      ctx.fillText(line, x, y + (index * lineHeight));
    });

    // Draw author name
    ctx.font = 'italic 24px serif';
    ctx.fillText(`— ${currentQuote.person_name}`, x, y + lines.length * lineHeight + 60);

    // Draw quote marks
    ctx.font = 'bold 60px serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.fillText('"', 120, 180);
    ctx.fillText('"', 680, 420);
  };

  const downloadImage = () => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const link = document.createElement('a');
    link.download = `quote-${currentQuote.person_name.replace(/\s+/g, '-').toLowerCase()}.png`;
    link.href = canvas.toDataURL();
    link.click();
  };

  const selectedPerson = people.find(p => p.id === selectedPersonId);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Quote Generator
          </h1>
          <p className="text-gray-600">
            Generate beautiful, shareable quotes from famous people
          </p>
        </div>

        {/* Person Selector */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Select a Famous Person
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Select value={selectedPersonId} onValueChange={setSelectedPersonId}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Choose a famous person..." />
              </SelectTrigger>
              <SelectContent>
                {people.map((person) => (
                  <SelectItem key={person.id} value={person.id}>
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{person.name}</span>
                      <span className="text-gray-500 text-sm">
                        {person.description}
                      </span>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </CardContent>
        </Card>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* Current Quote Display */}
        {currentQuote && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Quote className="h-5 w-5" />
                Current Quote
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-gradient-to-r from-blue-100 to-purple-100 rounded-lg p-6">
                <blockquote className="text-xl italic text-gray-800 mb-4">
                  "{currentQuote.text}"
                </blockquote>
                <div className="flex items-center gap-3">
                  {selectedPerson?.image_url && (
                    <img
                      src={selectedPerson.image_url}
                      alt={currentQuote.person_name}
                      className="w-12 h-12 rounded-full object-cover"
                    />
                  )}
                  <div>
                    <p className="font-semibold text-gray-800">
                      — {currentQuote.person_name}
                    </p>
                    <p className="text-sm text-gray-600">
                      {currentQuote.person_description}
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 justify-center">
                <Button
                  onClick={generateRandomQuote}
                  disabled={loading}
                  variant="outline"
                >
                  <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                  {loading ? 'Loading...' : 'New Quote'}
                </Button>
                <Button
                  onClick={() => {
                    generateQuoteImage();
                    setTimeout(() => {
                      downloadImage();
                    }, 100);
                  }}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download Image
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Canvas for Image Generation (Hidden) */}
        <canvas
          ref={canvasRef}
          className="hidden"
          width="800"
          height="600"
        />

        {/* Preview */}
        {currentQuote && (
          <Card>
            <CardHeader>
              <CardTitle>Preview</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg p-8 text-white text-center">
                <div className="text-3xl font-bold mb-4 leading-relaxed">
                  "{currentQuote.text}"
                </div>
                <div className="text-xl italic">
                  — {currentQuote.person_name}
                </div>
              </div>
              <p className="text-center text-gray-500 text-sm mt-2">
                This is how your downloaded image will look
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default QuoteGenerator;