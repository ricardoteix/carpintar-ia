import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- Estado da Aplicação ---
let scene, camera, renderer, controls;
let currentMeshes = [];
let raycaster, mouse;
let selectedMesh = null;
let currentMaterialType = 'pinus';
let autoRotate = false;

// --- Texturas Procedurais (Sem dependência de imagens externas) ---
function createProceduralWoodTexture(type = 'pinus') {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d');

  let baseColor, veinColor;
  if (type === 'pinus') {
    baseColor = '#deb887';
    veinColor = '#c2975b';
  } else if (type === 'madeirado') {
    baseColor = '#8b5a2b';
    veinColor = '#5c3a1e';
  } else {
    // MDF Branco Texturizado
    baseColor = '#f8fafc';
    veinColor = '#e2e8f0';
  }

  ctx.fillStyle = baseColor;
  ctx.fillRect(0, 0, 512, 512);

  if (type !== 'mdf_branco') {
    ctx.strokeStyle = veinColor;
    ctx.lineWidth = 2.5;
    for (let i = 0; i < 45; i++) {
      ctx.beginPath();
      const y = Math.random() * 512;
      ctx.moveTo(0, y);
      ctx.bezierCurveTo(170, y + (Math.random() - 0.5) * 45, 340, y + (Math.random() - 0.5) * 45, 512, y);
      ctx.globalAlpha = 0.28;
      ctx.stroke();
    }
  } else {
    ctx.fillStyle = veinColor;
    ctx.globalAlpha = 0.08;
    for (let x = 0; x < 512; x += 4) {
      for (let y = 0; y < 512; y += 4) {
        if (Math.random() > 0.5) ctx.fillRect(x, y, 2, 2);
      }
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  return texture;
}

function getMaterial(type = 'pinus') {
  const texture = createProceduralWoodTexture(type);
  return new THREE.MeshStandardMaterial({
    map: texture,
    roughness: type === 'mdf_branco' ? 0.35 : 0.65,
    metalness: 0.05,
  });
}

// --- Definição dos Projetos (Presets) ---
const PROJECTS = {
  krat: {
    "title": "Cadeira Krat (Gerrit Rietveld, 1934)",
    "dimensions": "590 x 630 x 686 mm",
    "description": "Design modernista autêntico de 1934 extraído do modelo técnico (krat-model.dae) e manual de montagem oficial: 18 peças de 20mm sem peças soltas ou flutuando.",
    "pieces": [
        {
            "id": "group_0_braco",
            "name": "Lateral Esquerda - Apoio de Braço",
            "sub": "Braço",
            "group": "group_0",
            "groupLabel": "Lateral Esquerda",
            "size": [
                20.0,
                70.0,
                600.0
            ],
            "pos": [
                -260.0,
                460.0,
                0.0
            ],
            "rot": [
                -3.14159,
                -0.0,
                -1.5708
            ],
            "quaternion": [
                0.70711,
                0.70711,
                -0.0,
                -0.0
            ],
            "dir": [
                -1.6,
                0.0,
                0.0
            ],
            "dims": [
                20.0,
                70.0,
                600.0
            ]
        },
        {
            "id": "group_0_travessa",
            "name": "Lateral Esquerda - Travessa Larga",
            "sub": "Travessa lateral",
            "group": "group_0",
            "groupLabel": "Lateral Esquerda",
            "size": [
                20.0,
                140.0,
                600.0
            ],
            "pos": [
                -255.0,
                225.0,
                0.0
            ],
            "rot": [
                3.14159,
                -0.0,
                -0.0
            ],
            "quaternion": [
                1.0,
                0.0,
                -0.0,
                0.0
            ],
            "dir": [
                -1.6,
                0.0,
                0.0
            ],
            "dims": [
                20.0,
                140.0,
                600.0
            ]
        },
        {
            "id": "group_0_pe_frontal",
            "name": "Lateral Esquerda - Pé Frontal",
            "sub": "Pé frontal",
            "group": "group_0",
            "groupLabel": "Lateral Esquerda",
            "size": [
                20.0,
                140.0,
                450.0
            ],
            "pos": [
                -275.0,
                225.0,
                230.0
            ],
            "rot": [
                1.5708,
                0.0,
                -0.0
            ],
            "quaternion": [
                0.70711,
                0.0,
                -0.0,
                0.70711
            ],
            "dir": [
                -1.6,
                0.0,
                0.0
            ],
            "dims": [
                20.0,
                140.0,
                450.0
            ]
        },
        {
            "id": "group_0_pe_traseiro",
            "name": "Lateral Esquerda - Pé Traseiro",
            "sub": "Pé traseiro",
            "group": "group_0",
            "groupLabel": "Lateral Esquerda",
            "size": [
                20.0,
                140.0,
                450.0
            ],
            "pos": [
                -235.0,
                225.0,
                -230.0
            ],
            "rot": [
                1.5708,
                0.0,
                -0.0
            ],
            "quaternion": [
                0.70711,
                0.0,
                -0.0,
                0.70711
            ],
            "dir": [
                -1.6,
                0.0,
                0.0
            ],
            "dims": [
                20.0,
                140.0,
                450.0
            ]
        },
        {
            "id": "group_1_braco",
            "name": "Lateral Direita - Apoio de Braço",
            "sub": "Braço",
            "group": "group_1",
            "groupLabel": "Lateral Direita",
            "size": [
                20.0,
                70.0,
                600.0
            ],
            "pos": [
                260.0,
                460.0,
                0.0
            ],
            "rot": [
                0.0,
                0.0,
                1.5708
            ],
            "quaternion": [
                0.0,
                0.0,
                0.70711,
                0.70711
            ],
            "dir": [
                1.6,
                0.0,
                0.0
            ],
            "dims": [
                20.0,
                70.0,
                600.0
            ]
        },
        {
            "id": "group_1_travessa",
            "name": "Lateral Direita - Travessa Larga",
            "sub": "Travessa lateral",
            "group": "group_1",
            "groupLabel": "Lateral Direita",
            "size": [
                20.0,
                140.0,
                600.0
            ],
            "pos": [
                255.0,
                225.0,
                0.0
            ],
            "rot": [
                -0.0,
                0.0,
                -3.14159
            ],
            "quaternion": [
                0.0,
                0.0,
                1.0,
                0.0
            ],
            "dir": [
                1.6,
                0.0,
                0.0
            ],
            "dims": [
                20.0,
                140.0,
                600.0
            ]
        },
        {
            "id": "group_1_pe_frontal",
            "name": "Lateral Direita - Pé Frontal",
            "sub": "Pé frontal",
            "group": "group_1",
            "groupLabel": "Lateral Direita",
            "size": [
                20.0,
                140.0,
                450.0
            ],
            "pos": [
                275.0,
                225.0,
                230.0
            ],
            "rot": [
                1.5708,
                -0.0,
                -3.14159
            ],
            "quaternion": [
                -0.0,
                -0.70711,
                0.70711,
                0.0
            ],
            "dir": [
                1.6,
                0.0,
                0.0
            ],
            "dims": [
                20.0,
                140.0,
                450.0
            ]
        },
        {
            "id": "group_1_pe_traseiro",
            "name": "Lateral Direita - Pé Traseiro",
            "sub": "Pé traseiro",
            "group": "group_1",
            "groupLabel": "Lateral Direita",
            "size": [
                20.0,
                140.0,
                450.0
            ],
            "pos": [
                235.0,
                225.0,
                -230.0
            ],
            "rot": [
                1.5708,
                -0.0,
                -3.14159
            ],
            "quaternion": [
                -0.0,
                -0.70711,
                0.70711,
                0.0
            ],
            "dir": [
                1.6,
                0.0,
                0.0
            ],
            "dims": [
                20.0,
                140.0,
                450.0
            ]
        },
        {
            "id": "group_2_suporte_frente",
            "name": "Assento - Travessa Suporte Frontal",
            "sub": "Suporte frontal assento",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [
                20.0,
                70.0,
                490.0
            ],
            "pos": [
                -0.0,
                258.0,
                272.6
            ],
            "rot": [
                1.7942,
                -1.5708,
                0.0
            ],
            "quaternion": [
                -0.55262,
                -0.44115,
                0.55262,
                0.44116
            ],
            "dir": [
                0.0,
                0.8,
                1.2
            ],
            "dims": [
                20.0,
                70.0,
                490.0
            ]
        },
        {
            "id": "group_2_suporte_tras",
            "name": "Assento - Travessa Suporte Traseira",
            "sub": "Suporte traseiro assento",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [
                20.0,
                70.0,
                490.0
            ],
            "pos": [
                -0.0,
                173.8,
                -98.0
            ],
            "rot": [
                1.7942,
                -1.5708,
                0.0
            ],
            "quaternion": [
                -0.55262,
                -0.44115,
                0.55262,
                0.44116
            ],
            "dir": [
                0.0,
                0.8,
                1.2
            ],
            "dims": [
                20.0,
                70.0,
                490.0
            ]
        },
        {
            "id": "group_2_tabua_esq",
            "name": "Assento - Tábua Lateral Esquerda",
            "sub": "Tábua assento",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [
                20.0,
                140.0,
                450.0
            ],
            "pos": [
                -175.0,
                235.4,
                82.8
            ],
            "rot": [
                -0.2234,
                0.0,
                1.5708
            ],
            "quaternion": [
                -0.07882,
                0.07882,
                0.7027,
                0.7027
            ],
            "dir": [
                0.0,
                0.8,
                1.2
            ],
            "dims": [
                20.0,
                140.0,
                450.0
            ]
        },
        {
            "id": "group_2_tabua_dir",
            "name": "Assento - Tábua Lateral Direita",
            "sub": "Tábua assento",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [
                20.0,
                140.0,
                450.0
            ],
            "pos": [
                175.0,
                235.4,
                82.8
            ],
            "rot": [
                -0.2234,
                0.0,
                1.5708
            ],
            "quaternion": [
                -0.07882,
                0.07882,
                0.7027,
                0.7027
            ],
            "dir": [
                0.0,
                0.8,
                1.2
            ],
            "dims": [
                20.0,
                140.0,
                450.0
            ]
        },
        {
            "id": "group_2_tabua_centro",
            "name": "Assento - Tábua Central",
            "sub": "Tábua assento",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [
                20.0,
                140.0,
                450.0
            ],
            "pos": [
                0.0,
                235.4,
                82.8
            ],
            "rot": [
                -0.2234,
                0.0,
                1.5708
            ],
            "quaternion": [
                -0.07882,
                0.07882,
                0.7027,
                0.7027
            ],
            "dir": [
                0.0,
                0.8,
                1.2
            ],
            "dims": [
                20.0,
                140.0,
                450.0
            ]
        },
        {
            "id": "group_3_tabua_esq",
            "name": "Encosto - Tábua Lateral Esquerda",
            "sub": "Tábua encosto",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [
                20.0,
                140.0,
                445.0
            ],
            "pos": [
                -155.0,
                423.1,
                -261.7
            ],
            "rot": [
                -2.00015,
                -0.0,
                -1.5708
            ],
            "quaternion": [
                0.59504,
                0.59504,
                0.38201,
                -0.38201
            ],
            "dir": [
                0.0,
                1.2,
                -1.2
            ],
            "dims": [
                20.0,
                140.0,
                445.0
            ]
        },
        {
            "id": "group_3_tabua_centro",
            "name": "Encosto - Tábua Central",
            "sub": "Tábua encosto",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [
                20.0,
                140.0,
                445.0
            ],
            "pos": [
                -0.0,
                423.1,
                -261.7
            ],
            "rot": [
                -2.00015,
                -0.0,
                -1.5708
            ],
            "quaternion": [
                0.59504,
                0.59504,
                0.38201,
                -0.38201
            ],
            "dir": [
                0.0,
                1.2,
                -1.2
            ],
            "dims": [
                20.0,
                140.0,
                445.0
            ]
        },
        {
            "id": "group_3_suporte_topo",
            "name": "Encosto - Travessa Traseira Superior",
            "sub": "Travessa superior encosto",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [
                20.0,
                70.0,
                450.0
            ],
            "pos": [
                0.0,
                585.3,
                -357.9
            ],
            "rot": [
                2.71224,
                1.5708,
                0.0
            ],
            "quaternion": [
                0.69088,
                0.15064,
                0.69088,
                0.15064
            ],
            "dir": [
                0.0,
                1.2,
                -1.2
            ],
            "dims": [
                20.0,
                70.0,
                450.0
            ]
        },
        {
            "id": "group_3_tabua_dir",
            "name": "Encosto - Tábua Lateral Direita",
            "sub": "Tábua encosto",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [
                20.0,
                140.0,
                445.0
            ],
            "pos": [
                155.0,
                423.1,
                -261.7
            ],
            "rot": [
                -2.00015,
                -0.0,
                -1.5708
            ],
            "quaternion": [
                0.59504,
                0.59504,
                0.38201,
                -0.38201
            ],
            "dir": [
                0.0,
                1.2,
                -1.2
            ],
            "dims": [
                20.0,
                140.0,
                445.0
            ]
        },
        {
            "id": "group_3_suporte_base",
            "name": "Encosto - Travessa Traseira Inferior",
            "sub": "Travessa inferior encosto",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [
                20.0,
                70.0,
                450.0
            ],
            "pos": [
                0.0,
                244.3,
                -201.8
            ],
            "rot": [
                2.71224,
                1.5708,
                0.0
            ],
            "quaternion": [
                0.69088,
                0.15064,
                0.69088,
                0.15064
            ],
            "dir": [
                0.0,
                1.2,
                -1.2
            ],
            "dims": [
                20.0,
                70.0,
                450.0
            ]
        }
    ]
},

  armario: {
    title: 'Armário Aéreo de 2 Portas',
    dimensions: '800 x 600 x 350 mm',
    description: 'Caixaria clássica em MDF 15mm com 2 portas de giro e prateleira divisória central.',
    pieces: [
      { id: 'lateral_esq', name: 'Lateral Esquerda', size: [15, 600, 350], pos: [-392.5, 300, 0], rot: [0, 0, 0], dir: [-1.2, 0, 0] },
      { id: 'lateral_dir', name: 'Lateral Direita', size: [15, 600, 350], pos: [392.5, 300, 0], rot: [0, 0, 0], dir: [1.2, 0, 0] },
      { id: 'tampo_sup', name: 'Tampo Superior', size: [770, 15, 350], pos: [0, 592.5, 0], rot: [0, 0, 0], dir: [0, 1.2, 0] },
      { id: 'base_inf', name: 'Base Inferior', size: [770, 15, 350], pos: [0, 7.5, 0], rot: [0, 0, 0], dir: [0, -1.2, 0] },
      { id: 'prat_meio', name: 'Prateleira Interna', size: [768, 15, 330], pos: [0, 300, -10], rot: [0, 0, 0], dir: [0, 0, 0.6] },
      { id: 'porta_esq', name: 'Porta Esquerda', size: [396, 596, 15], pos: [-199, 300, 182.5], rot: [0, 0, 0], dir: [-0.6, 0, 1.5] },
      { id: 'porta_dir', name: 'Porta Direita', size: [396, 596, 15], pos: [199, 300, 182.5], rot: [0, 0, 0], dir: [0.6, 0, 1.5] },
    ]
  },

  nicho: {
    title: 'Nicho Retangular de Parede',
    dimensions: '600 x 400 x 200 mm',
    description: 'Nicho decorativo clean em MDF 15mm ideal para livros e decoração suspensa.',
    pieces: [
      { id: 'tampo', name: 'Tampo Superior', size: [600, 15, 200], pos: [0, 392.5, 0], rot: [0, 0, 0], dir: [0, 1.2, 0] },
      { id: 'base', name: 'Base Inferior', size: [600, 15, 200], pos: [0, 7.5, 0], rot: [0, 0, 0], dir: [0, -1.2, 0] },
      { id: 'lateral_esq', name: 'Lateral Esquerda', size: [15, 370, 200], pos: [-292.5, 200, 0], rot: [0, 0, 0], dir: [-1.2, 0, 0] },
      { id: 'lateral_dir', name: 'Lateral Direita', size: [15, 370, 200], pos: [292.5, 200, 0], rot: [0, 0, 0], dir: [1.2, 0, 0] },
      { id: 'fundo', name: 'Fundo (MDF 6mm)', size: [580, 380, 6], pos: [0, 200, -97], rot: [0, 0, 0], dir: [0, 0, -1.5] },
    ]
  }
};


function showWebGLError(container) {
  container.innerHTML = `
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color:#f8fafc; padding:30px; text-align:center;">
      <div style="background:#27272a; border:1px solid #ef4444; border-radius:12px; padding:30px; max-width:620px; box-shadow:0 20px 25px -5px rgba(0,0,0,0.5);">
        <div style="font-size:3rem; margin-bottom:10px;">⚠️</div>
        <h2 style="color:#ef4444; margin-bottom:12px; font-size:1.4rem;">Aceleração Gráfica (WebGL) Desativada no Navegador</h2>
        <p style="color:#cbd5e1; font-size:0.92rem; line-height:1.6; margin-bottom:20px;">
          O Opera/Chromium desativou a aceleração 3D por hardware (<strong>GL_VENDOR = Disabled</strong>). Isso ocorre após crash do processo gráfico ou desativação de aceleração de hardware.
        </p>
        <div style="text-align:left; background:#18181b; padding:16px 20px; border-radius:8px; font-size:0.88rem; line-height:1.7; margin-bottom:24px;">
          <strong style="color:#fbbf24;">Como reativar em menos de 1 minuto:</strong>
          <ol style="margin-left:20px; margin-top:8px;">
            <li>Digite <code style="background:#3f3f46; padding:2px 6px; border-radius:4px; color:#fbbf24;">opera://restart</code> na barra de endereços e pressione Enter.</li>
            <li>Acesse <code style="background:#3f3f46; padding:2px 6px; border-radius:4px; color:#fbbf24;">opera://settings/system</code> e ative <strong>"Usar aceleração de hardware quando disponível"</strong>.</li>
            <li>No Windows, pressione o atalho <kbd style="background:#3f3f46; padding:2px 6px; border-radius:4px;">Win + Ctrl + Shift + B</kbd> para resetar o driver da GPU.</li>
            <li>Se persistir, abra <code style="background:#3f3f46; padding:2px 6px; border-radius:4px; color:#fbbf24;">opera://flags/#ignore-gpu-blocklist</code> e mude para <strong>Enabled</strong>.</li>
          </ol>
        </div>
        <button onclick="window.location.reload()" style="background:#f59e0b; color:#0f172a; font-weight:700; border:none; padding:10px 22px; border-radius:6px; cursor:pointer; font-size:0.95rem;">
          🔄 Tentar Novamente
        </button>
      </div>
    </div>
  `;
}

// --- Inicialização Three.js ---
function init() {
  const container = document.getElementById('canvas-container');

  scene = new THREE.Scene();
  scene.background = new THREE.Color('#1a1c23');

  camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 1, 10000);
  camera.position.set(950, 750, 1250);

  // Tentativa de inicialização com fallbacks graduais caso a GPU esteja em modo de economia ou tenha travado
  const rendererOptions = [
    { antialias: true, powerPreference: 'high-performance' },
    { antialias: true, powerPreference: 'default' },
    { antialias: false, failIfMajorPerformanceCaveat: false },
    { antialias: false, powerPreference: 'low-power', failIfMajorPerformanceCaveat: false }
  ];

  renderer = null;
  for (const opt of rendererOptions) {
    try {
      renderer = new THREE.WebGLRenderer(opt);
      if (renderer) break;
    } catch (e) {
      console.warn('Tentativa WebGL falhou com opções:', opt, e);
    }
  }

  if (!renderer) {
    showWebGLError(container);
    return;
  }

  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.target.set(0, 300, 0);

  // Iluminação de Estúdio
  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444455, 1.3);
  hemiLight.position.set(0, 1000, 0);
  scene.add(hemiLight);

  const dirLight = new THREE.DirectionalLight(0xffffff, 1.6);
  dirLight.position.set(600, 1200, 800);
  dirLight.castShadow = true;
  dirLight.shadow.mapSize.width = 2048;
  dirLight.shadow.mapSize.height = 2048;
  scene.add(dirLight);

  const fillLight = new THREE.DirectionalLight(0xffeedd, 0.7);
  fillLight.position.set(-600, 400, -600);
  scene.add(fillLight);

  // Grade de chão
  const grid = new THREE.GridHelper(2200, 44, 0x4a5568, 0x2d3748);
  grid.position.y = 0;
  scene.add(grid);

  raycaster = new THREE.Raycaster();
  mouse = new THREE.Vector2();

  window.addEventListener('resize', onWindowResize);
  renderer.domElement.addEventListener('pointerdown', onPointerClick);

  setupUI();

  // Verifica se o assistente gerou um projeto ativo no chat
  if (window.CURRENT_PROJECT && window.CURRENT_PROJECT.pieces) {
    PROJECTS['chat'] = window.CURRENT_PROJECT;
    const projSelect = document.getElementById('projectSelect');
    const opt = document.createElement('option');
    opt.value = 'chat';
    opt.innerText = `🌟 ${window.CURRENT_PROJECT.title || 'Projeto Atual do Chat'}`;
    projSelect.insertBefore(opt, projSelect.firstChild);
    projSelect.value = 'chat';
    loadProject('chat');
  } else {
    loadProject('krat');
  }

  animate();
}

