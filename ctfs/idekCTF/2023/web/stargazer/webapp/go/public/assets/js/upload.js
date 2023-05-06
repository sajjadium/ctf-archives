
let u = document.querySelector('#upl')
u.onchange = ()=>{
  document.querySelector('#title').value = prompt('Title of File? ')
  u.submit()
}