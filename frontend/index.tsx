import React from 'react'
import ReactDOM from 'react-dom'
import LandingPage from './components/LandingPage'
import {
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

class LandingPageWrapper extends StreamlitComponentBase {
  render() {
    return <LandingPage />
  }
}

// Wrap your component with Streamlit connection
const Component = withStreamlitConnection(LandingPageWrapper)

// Create and render component
ReactDOM.render(
  <React.StrictMode>
    <Component />
  </React.StrictMode>,
  document.getElementById("root")
)