CraftConnect/
│
├── backend/                                # Server-side code
│   ├── app/
│   │   ├── main.py                         # FastAPI entrypoint
│   │   ├── config.py                       # Project configs, env vars, API keys
│   │   ├── routes/                         # API endpoints per feature
│   │   │   ├── copilot.py                  # Photo → attributes & image enhancement
│   │   │   ├── storyteller.py              # 2-prompt story generation
│   │   │   ├── translation.py              # Multilingual translations + QA
│   │   │   ├── pricing.py                  # Price suggestion engine
│   │   │   ├── sales.py                    # Simulated commission / orders
│   │   │   └── recommender.py              # Mini recommendation engine
│   │   ├── models/                         # AI/ML model wrappers & helpers
│   │   │   ├── vertex_vision.py            # Gemini Vision wrapper
│   │   │   ├── vertex_text.py              # LLM wrapper for storytelling
│   │   │   ├── translation_model.py        # Translation + back-translation QA
│   │   │   └── price_model.py              # Price suggestion logic
│   │   ├── cloud_services/                 # Direct interaction with Google Cloud
│   │   │   ├── storage.py                  # Cloud Storage operations
│   │   │   ├── firestore.py                # Firestore CRUD ops
│   │   │   ├── vertex_vision_service.py    # Calls to Vision API
│   │   │   ├── vertex_text_service.py      # Calls to LLM/Text API
│   │   │   ├── translation_service.py      # Calls to Translation API
│   │   │   └── faiss_service.py            # FAISS embeddings & similarity search
│   │   └── utils/                          # Helper functions
│   │       ├── image_utils.py
│   │       ├── text_utils.py
│   │       └── price_utils.py
│   └── requirements.txt                     # Python dependencies
│
├── frontend/                               # Web frontend (React / NextJS)
│   ├── public/                             # Static files (images, icons)
│   ├── src/
│   │   ├── components/                     # Reusable UI components
│   │   │   ├── photo_upload.jsx
│   │   │   ├── story_form.jsx
│   │   │   ├── translation_box.jsx
│   │   │   ├── price_input.jsx
│   │   │   ├── order_button.jsx
│   │   │   └── recommendations.jsx
│   │   ├── pages/                          # App pages
│   │   │   ├── index.jsx
│   │   │   ├── product_detail.jsx
│   │   │   └── dashboard.jsx
│   │   ├── services/                       # Frontend API calls to backend
│   │   │   └── api.js
│   │   └── utils/                          # Helpers
│   │       └── formatting.js
│   └── package.json
│
├── data/                                   # Sample/test data
│   ├── images/
│   └── sample_products.json
│
├── notebooks/                              # AI prototyping notebooks
│   └── ai_prototyping.ipynb
│
├── scripts/                                # Deployment / setup scripts
│   ├── deploy_backend.sh
│   └── deploy_frontend.sh
│
├── docs/                                   # Documentation
│   ├── README.md
│   └── workflow_diagram.png
│
└── .gitignore
