# Indus AI Backend

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-red.svg)

*An AI-powered platform for preserving and sharing traditional artisan stories and cultural heritage*

</div>

---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Data Models](#-data-models)
- [Testing](#-testing)
- [Security & Safety](#-security--safety)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Project Overview

Indus AI Backend is a Django REST API that serves as the backbone for a cultural heritage preservation platform. It combines the power of AI storytelling with structured data management to preserve and share the rich traditions of artisans and their crafts.

### 🎨 What Makes It Special

- **AI-Powered Storytelling**: Generate culturally authentic narratives using advanced language models
- **Cultural Heritage Preservation**: Structured approach to documenting traditional crafts and techniques  
- **Intelligent Mentorship Matching**: Connect experienced artisans with newcomers
- **Comprehensive Assessment Tools**: Evaluate and improve craft quality
- **Multi-Language Support**: Accommodate diverse linguistic communities

---

## ✨ Features

### 🤖 AI & Generation
- Multi-model AI support (Gemini, OpenAI, Hugging Face)
- Safety-first content filtering with prompt neutralization
- Intelligent retry logic with exponential backoff
- Cultural sensitivity awareness
- User guidance for optimal prompts

### 👥 Artisan Management
- Complete CRUD operations for artisan profiles
- Regional and linguistic categorization
- Approval workflow management
- Skill and expertise tracking

### 📊 Data Management
- RESTful API design with consistent patterns
- Real-time Firestore integration
- Flexible document structure
- Batch operations support

### 🛡️ Safety & Reliability
- Comprehensive error handling
- Rate limiting and quota management
- Input validation and sanitization
- Detailed logging and monitoring

---

## 🏗️ Architecture

```
indus_ai_backend/
├── 🎛️ indus_ai_backend/          # Django Project Core
│   ├── settings.py               # Configuration & Environment
│   ├── urls.py                   # Main URL Routing
│   └── wsgi.py                   # WSGI Application Entry
│
├── 🔌 api/                       # Core API Application  
│   ├── views.py                  # Business Logic & Endpoints
│   ├── urls.py                   # API URL Patterns
│   ├── firestore_client.py       # Database Abstraction Layer
│   └── templates/                # Development & Testing UI
│
├── 🎨 templates/                 # Global Template Directory
├── 📦 requirements.txt           # Python Dependencies
└── 🔐 .env.example              # Environment Configuration Template
```

### 🌐 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | Django 5.2.6 | Web framework and API foundation |
| **API** | Django REST Framework | RESTful API development |
| **Database** | Google Firestore | NoSQL document storage |
| **AI/ML** | Google Gemini AI | Primary story generation |
| **Fallback AI** | OpenAI GPT / Hugging Face | Backup generation models |
| **CORS** | django-cors-headers | Cross-origin request handling |

---

## 🚀 Quick Start

### 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Git** for version control
- **Google Cloud Account** with billing enabled
- **Text Editor/IDE** of your choice

### ⚡ Installation

1. **Clone & Navigate**
   ```bash
   git clone <repository-url>
   cd indus_ai_backend
   ```

2. **Virtual Environment Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Linux/Mac)
   source venv/bin/activate
   
   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Create `.env` file in project root:
   ```env
   # Required: AI Service
   GOOGLE_API_KEY=your_gemini_api_key_here
   
   # Required: Database
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/firestore-key.json
   
   # Optional: Fallback AI Services  
   OPENAI_API_KEY=your_openai_key_here
   HUGGINGFACE_API_KEY=your_huggingface_key_here
   
   # Optional: Development
   DEBUG=True
   ```

5. **Google Cloud Setup**
   
   - Create a [Google Cloud Project](https://console.cloud.google.com/)
   - Enable **Firestore in Native Mode**
   - Enable **Generative AI API**
   - Create a **Service Account** with Firestore permissions
   - Download the **JSON key file**
   - Update the path in your `.env` file

6. **Launch Server**
   ```bash
   python manage.py runserver
   ```

   🎉 **Success!** Your API is now running at `http://localhost:8000/api/`

### 🧪 Quick Test

Verify your setup with a simple test:

```bash
curl -X GET http://localhost:8000/api/
```

Expected response:
```json
{
  "message": "Indus AI Backend API",
  "version": "1.0.0",
  "status": "operational"
}
```

---

## 📚 API Documentation

### 🌍 Base Information

- **Base URL**: `http://localhost:8000/api/`
- **Content Type**: `application/json`
- **Authentication**: Not required (development mode)
- **Rate Limiting**: Not enforced (development mode)

---

### 🤖 AI Story Generation

#### Generate Story
Create AI-powered stories about artisans with cultural authenticity.

**Endpoint**: `POST /stories/generate/`

**Request Body**:
```json
{
  "prompt": "Write an inspiring story about a traditional weaver",
  "model": "gemini-1.5-flash"  // Optional
}
```

**Success Response** (200):
```json
{
  "story": "In the bustling lanes of a traditional marketplace, Meera's nimble fingers danced across the wooden loom...",
  "model_used": "gemini-1.5-flash",
  "prompt": "Write an inspiring story about a traditional weaver",
  "word_count": 285,
  "generation_time": "2.3s"
}
```

**Short Story Response** (200):
```json
{
  "story": "A brief tale of craftsmanship.",
  "model_used": "gemini-1.5-flash", 
  "guidance": {
    "message": "Story seems brief. Try these suggestions for richer content:",
    "suggestions": [
      "Add specific craft details (tools, techniques, materials)",
      "Include cultural context (festivals, traditions, family history)",
      "Describe the artisan's journey and challenges",
      "Mention the significance of their work to the community"
    ]
  }
}
```

**Error Response** (400):
```json
{
  "error": "Content blocked by safety filter",
  "details": "Prompt contains potentially sensitive cultural references",
  "suggestions": [
    "Use general terms instead of specific ethnic identifiers",
    "Focus on craft techniques rather than cultural practices",
    "Avoid religious or political references"
  ]
}
```

**Supported Models**:
- `gemini-1.5-flash` (default, fastest)
- `gemini-1.5-pro` (higher quality)
- `gpt-3.5-turbo` (fallback)
- `text-davinci-003` (fallback)

**Example Usage**:
```bash
curl -X POST http://localhost:8000/api/stories/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Tell a story about a master potter who teaches young apprentices the ancient techniques passed down through generations",
    "model": "gemini-1.5-pro"
  }'
```

---

### 👥 Artisan Management

#### Create Artisan Profile
Register a new artisan in the system.

**Endpoint**: `POST /artisans/create/`

**Request Body**:
```json
{
  "name": "Rajesh Kumar",
  "region": "Rajasthan, India",
  "languages": ["Hindi", "English", "Rajasthani"],
  "approval_status": "pending",
  "crafts": ["pottery", "ceramics"],
  "experience_years": 15,
  "contact_info": {
    "phone": "+91-9876543210",
    "email": "rajesh.potter@example.com"
  }
}
```

**Success Response** (201):
```json
{
  "id": "artisan_abc123def456",
  "message": "Artisan profile created successfully",
  "data": {
    "name": "Rajesh Kumar",
    "region": "Rajasthan, India",
    "languages": ["Hindi", "English", "Rajasthani"],
    "approval_status": "pending",
    "created_at": "2025-09-16T10:30:00Z"
  }
}
```

---

### 📊 CRUD Operations

All collections support full CRUD operations with consistent patterns.

#### Available Collections

| Collection | Endpoint | Description |
|------------|----------|-------------|
| **Assessments** | `/assessments/` | Craft quality evaluations |
| **Heritage Nodes** | `/heritage_nodes/` | Cultural knowledge base |
| **Mentorship Matches** | `/mentorship_matches/` | Mentor-artisan connections |
| **Products** | `/products/` | Artisan creations catalog |
| **Story Drafts** | `/story_drafts/` | Generated story management |

#### Standard HTTP Methods

| Method | Endpoint Pattern | Description |
|--------|------------------|-------------|
| `GET` | `/collection/` | List all items (with pagination) |
| `POST` | `/collection/` | Create new item |
| `GET` | `/collection/{id}/` | Retrieve specific item |
| `PUT` | `/collection/{id}/` | Complete update |
| `PATCH` | `/collection/{id}/` | Partial update |
| `DELETE` | `/collection/{id}/` | Delete item |

#### Example: Products API

**List Products** - `GET /api/products/`
```bash
curl -X GET http://localhost:8000/api/products/
```

Response:
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": "product_xyz789",
      "name": "Handwoven Banarasi Saree",
      "artisan_id": "artisan_abc123",
      "description": "Exquisite silk saree with traditional gold zari work",
      "media_urls": ["https://example.com/saree1.jpg"],
      "craft_tags": ["weaving", "textile", "silk"],
      "materials": ["silk", "gold_thread"],
      "price_range_suggestion": "₹15,000 - ₹25,000",
      "created_at": "2025-09-15T14:20:00Z"
    }
  ]
}
```

**Create Product** - `POST /api/products/`
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Traditional Madhubani Painting",
    "artisan_id": "artisan_def456", 
    "description": "Vibrant folk art depicting mythological themes",
    "media_urls": ["https://example.com/madhubani1.jpg"],
    "craft_tags": ["painting", "folk_art", "madhubani"],
    "materials": ["natural_pigments", "handmade_paper", "bamboo_brush"],
    "price_range_suggestion": "₹2,000 - ₹5,000"
  }'
```

