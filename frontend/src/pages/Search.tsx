import { useSearchParams } from 'react-router-dom'
import { useQuery } from '@apollo/client/react'
import ItemCard from '../components/ItemCard'
import { GET_ITEMS } from '../graphql/queries'
import SearchBar from '../components/SearchBar'
import FilterTray from '../components/FilterTray'
import { useRef, useEffect } from 'react'

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

interface Page {
    hasMore: boolean
    items: Item[]
}


function Search() {
  const [searchParams] = useSearchParams()

  const query = searchParams.get('q') ?? ''
  const categories = searchParams.getAll('category')
  const tradeable = searchParams.get('tradeable') === 'true' ? true : undefined
  const outdoor = searchParams.get('outdoor') === 'true' ? true : undefined
  const dyeable = searchParams.get('dyeable') === 'true' ? true : undefined
  const loadMoreRef = useRef<HTMLDivElement | null>(null)

  const { data, loading, fetchMore, error} = useQuery<{ page: Page }>(GET_ITEMS, {
    variables: {
        search: query || undefined,
        categories: categories.length > 0 ? categories : undefined,
        tradeable,
        outdoor,
        dyeable,
        limit: 20,
        offset: 0,
    },
    notifyOnNetworkStatusChange: true,
  })

  useEffect(() => {
  const node = loadMoreRef.current
  if (!node) return

  const observer = new IntersectionObserver(entries => {
    console.log(data?.page)
    if (entries[0].isIntersecting && !loading && data?.page?.hasMore) {
      fetchMore({
        variables: {
          offset: data?.page?.items.length ?? 0,
        },
        updateQuery: (prev, { fetchMoreResult }) => {
          if (!fetchMoreResult) return prev

          return {
            ...prev,
            page: {
                ...prev.page,
                hasMore: fetchMoreResult.page.hasMore,
                items: [
                    ...prev.page.items, 
                    ...fetchMoreResult.page.items
                ],
            }
          }
        },
      })
    }
  })

  observer.observe(node)

  return () => observer.disconnect()
}, [data, loading, fetchMore])

  return (
    <div className="flex flex-col-reverse md:flex-row h-screen">
      {/* Side tray */}
      <aside className="md:w-64 md:h-full md:shrink-0 border-t md:border-t-0 md:border-r border-gray-200 p-4 flex flex-col gap-6 overflow-y-auto">
        <a href="/" className="text-xl font-bold hidden md:block">Eorzea Housing</a>
        <SearchBar />
        <FilterTray />
      </aside>

      {/* Item grid */}
      <main className="flex-1 overflow-y-auto p-6">
        {loading && (
          <p className="text-gray-400">Loading...</p>
        )}
        {error && (
          <p className="text-red-400">Something went wrong: {error.message}</p>
        )}
        {data && (
            <>
                <div className="flex flex-wrap gap-2">
                    {data?.page?.items?.map((item: Item) => (
                    <ItemCard key={item.id} item={item} />
                ))}
                </div>
                
                <div ref={loadMoreRef} className="h-10 flex items-center justify-center">
                    {data?.page?.hasMore ? (
                        <span className="text-gray-400 text-sm">Loading more...</span>
                    ) :
                    (<span className="text-gray-400 text-sm">No more</span>)
                    }
                </div>
            </>
        )}
      </main>
    </div>
  )
}

export default Search