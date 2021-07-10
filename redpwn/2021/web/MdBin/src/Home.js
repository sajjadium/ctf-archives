import { Link } from 'react-router-dom'
import { useTitle } from './util'

const Home = () => {
  useTitle()

  return (
    <div className="hero" >
      <h1>MdBin</h1>
      <p>A markdown pastebin service</p>
      <div className='spacer' />
      <Link className='button primary' to='/create'>Create</Link>
    </div>
  )
}

export default Home
