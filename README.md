# 🛡️ DataBreach Monitor

A comprehensive full-stack platform for monitoring data breaches across deep web marketplaces, forums, and Telegram channels with real-time alerting capabilities.

## 🚀 Features

### Core Monitoring
- **Deep Web Monitoring** - Monitor marketplaces, forums, and darknet sites
- **Telegram Integration** - Track public and private channels/groups
- **Real-time Alerts** - Multi-channel notifications (Email, SMS, Slack, Telegram)
- **AI-Powered Analysis** - Threat classification using advanced ML models
- **Comprehensive Dashboard** - React-based interface with real-time updates

### Advanced Capabilities
- **Tor Network Support** - Secure access to .onion sites
- **Authentication Handling** - Automated login for protected sources
- **CAPTCHA Solving** - Integration with 2captcha and Anti-Captcha services
- **Session Management** - Persistent authentication across crawling sessions
- **Keyword Monitoring** - Configurable keyword alerts and filtering
- **Threat Classification** - Automatic risk assessment and categorization

## 🏗️ Architecture

```
Frontend (React) ↔ WebSocket ↔ Backend (FastAPI)
                                    ↓
                [Authentication Manager] → Marketplace Credentials
                                    ↓
                [Crawl4AI + Tor + Selenium] → Deep Web Sources
                                    ↓
                [Telegram Clients Pool] → Telegram Channels/Groups
                                    ↓
                [AI Analysis Pipeline] → Threat Analysis
                                    ↓
                [PostgreSQL + Redis] → Data Storage
                                    ↓
                [Alert Engine] → Multi-channel Notifications
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL + Redis
- **AI/ML**: Transformers, PyTorch
- **Web Scraping**: Crawl4AI, Selenium
- **Network**: Tor/STEM, Proxy chains
- **Telegram**: Telethon, Pyrogram
- **Authentication**: JWT, OAuth2

### Frontend
- **Framework**: React 18
- **UI Library**: Tailwind CSS
- **State Management**: React Query
- **Real-time**: WebSocket
- **Charts**: Recharts
- **Routing**: React Router

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **Monitoring**: Prometheus, Grafana
- **Deployment**: Kubernetes ready

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone the Repository
```bash
git clone https://github.com/youssef-mundia/DataBreach.git
cd DataBreach
```

### 2. Environment Setup
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit environment variables
nano backend/.env
```

### 3. Start with Docker Compose
```bash
# Run setup script (Linux/Mac)
./scripts/setup-dev.sh

# Or manually start services
docker-compose up -d --build
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 5. Default Login
- **Username**: `admin`
- **Password**: `admin123`

## 📊 Configuration

### Environment Variables

```env
# Application
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=databreach
POSTGRES_PASSWORD=databreach123
POSTGRES_DB=databreach

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Telegram (Optional)
TELEGRAM_API_ID=your-telegram-api-id
TELEGRAM_API_HASH=your-telegram-api-hash
TELEGRAM_BOT_TOKEN=your-bot-token

# AI/ML (Optional)
HUGGINGFACE_TOKEN=your-huggingface-token

# CAPTCHA Services (Optional)
TWOCAPTCHA_API_KEY=your-2captcha-key
ANTICAPTCHA_API_KEY=your-anticaptcha-key
```

### Adding Monitoring Sources

1. Navigate to the **Sources** page
2. Click **Add Source**
3. Configure:
   - **Name**: Descriptive name for the source
   - **Type**: deep_web, telegram, forum, or marketplace
   - **URL**: Source URL or Telegram channel (@channel_name)
   - **Keywords**: Comma-separated monitoring keywords

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## 🔐 Security Features

- **Encrypted Storage** - All credentials and sensitive data encrypted
- **JWT Authentication** - Secure API access with token-based auth
- **Rate Limiting** - Built-in protection against abuse
- **CORS Protection** - Configurable cross-origin resource sharing
- **Input Validation** - Comprehensive data validation and sanitization
- **Audit Logging** - Complete audit trail of all activities

## 📡 Monitoring Sources

### Supported Source Types
- **Deep Web Marketplaces** - AlphaBay-style, Empire-style markets
- **Forums** - phpBB, vBulletin, custom forums
- **Telegram Channels** - Public and private channels/groups
- **Dark Web Forums** - Specialized breach discussion forums

### Authentication Support
- **Multi-step Registration** - Automated account creation
- **CAPTCHA Solving** - Integrated solving services
- **Session Persistence** - Maintain authentication across sessions
- **Credential Rotation** - Automatic credential management

## 🚨 Alert System

### Alert Channels
- **Email** - SMTP-based email notifications
- **SMS** - Text message alerts
- **Slack** - Webhook-based Slack notifications
- **Telegram** - Bot-based notifications
- **Webhooks** - Custom webhook endpoints

### Alert Prioritization
- **Critical** - Immediate notification (verified breaches)
- **High** - Within 15 minutes (high-confidence matches)
- **Medium** - Within 1 hour (potential matches)
- **Low** - Daily digest (low-priority items)

## 🤖 AI Integration

### Threat Analysis
- **Content Classification** - Automatic threat categorization
- **Confidence Scoring** - ML-based confidence assessment
- **Pattern Recognition** - Identify common breach patterns
- **Sentiment Analysis** - Assess threat severity
- **False Positive Reduction** - Intelligent filtering

### Supported Models
- **Llama 3.3** - Advanced language understanding
- **Custom Models** - Domain-specific threat detection
- **Ensemble Methods** - Multiple model consensus

## 📈 Monitoring & Analytics

### Metrics Dashboard
- **Source Status** - Real-time monitoring of all sources
- **Breach Statistics** - Comprehensive breach analytics
- **Alert Performance** - Alert delivery and response metrics
- **System Health** - Infrastructure monitoring

### Reporting
- **Automated Reports** - Scheduled PDF/Excel reports
- **Custom Analytics** - Configurable metrics and KPIs
- **Export Capabilities** - Data export in multiple formats

## 🛡️ Legal & Compliance

### Data Protection
- **GDPR Compliance** - European data protection compliance
- **Data Retention** - Configurable retention policies
- **Anonymization** - Automatic PII anonymization
- **Audit Trails** - Complete data access logging

### Ethical Considerations
- **Responsible Disclosure** - Ethical breach reporting
- **Legal Compliance** - Adherence to local cybersecurity laws
- **Privacy Protection** - User privacy safeguards
- **Consent Management** - Proper consent handling

## 🚀 Deployment

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n databreach
```

## 📚 API Documentation

### Authentication
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use token in subsequent requests
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/v1/sources"
```

### Core Endpoints
- `GET /api/v1/sources` - List monitoring sources
- `POST /api/v1/sources` - Create new source
- `GET /api/v1/breaches` - List detected breaches
- `GET /api/v1/alerts` - List alerts
- `GET /api/v1/health` - System health check

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is intended for legitimate cybersecurity research and monitoring purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations in their jurisdiction.

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/youssef-mundia/DataBreach/wiki)
- **Issues**: [GitHub Issues](https://github.com/youssef-mundia/DataBreach/issues)
- **Discussions**: [GitHub Discussions](https://github.com/youssef-mundia/DataBreach/discussions)

---

**⚡ DataBreach Monitor - Protecting organizations through proactive threat intelligence**