**Update Product** - `PATCH /api/products/{id}/`
```bash
curl -X PATCH http://localhost:8000/api/products/product_xyz789/ \
  -H "Content-Type: application/json" \
  -d '{
    "price_range_suggestion": "₹18,000 - ₹28,000",
    "description": "Exquisite silk saree with traditional gold zari work, recently awarded at cultural festival"
  }'
```

---

## 🗄️ Data Models

### 👤 Artisan
```json
{
  "id": "string",
  "name": "string",
  "region": "string",
  "languages": ["string", ...],
  "approval_status": "pending|approved|rejected",
  "crafts": ["string", ...],
  "experience_years": "integer",
  "contact_info": {
    "phone": "string",
    "email": "string"
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 📋 Assessment
```json
{
  "id": "string",
  "product_id": "string",
  "assessor_id": "string",
  "criteria_scores": {
    "cultural_alignment": 8.5,
    "motif_accuracy": 9.0,
    "technique_preservation": 7.8,
    "innovation_balance": 8.2
  },
  "overall_score": 8.38,
  "feedback_text": "string",
  "before_image_url": "string",
  "after_image_url": "string",
  "assessment_date": "datetime",
  "recommendations": ["string", ...]
}
```

### 🏛️ Heritage Node
```json
{
  "id": "string",
  "craft": "string",
  "region": "string",
  "historical_period": "string",
  "techniques": ["string", ...],
  "motifs": ["string", ...],
  "cultural_significance": "string",
  "references": ["string", ...],
  "related_festivals": ["string", ...],
  "preservation_status": "thriving|declining|endangered|extinct"
}
```

### 🤝 Mentorship Match
```json
{
  "id": "string",
  "artisan_id": "string",
  "mentor_id": "string",
  "compatibility_score": 85.7,
  "match_criteria": {
    "craft_alignment": 90,
    "regional_proximity": 75,
    "language_compatibility": 95,
    "experience_gap": 80
  },
  "goals": ["skill_enhancement", "market_access", "cultural_preservation"],
  "status": "proposed|accepted|active|completed|terminated",
  "created_at": "datetime"
}
```

### 🛍️ Product
```json
{
  "id": "string",
  "name": "string",
  "artisan_id": "string",
  "description": "string",
  "media_urls": ["string", ...],
  "craft_tags": ["string", ...],
  "materials": ["string", ...],
  "dimensions": {
    "length": "string",
    "width": "string", 
    "height": "string",
    "weight": "string"
  },
  "price_range_suggestion": "string",
  "cultural_context": "string",
  "production_time": "string",
  "availability_status": "available|sold|reserved|discontinued"
}
```

### 📝 Story Draft
```json
{
  "id": "string",
  "artisan_id": "string",
  "title": "string",
  "draft_text": "string",
  "cultural_context": "string",
  "themes": ["string", ...],
  "status": "draft|review|approved|published|rejected",
  "generated_by": "ai|human|collaborative",
  "model_used": "string",
  "word_count": "integer",
  "created_at": "datetime",
  "publish_date": "datetime"
}
```

---

## 🧪 Testing

### 🎯 Test Endpoints

Access these endpoints for development and testing:

- **API Home**: `http://localhost:8000/api/`
- **Interactive Tests**: `http://localhost:8000/api/test/`
- **Collection Tests**: `http://localhost:8000/api/test_collections/`
- **AI Generation Test**: `http://localhost:8000/api/test/stories/`

