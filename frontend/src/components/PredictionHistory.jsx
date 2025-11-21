import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { History, TrendingDown } from 'lucide-react';

const PredictionHistory = ({ history }) => {
    if (history.length === 0) {
        return (
            <div className="card">
                <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <History className="text-primary-600" />
                    Prediction History
                </h2>
                <div className="text-center text-gray-500 py-8">
                    <p>No predictions yet</p>
                </div>
            </div>
        );
    }

    const chartData = history.map((item, index) => ({
        name: `#${index + 1}`,
        RUL: item.RUL,
        timestamp: new Date(item.timestamp).toLocaleTimeString(),
    }));

    const avgRUL = (history.reduce((sum, item) => sum + item.RUL, 0) / history.length).toFixed(1);

    return (
        <div className="card">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                    <History className="text-primary-600" />
                    Prediction History
                </h2>
                <div className="text-right">
                    <div className="text-sm text-gray-600">Average RUL</div>
                    <div className="text-2xl font-bold text-primary-600">{avgRUL}</div>
                </div>
            </div>

            {/* Chart */}
            <div className="mb-6">
                <ResponsiveContainer width="100%" height={200}>
                    <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="RUL" stroke="#2563eb" strokeWidth={2} />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {/* History List */}
            <div className="space-y-2 max-h-64 overflow-y-auto">
                {history.slice().reverse().map((item, index) => (
                    <div
                        key={index}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <div className="flex items-center gap-3">
                            <TrendingDown size={18} className="text-primary-600" />
                            <div>
                                <div className="font-semibold text-gray-800">{item.RUL.toFixed(1)} cycles</div>
                                <div className="text-xs text-gray-500">{new Date(item.timestamp).toLocaleString()}</div>
                            </div>
                        </div>
                        <div className={`px-3 py-1 rounded-full text-xs font-semibold ${item.RUL > 150 ? 'bg-green-200 text-green-800' :
                                item.RUL > 75 ? 'bg-yellow-200 text-yellow-800' :
                                    'bg-red-200 text-red-800'
                            }`}>
                            {item.RUL > 150 ? 'Healthy' : item.RUL > 75 ? 'Monitor' : 'Critical'}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PredictionHistory;
