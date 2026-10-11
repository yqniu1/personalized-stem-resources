// Bundle the renderer and loaders for a standalone offline HTML file.
// Meshopt includes its WASM decoder, so opening from disk needs no network fetch.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';

window.THREE = THREE;
window.GLTFLoader = GLTFLoader;
window.OrbitControls = OrbitControls;
window.MeshoptDecoder = MeshoptDecoder;
