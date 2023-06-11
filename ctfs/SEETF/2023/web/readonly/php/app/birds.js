/* TEXTURE WIDTH FOR SIMULATION */
let WIDTH = 32;

let BIRDS = WIDTH * WIDTH;

let container;
let camera, scene, renderer, geometry, i, h, color;
let mouseX = 0, mouseY = 0;

let windowHalfX = window.innerWidth / 2;
let windowHalfY = window.innerHeight / 2;

let BOUNDS = 800, BOUNDS_HALF = BOUNDS / 2;

let last = performance.now();

let gpuCompute;
let velocityVariable;
let positionVariable;
let positionUniforms;
let velocityUniforms;
let birdUniforms;
let birdTextures = [];

init();

function init() {

    container = document.createElement( 'div' );
    document.body.appendChild( container );

    loader = new THREE.TextureLoader();
    birdTextures[ 0 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-00.png' );
    birdTextures[ 1 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-01.png' );
    birdTextures[ 2 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-02.png' );
    birdTextures[ 3 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-03.png' );
    birdTextures[ 4 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-04.png' );
    birdTextures[ 5 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-05.png' );
    birdTextures[ 6 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-06.png' );
    birdTextures[ 7 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-07.png' );
    birdTextures[ 8 ] = loader.load( 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/896175/crow-08.png' );

    camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 1, 3000 );
    camera.position.z = 350;

    scene = new THREE.Scene();

    scene.fog = new THREE.Fog( 0xffffff, 100, 1000 );

    renderer = new THREE.WebGLRenderer();
    renderer.setClearColor( scene.fog.color );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    container.appendChild( renderer.domElement );

    initComputeRenderer();

    document.addEventListener( 'mousemove', onDocumentMouseMove, false );
    document.addEventListener( 'touchstart', onDocumentTouchStart, false );
    document.addEventListener( 'touchmove', onDocumentTouchMove, false );

    //

    window.addEventListener( 'resize', onWindowResize, false );



    let effectController = {
        seperation: 20.0,
        alignment: 20.0,
        cohesion: 20.0,
        freedom: 0.75
    };

    let valuesChanger = function() {

        velocityUniforms.seperationDistance.value = effectController.seperation;
        velocityUniforms.alignmentDistance.value = effectController.alignment;
        velocityUniforms.cohesionDistance.value = effectController.cohesion;
        velocityUniforms.freedomFactor.value = effectController.freedom;

    };

    valuesChanger();

    initBirds();

    animate();
}

function initComputeRenderer() {

        gpuCompute = new GPUComputationRenderer( WIDTH, WIDTH, renderer );

    let dtPosition = gpuCompute.createTexture();
    let dtVelocity = gpuCompute.createTexture();
    fillPositionTexture( dtPosition );
    fillVelocityTexture( dtVelocity );

    velocityVariable = gpuCompute.addVariable( "textureVelocity", document.getElementById( 'fragmentShaderVelocity' ).textContent, dtVelocity );
    positionVariable = gpuCompute.addVariable( "texturePosition", document.getElementById( 'fragmentShaderPosition' ).textContent, dtPosition );

    gpuCompute.setVariableDependencies( velocityVariable, [ positionVariable, velocityVariable ] );
    gpuCompute.setVariableDependencies( positionVariable, [ positionVariable, velocityVariable ] );

    positionUniforms = positionVariable.material.uniforms;
    velocityUniforms = velocityVariable.material.uniforms;

    positionUniforms.time = { value: 0.0 };
    positionUniforms.delta = { value: 0.0 };
    velocityUniforms.time = { value: 1.0 };
    velocityUniforms.delta = { value: 0.0 };
    velocityUniforms.testing = { value: 1.0 };
    velocityUniforms.seperationDistance = { value: 1.0 };
    velocityUniforms.alignmentDistance = { value: 1.0 };
    velocityUniforms.cohesionDistance = { value: 1.0 };
    velocityUniforms.freedomFactor = { value: 1.0 };
    velocityUniforms.predator = { value: new THREE.Vector3() };
    velocityVariable.material.defines.BOUNDS = BOUNDS.toFixed( 2 );

    velocityVariable.wrapS = THREE.RepeatWrapping;
    velocityVariable.wrapT = THREE.RepeatWrapping;
    positionVariable.wrapS = THREE.RepeatWrapping;
    positionVariable.wrapT = THREE.RepeatWrapping;

    let error = gpuCompute.init();
    if ( error !== null ) {
        console.error( error );
    }

}

function initBirds() {

    let geometry = new THREE.BufferGeometry();
    let positions = new Float32Array( BIRDS * 3 );
    let references = new THREE.BufferAttribute( new Float32Array( BIRDS * 2 ), 2 );
    let frameIds = new THREE.BufferAttribute( new Float32Array( BIRDS ), 1 );

    geometry.addAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
    geometry.addAttribute( 'reference', references );
    geometry.addAttribute( 'frameId', frameIds );

    for( let i = 0; i < BIRDS; i++ ) {
        let x = (i % WIDTH) / WIDTH;
        let y = ~~(i / WIDTH) / WIDTH;
        references.array[ i * 2 ] = x;
        references.array[ i * 2 + 1 ] = y;
        frameIds.array[ i ] = Math.random() * 9.0;
    }

    // For Vertex and Fragment
    birdUniforms = {
        texturesBird: { value: birdTextures },
        color: { value: new THREE.Color( 0xff2200 ) },
        texturePosition: { value: null },
        textureVelocity: { value: null },
        time: { value: 1.0 },
        delta: { value: 0.0 }
    };

    let shaderMaterial = new THREE.ShaderMaterial( {

        uniforms: birdUniforms,
        vertexShader: document.getElementById( 'birdVS' ).textContent,
        fragmentShader: document.getElementById( 'birdFS' ).textContent,
        depthTest: false,
        transparent: true
    });

    let particles = new THREE.Points( geometry, shaderMaterial );
    scene.add( particles );
}

function fillPositionTexture( texture ) {

    let theArray = texture.image.data;

    for ( let k = 0, kl = theArray.length; k < kl; k += 4 ) {

        let x = Math.random() * BOUNDS - BOUNDS_HALF;
        let y = Math.random() * BOUNDS - BOUNDS_HALF;
        let z = Math.random() * BOUNDS - BOUNDS_HALF;

        theArray[ k + 0 ] = x;
        theArray[ k + 1 ] = y;
        theArray[ k + 2 ] = z;
        theArray[ k + 3 ] = 1;

    }

}

function fillVelocityTexture( texture ) {

    let theArray = texture.image.data;

    for ( let k = 0, kl = theArray.length; k < kl; k += 4 ) {

        let x = Math.random() - 0.5;
        let y = Math.random() - 0.5;
        let z = Math.random() - 0.5;

        theArray[ k + 0 ] = x * 10;
        theArray[ k + 1 ] = y * 10;
        theArray[ k + 2 ] = z * 10;
        theArray[ k + 3 ] = 1;

    }

}


function onWindowResize() {

    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

}

function onDocumentMouseMove( event ) {

    mouseX = event.clientX - windowHalfX;
    mouseY = event.clientY - windowHalfY;

}

function onDocumentTouchStart( event ) {

    if ( event.touches.length === 1 ) {

        event.preventDefault();

        mouseX = event.touches[ 0 ].pageX - windowHalfX;
        mouseY = event.touches[ 0 ].pageY - windowHalfY;

    }

}

function onDocumentTouchMove( event ) {

    if ( event.touches.length === 1 ) {

        event.preventDefault();

        mouseX = event.touches[ 0 ].pageX - windowHalfX;
        mouseY = event.touches[ 0 ].pageY - windowHalfY;

    }

}

//

function animate() {

    requestAnimationFrame( animate );

    render();
}

function render() {

    let now = performance.now();
    let delta = (now - last) / 1000;

    if (delta > 1) delta = 1; // safety cap on large deltas
    last = now;

    positionUniforms.time.value = now;
    positionUniforms.delta.value = delta;
    velocityUniforms.time.value = now;
    velocityUniforms.delta.value = delta;
    birdUniforms.time.value = now;
    birdUniforms.delta.value = delta;

    velocityUniforms.predator.value.set( 0.5 * mouseX / windowHalfX, - 0.5 * mouseY / windowHalfY, 0 );

    mouseX = 10000;
    mouseY = 10000;

    gpuCompute.compute();

    birdUniforms.texturePosition.value = gpuCompute.getCurrentRenderTarget( positionVariable ).texture;
    birdUniforms.textureVelocity.value = gpuCompute.getCurrentRenderTarget( velocityVariable ).texture;

    renderer.render( scene, camera );

}
