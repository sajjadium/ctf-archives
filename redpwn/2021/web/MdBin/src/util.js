import { useState, useCallback, useEffect } from 'react'

const deepmerge2 = (a, b) => {
  for (const key in b) {
    if (typeof a[key] === 'object' && typeof b[key] === 'object'
      && !(a instanceof Array) && !(b instanceof Array)
    ) {
      deepmerge2(a[key], b[key])
    } else {
      if (typeof b[key] === 'object' && !(b instanceof Array)) {
        a[key] = {}
        deepmerge2(a[key], b[key])
      } else {
        a[key] = b[key]
      }
    }
  }
}
export const deepmerge = (a, ...rest) => {
  let curr = a
  while (rest.length > 0) {
    deepmerge2(curr, rest.shift())
  }
  return curr
}

export const useInput = (initial) => {
  const [val, setVal] = useState(initial)
  const updateVal = useCallback(e => {
    setVal(e.target.value)
  }, [])
  return [val, updateVal, setVal]
}

export const useToggle = (initial) => {
  const [val, setVal] = useState(initial)
  const toggleVal = useCallback(() => {
    setVal(v => !v)
  }, [])
  return [val, toggleVal, setVal]
}

export const useTitle = (title) => {
  useEffect(() => {
    document.title = title ? `${title} | MdBin` : 'MdBin'
  }, [title])
}
