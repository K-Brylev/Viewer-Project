import { useNavigate } from 'react-router-dom'

interface Item {
  id: number
  name: string
  category: string
  subCategory: string
  description: string
  icon: string
  dyeable: boolean
  tradeable: boolean
  outdoor: boolean
  tags: string[]
  patch: string
}

interface ItemCardProps {
  item: Item
}

function ItemCard({ item }: ItemCardProps) {
  const navigate = useNavigate()

  return (
    <div
      onClick={() => navigate(`/item/${item.id}`)}
      className="flex flex-col w-32 gap-2 p-4 border border-gray-200 rounded-xl cursor-pointer hover:shadow-md transition-shadow"
    >
      <img
        src={`https://v2.xivapi.com/api/asset?path=${item.icon}&format=png`}
        alt={item.name}
        className="w-full aspect-square object-contain bg-gray-50 rounded-lg"
      />
      <p className="font-semibold text-sm">{item.name}</p>
      <p className="text-xs text-gray-400">{item.category}</p>
    </div>
  )
}

export default ItemCard