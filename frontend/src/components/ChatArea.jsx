import { useState, useRef, useEffect } from 'react'
import { queryDocument } from '../api/client'
import MessageBubble from './MessageBubble'

export default function ChatArea({ document }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef()

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Reset chat when document changes
  useEffect(() => {
    setMessages([])
  }, [document?.collection_id])

  async function sendMessage() {
    const question = input.trim()
    if (!question || !document || loading) return

    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: question }])
    setLoading(true)

    try {
      const result = await queryDocument(question, document.collection_id)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: result.answer,
        sources: result.sources,
      }])
    } catch (e) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `حدث خطأ: ${e.message}`,
        sources: [],
      }])
    } finally {
      setLoading(false)
    }
  }

  function onKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0 }}>
      <div style={{
        padding: '14px 20px',
        borderBottom: '0.5px solid #ddd',
      }}>
        <div style={{ fontSize: 15, fontWeight: 500 }}>سؤال وجواب</div>
        <div style={{ fontSize: 12, color: '#aaa' }}>
          {document ? document.filename : 'ارفع مستنداً للبدء'}
        </div>
      </div>

      <div style={{
        flex: 1, overflowY: 'auto',
        padding: 20,
        display: 'flex', flexDirection: 'column', gap: 16,
      }}>
        {messages.length === 0 && (
          <div style={{
            textAlign: 'center', color: '#bbb',
            marginTop: 60, fontSize: 13,
            direction: 'rtl',
          }}>
            {document
              ? 'اطرح سؤالاً عن المستند'
              : 'ارفع ملف PDF من القائمة على اليسار للبدء'
            }
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {loading && (
          <div style={{
            alignSelf: 'flex-start',
            padding: '10px 14px',
            borderRadius: '2px 12px 12px 12px',
            background: 'white', border: '0.5px solid #ddd',
            fontSize: 13, color: '#aaa',
          }}>
            جارٍ البحث والإجابة...
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div style={{
        padding: '12px 16px',
        borderTop: '0.5px solid #ddd',
        display: 'flex', alignItems: 'center', gap: 10,
      }}>
        <button
          onClick={sendMessage}
          disabled={!document || !input.trim() || loading}
          style={{
            width: 36, height: 36,
            borderRadius: 8,
            background: document && input.trim() && !loading ? '#1a1a18' : '#ddd',
            border: 'none', cursor: document && input.trim() && !loading ? 'pointer' : 'not-allowed',
            color: 'white', fontSize: 16,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0, transition: 'background 0.15s',
          }}
          aria-label="إرسال"
        >
          →
        </button>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder={document ? 'اكتب سؤالك هنا...' : 'ارفع ملفاً أولاً...'}
          disabled={!document || loading}
          style={{
            flex: 1,
            border: '0.5px solid #ccc',
            borderRadius: 8,
            padding: '9px 14px',
            fontSize: 13,
            direction: 'rtl',
            textAlign: 'right',
            fontFamily: "'Tajawal', sans-serif",
            background: document ? 'white' : '#f5f5f5',
            color: '#1a1a18',
            outline: 'none',
          }}
        />
      </div>
    </div>
  )
}