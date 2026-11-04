/**
 * Pet Care Companion - Professional 3D Interactive WebGL Background
 * Built with Three.js (r128)
 * Features:
 *  - Dynamic Dual-Theme Support: High-Contrast Vibrant Colors in Light Mode (White Background) & Neon Glow in Dark Mode
 *  - 3D Harmonic Wave Particle Grid with interactive mouse ripples and harmonic deformation
 *  - Floating Holographic Wireframe Polyhedra (Icosahedrons, Toruses, Octahedrons, Dodecahedrons, Tetrahedrons)
 *  - Dynamic Constellation Network (Cluster nodes & distance-connected neural lines)
 *  - Responsive Camera Parallax & Elastic Wave Motion
 *  - 60fps Animation Loop with Real-Time Theme Transition Listener
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
      // 1. Determine Initial Theme (Light / Dark)
      const isInitialLight = (document.documentElement.getAttribute('data-bs-theme') === 'light') ||
        (localStorage.getItem('petcare_theme_preference') === 'light');

      // 2. Scene & Depth Atmospheric Fog
      const scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(
        isInitialLight ? 0xffffff : 0x090d16,
        isInitialLight ? 0.0055 : 0.0075
      );

      // 3. Perspective Camera
      const camera = new THREE.PerspectiveCamera(
        60,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      );
      camera.position.set(0, 15, 80);

      // 4. WebGL Renderer with Alpha Channel
      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      // 5. Lighting Setup
      const ambientLight = new THREE.AmbientLight(
        isInitialLight ? 0xffffff : 0x818cf8,
        isInitialLight ? 0.95 : 0.6
      );
      scene.add(ambientLight);

      const pointLight1 = new THREE.PointLight(
        isInitialLight ? 0x059669 : 0x34d399,
        isInitialLight ? 1.4 : 1.2,
        120
      );
      pointLight1.position.set(30, 20, 20);
      scene.add(pointLight1);

      const pointLight2 = new THREE.PointLight(
        isInitialLight ? 0x4338ca : 0x818cf8,
        isInitialLight ? 1.4 : 1.2,
        120
      );
      pointLight2.position.set(-30, -20, 30);
      scene.add(pointLight2);

      // 6. Smooth Radial Particle Texture (Clean Alpha Mask for Perfect Color Multiplication)
      const canvasTexture = document.createElement('canvas');
      canvasTexture.width = 64;
      canvasTexture.height = 64;
      const ctx = canvasTexture.getContext('2d');
      const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
      gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
      gradient.addColorStop(0.35, 'rgba(255, 255, 255, 0.9)');
      gradient.addColorStop(0.7, 'rgba(255, 255, 255, 0.3)');
      gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 64, 64);
      const particleTex = new THREE.CanvasTexture(canvasTexture);

      // 7. 3D Wave Particle Grid (42 x 42 = 1,764 Particles)
      const countX = 42;
      const countY = 42;
      const totalParticles = countX * countY;
      const positions = new Float32Array(totalParticles * 3);
      const originalPositions = new Float32Array(totalParticles * 3);
      const colors = new Float32Array(totalParticles * 3);

      const spacingX = 4.8;
      const spacingY = 4.8;
      let pIdx = 0;

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

          pIdx++;
        }
      }

      const particleGeo = new THREE.BufferGeometry();
      particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      const particleMat = new THREE.PointsMaterial({
        size: isInitialLight ? 2.4 : 2.2,
        map: particleTex,
        vertexColors: true,
        transparent: true,
        opacity: isInitialLight ? 0.45 : 0.55,
        blending: isInitialLight ? THREE.NormalBlending : THREE.AdditiveBlending,
        depthWrite: false
      });

      const particleGrid = new THREE.Points(particleGeo, particleMat);
      scene.add(particleGrid);

      // 8. Floating Holographic Wireframe Polyhedra
      const floatingShapes = [];
      const geometries = [
        new THREE.IcosahedronGeometry(4.2, 1),
        new THREE.TorusGeometry(3.6, 0.9, 16, 32),
        new THREE.OctahedronGeometry(3.8, 0),
        new THREE.DodecahedronGeometry(3.5, 0),
        new THREE.TetrahedronGeometry(3.2, 0)
      ];

      const darkShapeColors = [0x818cf8, 0x34d399, 0x38bdf8, 0xa78bfa, 0x6ee7b7];
      const lightShapeColors = [0x4338ca, 0x059669, 0x0284c7, 0x7c3aed, 0xd97706];

      for (let k = 0; k < 14; k++) {
        const geom = geometries[k % geometries.length];
        const color = isInitialLight
          ? lightShapeColors[k % lightShapeColors.length]
          : darkShapeColors[k % darkShapeColors.length];

        const wireMat = new THREE.MeshBasicMaterial({
          color: color,
          wireframe: true,
          transparent: true,
          opacity: isInitialLight ? 0.15 : 0.16
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

      // 9. Neural Constellation Network
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
        size: isInitialLight ? 3.0 : 2.8,
        color: isInitialLight ? 0x4338ca : 0x38bdf8,
        map: particleTex,
        transparent: true,
        opacity: isInitialLight ? 0.40 : 0.45,
        blending: isInitialLight ? THREE.NormalBlending : THREE.AdditiveBlending,
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
        color: isInitialLight ? 0x6366f1 : 0x818cf8,
        transparent: true,
        opacity: isInitialLight ? 0.10 : 0.12,
        blending: isInitialLight ? THREE.NormalBlending : THREE.AdditiveBlending
      });
      const constellationLines = new THREE.LineSegments(lineGeo, lineMat);
      scene.add(constellationLines);

      // 10. Dynamic Theme Adaptation Function
      function applyThreeTheme(isLight) {
        // High-contrast vibrant colors on white: Deep Royal Indigo, Vivid Cyan, Lush Emerald Teal
        // Luminescent neon colors on dark: Light Violet, Neon Sky Blue, Neon Emerald
        const col1 = isLight ? new THREE.Color(0x4338ca) : new THREE.Color(0x818cf8);
        const col2 = isLight ? new THREE.Color(0x0284c7) : new THREE.Color(0x38bdf8);
        const col3 = isLight ? new THREE.Color(0x059669) : new THREE.Color(0x34d399);

        const colorAttr = particleGeo.attributes.color;
        let idx = 0;
        for (let ix = 0; ix < countX; ix++) {
          for (let iy = 0; iy < countY; iy++) {
            const factor = (ix + iy) / (countX + countY);
            let chosenColor;
            if (factor < 0.33) {
              chosenColor = col1.clone().lerp(col2, factor * 3);
            } else if (factor < 0.66) {
              chosenColor = col2.clone().lerp(col3, (factor - 0.33) * 3);
            } else {
              chosenColor = col3.clone().lerp(col1, (factor - 0.66) * 3);
            }
            colorAttr.array[idx * 3] = chosenColor.r;
            colorAttr.array[idx * 3 + 1] = chosenColor.g;
            colorAttr.array[idx * 3 + 2] = chosenColor.b;
            idx++;
          }
        }
        colorAttr.needsUpdate = true;

        // Subtle, elegant opacities that never dominate text
        particleMat.blending = isLight ? THREE.NormalBlending : THREE.AdditiveBlending;
        particleMat.opacity = isLight ? 0.45 : 0.55;
        particleMat.size = isLight ? 2.4 : 2.2;
        particleMat.needsUpdate = true;

        clusterMat.blending = isLight ? THREE.NormalBlending : THREE.AdditiveBlending;
        clusterMat.color.setHex(isLight ? 0x4338ca : 0x38bdf8);
        clusterMat.opacity = isLight ? 0.40 : 0.45;
        clusterMat.size = isLight ? 3.0 : 2.8;
        clusterMat.needsUpdate = true;

        lineMat.blending = isLight ? THREE.NormalBlending : THREE.AdditiveBlending;
        lineMat.color.setHex(isLight ? 0x6366f1 : 0x818cf8);
        lineMat.opacity = isLight ? 0.10 : 0.12;
        lineMat.needsUpdate = true;

        const currentShapePalette = isLight ? lightShapeColors : darkShapeColors;
        floatingShapes.forEach((mesh, k) => {
          mesh.material.color.setHex(currentShapePalette[k % currentShapePalette.length]);
          mesh.material.opacity = isLight ? 0.15 : 0.16;
          mesh.material.needsUpdate = true;
        });

        if (scene.fog) {
          scene.fog.color.setHex(isLight ? 0xffffff : 0x090d16);
          scene.fog.density = isLight ? 0.008 : 0.0085;
        }

        ambientLight.color.setHex(isLight ? 0xffffff : 0x818cf8);
        ambientLight.intensity = isLight ? 0.8 : 0.5;
        pointLight1.color.setHex(isLight ? 0x059669 : 0x34d399);
        pointLight2.color.setHex(isLight ? 0x4338ca : 0x818cf8);
      }

      // Initialize theme colors immediately
      applyThreeTheme(isInitialLight);

      // Listen for instant dynamic theme changes
      window.addEventListener('petcareThemeChanged', (e) => {
        const isLight = e.detail && e.detail.theme === 'light';
        applyThreeTheme(isLight);
      });

      // 11. Smooth Mouse Tracking & Parallax
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

      // 12. Master 60fps Animation Loop
      const clock = new THREE.Clock();

      function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        smoothMouseX += (mouseX - smoothMouseX) * 0.045;
        smoothMouseY += (mouseY - smoothMouseY) * 0.045;

        // Animate Wave Harmonics on Particle Grid
        const posArray = particleGrid.geometry.attributes.position.array;
        let index = 0;

        for (let ix = 0; ix < countX; ix++) {
          for (let iy = 0; iy < countY; iy++) {
            const origX = originalPositions[index * 3];
            const origY = originalPositions[index * 3 + 1];

            const wave1 = Math.sin(ix * 0.28 + elapsedTime * 1.6) * 4.5;
            const wave2 = Math.cos(iy * 0.28 + elapsedTime * 1.3) * 4.5;
            const wave3 = Math.sin((ix + iy) * 0.18 + elapsedTime * 1.8) * 3.0;

            const dx = origX - (smoothMouseX * 50);
            const dy = origY - (-smoothMouseY * 35);
            const dist = Math.sqrt(dx * dx + dy * dy);
            const mouseRipple = dist < 35 ? (35 - dist) * 0.4 : 0;

            posArray[index * 3 + 2] = wave1 + wave2 + wave3 + mouseRipple;
            index++;
          }
        }
        particleGrid.geometry.attributes.position.needsUpdate = true;

        // Rotation & drift
        particleGrid.rotation.y = elapsedTime * 0.035 + smoothMouseX * 0.15;
        particleGrid.rotation.x = Math.sin(elapsedTime * 0.2) * 0.05 - smoothMouseY * 0.12;

        clusterPoints.rotation.y = -elapsedTime * 0.02 + smoothMouseX * 0.08;
        constellationLines.rotation.y = -elapsedTime * 0.02 + smoothMouseX * 0.08;

        floatingShapes.forEach((mesh) => {
          mesh.rotation.x += mesh.userData.rotX;
          mesh.rotation.y += mesh.userData.rotY;
          mesh.rotation.z += mesh.userData.rotZ;

          mesh.position.y = mesh.userData.initialY + Math.sin(elapsedTime * mesh.userData.speedY) * 7;
          mesh.position.x = mesh.userData.initialX + Math.cos(elapsedTime * mesh.userData.speedX) * 4;
        });

        camera.position.x = smoothMouseX * 18;
        camera.position.y = 15 - smoothMouseY * 12;
        camera.lookAt(0, 0, 0);

        renderer.render(scene, camera);
      }

      animate();

      // 13. Responsive Window Resizing
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
