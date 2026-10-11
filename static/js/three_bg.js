/**
 * Pet Care Companion - Professional 3D Interactive WebGL Background
 * Built with Three.js (r128)
 * Features:
 *  - 3D Harmonic Wave Particle Grid with dynamic vertex coloring
 *  - Interactive Mouse Parallax & Elastic Wave Deformation
 *  - Floating Holographic Wireframe Polyhedra (Icosahedrons, Toruses, Octahedrons)
 *  - Dynamic Constellation Lines & Ambient Atmospheric Depth Fog
 *  - High-performance 60fps animation loop with automated resize handling
 */

(function init3DBackground() {
  function start() {
    const canvas = document.getElementById('three-bg-canvas');
    if (!canvas) return;

    if (typeof THREE === 'undefined') {
      setTimeout(start, 100);
      return;
    }

    try {
      // 1. Scene & Camera Setup
      const scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x090d16, 0.0075);

      const camera = new THREE.PerspectiveCamera(
        60,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      );
      camera.position.set(0, 15, 80);

      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      // 2. Ambient & Subtle Point Lighting
      const ambientLight = new THREE.AmbientLight(0x818cf8, 0.6);
      scene.add(ambientLight);

      const pointLight1 = new THREE.PointLight(0x34d399, 1.2, 120);
      pointLight1.position.set(30, 20, 20);
      scene.add(pointLight1);

      const pointLight2 = new THREE.PointLight(0x818cf8, 1.2, 120);
      pointLight2.position.set(-30, -20, 30);
      scene.add(pointLight2);

      // 3. 3D Wave Particle Grid (42 x 42 = 1,764 Particles)
      const countX = 42;
      const countY = 42;
      const totalParticles = countX * countY;
      const positions = new Float32Array(totalParticles * 3);
      const originalPositions = new Float32Array(totalParticles * 3);
      const colors = new Float32Array(totalParticles * 3);

      const colViolet = new THREE.Color(0x818cf8); // Luminescent violet
      const colCyan = new THREE.Color(0x38bdf8);   // Glowing sky blue
      const colEmerald = new THREE.Color(0x34d399);// Neon emerald

      let pIdx = 0;
      const spacingX = 4.8;
      const spacingY = 4.8;

      for (let ix = 0; ix < countX; ix++) {
        for (let iy = 0; iy < countY; iy++) {
          const x = (ix - countX / 2) * spacingX;
          const y = (iy - countY / 2) * spacingY - 10;
          const z = (Math.sin(ix * 0.3) + Math.cos(iy * 0.3)) * 6;

          positions[pIdx * 3] = x;
          positions[pIdx * 3 + 1] = y;
          positions[pIdx * 3 + 2] = z;

          originalPositions[pIdx * 3] = x;
          originalPositions[pIdx * 3 + 1] = y;
          originalPositions[pIdx * 3 + 2] = z;

          // Multi-harmonic color gradient
          const factor = (ix + iy) / (countX + countY);
          let chosenColor;
          if (factor < 0.33) {
            chosenColor = colViolet.clone().lerp(colCyan, factor * 3);
          } else if (factor < 0.66) {
            chosenColor = colCyan.clone().lerp(colEmerald, (factor - 0.33) * 3);
          } else {
            chosenColor = colEmerald.clone().lerp(colViolet, (factor - 0.66) * 3);
          }

          colors[pIdx * 3] = chosenColor.r;
          colors[pIdx * 3 + 1] = chosenColor.g;
          colors[pIdx * 3 + 2] = chosenColor.b;

          pIdx++;
        }
      }

      const particleGeo = new THREE.BufferGeometry();
      particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      // Create glowing circular particle texture
      const canvasTexture = document.createElement('canvas');
      canvasTexture.width = 64;
      canvasTexture.height = 64;
      const ctx = canvasTexture.getContext('2d');
      const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
      gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
      gradient.addColorStop(0.3, 'rgba(129, 140, 248, 0.85)');
      gradient.addColorStop(0.7, 'rgba(52, 211, 153, 0.35)');
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 64, 64);

      const particleTex = new THREE.CanvasTexture(canvasTexture);

      const particleMat = new THREE.PointsMaterial({
        size: 3.2,
        map: particleTex,
        vertexColors: true,
        transparent: true,
        opacity: 0.85,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });

      const particleGrid = new THREE.Points(particleGeo, particleMat);
      scene.add(particleGrid);

      // 4. Floating Holographic 3D Geometric Meshes
      const floatingShapes = [];
      const geometries = [
        new THREE.IcosahedronGeometry(4.2, 1),
        new THREE.TorusGeometry(3.6, 0.9, 16, 32),
        new THREE.OctahedronGeometry(3.8, 0),
        new THREE.DodecahedronGeometry(3.5, 0),
        new THREE.TetrahedronGeometry(3.2, 0)
      ];

      const shapeColors = [0x818cf8, 0x34d399, 0x38bdf8, 0xa78bfa, 0x6ee7b7];

      for (let k = 0; k < 14; k++) {
        const geom = geometries[k % geometries.length];
        const color = shapeColors[k % shapeColors.length];

        const wireMat = new THREE.MeshBasicMaterial({
          color: color,
          wireframe: true,
          transparent: true,
          opacity: 0.28
        });

        const shapeMesh = new THREE.Mesh(geom, wireMat);
        shapeMesh.position.set(
          (Math.random() - 0.5) * 160,
          (Math.random() - 0.5) * 110,
          (Math.random() - 0.5) * 70 - 10
        );

        shapeMesh.userData = {
          rotX: (Math.random() - 0.5) * 0.018 + 0.006,
          rotY: (Math.random() - 0.5) * 0.018 + 0.006,
          rotZ: (Math.random() - 0.5) * 0.012,
          speedY: Math.random() * 0.6 + 0.4,
          speedX: Math.random() * 0.4 + 0.2,
          initialY: shapeMesh.position.y,
          initialX: shapeMesh.position.x
        };

        scene.add(shapeMesh);
        floatingShapes.push(shapeMesh);
      }

      // 5. Neural Constellation Network (Floating cluster nodes + lines)
      const clusterCount = 36;
      const clusterPositions = new Float32Array(clusterCount * 3);
      for (let c = 0; c < clusterCount; c++) {
        clusterPositions[c * 3] = (Math.random() - 0.5) * 130;
        clusterPositions[c * 3 + 1] = (Math.random() - 0.5) * 90;
        clusterPositions[c * 3 + 2] = (Math.random() - 0.5) * 50 + 10;
      }

      const clusterGeo = new THREE.BufferGeometry();
      clusterGeo.setAttribute('position', new THREE.BufferAttribute(clusterPositions, 3));

      const clusterMat = new THREE.PointsMaterial({
        size: 4.5,
        color: 0x38bdf8,
        map: particleTex,
        transparent: true,
        opacity: 0.7,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });
      const clusterPoints = new THREE.Points(clusterGeo, clusterMat);
      scene.add(clusterPoints);

      // Constellation Connecting Lines
      const linePositions = [];
      for (let a = 0; a < clusterCount; a++) {
        for (let b = a + 1; b < clusterCount; b++) {
          const dx = clusterPositions[a * 3] - clusterPositions[b * 3];
          const dy = clusterPositions[a * 3 + 1] - clusterPositions[b * 3 + 1];
          const dz = clusterPositions[a * 3 + 2] - clusterPositions[b * 3 + 2];
          const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
          if (dist < 32) {
            linePositions.push(
              clusterPositions[a * 3], clusterPositions[a * 3 + 1], clusterPositions[a * 3 + 2],
              clusterPositions[b * 3], clusterPositions[b * 3 + 1], clusterPositions[b * 3 + 2]
            );
          }
        }
      }

      const lineGeo = new THREE.BufferGeometry();
      lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
      const lineMat = new THREE.LineBasicMaterial({
        color: 0x818cf8,
        transparent: true,
        opacity: 0.16,
        blending: THREE.AdditiveBlending
      });
      const constellationLines = new THREE.LineSegments(lineGeo, lineMat);
      scene.add(constellationLines);

      // 6. Smooth Mouse Coordinates Tracking & Parallax
      let mouseX = 0;
      let mouseY = 0;
      let smoothMouseX = 0;
      let smoothMouseY = 0;

      window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) / (window.innerWidth / 2);
        mouseY = (e.clientY - window.innerHeight / 2) / (window.innerHeight / 2);
      }, { passive: true });

      window.addEventListener('touchmove', (e) => {
        if (e.touches.length > 0) {
          mouseX = (e.touches[0].clientX - window.innerWidth / 2) / (window.innerWidth / 2);
          mouseY = (e.touches[0].clientY - window.innerHeight / 2) / (window.innerHeight / 2);
        }
      }, { passive: true });

      // 7. Master 60fps Animation Loop
      const clock = new THREE.Clock();

      function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        // Smooth Lerp for Mouse
        smoothMouseX += (mouseX - smoothMouseX) * 0.045;
        smoothMouseY += (mouseY - smoothMouseY) * 0.045;

        // Animate Wave Harmonics on Particle Grid
        const posArray = particleGrid.geometry.attributes.position.array;
        let index = 0;

        for (let ix = 0; ix < countX; ix++) {
          for (let iy = 0; iy < countY; iy++) {
            const origX = originalPositions[index * 3];
            const origY = originalPositions[index * 3 + 1];

            // Harmonic undulating waves
            const wave1 = Math.sin(ix * 0.28 + elapsedTime * 1.6) * 4.5;
            const wave2 = Math.cos(iy * 0.28 + elapsedTime * 1.3) * 4.5;
            const wave3 = Math.sin((ix + iy) * 0.18 + elapsedTime * 1.8) * 3.0;

            // Mouse repulsion distortion
            const dx = origX - (smoothMouseX * 50);
            const dy = origY - (-smoothMouseY * 35);
            const dist = Math.sqrt(dx * dx + dy * dy);
            const mouseRipple = dist < 35 ? (35 - dist) * 0.4 : 0;

            posArray[index * 3 + 2] = wave1 + wave2 + wave3 + mouseRipple;
            index++;
          }
        }
        particleGrid.geometry.attributes.position.needsUpdate = true;

        // Dynamic slight rotation on grid
        particleGrid.rotation.y = elapsedTime * 0.035 + smoothMouseX * 0.15;
        particleGrid.rotation.x = Math.sin(elapsedTime * 0.2) * 0.05 - smoothMouseY * 0.12;

        // Rotate & Drift Constellation
        clusterPoints.rotation.y = -elapsedTime * 0.02 + smoothMouseX * 0.08;
        constellationLines.rotation.y = -elapsedTime * 0.02 + smoothMouseX * 0.08;

        // Animate Floating Geometric Polyhedra
        floatingShapes.forEach((mesh) => {
          mesh.rotation.x += mesh.userData.rotX;
          mesh.rotation.y += mesh.userData.rotY;
          mesh.rotation.z += mesh.userData.rotZ;

          mesh.position.y = mesh.userData.initialY + Math.sin(elapsedTime * mesh.userData.speedY) * 7;
          mesh.position.x = mesh.userData.initialX + Math.cos(elapsedTime * mesh.userData.speedX) * 4;
        });

        // Camera Parallax
        camera.position.x = smoothMouseX * 18;
        camera.position.y = 15 - smoothMouseY * 12;
        camera.lookAt(0, 0, 0);

        renderer.render(scene, camera);
      }

      animate();

      // 8. Responsive Window Resizing
      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      }, { passive: true });

    } catch (err) {
      console.error('Three.js background initialization error:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
