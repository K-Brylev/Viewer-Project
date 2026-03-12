import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Search from './pages/Search'
import ItemDetail from './pages/ItemDetail'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing/>} />
      <Route path="/search" element={<Search/>} />
      <Route path="/item/:id" element={<ItemDetail/>} />
    </Routes>
  )
}

export default App
