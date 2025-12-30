# Day 19: Multimodal Messages

**LangChain Academy - Module 1, Lesson 1.4**

## 📚 What You'll Learn

- Send text + image in ONE message
- Base64 encoding for images
- Multimodal content structure
- Vision model requirements

## 🗂️ Files

1. **01_multimodal_demo.py** - Sending images to AI

## 🎯 Key Concepts

### Multimodal = Multiple Data Types
- Text + Image
- Text + Audio
- Text + Image + Audio

### Content Structure
```python
HumanMessage(
    content=[
        {"type": "text", "text": "What's in this image?"},
        {"type": "image", "image": base64_string, "mime_type": "image/png"}
    ]
)
```

### Image Flow
1. Read image file → bytes
2. Base64 encode → string
3. Add to message content
4. AI processes image + text together

### Base64 Encoding
- Converts binary data (images) → text string
- Required for JSON API compatibility
- AI can decode and process automatically

### Model Requirements
- **Text + Image**: gpt-4o-mini, gpt-5-nano
- **Text + Audio**: gpt-4o-audio-preview
- Not all models support all modalities!

## 🚀 How to Run

```bash
cd /home/intruder/langchain_v1.1/day19_multimodal
python 01_multimodal_demo.py
```

## 📖 Notes
- Requires vision-capable model
- Image must be base64 encoded
- Can send multiple images in one message
- Audio requires special models
