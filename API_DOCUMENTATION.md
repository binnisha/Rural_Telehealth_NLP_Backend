# MediBridge API Documentation
### Low-Bandwidth Multilingual Telehealth Platform

**Base URL (Development):** `http://localhost:8000`  
**Base URL (Production):** `Coming soon - AWS deployment`  
**Interactive Docs:** `http://localhost:8000/docs`  
**Version:** 1.0.0

---

## 🔌 Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Server health check |
| GET | /health | Detailed health status |
| POST | /transcribe | Speech to text only |
| POST | /translate | Text translation only |
| POST | /transcribe-and-translate | Full pipeline (recommended) |

---

## 📍 Endpoint Details

### 1. GET /
Check if server is running.

**Response:**
```json
{
  "message": "MediBridge Backend is running!",
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### 2. GET /health
Detailed server health status.

**Response:**
```json
{
  "status": "ok",
  "service": "MediBridge API"
}
```

---

### 3. POST /transcribe
Upload audio file and get transcribed text.

**Request:**
- Content-Type: `multipart/form-data`
- Body: audio file (wav, mp3, m4a, mpeg, ogg, webm)

**Response:**
```json
{
  "success": true,
  "transcribed_text": "मेरा नाम बिनीशा ठाकुर है और मुझे बुखार है",
  "detected_language": "hi",
  "filename": "audio.mpeg"
}
```

---

### 4. POST /translate
Translate text from any Indian language to English.

**Request:**
- Content-Type: `application/json`
- Body:
```json
{
  "text": "मेरा नाम बिनीशा ठाकुर है और मुझे बुखार है",
  "source_language": "hi"
}
```

**Response:**
```json
{
  "success": true,
  "original_text": "मेरा नाम बिनीशा ठाकुर है और मुझे बुखार है",
  "translated_text": "my name is binisha thakur and i have fever",
  "source_language": "Hindi",
  "target_language": "English"
}
```

---

### 5. POST /transcribe-and-translate ⭐
**THE MAIN ENDPOINT — Use this for frontend integration.**

Upload audio in any Indian language, get English translation directly.
One API call handles everything.

**Request:**
- Content-Type: `multipart/form-data`
- Body: audio file (wav, mp3, m4a, mpeg, ogg, webm)

**Response:**
```json
{
  "success": true,
  "detected_language": "hi",
  "original_text": "मेरा नाम बिनीशा ठाकुर है और मुझे बुखार है",
  "english_translation": "My name is Vinisha Thakur and I have fever.",
  "filename": "audio.mpeg",
  "message": "Audio successfully transcribed and translated"
}
```

---

## 🌐 Supported Languages

| Language | Code |
|----------|------|
| Hindi | `hi` |
| Bengali | `bn` |
| Tamil | `ta` |
| Telugu | `te` |
| Marathi | `mr` |
| Gujarati | `gu` |
| Kannada | `kn` |
| Malayalam | `ml` |
| Punjabi | `pa` |
| Odia | `or` |
| Maithili | `mai` |

---

## 💻 Frontend Integration Example

### React / JavaScript:
```javascript
// Transcribe and translate audio in one call
const transcribeAndTranslate = async (audioFile) => {
  const formData = new FormData();
  formData.append('file', audioFile);

  const response = await fetch(
    'http://localhost:8000/transcribe-and-translate',
    {
      method: 'POST',
      body: formData
    }
  );

  const result = await response.json();
  
  if (result.success) {
    console.log('Original:', result.original_text);
    console.log('English:', result.english_translation);
    console.log('Language:', result.detected_language);
  }
};
```

### Translate text only:
```javascript
const translateText = async (text, language) => {
  const response = await fetch('http://localhost:8000/translate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: text,
      source_language: language
    })
  });
  
  const result = await response.json();
  return result.translated_text;
};
```

---

## ⚠️ Error Responses

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (wrong file type or empty text) |
| 500 | Server error (transcription or translation failed) |

---

## 🔒 Security Notes
- All endpoints will require JWT authentication in production
- Patient data encrypted with AES-256
- DISHA compliant data handling
- TLS encryption for all data in transit

---

*For questions contact the MediBridge backend team*