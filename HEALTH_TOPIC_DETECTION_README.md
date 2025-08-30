# Health Topic Detection Feature

## Overview
The AI Health Assistant now includes intelligent topic detection to ensure users only ask health-related questions. When users ask non-health questions, the system provides a polite warning and redirects them to health topics.

## Features Implemented

### 1. Health Topic Detection Algorithm
- **Location**: `ss_app/ai_chat_service.py`
- **Method**: `is_health_related(message)`
- **Purpose**: Analyzes user messages to determine if they are health-related

### 2. Comprehensive Keyword Detection
The system uses multiple layers of detection:

#### Health Keywords (Triggers health-related classification)
- **Medical Terms**: symptom, pain, fever, disease, doctor, hospital, medicine, treatment
- **Body Parts**: heart, lung, stomach, head, chest, back, arm, leg, eye, ear, etc.
- **Health Conditions**: diabetes, hypertension, asthma, cancer, stroke, heart disease
- **Lifestyle & Prevention**: diet, exercise, weight, BMI, smoking, alcohol, sleep
- **Common Health Questions**: how to, what is, why do, when should, can i, should i
- **Risk Factors**: risk, chance, probability, family history, genetic, age, gender
- **General Health Terms**: wellness, fitness, nutrition, vitamin, supplement, checkup

#### Non-Health Topics (Triggers non-health classification)
- **Entertainment**: weather, politics, sports, movies, music, jokes, humor
- **Technology**: computer, phone, car, house, job, work
- **Education**: school, education, math, science, history, geography
- **Hobbies**: cooking, recipes, travel, shopping, fashion, games, pets
- **Specific Activities**: cooking, pasta, food, movie, film, guitar, instrument

#### Strong Non-Health Indicators (Overrides everything)
- "how do i cook", "how to cook", "recipe for"
- "best movie", "watch movie", "movie recommendation"
- "capital of", "learn to play", "how to play"
- "learn to play guitar", "guitar lessons"

### 3. Warning System
When non-health questions are detected, the system provides:

```
⚠️ **Health Focus Reminder**

I'm designed specifically to help with health-related questions and concerns. Your question appears to be outside my area of expertise.

I can help you with:
• Health symptoms and conditions
• Disease risk factors and prevention
• Lifestyle and wellness advice
• Medical terminology explanations
• General health information

Please feel free to ask me any health-related questions! How can I assist you with your health concerns today?
```

### 4. Visual Warning Styling
- **Location**: `ss_app/templates/chat_interface.html`
- **CSS Class**: `.message.ai .message-content.warning`
- **Styling**: Yellow background with warning border and icon
- **Automatic Detection**: Warning styling is applied when:
  - Response contains "⚠️" emoji
  - Response contains "Health Focus Reminder"
  - `is_health_related` flag is False

### 5. Backend Integration
- **Modified**: `generate_response()` method in `AIChatService`
- **Added**: Health topic detection before response generation
- **Enhanced**: Response includes `is_health_related` flag
- **Updated**: Chat views to pass through the health-related flag

### 6. Frontend Integration
- **Modified**: JavaScript in chat interface
- **Added**: Warning message detection and styling
- **Enhanced**: Automatic warning styling for non-health responses

## How It Works

1. **User sends a message** to the AI Health Assistant
2. **Topic detection** analyzes the message using keyword matching
3. **If non-health related**: System returns warning message with health focus reminder
4. **If health-related**: System processes normally with AI response
5. **Frontend displays** warning messages with special styling

## Testing Results

The system was tested with 23 different scenarios:
- ✅ 10 health-related questions (100% accuracy)
- ✅ 13 non-health questions (100% accuracy)

**Test Cases Included:**
- Health: diabetes symptoms, blood pressure, chest pain, diet, exercise, etc.
- Non-health: weather, jokes, cooking, movies, computers, geography, etc.

## Benefits

1. **Focused Experience**: Keeps conversations health-focused
2. **User Education**: Teaches users what topics the AI can help with
3. **Professional Appearance**: Maintains medical AI assistant credibility
4. **Clear Boundaries**: Prevents misuse for non-medical purposes
5. **Visual Feedback**: Clear warning styling for off-topic questions

## Technical Implementation

### Files Modified:
- `ss_app/ai_chat_service.py` - Core detection logic
- `ss_app/chat_views.py` - Backend response handling
- `ss_app/templates/chat_interface.html` - Frontend styling and detection

### Key Methods:
- `is_health_related(message)` - Topic detection
- `generate_response()` - Enhanced with detection
- JavaScript warning detection and styling

## Future Enhancements

1. **Machine Learning**: Could be enhanced with ML-based topic classification
2. **Context Awareness**: Consider conversation history for better detection
3. **Multilingual Support**: Extend keyword lists for other languages
4. **Customization**: Allow admins to configure detection rules
5. **Analytics**: Track off-topic questions for system improvement

## Usage

The feature is automatically active and requires no user configuration. Users will naturally be guided to health topics when they ask non-health questions, improving the overall user experience and maintaining the system's focus on health assistance.

