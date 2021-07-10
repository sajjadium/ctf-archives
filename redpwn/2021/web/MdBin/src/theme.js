import { useEffect } from 'react'

export const defaultTheme = {
  color: {
    background: '#293038',
    foreground: '#e9ebec',
    muted: '#676e71',
    primary: '#46b6c7',
  },
  size: {
    base: '1rem',
  },
  lineheight: 'normal',
}

export const useTheme = (theme) => {
  useEffect(() => {
    const style = document.body.style
    for (const key in theme) {
      const prefix = `--${key}`
      if (typeof theme[key] === 'object') {
        for (const subkey in theme[key]) {
          style.setProperty(`${prefix}-${subkey}`, theme[key][subkey])
        }
      } else {
        style.setProperty(prefix, theme[key])
      }
    }
  }, [theme])
}
