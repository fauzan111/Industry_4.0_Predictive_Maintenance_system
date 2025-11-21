import { AlertCircle, CheckCircle, AlertTriangle } from 'lucide-react';

const ResultsDisplay = ({ result, error }) => {
    if (error) {
        return (
            <div className="card bg-red-50 border-2 border-red-200">
                <div className="flex items-center gap-3 text-red-700">
                    <AlertCircle size={24} />
                    <div>
                        <h3 className="font-semibold text-lg">Prediction Error</h3>
                        <p className="text-sm">{error}</p>
                    </div>
                </div>
            </div>
        );
    }

    if (!result) {
        return (
            <div className="card bg-gray-50 border-2 border-gray-200">
                <div className="text-center text-gray-500 py-8">
                    <p className="text-lg">No prediction yet</p>
                    <p className="text-sm mt-2">Enter sensor data and click "Predict RUL" to get started</p>
                </div>
            </div>
        );
    }

    const rul = result.RUL;
    const getStatus = (rul) => {
        if (rul > 150) return { color: 'green', text: 'Healthy', icon: CheckCircle };
        if (rul > 75) return { color: 'yellow', text: 'Monitor', icon: AlertTriangle };
        return { color: 'red', text: 'Critical', icon: AlertCircle };
    };

    const status = getStatus(rul);
    const StatusIcon = status.icon;

    const colorClasses = {
        green: 'bg-green-50 border-green-200 text-green-700',
        yellow: 'bg-yellow-50 border-yellow-200 text-yellow-700',
        red: 'bg-red-50 border-red-200 text-red-700',
    };

    const gaugePercentage = Math.min((rul / 300) * 100, 100);

    return (
        <div className={`card border-2 ${colorClasses[status.color]}`}>
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold flex items-center gap-2">
                    <StatusIcon size={28} />
                    Prediction Result
                </h2>
                <span className={`px-4 py-2 rounded-full font-semibold ${status.color === 'green' ? 'bg-green-200' :
                        status.color === 'yellow' ? 'bg-yellow-200' : 'bg-red-200'
                    }`}>
                    {status.text}
                </span>
            </div>

            <div className="text-center mb-6">
                <div className="text-6xl font-bold mb-2">
                    {rul.toFixed(1)}
                </div>
                <div className="text-xl text-gray-600">
                    Cycles Remaining
                </div>
            </div>

            {/* Visual Gauge */}
            <div className="mb-6">
                <div className="w-full bg-gray-200 rounded-full h-6 overflow-hidden">
                    <div
                        className={`h-full transition-all duration-500 ${status.color === 'green' ? 'bg-green-500' :
                                status.color === 'yellow' ? 'bg-yellow-500' : 'bg-red-500'
                            }`}
                        style={{ width: `${gaugePercentage}%` }}
                    ></div>
                </div>
                <div className="flex justify-between text-xs text-gray-600 mt-1">
                    <span>0</span>
                    <span>150</span>
                    <span>300+</span>
                </div>
            </div>

            {/* Recommendations */}
            <div className="bg-white bg-opacity-50 rounded-lg p-4">
                <h4 className="font-semibold mb-2">Recommendation:</h4>
                <p className="text-sm">
                    {rul > 150 && "Engine is in good condition. Continue normal operations and routine maintenance."}
                    {rul > 75 && rul <= 150 && "Engine showing signs of wear. Schedule inspection and monitor closely."}
                    {rul <= 75 && "Engine approaching failure. Plan immediate maintenance or replacement to avoid downtime."}
                </p>
            </div>
        </div>
    );
};

export default ResultsDisplay;
