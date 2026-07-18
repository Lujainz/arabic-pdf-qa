import UploadZone from './UploadZone'

export default function Sidebar({ document, onDocumentReady }) {
  return (
    <div style={{
      width: 260,
      background: '#f0efe9',
      borderRight: '0.5px solid #ddd',
      display: 'flex',
      flexDirection: 'column',
      padding: 16,
      gap: 12,
      flexShrink: 0,
    }}>
      <div style={{
        fontSize: 13, fontWeight: 500, color: '#888',
        paddingBottom: 8, borderBottom: '0.5px solid #ddd',
        direction: 'rtl', textAlign: 'right',
      }}>
        المستندات
      </div>

      <UploadZone onDocumentReady={onDocumentReady} />

      {document && (
        <div style={{
          display: 'flex', alignItems: 'flex-start', gap: 8,
          padding: '10px 12px', borderRadius: 8,
          background: 'white', border: '0.5px solid #1D9E75',
          direction: 'rtl',
        }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{
              fontSize: 12, fontWeight: 500, color: '#1a1a18',
              whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
            }}>
              {document.filename}
            </div>
            <div style={{ fontSize: 11, color: '#999', marginTop: 2 }}>
              {document.chunks_stored} مقطع · {document.pages_extracted} صفحة
            </div>
          </div>
          <span style={{
            fontSize: 11, padding: '2px 8px', borderRadius: 99,
            background: '#E1F5EE', color: '#0F6E56', fontWeight: 500,
            flexShrink: 0,
          }}>
            جاهز
          </span>
        </div>
      )}

      <div style={{
        marginTop: 'auto', paddingTop: 12,
        borderTop: '0.5px solid #ddd',
        fontSize: 11, color: '#aaa',
        direction: 'rtl', textAlign: 'right',
        lineHeight: 1.6,
      }}>
        الإجابات مبنية على محتوى المستند فقط
      </div>
    </div>
  )
}