import React from 'react';
import { ArrowRight, BarChart2, Shield, Zap } from 'lucide-react';

const LandingPage = () => {
  const features = [
    {
      icon: <BarChart2 className="w-6 h-6" />,
      title: "Data Visualization",
      description: "Interactive charts and graphs to help you understand your data better"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Real-time Analysis",
      description: "Get instant insights with our powerful analytics engine"
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Secure Platform",
      description: "Your data is protected with enterprise-grade security"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Navigation */}
      <nav className="px-4 py-5 mx-auto max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="text-2xl font-bold text-blue-600">YourApp</div>
          <div className="space-x-8">
            <a href="#features" className="text-gray-600 hover:text-blue-600">Features</a>
            <a href="#about" className="text-gray-600 hover:text-blue-600">About</a>
            <button className="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700">
              Launch App
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="px-4 py-20 mx-auto text-center max-w-7xl">
        <h1 className="mb-4 text-5xl font-bold text-gray-900">
          Transform Your Data Into Insights
        </h1>
        <p className="mb-8 text-xl text-gray-600">
          Powerful analytics and visualization tools built with Streamlit
        </p>
        <button className="inline-flex items-center px-6 py-3 text-lg text-white bg-blue-600 rounded-lg hover:bg-blue-700">
          Get Started
          <ArrowRight className="w-5 h-5 ml-2" />
        </button>
      </div>

      {/* Features Section */}
      <div id="features" className="px-4 py-16 mx-auto max-w-7xl">
        <h2 className="mb-12 text-3xl font-bold text-center text-gray-900">
          Powerful Features
        </h2>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {features.map((feature, index) => (
            <div key={index} className="p-6 bg-white rounded-lg shadow-lg">
              <div className="flex items-center justify-center w-12 h-12 mb-4 text-blue-600 bg-blue-100 rounded-lg">
                {feature.icon}
              </div>
              <h3 className="mb-2 text-xl font-semibold">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* About Section */}
      <div id="about" className="px-4 py-16 mx-auto max-w-7xl">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="mb-4 text-3xl font-bold text-gray-900">About Our Platform</h2>
          <p className="text-lg text-gray-600">
            We've built a powerful data analysis platform that helps you make better decisions.
            Our Streamlit-powered application provides real-time insights and beautiful
            visualizations that make complex data easy to understand.
          </p>
        </div>
      </div>

      {/* Footer */}
      <footer className="px-4 py-8 bg-gray-50">
        <div className="mx-auto max-w-7xl">
          <div className="text-center text-gray-600">
            © {new Date().getFullYear()} YourApp. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;