// --- Criação das Peças 3D ---
function loadProject(projectKey) {
  const project = PROJECTS[projectKey];
  if (!project) return;

  // Limpa malhas anteriores
  currentMeshes.forEach(mesh => scene.remove(mesh));
  currentMeshes = [];
  selectedMesh = null;

  // Atualiza painel
  document.getElementById('panelProjectTitle').innerText = project.title;
  document.getElementById('panelPieceCount').innerText = `${project.pieces.length} Peças`;
  document.getElementById('summaryDimensions').innerText = project.dimensions;
  document.getElementById('summaryDesc').innerText = project.description;

  const partsListEl = document.getElementById('partsList');
  partsListEl.innerHTML = '';

  const mat = getMaterial(currentMaterialType);

  project.pieces.forEach(p => {
    const geom = new THREE.BoxGeometry(p.size[0], p.size[1], p.size[2]);
    const mesh = new THREE.Mesh(geom, mat.clone());
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    mesh.position.set(p.pos[0], p.pos[1], p.pos[2]);
    if (p.quaternion) {
      mesh.quaternion.set(p.quaternion[0], p.quaternion[1], p.quaternion[2], p.quaternion[3]);
    } else if (p.rot) {
      mesh.rotation.set(p.rot[0], p.rot[1], p.rot[2]);
    }

    // Linhas de contorno chanfradas (estética técnica de marcenaria)
    const edges = new THREE.EdgesGeometry(geom);
    const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x222222, linewidth: 1.5 }));
    mesh.add(line);

    mesh.userData = {
      id: p.id,
      name: p.name,
      group: p.group || '',
      groupLabel: p.groupLabel || '',
      basePos: new THREE.Vector3(p.pos[0], p.pos[1], p.pos[2]),
      explodeDir: new THREE.Vector3(p.dir[0], p.dir[1], p.dir[2]).normalize(),
      size: p.size,
      dims: p.dims || p.size,
    };

    scene.add(mesh);
    currentMeshes.push(mesh);

    // Adiciona na lista do painel lateral
    const li = document.createElement('li');
    li.innerText = `${p.name} (${p.size[0]}x${p.size[1]}x${p.size[2]}mm)`;
    li.dataset.pieceId = p.id;
    li.addEventListener('click', () => selectPiece(mesh));
    partsListEl.appendChild(li);
  });

  // Atualiza visão explodida para o valor atual do slider
  updateExplode(parseFloat(document.getElementById('explodeSlider').value));
}

