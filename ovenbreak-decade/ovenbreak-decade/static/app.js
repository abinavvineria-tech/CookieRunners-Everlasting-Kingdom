// OvenBreak Decade — The Golden Run JavaScript
// Handles interactivity: menu, celebration, countdown, mini-game, memory oven

document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.querySelector('nav ul');
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Celebration button and panel
    const celebrateBtn = document.getElementById('celebrate-btn');
    const celebrationPanel = document.getElementById('celebration-panel');
    celebrateBtn.addEventListener('click', () => {
        celebrationPanel.classList.toggle('hidden');
    });

    // Countdown timer
    const countdownDisplay = document.getElementById('countdown-display');
    const anniversaryDate = new Date('October 27, 2026 00:00:00').getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = anniversaryDate - now;

        if (distance > 0) {
            // Before anniversary
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            countdownDisplay.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s until October 27, 2026 — Ten Years of CookieRun: OvenBreak`;
        } else if (distance === 0) {
            // Exactly on anniversary (unlikely to hit exactly, but handle)
            countdownDisplay.textContent = 'Happy 10th Anniversary!';
        } else {
            // After anniversary
            countdownDisplay.textContent = 'Celebrating 10 Years of CookieRun: OvenBreak!';
        }
    }

    // Update immediately and then every second
    updateCountdown();
    setInterval(updateCountdown, 1000);

    // Jump & Slide Arcade
    const canvas = document.getElementById('game-canvas');
    const ctx = canvas.getContext('2d');
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const restartBtn = document.getElementById('restart-btn');
    const scoreEl = document.getElementById('score');
    const bestScoreEl = document.getElementById('best-score');
    const instructionsEl = document.getElementById('instructions');
    const toggleInstructionsBtn = document.getElementById('toggle-instructions');

    // Game settings
    const GRAVITY = 0.6;
    const GAME_SPEED = 3;
    const INITIAL_OBSTACLE_INTERVAL = 1500; // ms
    const MIN_OBSTACLE_INTERVAL = 500; // ms
    const OBSTACLE_INTERVAL_DECREASE = 50; // per point

    // Game state
    let gameActive = false;
    let gamePaused = false;
    let score = 0;
    let bestScore = 0;
    let obstacleTimer = 0;
    let obstacleInterval = INITIAL_OBSTACLE_INTERVAL;
    let lastTime = 0;
    let gameWidth = canvas.width;
    let gameHeight = canvas.height;

    // Player
    const player = {
        x: 50,
        y: 0,
        width: 40,
        height: 40,
        velocityY: 0,
        isJumping: false,
        isSliding: false,
        originalHeight: 40,
        slideHeight: 20
    };

    // Obstacles and collectibles
    const obstacles = [];
    const jellies = [];

    // Colors for drawing (since we're using CSS illustrations, we'll draw simple shapes for now)
    const PLAYER_COLOR = '#ffeb3b'; // Yellow for cookie
    const OBSTACLE_COLOR = '#8bc34a'; // Green for obstacle
    const JELLY_COLOR = '#ff9800'; // Orange for jelly

    // Input handling
    const keys = {};
    window.addEventListener('keydown', (e) => {
        keys[e.code] = true;
        if (e.code === 'Space' && gameActive && !gamePaused) {
            jump();
            e.preventDefault(); // Prevent page scroll
        }
        if (e.code === 'ArrowDown' && gameActive && !gamePaused) {
            startSlide();
            e.preventDefault();
        }
    });
    window.addEventListener('keyup', (e) => {
        keys[e.code] = false;
        if (e.code === 'ArrowDown') {
            endSlide();
        }
    });

    // Touch controls (we'll create on-screen buttons for mobile)
    function createTouchControls() {
        if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
            const touchContainer = document.createElement('div');
            touchContainer.style.position = 'absolute';
            touchContainer.style.bottom = '20px';
            touchContainer.style.left = '50%';
            touchContainer.style.transform = 'translateX(-50%)';
            touchContainer.style.display = 'flex';
            touchContainer.style.gap = '10px';
            touchContainer.style.zIndex = '10';

            const jumpBtn = document.createElement('button');
            jumpBtn.textContent = 'Jump';
            jumpBtn.style.padding = '10px 20px';
            jumpBtn.style.fontSize = '16px';
            jumpBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                if (gameActive && !gamePaused) jump();
            });

            const slideBtn = document.createElement('button');
            slideBtn.textContent = 'Slide';
            slideBtn.style.padding = '10px 20px';
            slideBtn.style.fontSize = '16px';
            slideBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                if (gameActive && !gamePaused) startSlide();
            });
            slideBtn.addEventListener('touchend', endSlide);

            touchContainer.appendChild(jumpBtn);
            touchContainer.appendChild(slideBtn);
            document.body.appendChild(touchContainer);
        }
    }

    // Game functions
    function jump() {
        if (!player.isJumping && !player.isSliding) {
            player.velocityY = -15;
            player.isJumping = true;
        }
    }

    function startSlide() {
        if (!player.isJumping && !player.isSliding) {
            player.isSliding = true;
            player.height = player.slideHeight;
            player.y = gameHeight - player.height - 50; // Adjust y to keep feet on ground
        }
    }

    function endSlide() {
        if (player.isSliding) {
            player.isSliding = false;
            player.height = player.originalHeight;
            player.y = gameHeight - player.height - 50;
        }
    }

    function spawnObstacle() {
        // Randomly decide obstacle or jelly
        const type = Math.random() > 0.7 ? 'jelly' : 'obstacle';
        const size = 30 + Math.random() * 20; // 30-50
        const obstacle = {
            x: gameWidth,
            y: gameHeight - size - 50, // Ground level
            width: size,
            height: size,
            type: type
        };
        if (type === 'jelly') {
            jellies.push(obstacle);
        } else {
            obstacles.push(obstacle);
        }
    }

    function updateGame(deltaTime) {
        // Player physics
        player.velocityY += GRAVITY;
        player.y += player.velocityY;

        // Ground collision
        if (player.y > gameHeight - player.height - 50) {
            player.y = gameHeight - player.height - 50;
            player.velocityY = 0;
            player.isJumping = false;
        }

        // Move obstacles and jellies
        obstacles.forEach((obs, index) => {
            obs.x -= GAME_SPEED;
            if (obs.x + obs.width < 0) {
                obstacles.splice(index, 1);
            }
        });

        jellies.forEach((jelly, index) => {
            jelly.x -= GAME_SPEED;
            if (jelly.x + jelly.width < 0) {
                jellies.splice(index, 1);
            }
        });

        // Collision detection
        obstacles.forEach(obs => {
            if (
                player.x < obs.x + obs.width &&
                player.x + player.width > obs.x &&
                player.y < obs.y + obs.height &&
                player.y + player.height > obs.y
            ) {
                gameOver();
            }
        });

        // Jelly collection
        jellies.forEach((jelly, index) => {
            if (
                player.x < jelly.x + jelly.width &&
                player.x + player.width > jelly.x &&
                player.y < jelly.y + jelly.height &&
                player.y + player.height > jelly.y
            ) {
                score += 10;
                // Decrease obstacle interval as score increases (but cap)
                obstacleInterval = Math.max(MIN_OBSTACLE_INTERVAL, INITIAL_OBSTACLE_INTERVAL - (score * OBSTACLE_INTERVAL_DECREASE));
                jellies.splice(index, 1);
            }
        });

        // Spawn obstacles and jellies
        obstacleTimer += deltaTime;
        if (obstacleTimer > obstacleInterval) {
            spawnObstacle();
            obstacleTimer = 0;
        }

        // Update score
        scoreEl.textContent = Math.floor(score);
        if (Math.floor(score) > bestScore) {
            bestScore = Math.floor(score);
            bestScoreEl.textContent = bestScore;
            // Save best score to localStorage
            localStorage.setItem('ovenbreakBestScore', bestScore);
        }
    }

    function drawGame() {
        // Clear canvas
        ctx.clearRect(0, 0, gameWidth, gameHeight);

        // Draw ground
        ctx.fillStyle = '#8bc34a';
        ctx.fillRect(0, gameHeight - 50, gameWidth, 50);

        // Draw player (simple cookie)
        ctx.fillStyle = PLAYER_COLOR;
        ctx.beginPath();
        ctx.arc(player.x + player.width/2, player.y + player.height/2, player.width/2, 0, Math.PI * 2);
        ctx.fill();
        // Add a simple face
        ctx.fillStyle = '#3e2723';
        ctx.beginPath();
        ctx.arc(player.x + player.width/2 - 5, player.y + player.height/2 - 5, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.arc(player.x + player.width/2 + 5, player.y + player.height/2 - 5, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(player.x + player.width/2, player.y + player.height/2 + 5, 5, 0, Math.PI);
        ctx.stroke();

        // Draw obstacles
        ctx.fillStyle = OBSTACLE_COLOR;
        obstacles.forEach(obs => {
            ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
        });

        // Draw jellies
        ctx.fillStyle = JELLY_COLOR;
        jellies.forEach(jelly => {
            ctx.beginPath();
            ctx.ellipse(jelly.x + jelly.width/2, jelly.y + jelly.height/2, jelly.width/2, jelly.height/2, 0, 0, Math.PI * 2);
            ctx.fill();
        });
    }

    function gameLoop(timestamp) {
        if (!lastTime) lastTime = timestamp;
        const deltaTime = timestamp - lastTime;
        lastTime = timestamp;

        if (gameActive && !gamePaused) {
            updateGame(deltaTime);
            drawGame();
        }

        requestAnimationFrame(gameLoop);
    }

    function startGame() {
        gameActive = true;
        gamePaused = false;
        score = 0;
        player.y = gameHeight - player.height - 50;
        player.velocityY = 0;
        player.isJumping = false;
        player.isSliding = false;
        obstacles.length = 0;
        jellies.length = 0;
        obstacleTimer = 0;
        obstacleInterval = INITIAL_OBSTACLE_INTERVAL;
        lastTime = 0;
        scoreEl.textContent = '0';
        // Reset canvas size (in case of resize)
        resizeCanvas();
        requestAnimationFrame(gameLoop);
    }

    function pauseGame() {
        gamePaused = true;
    }

    function resumeGame() {
        gamePaused = false;
        lastTime = performance.now(); // Reset lastTime to avoid large delta
        requestAnimationFrame(gameLoop);
    }

    function restartGame() {
        pauseGame();
        startGame();
    }

    function gameOver() {
        gameActive = false;
        alert(`Game Over! Your score: ${Math.floor(score)}`);
        // Optionally, we could show a game over screen instead of alert
    }

    function resizeCanvas() {
        canvas.width = canvas.clientWidth;
        canvas.height = canvas.clientHeight;
        gameWidth = canvas.width;
        gameHeight = canvas.height;
        // Reset player position based on new height
        player.y = gameHeight - player.height - 50;
    }

    // Event listeners for game buttons
    startBtn.addEventListener('click', startGame);
    pauseBtn.addEventListener('click', pauseGame);
    restartBtn.addEventListener('click', restartGame);
    toggleInstructionsBtn.addEventListener('click', () => {
        instructionsEl.classList.toggle('hidden');
        toggleInstructionsBtn.textContent = instructionsEl.classList.contains('hidden') ? 'Show Instructions' : 'Hide Instructions';
    });

    // Initialize
    createTouchControls();
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Load best score from localStorage
    const savedBestScore = localStorage.getItem('ovenbreakBestScore');
    if (savedBestScore) {
        bestScore = parseInt(savedBestScore);
        bestScoreEl.textContent = bestScore;
    }

    // Memory Oven
    const memoryForm = document.getElementById('memory-form');
    const memoryTitleInput = document.getElementById('memory-title');
    const memoryContentInput = document.getElementById('memory-content');
    const favoriteCookieInput = document.getElementById('favorite-cookie');
    const bakeMemoryBtn = document.getElementById('bake-memory-btn');
    const memoryPreview = document.getElementById('memory-preview');
    const previewTitle = document.getElementById('preview-title');
    const previewContent = document.getElementById('preview-content');
    const previewCookie = document.getElementById('preview-cookie');
    const copyBtn = document.getElementById('copy-btn');
    const saveMemoryBtn = document.getElementById('save-memory-btn');
    const savedMemoriesList = document.getElementById('saved-memories-list');
    const clearAllBtn = document.getElementById('clear-all-btn');

    let currentMemoryId = null; // For editing

    // Show preview when baking
    bakeMemoryBtn.addEventListener('click', () => {
        const title = memoryTitleInput.value.trim();
        const content = memoryContentInput.value.trim();
        const favoriteCookie = favoriteCookieInput.value.trim();

        if (!content) {
            alert('Please enter a memory.');
            return;
        }

        previewTitle.textContent = title || 'Untitled Memory';
        previewContent.textContent = content;
        previewCookie.textContent = favoriteCookie ? `Favorite Cookie: ${favoriteCookie}` : '';
        memoryPreview.classList.remove('hidden');
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', () => {
        const title = previewTitle.textContent;
        const content = previewContent.textContent;
        const cookieText = previewCookie.textContent;
        const textToCopy = `${title}\n\n${content}\n\n${cookieText}`;
        navigator.clipboard.writeText(textToCopy).then(() => {
            alert('Copied to clipboard!');
        }).catch(err => {
            alert('Failed to copy: ' + err);
        });
    });

    // Save memory
    saveMemoryBtn.addEventListener('click', () => {
        const title = previewTitle.textContent;
        const content = previewContent.textContent;
        const cookieText = previewCookie.textContent;

        // Extract favorite cookie from the text (if present)
        let favoriteCookie = '';
        if (cookieText.startsWith('Favorite Cookie:')) {
            favoriteCookie = cookieText.substring('Favorite Cookie: '.length);
        }

        const memoryData = {
            id: currentMemoryId || Date.now(),
            title: title,
            content: content,
            favoriteCookie: favoriteCookie,
            timestamp: new Date().toISOString()
        };

        // Get existing memories
        let memories = JSON.parse(localStorage.getItem('ovenbreakMemories') || '[]');

        // If editing, remove the old version
        if (currentMemoryId !== null) {
            memories = memories.filter(mem => mem.id !== currentMemoryId);
            currentMemoryId = null; // Reset after editing
        }

        // Add the new/updated memory
        memories.push(memoryData);
        localStorage.setItem('ovenbreakMemories', JSON.stringify(memories));

        // Reset form and preview
        memoryForm.reset();
        memoryPreview.classList.add('hidden');
        renderSavedMemories();
    });

    // Delete memory
    function deleteMemory(id) {
        let memories = JSON.parse(localStorage.getItem('ovenbreakMemories') || '[]');
        memories = memories.filter(mem => mem.id !== id);
        localStorage.setItem('ovenbreakMemories', JSON.stringify(memories));
        renderSavedMemories();
    }

    // Edit memory
    function editMemory(id) {
        let memories = JSON.parse(localStorage.getItem('ovenbreakMemories') || '[]');
        const memory = memories.find(mem => mem.id === id);
        if (memory) {
            memoryTitleInput.value = memory.title;
            memoryContentInput.value = memory.content;
            favoriteCookieInput.value = memory.favoriteCookie;
            currentMemoryId = id;
            // Trigger preview
            bakeMemoryBtn.click();
            // Scroll to form
            memoryForm.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // Render saved memories
    function renderSavedMemories() {
        const memories = JSON.parse(localStorage.getItem('ovenbreakMemories') || '[]');
        savedMemoriesList.innerHTML = '';

        memories.forEach(memory => {
            const memoryDiv = document.createElement('div');
            memoryDiv.className = 'saved-memory';

            const contentDiv = document.createElement('div');
            contentDiv.className = 'saved-memory-content';
            contentDiv.innerHTML = `
                <strong>${memory.title || 'Untitled'}</strong>
                <p>${memory.content}</p>
                ${memory.favoriteCookie ? `<p><em>Favorite Cookie: ${memory.favoriteCookie}</em></p>` : ''}
            `;

            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'saved-memory-actions';

            const editBtn = document.createElement('button');
            editBtn.textContent = 'Edit';
            editBtn.addEventListener('click', () => editMemory(memory.id));

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.addEventListener('click', () => deleteMemory(memory.id));

            actionsDiv.appendChild(editBtn);
            actionsDiv.appendChild(deleteBtn);

            memoryDiv.appendChild(contentDiv);
            memoryDiv.appendChild(actionsDiv);
            savedMemoriesList.appendChild(memoryDiv);
        });
    }

    // Clear all memories
    clearAllBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to delete all memories? This cannot be undone.')) {
            localStorage.removeItem('ovenbreakMemories');
            savedMemoriesList.innerHTML = '';
        }
    });

    // Initial render of saved memories
    renderSavedMemories();
});