### 🔧 Manual Testing Examples

**Test Story Generation**:
```bash
# Basic story generation
curl -X POST http://localhost:8000/api/stories/generate/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write about a master craftsperson teaching traditional techniques"}'

# Advanced story generation with specific model
curl -X POST http://localhost:8000/api/stories/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a narrative about a young apprentice learning the ancient art of metalwork from a seasoned artisan",
    "model": "gemini-1.5-pro"
  }'
```

**Test Artisan Creation**:
```bash
curl -X POST http://localhost:8000/api/artisans/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priya Sharma",
    "region": "Gujarat, India",
    "languages": ["Gujarati", "Hindi", "English"],
    "crafts": ["bandhani", "textile_dyeing"],
    "experience_years": 12
  }'
```

**Test Product Listing**:
```bash
# Get all products
curl -X GET http://localhost:8000/api/products/

# Get specific product
curl -X GET http://localhost:8000/api/products/{product_id}/

# Search products by craft
curl -X GET "http://localhost:8000/api/products/?craft_tags=pottery"
```

### ✅ Testing Checklist

Before deploying, verify:

- [ ] Story generation works with different prompts
- [ ] All CRUD operations function correctly
- [ ] Error handling responds appropriately
- [ ] Firestore connection is stable
- [ ] AI model fallbacks work when primary fails
- [ ] CORS is properly configured for your frontend
- [ ] Environment variables are properly loaded

