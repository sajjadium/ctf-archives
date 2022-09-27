window.addEventListener('load', () => {
  document.getElementById('encode-btn-x2b')
    .addEventListener('click', e => {
      e.preventDefault();

      let resp = document.getElementById('base64-data-x2b');
      let data = document.getElementById('hex-data-x2b').value;
        
      let len  = data.length;
      let body = {data: data, len: len};
     
      fetch('/hex_to_base64', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      })
      .then(res => res.json())
      .then(data => {
        resp.value = data.data;
      });
    });

  document.getElementById('encode-btn-b2x')
    .addEventListener('click', e => {
      e.preventDefault();

      let resp = document.getElementById('hex-data-b2x');
      let data = document.getElementById('base64-data-b2x').value;
        
      let len  = data.length;
      let body = {data: data, len: len};
     
      fetch('/base64_to_hex', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      })
      .then(res => res.json())
      .then(data => {
        resp.value = data.data;
      });
    });

  document.getElementById('link-x2b')
    .addEventListener('click', e => {
      e.preventDefault();

      const container_x2b = document.querySelector('#container-x2b');
      container_x2b.style.display = 'block';
      const container_b2x = document.querySelector('#container-b2x');
      container_b2x.style.display = 'none';

      const link_x2b = document.getElementById('link-x2b');
      link_x2b.classList.add('active');
      const link_b2x = document.getElementById('link-b2x');
      link_b2x.classList.remove('active');
    });

  document.getElementById('link-b2x')
    .addEventListener('click', e => {
      e.preventDefault();

      const container_b2x = document.getElementById('container-b2x');
      container_b2x.style.display = 'block';
      const container_x2b = document.getElementById('container-x2b');
      container_x2b.style.display = 'none';

      const link_b2x = document.getElementById('link-b2x');
      link_b2x.classList.add('active');
      const link_x2b = document.getElementById('link-x2b');
      link_x2b.classList.remove('active');
    });
});
