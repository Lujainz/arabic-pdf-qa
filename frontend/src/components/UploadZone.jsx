import { useState, useRef } from 'react'
import { uploadPDF } from '../api/client'

export default function UploadZone({ onDocumentReady }) {
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const inputRef = useRef()

  async function handleFile(file) {
    if (!file || !file.name.endsWith('.pdf')) {
      setError('الرجاء اختيار ملف PDF فقط.')
      return
    }

    setError(null)
    setLoading(true)

    try {
      const result = await uploadPDF(file)
      onDocumentReady(result)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  function onDrop(e) {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    handleFile(file)
  }

  return (
    <div>
      <div
        onClick={() => !loading && inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        style={{
          border: `1.5px dashed ${dragging ? '#1D9E75' : '#ccc'}`,
          borderRadius: 10,
          padding: '20px 16px',
          textAlign: 'center',
          cursor: loading ? 'not-allowed' : 'pointer',
          background: dragging ? '#E1F5EE' : 'white',
          transition: 'all 0.15s',
          direction: 'rtl',
        }}
      >
        <div style={{ fontSize: 24, marginBottom: 8, color: '#888' }}>
          {loading ? '⏳' : '📄'}
        </div>
        <div style={{ fontSize: 13, color: '#555', lineHeight: 1.6 }}>
          {loading
            ? 'جارٍ معالجة الملف...'
            : <><span style={{ color: '#1D9E75', fontWeight: 500 }}>اختر ملف PDF</span><br />أو اسحب وأفلت هنا<br /><span style={{ fontSize: 11, color: '#aaa' }}>حد أقصى 20 ميجابايت</span></>
          }
        </div>
      </div>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        style={{ display: 'none' }}
        onChange={(e) => handleFile(e.target.files[0])}
      />

      {error && (
        <div style={{
          marginTop: 8, padding: '8px 12px', borderRadius: 8,
          background: '#FCEBEB', color: '#A32D2D',
          fontSize: 12, direction: 'rtl', textAlign: 'right',
        }}>
          {error}
        </div>
      )}
    </div>
  )
}