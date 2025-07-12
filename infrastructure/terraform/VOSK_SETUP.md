#  Vosk Speech-to-Text Model Setup

## Download Vosk Model
1. Go to: https://alphacephei.com/vosk/models
2. Download: \`vosk-model-small-en-us-0.15.tar.gz\`
3. Extract to: \`backend/vosk-model-small-en-us-0.15/\`

## Expected Structure
\`\`\`
backend/
├── vosk-model-small-en-us-0.15/
│   └── vosk-model-small-en-us-0.15/
│       ├── am/
│       ├── conf/
│       ├── graph/
│       ├── ivector/
│       └── README
\`\`\`

## Model Path Configuration
The model path in your code should be:
\`\`\`python
vosk_model_path = "vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"
\`\`\`

## Verification
Run this command to test:
\`\`\`python
from vosk import Model
model = Model("vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")
print("Vosk model loaded successfully!")
\`\`\`
