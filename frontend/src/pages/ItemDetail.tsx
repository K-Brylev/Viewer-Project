import { useQuery } from '@apollo/client/react'
import { useState } from 'react'
import { GET_ITEM } from '../graphql/queries'
import { useParams, useNavigate } from 'react-router-dom'

interface Page {
  items: Item[]
}

interface Item {
  id: number
  name: string
  category: string
  subCategory: string
  description: string
  dyeable: boolean
  tradeable: boolean
  outdoor: boolean
  tags: string[]
  patch: string
  icon: string
}

function ItemDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [activeImage, setActiveImage] = useState(0)
  const [view, setView] = useState<'images' | '3d'>('images')

  const { data, loading, error } = useQuery<{ page: Page }>(GET_ITEM, {
    variables: { id: id ? parseInt(id) : undefined },
  })

  if (loading) return <p className="p-8 text-gray-400">Loading...</p>
  if (error) return <p className="p-8 text-red-400">Something went wrong: {error.message}</p>
  if (!data?.page?.items) return <p className="p-8 text-gray-400">Item not found.</p>

  const item = data.page.items[0]

  const images = [
    `https://v2.xivapi.com/api/asset?path=${item.icon}&format=png`
  ]

  return (
    <div className="flex h-screen">
      {/* Left: item info */}
      <aside className="w-80 shrink-0 border-r border-gray-200 p-8 flex flex-col gap-6 overflow-y-auto">
        <a href="/" className="text-xl font-bold">Eorzea Housing</a>
        
        <button
        onClick={() => navigate(-1)}
        className="text-sm text-gray-400 hover:text-gray-700 text-left cursor-pointer transition-colors"
        >
        ← Back to search
        </button>

        <div className="flex flex-col gap-2">
          <p className="text-xs text-gray-400 uppercase tracking-wide">{item.category}</p>
          <h1 className="text-2xl font-bold">{item.name}</h1>
          <p className="text-sm text-gray-500 leading-relaxed">{item.description}</p>
        </div>

        <div className="flex flex-col gap-2">
          {[
            { label: 'Subcategory', value: item.subCategory },
            { label: 'Patch', value: item.patch },
            { label: 'Tradeable', value: item.tradeable ? 'Yes' : 'No' },
            { label: 'Dyeable', value: item.dyeable ? 'Yes' : 'No' },
            { label: 'Outdoor', value: item.outdoor ? 'Yes' : 'No' },
          ].map(stat => (
            <div key={stat.label} className="flex justify-between text-sm">
              <span className="text-gray-400">{stat.label}</span>
              <span className="font-medium">{stat.value}</span>
            </div>
          ))}
        </div>
      </aside>

      {/* Right: viewer */}
      <main className="flex-1 flex flex-col p-8 gap-4">
        {/* View toggle */}
        <div className="flex gap-2">
          <button
            onClick={() => setView('images')}
            className={`px-4 py-2 rounded-lg text-sm font-medium cursor-pointer transition-colors ${
              view === 'images' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Images
          </button>
          <button
            onClick={() => setView('3d')}
            className={`px-4 py-2 rounded-lg text-sm font-medium cursor-pointer transition-colors ${
              view === '3d' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            3D View
          </button>
        </div>

        {view === 'images' ? (
          <div className="flex flex-col gap-4 flex-1">
            {/* Main image */}
            <div className="flex flex-1 bg-gray-50 rounded-xl overflow-hidden items-center justify-center">
              <img
                src={images[activeImage]}
                alt={item.name}
                className="h-full object-contain self-center"
              />
            </div>
            {/* Thumbnails */}
            <div className="flex gap-2">
              {images.map((img, i) => (
                <img
                  key={i}
                  src={img}
                  alt={`View ${i + 1}`}
                  onClick={() => setActiveImage(i)}
                  className={`w-20 h-20 object-cover rounded-lg cursor-pointer border-2 transition-colors ${
                    activeImage === i ? 'border-gray-900' : 'border-transparent hover:border-gray-300'
                  }`}
                />
              ))}
            </div>
          </div>
        ) : (
          <div className="flex-1 bg-gray-50 rounded-xl flex items-center justify-center">
            <p className="text-gray-400">3D viewer coming soon</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default ItemDetail