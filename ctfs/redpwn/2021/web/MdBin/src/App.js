import { Suspense } from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from './Home'
import View from './View'
import Create from './Create'
import FourOhFour from './FourOhFour'
import Spinner from './Spinner'
import './App.css'

const Loader = () => (
  <div className="hero">
    <Spinner />
  </div>
)

const App = () => {

  return (
    <Suspense fallback={<Loader />}>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/create' element={<Create />} />
        <Route path='/view/:data' element={<View />} />
        <Route path='*' element={<FourOhFour />} />
      </Routes>
    </Suspense>
  )
}

export default App
