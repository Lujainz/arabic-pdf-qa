const API_URL = import.meta.env.VITE_API_URL
const API_KEY = import.meta.env.VITE_API_KEY

export async function uploadPDF(file) {
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`${API_URL}/api/upload`, {
    method: 'POST',
    headers: { 'x-api-key': API_KEY },
    body: formData,
  })

  const data = await res.json()

  if (!res.ok) {
    throw new Error(data.detail || 'Upload failed.')
  }

  return data  // { filename, collection_id, pages_extracted, chunks_stored }
}

export async function queryDocument(question, collectionId) {
  const res = await fetch(`${API_URL}/api/query`, {
    method: 'POST',
    headers: {
      'x-api-key': API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question,
      collection_id: collectionId,
    }),
  })

  const data = await res.json()

  if (!res.ok) {
    throw new Error(data.detail || 'Query failed.')
  }

  return data  // { answer, sources, usage }
}