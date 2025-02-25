# Climetrics Landing Page

A modern landing page for Climetrics - a platform that provides powerful surgical data analytics to help healthcare organizations understand and improve surgical outcomes.

## Features

- Modern React frontend with TypeScript
- Responsive design with Tailwind CSS
- Clean, professional UI using shadcn/ui components
- Automatic deployment with GitHub Actions
- Contact form with EmailJS integration

## Development

### Prerequisites

- Node.js (v18+)
- npm or yarn
- EmailJS account (for contact form)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd climetrics

# Navigate to the frontend directory
cd react-frontend

# Install dependencies
npm install --legacy-peer-deps
```

### EmailJS Setup

To enable the contact form functionality:

1. Sign up at [EmailJS](https://www.emailjs.com/)
2. Create a new Email Service (Gmail, Outlook, etc.)
3. Create an Email Template with the following variables:
   - `name` - Sender's name
   - `email` - Sender's email
   - `message` - Message content
4. Get your Service ID, Template ID, and Public Key
5. Update these values in `src/pages/LandingPage.tsx`:

```typescript
emailjs.sendForm(
  'YOUR_SERVICE_ID', 
  'YOUR_TEMPLATE_ID',
  formRef.current!,
  'YOUR_PUBLIC_KEY'
)
```

### Running Locally

```bash
npm run dev
```

### Building for Production

```bash
npm run build
```

## Deployment

This project is configured to automatically deploy to GitHub Pages using GitHub Actions. When you push changes to the `gh-pages` branch, the site will be built and deployed automatically.

### Manual Deployment

If you need to manually trigger a deployment, you can:

1. Go to the GitHub repository
2. Navigate to Actions tab
3. Select the "Deploy Landing Page" workflow
4. Click "Run workflow" and select the branch you want to deploy from

## Project Structure

- `/react-frontend` - React application code
  - `/src` - Source code
    - `/components` - Reusable React components
    - `/pages` - Page components
    - `/lib` - Utility functions and helpers

## License

This project is open source under the [MIT License](LICENSE). 