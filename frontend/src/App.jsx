import { useState } from 'react';
import { Factory, Github, ExternalLink } from 'lucide-react';
import PredictionForm from './components/PredictionForm';
import ResultsDisplay from './components/ResultsDisplay';
import PredictionHistory from './components/PredictionHistory';
import { predictRUL } from './services/api';
import './index.css';

function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handlePredict = async (sensorData) => {
    setLoading(true);
    setError(null);

    try {
      const prediction = await predictRUL(sensorData);
      setResult(prediction);

      // Add to history
      setHistory(prev => [...prev, {
        ...prediction,
        timestamp: new Date().toISOString(),
      }]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get prediction. Please check if the API is running.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Factory size={48} className="text-white" />
            <h1 className="text-5xl font-bold text-white">
              Industry 4.0
            </h1>
          </div>
          <p className="text-xl text-white/90 mb-2">
            Predictive Maintenance Dashboard
          </p>
          <p className="text-white/75">
            Turbofan Engine Remaining Useful Life Prediction
          </p>

          {/* Links */}
          <div className="flex items-center justify-center gap-4 mt-6">
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-all"
            >
              <ExternalLink size={18} />
              API Docs
            </a>
            <a
              href="http://localhost:5000"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-all"
            >
              <ExternalLink size={18} />
              MLflow
            </a>
          </div>
        </header>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Left Column */}
          <div>
            <PredictionForm onPredict={handlePredict} loading={loading} />
          </div>

          {/* Right Column */}
          <div className="space-y-8">
            <ResultsDisplay result={result} error={error} />
            <PredictionHistory history={history} />
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center text-white/75 mt-12">
          <p className="flex items-center justify-center gap-2">
            Built with React, FastAPI, MLflow & Docker
            <Github size={18} />
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
