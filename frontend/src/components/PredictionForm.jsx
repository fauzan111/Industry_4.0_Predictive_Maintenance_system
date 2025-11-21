import { useState } from 'react';
import { Activity, Settings, Gauge } from 'lucide-react';

const PredictionForm = ({ onPredict, loading }) => {
    const [formData, setFormData] = useState({
        setting_1: 0.5,
        setting_2: 0.3,
        setting_3: 0.2,
        s_2: 0.7,
        s_3: 0.6,
        s_4: 0.8,
        s_6: 0.5,
        s_7: 0.4,
        s_8: 0.6,
        s_9: 0.7,
        s_11: 0.5,
        s_12: 0.6,
        s_13: 0.7,
        s_14: 0.8,
        s_15: 0.5,
        s_17: 0.6,
        s_20: 0.7,
        s_21: 0.8,
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: parseFloat(value) || 0
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onPredict(formData);
    };

    const loadExample = () => {
        setFormData({
            setting_1: 0.5,
            setting_2: 0.3,
            setting_3: 0.2,
            s_2: 0.7,
            s_3: 0.6,
            s_4: 0.8,
            s_6: 0.5,
            s_7: 0.4,
            s_8: 0.6,
            s_9: 0.7,
            s_11: 0.5,
            s_12: 0.6,
            s_13: 0.7,
            s_14: 0.8,
            s_15: 0.5,
            s_17: 0.6,
            s_20: 0.7,
            s_21: 0.8,
        });
    };

    const settings = ['setting_1', 'setting_2', 'setting_3'];
    const sensors = ['s_2', 's_3', 's_4', 's_6', 's_7', 's_8', 's_9', 's_11', 's_12', 's_13', 's_14', 's_15', 's_17', 's_20', 's_21'];

    return (
        <form onSubmit={handleSubmit} className="card">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                    <Activity className="text-primary-600" />
                    Sensor Input
                </h2>
                <button
                    type="button"
                    onClick={loadExample}
                    className="btn-secondary text-sm"
                >
                    Load Example
                </button>
            </div>

            {/* Operational Settings */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center gap-2">
                    <Settings size={20} className="text-primary-600" />
                    Operational Settings
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {settings.map((setting) => (
                        <div key={setting}>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                {setting.replace('_', ' ').toUpperCase()}
                            </label>
                            <input
                                type="number"
                                name={setting}
                                value={formData[setting]}
                                onChange={handleChange}
                                step="0.01"
                                className="input-field"
                            />
                        </div>
                    ))}
                </div>
            </div>

            {/* Sensor Readings */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center gap-2">
                    <Gauge size={20} className="text-primary-600" />
                    Sensor Readings
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                    {sensors.map((sensor) => (
                        <div key={sensor}>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                {sensor.toUpperCase()}
                            </label>
                            <input
                                type="number"
                                name={sensor}
                                value={formData[sensor]}
                                onChange={handleChange}
                                step="0.01"
                                className="input-field"
                            />
                        </div>
                    ))}
                </div>
            </div>

            <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {loading ? (
                    <span className="flex items-center justify-center gap-2">
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Predicting...
                    </span>
                ) : (
                    'Predict RUL'
                )}
            </button>
        </form>
    );
};

export default PredictionForm;
