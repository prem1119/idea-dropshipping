import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { MessageSquare, Send, Bot } from 'lucide-react'
import './CustomerService.css'

function CustomerService() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMessages()
    const interval = setInterval(fetchMessages, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchMessages = async () => {
    try {
      const response = await axios.get('/api/v1/customer/messages?answered=false')
      setMessages(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching messages:', error)
      setLoading(false)
    }
  }

  const handleMessage = async (messageId) => {
    try {
      const response = await axios.post(`/api/v1/customer/messages/${messageId}/respond`)
      alert('Response sent automatically!')
      fetchMessages()
    } catch (error) {
      console.error('Error handling message:', error)
      alert('Failed to send response')
    }
  }

  if (loading) {
    return <div className="customer-service-loading">Loading messages...</div>
  }

  return (
    <div className="customer-service">
      <div className="customer-service-header">
        <div>
          <h1>Customer Service</h1>
          <p>AI-powered customer message handling</p>
        </div>
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-messages">
            <MessageSquare size={64} />
            <h2>No pending messages</h2>
            <p>All customer messages have been handled</p>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className="message-card">
              <div className="message-header">
                <div>
                  <h3>{message.subject}</h3>
                  <p className="message-meta">
                    From: {message.customer_name} ({message.customer_email})
                    {message.order_id && ` • Order: #${message.order_id}`}
                  </p>
                </div>
                <span className="message-status">
                  {message.answered ? 'Answered' : 'Pending'}
                </span>
              </div>
              <div className="message-body">
                <p>{message.message}</p>
              </div>
              {message.ai_response && (
                <div className="ai-response">
                  <div className="ai-response-header">
                    <Bot size={16} />
                    <span>AI Response</span>
                  </div>
                  <p>{message.ai_response}</p>
                </div>
              )}
              {!message.answered && (
                <div className="message-actions">
                  <button
                    className="respond-btn"
                    onClick={() => handleMessage(message.id)}
                  >
                    <Send size={16} />
                    Auto-Respond
                  </button>
                </div>
              )}
              <div className="message-footer">
                <span>Received: {new Date(message.created_at).toLocaleString()}</span>
                {message.responded_at && (
                  <span>Responded: {new Date(message.responded_at).toLocaleString()}</span>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default CustomerService

