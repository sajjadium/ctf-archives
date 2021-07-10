import { useParams } from 'react-router-dom'
import { useTitle, deepmerge } from './util'
import { defaultTheme, useTheme } from './theme'
import { markdown2hast } from './md-processor'
import { hast2reactCompiler } from './hast-processor'

const Renderer = ({ title, hast, theme }) => {
  useTitle(title)

  useTheme(deepmerge({}, defaultTheme, theme))

  return (
    <div className='container md-content'>
      {hast2reactCompiler(hast)}
    </div>
  )
}

const View = () => {
  const { data } = useParams()
  try {
    const { title, content, theme } = JSON.parse(atob(data))
    return <Renderer title={title} hast={markdown2hast(content)} theme={theme} />
  } catch {
    return (
      <div className='hero'>
        <h1>Invalid URL</h1>
      </div>
    )
  }
}

export default View
