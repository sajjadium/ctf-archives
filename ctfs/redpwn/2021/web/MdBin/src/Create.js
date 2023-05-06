import { useEffect, useState, useCallback } from 'react'
import { useInput, useToggle, useTitle } from './util'
import { useLocation, useNavigate, Link } from 'react-router-dom'
import { markdown2hast } from './md-processor'
import { hast2reactCompiler } from './hast-processor'
import { defaultTheme, useTheme } from './theme'

const createUrl = ({ title, content, theme }) => {
  const data = btoa(JSON.stringify({ title, content, theme }))
  return `/view/${data}`
}

const Create = () => {
  const { state: initialState } = useLocation()
  const navigate = useNavigate()

  useTitle('Create')

  const [title, onTitleChange] = useInput(initialState?.title ?? '')
  const [content, onContentChange] = useInput(initialState?.content ?? '')
  const [theme, setTheme] = useState(initialState?.theme ?? defaultTheme)
  const [previewShown, togglePreview] = useToggle(true)
  const [themeEditorShown, toggleThemeEditor] = useToggle(false)

  useEffect(() => {
    navigate('.', {
      replace: true,
      state: {
        title,
        content,
        theme,
      },
    })
  }, [navigate, title, content, theme])

  useTheme(theme)

  return (
    <div className='container flexed-space'>
      <h1>Create paste</h1>
      <div className='form-element'>
        <label htmlFor='title'>Title</label>
        <input id='title' value={title} onChange={onTitleChange} />
      </div>
      <div className='row-flex'>
        <div className='form-element'>
          <label htmlFor='content'>Content</label>
          <textarea
            id='content'
            value={content}
            onChange={onContentChange}
            className='mono'
          />
        </div>
        {previewShown &&
          <div className='container md-content'>
            {hast2reactCompiler(markdown2hast(content))}
          </div>
        }
      </div>
      <div className='controls'>
        <button className='primary' onClick={togglePreview} type='button'>
          {previewShown ? 'Hide preview' : 'Show preview'}
        </button>
        <button className='primary' onClick={toggleThemeEditor} type='button'>
          {themeEditorShown ? 'Hide theme editor' : 'Show theme editor'}
        </button>
        <Link className='button primary' to={createUrl({ title, content, theme })}>
          Create!
        </Link>
      </div>
      {themeEditorShown &&
        <ThemeEditor theme={theme} setTheme={setTheme} />
      }
    </div>
  )
}

const ThemeEditor = ({ theme, setTheme }) => {
  const doReset = useCallback(() => {
    console.log(defaultTheme)
    setTheme(defaultTheme)
  }, [setTheme])

  // TODO: deduplicate this
  const modifyColor = useCallback((key, value) => {
    setTheme(theme => ({
      ...theme,
      color: {
        ...theme.color,
        [key]: value,
      },
    }))
  }, [setTheme])
  const onColorFgChange = useCallback((e) => {
    modifyColor('foreground', e.target.value)
  }, [modifyColor])
  const onColorBgChange = useCallback((e) => {
    modifyColor('background', e.target.value)
  }, [modifyColor])
  const onColorMutedChange = useCallback((e) => {
    modifyColor('muted', e.target.value)
  }, [modifyColor])
  const onColorPrimaryChange = useCallback((e) => {
    modifyColor('primary', e.target.value)
  }, [modifyColor])
  const onSizeBaseChange = useCallback((e) => {
    setTheme(theme => ({
      ...theme,
      size: {
        ...theme.size,
        base: e.target.value,
      },
    }))
  }, [setTheme])
  const onLineheightChange = useCallback((e) => {
    setTheme(theme => ({
      ...theme,
      lineheight: e.target.value,
    }))
  }, [setTheme])

  return (
    <div className='flexed-space'>
      <h2>Theme editor (beta)</h2>
      <button className='primary' onClick={doReset} type='button'>
        Reset to default
      </button>
      <h3>Colors</h3>
      <div className='form-element'>
        <label htmlFor='colorfg'>Foreground</label>
        <input id='colorfg' value={theme.color.foreground} onChange={onColorFgChange} />
      </div>
      <div className='form-element'>
        <label htmlFor='colorbg'>Background</label>
        <input id='colorbg' value={theme.color.background} onChange={onColorBgChange} />
      </div>
      <div className='form-element'>
        <label htmlFor='colormuted'>Muted</label>
        <input id='colormuted' value={theme.color.muted} onChange={onColorMutedChange} />
      </div>
      <div className='form-element'>
        <label htmlFor='colorprimary'>Primary</label>
        <input id='colorprimary' value={theme.color.primary} onChange={onColorPrimaryChange} />
      </div>
      <h3>Sizes</h3>
      <div className='form-element'>
        <label htmlFor='sizebase'>Base</label>
        <input id='sizebase' value={theme.size.base} onChange={onSizeBaseChange} />
      </div>
      <h3>Line height</h3>
      <div className='form-element'>
        <label htmlFor='lineheight'>Line height</label>
        <input id='lineheight' value={theme.lineheight} onChange={onLineheightChange} />
      </div>
    </div>
  )
}

export default Create
