import React from 'react'
import ReactDOM from 'react-dom/client'

// Create a simple App component
const App = () => {
  return (
    <div>
      <h1>Climetrics Dashboard</h1>
      <p>Welcome to the Climetrics Dashboard application.</p>
    </div>
  )
}

// Get the root element
const rootElement = document.getElementById('root')

// Create a root
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement)
  
  // Render the App component
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  )
}