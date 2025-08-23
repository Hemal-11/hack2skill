# CraftConnect Frontend

A Next.js frontend application for the CraftConnect AI-powered marketplace assistant for local artisans.

## Features

- **Landing Page**: Welcome page with login functionality
- **Dashboard**: Main overview with statistics and tool access
- **Photo Upload**: AI-powered image analysis and enhancement
- **Story Generator**: AI-generated product descriptions
- **Translation**: Multi-language support for global reach
- **Price Helper**: AI-powered pricing recommendations
- **Recommendations**: Personalized business insights

## Tech Stack

- **Framework**: Next.js 14
- **Styling**: Tailwind CSS + shadcn/ui components
- **Animations**: Framer Motion
- **Language**: JavaScript/TypeScript
- **Icons**: Lucide React

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

3. **Run Development Server**
   ```bash
   npm run dev
   ```

4. **Open in Browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── ui/             # shadcn/ui components
│   ├── photo_upload.jsx
│   ├── story_form.jsx
│   ├── translation_box.jsx
│   ├── price_input.jsx
│   ├── recommendations.jsx
│   └── order_button.jsx
├── pages/              # Next.js pages
│   ├── index.jsx       # Landing page
│   ├── dashboard.jsx   # Main dashboard
│   ├── upload.jsx      # Photo upload page
│   ├── story.jsx       # Story generation page
│   ├── translate.jsx   # Translation page
│   ├── price.jsx       # Pricing page
│   ├── recommend.jsx   # Recommendations page
│   └── profile.jsx     # User profile page
├── services/           # API integration
│   └── api.js
├── utils/              # Utility functions
│   └── formatting.js
├── lib/                # Core utilities
│   └── utils.ts
└── styles/             # Global styles
    └── globals.css
```

## API Integration

The frontend connects to the CraftConnect backend API running on `http://localhost:8000` by default. Key endpoints include:

- `/copilot/analyze` - Image analysis
- `/storyteller/generate` - Story generation
- `/translation/translate` - Text translation
- `/pricing/suggest` - Price recommendations
- `/recommender/suggestions` - Personalized recommendations

## UI Components

### shadcn/ui Components Used
- Button
- Card
- Input
- Skeleton

### Custom Components
- **PhotoUpload**: Drag-and-drop image upload with preview
- **StoryForm**: AI story generation interface
- **TranslationBox**: Multi-language translation tool
- **PriceInput**: Smart pricing calculator
- **Recommendations**: Personalized business insights
- **OrderButton**: E-commerce order placement

## Styling

The application uses:
- **Tailwind CSS** for utility-first styling
- **shadcn/ui** for consistent component design
- **Framer Motion** for smooth animations
- **Orange/Amber color scheme** matching the brand

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Code Style

- Use functional components with hooks
- Implement responsive design (mobile-first)
- Follow shadcn/ui design patterns
- Include loading states and error handling
- Use Framer Motion for animations

## Deployment

The frontend can be deployed to:
- Vercel (recommended for Next.js)
- Netlify
- Any static hosting service

Make sure to:
1. Set environment variables in your deployment platform
2. Update API URL for production backend
3. Configure domain and SSL certificates

## Contributing

1. Follow the existing code structure
2. Use TypeScript for new components when possible
3. Maintain responsive design principles
4. Include proper error handling
5. Test across different screen sizes

## License

MIT License - see LICENSE file for details