// --- Atualização do Slider de Visão Explodida ---
function updateExplode(percentage) {
  document.getElementById('explodeValue').innerText = `${Math.round(percentage)}%`;
  const factor = (percentage / 100) * 380; // até 380mm de afastamento máximo

  currentMeshes.forEach(mesh => {
    const base = mesh.userData.basePos;
    const dir = mesh.userData.explodeDir;
    mesh.position.set(
      base.x + dir.x * factor,
      base.y + dir.y * factor,
      base.z + dir.z * factor
    );
  });
}

// --- Seleção e Inspeção de Peça ---
function selectPiece(mesh) {
  if (selectedMesh && selectedMesh.material) {
    selectedMesh.material.emissive.setHex(0x000000);
  }

  selectedMesh = mesh;
  if (!mesh) {
    document.getElementById('pieceDetails').innerHTML = '<p class="placeholder-text">Clique sobre qualquer peça no modelo 3D para inspecionar medidas.</p>';
    return;
  }

  // Destaque brilhante
  mesh.material.emissive.setHex(0x554015);

  const u = mesh.userData;
  const s = u.dims || u.size;
  const grpBadge = u.groupLabel ? `<div class="piece-stat-row"><span class="piece-stat-label">Módulo:</span> <span class="piece-stat-value" style="color: #fbbf24;">${u.groupLabel}</span></div>` : '';
  document.getElementById('pieceDetails').innerHTML = `
    <div class="piece-stat-row"><span class="piece-stat-label">Nome:</span> <span class="piece-stat-value">${u.name}</span></div>
    ${grpBadge}
    <div class="piece-stat-row"><span class="piece-stat-label">Corte Bruto:</span> <span class="piece-stat-value">${s[0]} x ${s[1]} x ${s[2]} mm</span></div>
    <div class="piece-stat-row"><span class="piece-stat-label">Espessura:</span> <span class="piece-stat-value">${Math.min(s[0], s[1], s[2])} mm</span></div>
    <div class="piece-stat-row"><span class="piece-stat-label">Posição:</span> <span class="piece-stat-value">X:${Math.round(u.basePos.x)} Y:${Math.round(u.basePos.y)} Z:${Math.round(u.basePos.z)}</span></div>
  `;

  document.querySelectorAll('.parts-list li').forEach(li => {
    li.classList.toggle('active', li.dataset.pieceId === u.id);
  });
}

