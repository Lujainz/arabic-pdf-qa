import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'

export default function App() {
  const [document, setDocument] = useState(null)

  return (
    <div style={{
      display: 'flex',
      height: '100vh',
      background: 'white',
    }}>
      <Sidebar
        document={document}
        onDocumentReady={setDocument}
      />
      <ChatArea document={document} />
    </div>
  )
}