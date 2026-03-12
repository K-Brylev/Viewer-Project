import { useSearchParams } from 'react-router-dom'

const CATEGORIES = [
  { value: 'TABLE', label: 'Tables' },
  { value: 'OTDRFURN', label: 'Outdoor Furnishings' },
  { value: 'TABLETOP', label: 'Tabletop' },
  { value: 'RUG', label: 'Rug' },
  { value: 'WALLMNTD', label: 'Wall-mounted' },
  { value: 'FURNISHING', label: 'Furnishings' },
  { value: 'INTRFIX', label: 'Interior Fixtures' },
  { value: 'EXTRFIX', label: 'Exterior Fixtures' },
]

function FilterTray() {
  const [searchParams, setSearchParams] = useSearchParams()

  const selectedCategories = searchParams.getAll('category')
  const tradeable = searchParams.get('tradeable') === 'true'
  const outdoor = searchParams.get('outdoor') === 'true'
  const dyeable = searchParams.get('dyeable') === 'true'

  function updateParam(key: string, value: string | null) {
    const next = new URLSearchParams(searchParams)
    if (value === null) {
      next.delete(key)
    } else {
      next.set(key, value)
    }
    setSearchParams(next)
  }

  function toggleCategory(value: string) {
    const next = new URLSearchParams(searchParams)
    const current = next.getAll('category')
    if (current.includes(value)) {
      next.delete('category')
      current.filter(c => c !== value).forEach(c => next.append('category', c))
    } else {
      next.append('category', value)
    }
    setSearchParams(next)
  }

  function toggleBoolean(key: string, current: boolean) {
    updateParam(key, current ? null : 'true')
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Categories */}
      <div className="flex flex-col gap-2">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">Category</p>
        {CATEGORIES.map(cat => (
          <label key={cat.value} className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={selectedCategories.includes(cat.value)}
              onChange={() => toggleCategory(cat.value)}
              className="rounded"
            />
            <span className="text-sm">{cat.label}</span>
          </label>
        ))}
      </div>

      {/* Toggles */}
      <div className="flex flex-col gap-2">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">Properties</p>
        {[
          { key: 'tradeable', label: 'Tradeable', value: tradeable },
          { key: 'outdoor', label: 'Outdoor', value: outdoor },
          { key: 'dyeable', label: 'Dyeable', value: dyeable },
        ].map(({ key, label, value }) => (
          <label key={key} className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={value}
              onChange={() => toggleBoolean(key, value)}
              className="rounded"
            />
            <span className="text-sm">{label}</span>
          </label>
        ))}
      </div>
    </div>
  )
}

export default FilterTray