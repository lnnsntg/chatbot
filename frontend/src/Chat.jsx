import { useState, useEffect, useRef } from 'react'
import './App.css'

function Chat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I am an AI assistant. How can I help you?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEnd = useRef(null)

  const scrollToBottom = () => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(scrollToBottom, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    const userMsg = input
    setInput('')
    setMessages(m => [...m, { role: 'user', content: userMsg }])
    setLoading(true)

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg })
      })
      const data = await response.json()
      setMessages(m => [...m, { role: 'assistant', content: data.response }])
    } catch (err) {
      setMessages(m => [...m, { role: 'assistant', content: 'Sorry, I could not connect to the server.' }])
    }
    setLoading(false)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage()
  }

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>🤖 AI Chat Demo</h1>
        <p>Powered by Ollama (local)</p>
      </header>

      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <span className="role-icon">{msg.role === 'user' ? '👤' : '🤖'}</span>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <span className="role-icon">🤖</span>
            <div className="message-content typing">
              <span>.</span><span>.</span><span>.</span>
            </div>
          </div>
        )}
        <div ref={messagesEnd} />
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage} disabled={loading}>➤</button>
      </div>
    </div>
  )
}

export default Chat