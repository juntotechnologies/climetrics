import { useState, useRef } from 'react';
import { BarChart2, Shield, ActivitySquare, HeartPulse, ArrowRight, Send } from 'lucide-react';
import { Button } from '../components/ui/button';

const LandingPage = () => {
  const [showContactForm, setShowContactForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const formRef = useRef<HTMLFormElement>(null);
  
  // Create refs for each section
  const featuresRef = useRef<HTMLDivElement>(null);
  const aboutRef = useRef<HTMLDivElement>(null);
  const contactRef = useRef<HTMLDivElement>(null);

  // Handle scrolling to each section
  const scrollToFeatures = () => featuresRef.current?.scrollIntoView({ behavior: 'smooth' });
  const scrollToAbout = () => aboutRef.current?.scrollIntoView({ behavior: 'smooth' });
  const scrollToContact = () => contactRef.current?.scrollIntoView({ behavior: 'smooth' });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');
    
    // For development environment, simulate a successful submission
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.log('Development mode - simulating successful submission:', formData);
      setTimeout(() => {
        setFormSubmitted(true);
        setIsSubmitting(false);
      }, 1000); // Simulate network delay
      return;
    }
    
    // Production environment - use FormSubmit
    const formDataToSend = new FormData(formRef.current!);
    
    // Add the current page URL to form data
    formDataToSend.append('_url', window.location.href);
    
    fetch('https://formsubmit.co/shaun.porwal@gmail.com', {
      method: 'POST',
      body: formDataToSend
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      console.log('Email sent successfully');
      setFormSubmitted(true);
      setIsSubmitting(false);
    })
    .catch(error => {
      console.error('Failed to send email:', error);
      setError('Failed to send your message. Please try again later.');
      setIsSubmitting(false);
      
      // Fallback to mailto link if form submission fails
      window.open(`mailto:shaun.porwal@gmail.com?subject=Contact from ${formData.name}&body=${formData.message}`);
    });
  };

  const features = [
    {
      icon: <BarChart2 className="w-6 h-6" />,
      title: "Performance Analytics",
      description: "Comprehensive metrics and benchmarks to evaluate surgical outcomes and quality metrics"
    },
    {
      icon: <ActivitySquare className="w-6 h-6" />,
      title: "Risk-Adjusted Metrics",
      description: "Advanced statistical models that account for patient complexity and comorbidities"
    },
    {
      icon: <HeartPulse className="w-6 h-6" />,
      title: "Outcome Assessment",
      description: "Data-driven insights to help identify areas for surgical quality improvement"
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Secure & Confidential",
      description: "Enterprise-grade security with HIPAA-compliant access controls"
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="px-4 py-5 mx-auto max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="text-2xl font-bold text-primary">Climetrics</div>
          <div className="space-x-8">
            <button 
              onClick={scrollToFeatures} 
              className="text-muted-foreground hover:text-primary bg-transparent border-none cursor-pointer"
            >
              Features
            </button>
            <button 
              onClick={scrollToAbout} 
              className="text-muted-foreground hover:text-primary bg-transparent border-none cursor-pointer"
            >
              About
            </button>
            <button 
              onClick={scrollToContact} 
              className="text-muted-foreground hover:text-primary bg-transparent border-none cursor-pointer"
            >
              Contact Us
            </button>
            <Button variant="default">
              Login
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="px-4 py-20 mx-auto text-center max-w-7xl">
        <h1 className="mb-4 text-5xl font-bold text-foreground">
          Data-Driven Surgical Insights
        </h1>
        <p className="mb-8 text-xl text-muted-foreground">
          Powerful analytics and visualization tools for surgical performance data
        </p>
        <Button variant="default" size="lg" className="gap-2">
          Try Demo
          <ArrowRight className="w-5 h-5" />
        </Button>
      </div>

      {/* Features Section */}
      <div ref={featuresRef} className="px-4 py-16 mx-auto max-w-7xl scroll-mt-20">
        <h2 className="mb-12 text-3xl font-bold text-center">
          Comprehensive Surgical Analytics
        </h2>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => (
            <div key={index} className="p-6 bg-card text-card-foreground rounded-lg shadow-sm border">
              <div className="flex items-center justify-center w-12 h-12 mb-4 text-primary bg-primary/10 rounded-lg">
                {feature.icon}
              </div>
              <h3 className="mb-2 text-xl font-semibold">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* About Section */}
      <div ref={aboutRef} className="px-4 py-16 mx-auto max-w-7xl scroll-mt-20">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="mb-4 text-3xl font-bold">About Our Platform</h2>
          <p className="text-lg text-muted-foreground">
            Climetrics provides powerful surgical data analytics that help healthcare organizations understand and improve surgical outcomes.
            Our platform is built on open source technology, making it transparent, customizable, and community-driven.
          </p>
          <div className="mt-4 text-muted-foreground">
            <span className="bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium">Open Source</span>
          </div>
        </div>
      </div>
      
      {/* Contact Section */}
      <div ref={contactRef} className="px-4 py-16 mx-auto max-w-7xl bg-muted/30 scroll-mt-20">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="mb-4 text-3xl font-bold">Get in Touch</h2>
          <p className="text-lg text-muted-foreground mb-8">
            Interested in learning more about our services? Contact us today.
          </p>
          
          {!showContactForm ? (
            <Button 
              variant="default" 
              className="bg-black text-white hover:bg-gray-800"
              onClick={() => setShowContactForm(true)}
            >
              Contact Us
            </Button>
          ) : formSubmitted ? (
            <div className="p-6 bg-card text-card-foreground rounded-lg shadow-sm border">
              <h3 className="text-xl font-semibold text-green-600 mb-2">Thank You!</h3>
              <p className="mb-4">Your message has been sent. We'll get back to you soon.</p>
              <Button 
                variant="outline" 
                onClick={() => {
                  setFormSubmitted(false);
                  setShowContactForm(false);
                  setFormData({ name: '', email: '', message: '' });
                }}
              >
                Send Another Message
              </Button>
            </div>
          ) : (
            <form 
              ref={formRef}
              onSubmit={handleSubmit} 
              className="bg-card p-6 rounded-lg shadow-sm border text-left"
              action="https://formsubmit.co/shaun.porwal@gmail.com" 
              method="POST"
            >
              {/* Add honeypot field to prevent spam */}
              <input type="text" name="_honey" style={{ display: 'none' }} />
              
              {/* Disable captcha */}
              <input type="hidden" name="_captcha" value="false" />
              
              {/* Custom subject line */}
              <input type="hidden" name="_subject" value="New Contact Form Submission from Climetrics" />
              
              {/* Custom form source URL */}
              <input type="hidden" name="_source" value="Climetrics Landing Page" />
              
              {/* Add page URL explicitly */}
              <input type="hidden" name="page_url" value={window.location.href} />
              
              {/* Add success page URL - use your GitHub Pages URL + success parameter */}
              <input type="hidden" name="_next" value="https://juntotechnologies.github.io/climetrics/?success=true" />
              
              <div className="mb-4">
                <label htmlFor="name" className="block text-sm font-medium mb-1">
                  Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="w-full p-2 rounded-md border border-input bg-background"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label htmlFor="email" className="block text-sm font-medium mb-1">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full p-2 rounded-md border border-input bg-background"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label htmlFor="message" className="block text-sm font-medium mb-1">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleInputChange}
                  rows={4}
                  className="w-full p-2 rounded-md border border-input bg-background"
                  required
                />
              </div>
              
              {error && (
                <div className="mb-4 p-2 text-white bg-red-500 rounded">
                  {error}
                </div>
              )}
              
              <div className="flex justify-end gap-2">
                <Button 
                  type="button"
                  variant="outline" 
                  onClick={() => setShowContactForm(false)}
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>
                <Button 
                  type="submit"
                  variant="default"
                  className="bg-black text-white hover:bg-gray-800 gap-2"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Sending...' : 'Send Message'}
                  {!isSubmitting && <Send className="w-4 h-4" />}
                </Button>
              </div>
            </form>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="px-4 py-8 bg-muted/50">
        <div className="mx-auto max-w-7xl">
          <div className="text-center text-muted-foreground">
            © {new Date().getFullYear()} Climetrics. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage; 