import { useState, useRef, useEffect } from 'react';
import { BarChart2, Shield, ActivitySquare, HeartPulse, ArrowRight, Send } from 'lucide-react';
import { Button } from '../components/ui/button';

const LandingPage = () => {
  const [showContactForm, setShowContactForm] = useState(false);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);
  
  // Create refs for each section
  const featuresRef = useRef<HTMLDivElement>(null);
  const aboutRef = useRef<HTMLDivElement>(null);
  const contactRef = useRef<HTMLDivElement>(null);

  // Check for form success parameter in URL
  useEffect(() => {
    // Check for success parameter in URL when component mounts
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success') === 'true') {
      setFormSubmitted(true);
      setShowContactForm(true);
      // Scroll to contact section to show the success message
      contactRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  // Update the page_url hidden field when the contact form is shown
  useEffect(() => {
    if (showContactForm && !formSubmitted) {
      const pageUrlField = document.getElementById('page_url') as HTMLInputElement;
      if (pageUrlField) {
        pageUrlField.value = window.location.href;
      }
    }
  }, [showContactForm, formSubmitted]);

  // Handle scrolling to each section
  const scrollToFeatures = () => featuresRef.current?.scrollIntoView({ behavior: 'smooth' });
  const scrollToAbout = () => aboutRef.current?.scrollIntoView({ behavior: 'smooth' });
  const scrollToContact = () => contactRef.current?.scrollIntoView({ behavior: 'smooth' });

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
                }}
              >
                Send Another Message
              </Button>
            </div>
          ) : (
            <form 
              ref={formRef}
              method="POST"
              action="https://formsubmit.co/shaun.porwal@gmail.com" 
              className="bg-card p-6 rounded-lg shadow-sm border text-left"
              onSubmit={(e) => {
                // For local development, simulate submission
                if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                  e.preventDefault();
                  console.log('Development mode - simulating form submission');
                  // Simulate a delay then show success message
                  setTimeout(() => {
                    setFormSubmitted(true);
                  }, 1000);
                }
              }}
            >
              {/* Add honeypot field to prevent spam */}
              <input type="text" name="_honey" style={{ display: 'none' }} />
              
              {/* Disable captcha */}
              <input type="hidden" name="_captcha" value="false" />
              
              {/* Custom subject line */}
              <input type="hidden" name="_subject" value="New Contact Form Submission from Climetrics" />
              
              {/* Custom form source URL */}
              <input type="hidden" name="_source" value="Climetrics Landing Page" />
              
              {/* Add current URL explicitly */}
              <input type="hidden" name="page_url" id="page_url" />
              
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
                  rows={4}
                  className="w-full p-2 rounded-md border border-input bg-background"
                  required
                />
              </div>
              
              <div className="flex justify-end gap-2">
                <Button 
                  type="button"
                  variant="outline" 
                  onClick={() => setShowContactForm(false)}
                >
                  Cancel
                </Button>
                <Button 
                  type="submit"
                  variant="default"
                  className="bg-black text-white hover:bg-gray-800 gap-2"
                >
                  Send Message
                  <Send className="w-4 h-4" />
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