---

## 🛡️ Security & Safety

### 🔒 AI Safety Features

**Content Filtering**:
- Automatic detection of sensitive cultural references
- Prompt neutralization for safety filter triggers  
- Multi-level content validation
- Real-time safety scoring

**Prompt Guidelines**:

✅ **Recommended Prompts**:
```json
{
  "good_examples": [
    "Write a story about a skilled craftsperson preserving traditional techniques",
    "Tell a tale of an artisan teaching apprentices the secrets of their craft",
    "Create a narrative about the dedication required to master an ancient art form",
    "Describe the journey of someone learning traditional metalwork"
  ]
}
```

❌ **Avoid These Patterns**:
```json
{
  "problematic_examples": [
    "Write about [specific ethnic group] artisans",
    "Tell a story about [specific religious] craft traditions", 
    "Create content about [political region] cultural practices",
    "Describe [sensitive historical period] artistic movements"
  ]
}
```

### 🚨 Error Handling

**HTTP Status Codes**:

| Code | Meaning | Common Causes |
|------|---------|---------------|
| `200` | Success | Request processed successfully |
| `201` | Created | New resource created |
| `400` | Bad Request | Invalid input, safety filter block |
| `401` | Unauthorized | Authentication required (production) |
| `404` | Not Found | Resource doesn't exist |
| `429` | Rate Limited | Too many requests |
| `500` | Server Error | Internal system error |
| `503` | Service Unavailable | AI service temporarily down |

**Error Response Format**:
```json
{
  "error": "Primary error description",
  "error_code": "SAFETY_FILTER_BLOCK",
  "details": "Detailed explanation of what went wrong",
  "suggestions": [
    "Use more general terms instead of specific identifiers",
    "Focus on craft techniques rather than cultural practices", 
    "Try rephrasing without sensitive references"
  ],
  "timestamp": "2025-09-16T10:30:00Z",
  "request_id": "req_abc123def456"
}
```

### 🔐 Production Security

**Essential Security Measures**:

1. **Environment Variables**:
   ```env
   DEBUG=False
   SECRET_KEY=your_super_secret_django_key_here
   ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
   ```

2. **Database Security**:
   - Firestore security rules
   - Service account with minimal permissions
   - Regular security audits

3. **API Security**:
   - Rate limiting implementation
   - Request size limits
   - Input validation and sanitization
   - CORS configuration for production domains

4. **Monitoring**:
   - Error logging and alerting
   - Performance monitoring
   - Security event tracking

---

## 🌐 Frontend Integration

### 🔗 CORS Configuration

Current development setup allows:
- `http://localhost:3000` (React default)
- `http://127.0.0.1:3000` (Alternative localhost)

For production, update `CORS_ALLOWED_ORIGINS` in `settings.py`.

### 💻 JavaScript Integration Examples

**Story Generation**:
```javascript
const generateStory = async (prompt, model = 'gemini-1.5-flash') => {
  try {
    const response = await fetch('http://localhost:8000/api/stories/generate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt, model })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Story generation failed:', error);
    throw error;
  }
};

// Usage
generateStory("Write about a traditional weaver")
  .then(result => {
    console.log("Generated story:", result.story);
    if (result.guidance) {
      console.log("Suggestions:", result.guidance.suggestions);
    }
  })
  .catch(error => {
    console.error("Error:", error);
  });
```

**Artisan Management**:
```javascript
const createArtisan = async (artisanData) => {
  try {
    const response = await fetch('http://localhost:8000/api/artisans/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(artisanData)
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to create artisan');
    }
    
    return data;
  } catch (error) {
    console.error('Artisan creation failed:', error);
    throw error;
  }
};

// Usage
const newArtisan = {
  name: "Maya Patel",
  region: "Gujarat, India", 
  languages: ["Gujarati", "Hindi", "English"],
  crafts: ["pottery", "ceramics"],
  experience_years: 8
};

createArtisan(newArtisan)
  .then(result => {
    console.log("Artisan created:", result.id);
  })
  .catch(error => {
    console.error("Error:", error);
  });
```

