import { Link } from 'react-router-dom'
import { useTitle } from './util'

const FourOhFour = () => {
  useTitle('404')

  return (
    <div className="hero" >
      <h1>404</h1>
      <p>Not found.</p>
      <div className='spacer' />
      <Link className='button primary' to='/'>Go Home</Link>
    </div>
  )
}

export default FourOhFour
