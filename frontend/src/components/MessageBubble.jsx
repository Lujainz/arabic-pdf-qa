import ReactMarkdown from 'react-markdown'

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: isUser ? 'flex-end' : 'flex-start',
      gap: 8,
    }}>
      <div style={{
        maxWidth: '80%',
        padding: '10px 14px',
        borderRadius: isUser ? '12px 12px 2px 12px' : '2px 12px 12px 12px',
        background: isUser ? '#f0efe9' : 'white',
        border: '0.5px solid #ddd',
        fontSize: 13,
        direction: 'rtl',
        textAlign: 'right',
        lineHeight: 1.7,
        color: '#1a1a18',
      }}>
        {isUser
          ? message.content
          : <ReactMarkdown>{message.content}</ReactMarkdown>
        }
      </div>

      {message.sources && message.sources.length > 0 && (
        <div style={{ maxWidth: '80%', display: 'flex', flexDirection: 'column', gap: 6 }}>
          <div style={{ fontSize: 11, color: '#aaa', direction: 'rtl', textAlign: 'right' }}>
            المصادر المستخدمة
          </div>
          {message.sources.map((src, i) => (
            <div key={i} style={{
              border: '0.5px solid #EF9F27',
              borderRadius: 8,
              padding: '8px 12px',
              background: '#FAEEDA',
              direction: 'rtl',
              textAlign: 'right',
            }}>
              <div style={{
                fontSize: 11, color: '#854F0B', fontWeight: 500,
                marginBottom: 4,
              }}>
                {src.filename} · صفحة {src.page}
              </div>
              <div style={{ fontSize: 12, color: '#633806', lineHeight: 1.5 }}>
                {src.chunk_text}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}