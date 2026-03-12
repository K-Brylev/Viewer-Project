import { useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

function SearchBar() {
  const [searchParams, setSearchParams] = useSearchParams()
  const query = searchParams.get('q') ?? ''
  const [inputValue, setInputValue] = useState(query)
  const navigate = useNavigate()

  function handleSearch() {
    if (window.location.pathname === '/search') {
        setSearchParams({ q: inputValue })
      } else {
        navigate(`/search?q=${encodeURIComponent(inputValue)}`)
      }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') handleSearch()
  }

  return (
    <div className="flex flex-wrap gap-2">
      <input
        type="text"
        value={inputValue}
        onChange={e => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Search items..."
        className="flex-3 min-w-48 px-4 py-2 border border-gray-300 rounded-lg outline-none focus:border-gray-500"
      />
      <button
        onClick={handleSearch}
        className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-700 cursor-pointer transition-colors shrink-0 flex-1"
      >
        Search
      </button>
    </div>
  )
}

export default SearchBar