**Product Catalog**:
```javascript
const fetchProducts = async (filters = {}) => {
  const queryParams = new URLSearchParams(filters);
  
  try {
    const response = await fetch(`http://localhost:8000/api/products/?${queryParams}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch products:', error);
    throw error;
  }
};

// Usage
fetchProducts({ craft_tags: 'pottery', region: 'Rajasthan' })
  .then(result => {
    console.log("Products found:", result.count);
    console.log("Products:", result.results);
  })
  .catch(error => {
    console.error("Error:", error);
  });
```

### 📱 React Component Example

```jsx
import React, { useState } from 'react';

const StoryGenerator = () => {
  const [prompt, setPrompt] = useState('');
  const [story, setStory] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/stories/generate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt })
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate story');
      }
      
      setStory(data.story);
      
      if (data.guidance) {
        console.warn('Story guidance:', data.guidance);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="story-generator">
      <h2>AI Story Generator</h2>
      
      <div className="input-section">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe the story you'd like to generate about artisans..."
          rows={4}
          cols={50}
        />
        <button 
          onClick={handleGenerate} 
          disabled={loading || !prompt.trim()}
        >
          {loading ? 'Generating...' : 'Generate Story'}
        </button>
      </div>
      
      {error && (
        <div className="error">
          <p>Error: {error}</p>
        </div>
      )}
      
      {story && (
        <div className="story-output">
          <h3>Generated Story:</h3>
          <p>{story}</p>
        </div>
      )}
    </div>
  );
};

export default StoryGenerator;
```

---

## 🚀 Deployment

### 🌟 Production Readiness Checklist

**Security Configuration**:
- [ ] Set `DEBUG = False` in production settings
- [ ] Configure secure `SECRET_KEY`
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Implement authentication middleware
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper CORS origins

**Environment Setup**:
- [ ] All environment variables configured
- [ ] API keys secured and rotated regularly
- [ ] Database permissions properly scoped
- [ ] Service account security reviewed

**Performance & Monitoring**:
- [ ] Implement rate limiting
- [ ] Set up error logging (Sentry, CloudWatch)
- [ ] Configure performance monitoring
- [ ] Set up health check endpoints
- [ ] Configure auto-scaling if needed

### ☁️ Deployment Platforms

#### Google Cloud Run (Recommended)
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/indus-ai-backend
gcloud run deploy --image gcr.io/PROJECT-ID/indus-ai-backend --platform managed
```

**Benefits**:
- Native Firestore integration
- Auto-scaling
- Pay-per-request pricing
- Built-in security

#### Heroku
```bash
# Add buildpack and deploy
heroku buildpacks:add heroku/python
git push heroku main
```

#### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "indus_ai_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 🤝 Contributing

### 🛠️ Development Setup

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Install development dependencies**: `pip install -r requirements-dev.txt`
4. **Make your changes**
5. **Run tests**: `python manage.py test`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### 📝 Adding New Features

**New API Endpoints**:
1. Add view class in `api/views.py`
2. Add URL pattern in `api/urls.py`
3. Test using provided test interfaces
4. Update this documentation
5. Add tests for new functionality

**New AI Models**:
1. Update `valid_models` list in `StoryGenerateView`
2. Implement model-specific logic if needed
3. Test with various prompts
4. Update API documentation

### 🎯 Code Style

- Follow PEP 8 Python style guide
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Write comprehensive tests

---

## 🆘 Troubleshooting

### 🚨 Common Issues & Solutions

#### AI Generation Problems

**Issue**: Stories not generating or returning errors
```
"error": "API key not found or invalid"
```

**Solutions**:
1. Verify `GOOGLE_API_KEY` in `.env` file
2. Check API key permissions in Google Cloud Console
3. Ensure Generative AI API is enabled
4. Verify API quotas and billing

**Issue**: Content blocked by safety filter
```
"error": "Content blocked by safety filter"
```

**Solutions**:
1. Use more generic terms instead of specific cultural identifiers
2. Avoid political, religious, or sensitive regional references
3. Focus on craft techniques rather than cultural practices
4. Try rephrasing the prompt

#### Database Connection Issues

**Issue**: Firestore connection failing
```
"error": "Could not connect to Firestore"
```

**Solutions**:
1. Verify `GOOGLE_APPLICATION_CREDENTIALS` path is correct
2. Check service account has Firestore permissions
3. Ensure Firestore is enabled in Google Clou