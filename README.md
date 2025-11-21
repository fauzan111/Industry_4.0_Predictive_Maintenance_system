# Industry 4.0 Predictive Maintenance System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2.svg)](https://mlflow.org/)

An end-to-end MLOps pipeline for predicting the Remaining Useful Life (RUL) of turbofan engines using the NASA CMAPSS dataset. Features experiment tracking, model serving, drift detection, and a modern React dashboard.

![Dashboard](https://via.placeholder.com/800x400?text=Industry+4.0+Dashboard)

## 🎯 Project Overview

This project demonstrates a complete predictive maintenance solution suitable for automotive and industrial applications. It predicts when turbofan engines will fail, enabling proactive maintenance scheduling and reducing unplanned downtime.

### Key Features

- 🤖 **Machine Learning**: Random Forest model achieving ~52 cycles RMSE
- 📊 **Experiment Tracking**: MLflow for model versioning and comparison
- 🚀 **Model Serving**: FastAPI REST API with interactive documentation
- 🎨 **Web Dashboard**: Modern React UI with real-time predictions
- 📈 **Data Visualization**: Charts and gauges for insights
- 🔍 **Drift Detection**: Alibi Detect for monitoring data quality
- 🔄 **Orchestration**: Prefect workflows for automation
- 🐳 **Containerization**: Docker Compose for one-command deployment

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI    │────▶│   ML Model  │
│  Dashboard  │     │   Backend    │     │  (Random    │
│             │     │              │     │   Forest)   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   MLflow     │
                    │  Tracking    │
                    └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- (Optional) Python 3.9+ for local development

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/fauzan111/Industry_4.0_Predictive_Maintenance_system.git
cd Industry_4.0_Predictive_Maintenance_system
```

## 📖 Usage

### Training a Model

```bash
# Inside Docker container
docker exec -it industry40-app-1 python src/models/train.py

# With custom parameters
docker exec -it industry40-app-1 python src/models/train.py --n_estimators 200 --max_depth 20
```

### Making Predictions

**Via Web Dashboard:**
1. Open http://localhost:5173
2. Click "Load Example" to populate sensor data
3. Click "Predict RUL"
4. View the predicted remaining useful life

**Via API:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "setting_1": 0.5, "setting_2": 0.3, "setting_3": 0.2,
    "s_2": 0.7, "s_3": 0.6, "s_4": 0.8, "s_6": 0.5,
    "s_7": 0.4, "s_8": 0.6, "s_9": 0.7, "s_11": 0.5,
    "s_12": 0.6, "s_13": 0.7, "s_14": 0.8, "s_15": 0.5,
    "s_17": 0.6, "s_20": 0.7, "s_21": 0.8
  }'
```

### Running the Complete Pipeline

```bash
docker exec -it industry40-app-1 python src/pipelines/training_pipeline.py
```

## 📁 Project Structure

```
Industry_4.0_Predictive_Maintenance_system/
├── data/                      # Data storage
│   ├── raw/                   # Raw NASA CMAPSS data
│   └── processed/             # Processed datasets
├── frontend/                  # React dashboard
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API integration
│   │   └── App.jsx           # Main application
│   ├── Dockerfile            # Frontend container
│   └── package.json          # Dependencies
├── notebooks/                 # Jupyter notebooks for EDA
├── src/
│   ├── data/                 # Data processing scripts
│   ├── models/               # Model training
│   ├── pipelines/            # Prefect workflows
│   ├── serving/              # FastAPI application
│   └── drift/                # Drift detection
├── models/                   # Saved models
├── docker-compose.yml        # Service orchestration
├── Dockerfile               # Backend container
└── requirements.txt         # Python dependencies
```

## 🛠️ Technology Stack

### Backend
- **Python 3.9+**
- **FastAPI**: REST API framework
- **Scikit-learn**: Machine learning
- **MLflow**: Experiment tracking
- **Prefect**: Workflow orchestration
- **Alibi Detect**: Drift detection

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Recharts**: Data visualization
- **Axios**: HTTP client

### Infrastructure
- **Docker & Docker Compose**: Containerization
- **PostgreSQL**: MLflow backend
- **MinIO**: S3-compatible object storage
- **Nginx**: Frontend serving

## 📊 Model Performance

- **RMSE**: ~52 cycles
- **R² Score**: 0.21
- **Dataset**: NASA CMAPSS FD001 (20,631 training samples)
- **Features**: 18 sensor readings + 3 operational settings

## 🔬 Development

### Local Development

**Backend:**
```bash
pip install -r requirements.txt
python src/serving/app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Train and test model
docker exec -it industry40-app-1 python test_train.py

# Test drift detection
docker exec -it industry40-app-1 python src/drift/detector.py
```

## 📈 Future Enhancements

- [ ] LSTM/CNN models for time-series patterns
- [ ] Automated retraining pipeline
- [ ] A/B testing for model versions
- [ ] Real-time alerting system
- [ ] Multi-engine fleet monitoring
- [ ] Mobile application

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Fauzan Ejaz**
- GitHub: [@fauzan111](https://github.com/fauzan111)

## 🙏 Acknowledgments

- NASA for the CMAPSS dataset
- Open source community for the amazing tools and libraries

## 📧 Contact

For questions or collaboration opportunities, please open an issue or reach out via GitHub or Email me here- ejazfauzan14@gmail.com.

---

⭐ If you find this project useful, please consider giving it a star!