function onPointerClick(event) {
  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(currentMeshes);

  if (intersects.length > 0) {
    selectPiece(intersects[0].object);
  } else {
    selectPiece(null);
  }
}

// --- Controles de UI ---
function setupUI() {
  document.getElementById('projectSelect').addEventListener('change', (e) => {
    loadProject(e.target.value);
  });

  document.getElementById('materialSelect').addEventListener('change', (e) => {
    currentMaterialType = e.target.value;
    const newMat = getMaterial(currentMaterialType);
    currentMeshes.forEach(mesh => {
      mesh.material = newMat.clone();
    });
  });

  document.getElementById('explodeSlider').addEventListener('input', (e) => {
    updateExplode(parseFloat(e.target.value));
  });

  document.getElementById('btnResetView').addEventListener('click', () => {
    camera.position.set(850, 650, 950);
    controls.target.set(0, 310, 0);
  });

  const btnFront = document.getElementById('btnViewFront');
  if (btnFront) {
    btnFront.addEventListener('click', () => {
      camera.position.set(0, 310, 1200);
      controls.target.set(0, 310, 0);
    });
  }

  const btnSide = document.getElementById('btnViewSide');
  if (btnSide) {
    btnSide.addEventListener('click', () => {
      camera.position.set(1200, 310, 0);
      controls.target.set(0, 310, 0);
    });
  }

  const btnTop = document.getElementById('btnViewTop');
  if (btnTop) {
    btnTop.addEventListener('click', () => {
      camera.position.set(0, 1300, 0.01);
      controls.target.set(0, 310, 0);
    });
  }

  document.getElementById('btnAutoRotate').addEventListener('click', (e) => {
    autoRotate = !autoRotate;
    controls.autoRotate = autoRotate;
    e.target.style.borderColor = autoRotate ? '#fbbf24' : '#4a5568';
    e.target.style.color = autoRotate ? '#fbbf24' : '#f1f5f9';
  });

  // Botão de recarga dinâmica do projeto atual do chat
  const btnReload = document.getElementById('btnReloadProject');
  if (btnReload) {
    btnReload.addEventListener('click', () => {
      const script = document.createElement('script');
      script.src = `current_project.js?v=${Date.now()}`;
      script.onload = () => {
        if (window.CURRENT_PROJECT) {
          PROJECTS['chat'] = window.CURRENT_PROJECT;
          const projSelect = document.getElementById('projectSelect');
          let chatOpt = Array.from(projSelect.options).find(o => o.value === 'chat');
          if (!chatOpt) {
            chatOpt = document.createElement('option');
            chatOpt.value = 'chat';
            projSelect.insertBefore(chatOpt, projSelect.firstChild);
          }
          chatOpt.innerText = `🌟 ${window.CURRENT_PROJECT.title || 'Projeto Atual do Chat'}`;
          projSelect.value = 'chat';
          loadProject('chat');
        }
      };
      document.body.appendChild(script);
    });
  }

  document.getElementById('fileInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const customProject = JSON.parse(event.target.result);
        PROJECTS['custom'] = customProject;
        loadProject('custom');
      } catch (err) {
        alert('Erro ao carregar o arquivo JSON do projeto: ' + err.message);
      }
    };
    reader.readAsText(file);
  });
}

function onWindowResize() {
  const container = document.getElementById('canvas-container');
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

window.onload = init;
