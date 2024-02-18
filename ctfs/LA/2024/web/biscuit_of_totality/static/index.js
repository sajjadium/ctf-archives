(async () => {
  const viewingSave = window.location.href.includes("/viewSave")
  const defaultSavedata = {
    hasSavedata: 1,
    biscuits: 0,
    farmers: 0,
    bakeries: 0,
    fireFlowers: 0,
    waterFlowers: 0,
    earthFlowers: 0,
    skyFlowers: 0,
    manaFlowers: 0,
    elvenFlowers: 0,
    gaiaFlowers: 0,
    gaiaIIFlowers: 0,
    tinyPotatoes: [],
    userpfp: "", // TODO(arc) add a leaderboard
  }
  let savedata = {}
  let flagPotatoAdded = false

  console.log(`Viewing save: ${viewingSave}`)

  // util functions
  async function flate(stream, data) {
    let pulld = false
    const stream2 = new ReadableStream({
      pull(controller) {
        if (!pulld) {
          pulld = true
          controller.enqueue(data)
        } else {
          controller.close()
        }
      }
    })
    .pipeThrough(stream)

    let chunks = []
    let len = 0
    let reader2 = stream2.getReader()
    while (true) {
      const { done, value: chunk } = await reader2.read()
      if (done) break;
      chunks.push(chunk)
      len += chunk.length
    }

    let mergedChunks = new Uint8Array(len)
    let offset = 0
    for (const chunk of chunks) {
      mergedChunks.set(chunk, offset)
      offset += chunk.length
    }

    return mergedChunks
  }

  async function compress(data) {
    return [...await flate(new CompressionStream("deflate-raw"), new TextEncoder().encode(data))].map(x => (x <= 15 ? "0" : "") + x.toString(16)).join("")
  }

  async function decompress(data) {
    return new TextDecoder().decode(await flate(new DecompressionStream("deflate-raw"), Uint8Array.from(data.match(/[0-9a-z]{2}/g).map(b => parseInt(b, 16)))))
  }

  // FREE FLAG???
  const flag = (() => {
    for (const keyValue of document.cookie.split("; ")) {
      const eq = keyValue.indexOf("=")
      if (keyValue.substring(0, eq) === "flag") {
        const flag = keyValue.substring(eq + 1)
        return flag
      }
    }
    return "lactf{fake_flagz}"
  })()
  function addFlag(savedata) {
    if ((!savedata.tinyPotatoes.includes(flag) || viewingSave) && !flagPotatoAdded) {
      savedata.tinyPotatoes.splice(0, 0, flag)
      flagPotatoAdded = true
    }
  }

  // init / load savedata
  async function load() {
    let savedata = {}
    for (const keyValue of document.cookie.split("; ")) {
      const eq = keyValue.indexOf("=")
      const key = keyValue.substring(0, eq)
      const value = keyValue.substring(eq + 1)
      try {
        savedata[key] = JSON.parse(await decompress(value))
      } catch (e) {
        // this doesn't work when no cookies are set???
      }
    }
    delete savedata["flag"]
    if (!("hasSavedata" in savedata)) {
      savedata = structuredClone(defaultSavedata)
    }
    addFlag(savedata)
    return savedata
  }
  function loadView() {
    let parsed = JSON.parse(decodeURIComponent(window.location.hash.substring(1)))
    delete parsed["flag"]
    addFlag(parsed)
    return parsed
  }
  async function save(savedata) {
    const past = new Date(Date.now() - 1000).toUTCString()
    for (const key of Object.keys(savedata)) {
      document.cookie = `${key}=;expires=${past};samesite=strict`
    }
    for (const [key, value] of Object.entries(savedata)) {
      document.cookie = `${key}=${await compress(JSON.stringify(value))};samesite=strict`
    }
  }
  await save(viewingSave && window.location.hash.length > 1 ? loadView() : await load())
  savedata = await load()

  // prepare ui
  if (savedata.userpfp) {
    userpfp.src = savedata.userpfp
  }
  for (const potato of savedata.tinyPotatoes) {
    const li = document.createElement("li")
    li.textContent = potato
    potatoes.appendChild(li)
  }
  function updateBiscuits(b) {
    savedata.biscuits += b
    biscuits.textContent = savedata.biscuits
    if (savedata.biscuits == 69 || savedata.biscuits == 420) {
      biscuits.textContent += " (SUS?)"
    }
  }
  updateBiscuits(0)
  it.onclick = () => updateBiscuits(1)
  const upgrades = [
    "farmers",
    "bakeries",
    "fireFlowers",
    "waterFlowers",
    "earthFlowers",
    "skyFlowers",
    "manaFlowers",
    "elvenFlowers",
    "gaiaFlowers",
    "gaiaIIFlowers",
  ]
  for (let i = 0; i < upgrades.length; i++) {
    const upgrade = upgrades[i]
    const cost = 2 << (i + 6)
    window[upgrade + "_click"].onclick = () => {
      if (savedata.biscuits >= cost) {
        updateBiscuits(-cost)
        savedata[upgrade]++
        window[upgrade].textContent = savedata[upgrade]
      }
    }
    window[upgrade].textContent = savedata[upgrade]
  }
  const loop = setInterval(async () => {
    let totalGain = 0;
    for (let i = 0; i < upgrades.length; i++) {
      const gain = 2 << (i + 1)
      totalGain += savedata[upgrades[i]] * gain
    }
    updateBiscuits(totalGain)
    await save(savedata)
  }, 1000)
  if (!viewingSave) {
    const clear = document.createElement("span")
    clear.textContent = "Clear Save"
    clear.classList.add("thing")
    clear.onclick = () => {
      clearInterval(loop)
      save(structuredClone(defaultSavedata)).then(() => window.location.reload())
    }
    actions.appendChild(clear)
    actions.appendChild(document.createTextNode(" "))

    const share = document.createElement("span")
    share.textContent = "Share Save"
    share.classList.add("thing")
    share.onclick = () => {
      window.open("/viewSave#" + encodeURIComponent(JSON.stringify(savedata)))
    }
    actions.appendChild(share)
  }
})()
