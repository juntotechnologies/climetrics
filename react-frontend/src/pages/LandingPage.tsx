import { BarChart2, Shield, ActivitySquare, HeartPulse, ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/button';

const LandingPage = () => {
  const features = [
    {
      icon: <BarChart2 className="w-6 h-6" />,
      title: "Performance Analytics",
      description: "Comprehensive metrics and benchmarks to evaluate climate data and environmental impacts"
    },
    {
      icon: <ActivitySquare className="w-6 h-6" />,
      title: "Risk-Adjusted Metrics",
      description: "Advanced statistical models that account for regional and seasonal variations"
    },
    {
      icon: <HeartPulse className="w-6 h-6" />,
      title: "Impact Assessment",
      description: "Data-driven insights to help identify areas for environmental improvement"
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Secure & Confidential",
      description: "Enterprise-grade security with customizable access controls"
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="px-4 py-5 mx-auto max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="text-2xl font-bold text-primary">Climetrics</div>
          <div className="space-x-8">
            <a href="#features" className="text-muted-foreground hover:text-primary">Features</a>
            <a href="#about" className="text-muted-foreground hover:text-primary">About</a>
            <a href="#pricing" className="text-muted-foreground hover:text-primary">Services Pricing</a>
            <Button variant="default">
              Login
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="px-4 py-20 mx-auto text-center max-w-7xl">
        <h1 className="mb-4 text-5xl font-bold text-foreground">
          Data-Driven Climate Insights
        </h1>
        <p className="mb-8 text-xl text-muted-foreground">
          Powerful analytics and visualization tools for environmental data
        </p>
        <Button variant="default" size="lg" className="gap-2">
          Try Demo
          <ArrowRight className="w-5 h-5" />
        </Button>
      </div>

      {/* Features Section */}
      <div id="features" className="px-4 py-16 mx-auto max-w-7xl">
        <h2 className="mb-12 text-3xl font-bold text-center">
          Comprehensive Climate Analytics
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
      <div id="about" className="px-4 py-16 mx-auto max-w-7xl">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="mb-4 text-3xl font-bold">About Our Platform</h2>
          <p className="text-lg text-muted-foreground">
            Climetrics provides powerful environmental data analytics that help organizations understand and reduce their climate impact.
            Our platform is built on open source technology, making it transparent, customizable, and community-driven.
          </p>
          <div className="mt-4 text-muted-foreground">
            <span className="bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium">Open Source</span>
          </div>
        </div>
      </div>
      
      {/* Pricing Section */}
      <div id="pricing" className="px-4 py-16 mx-auto max-w-7xl bg-muted/30">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="mb-4 text-3xl font-bold">Services Pricing</h2>
          <p className="text-lg text-muted-foreground mb-8">
            We offer flexible pricing options to meet the needs of organizations of all sizes.
          </p>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="p-6 bg-card text-card-foreground rounded-lg shadow-sm border">
              <h3 className="text-xl font-semibold">Basic</h3>
              <div className="my-4 text-3xl font-bold">Free</div>
              <p className="text-muted-foreground mb-4">For individuals and small teams</p>
              <Button variant="outline" className="w-full">Get Started</Button>
            </div>
            <div className="p-6 bg-card text-card-foreground rounded-lg shadow-sm border border-primary">
              <h3 className="text-xl font-semibold">Pro</h3>
              <div className="my-4 text-3xl font-bold">$49<span className="text-lg font-normal">/month</span></div>
              <p className="text-muted-foreground mb-4">For growing organizations</p>
              <Button variant="default" className="w-full">Try Free</Button>
            </div>
            <div className="p-6 bg-card text-card-foreground rounded-lg shadow-sm border">
              <h3 className="text-xl font-semibold">Enterprise</h3>
              <div className="my-4 text-3xl font-bold">Custom</div>
              <p className="text-muted-foreground mb-4">For large organizations</p>
              <Button variant="outline" className="w-full">Contact Us</Button>
            </div>
          </div>
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