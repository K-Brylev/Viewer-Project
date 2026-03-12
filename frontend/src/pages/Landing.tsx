import SearchBar from "../components/SearchBar"

function Landing(){
    
    return (
        <div className="flex flex-col items-center justify-center h-screen gap-4">
            <h1 className="text-center text-5xl font-bold">Eorzea Housing Catalog</h1>
            <p className="text-center text-lg text-gray-500">Search for housing items from Final Fantasy XIV</p>
            <div className="w-fit w-max-125 mt-4 p-4">
                <SearchBar />
            </div>
        </div>
    )
}

export default Landing