// Dawnbringer - Interactive Anniversary Website Script

document.addEventListener('DOMContentLoaded', () => {
    console.log('[Dawnbringer] DOM loaded');
    // Elements
    const beginBtn = document.getElementById('beginBtn');
    console.log('[Dawnbringer] beginBtn:', beginBtn);
    const screens = document.querySelectorAll('.screen');
    const welcomeScreen = document.getElementById('welcome');
    const journeyScreen = document.getElementById('journey');
    const hallScreen = document.getElementById('hall');
    const messageScreen = document.getElementById('message');
    const celebrationScreen = document.getElementById('celebration');
    const communityScreen = document.getElementById('community');

    const petalContainer = document.getElementById('petalContainer');
    const visitorMessageInput = document.getElementById('visitorMessage');
    const saveMessageBtn = document.getElementById('saveMessageBtn');
    const messageStatus = document.getElementById('messageStatus');
    const savedMessagesDiv = document.getElementById('savedMessages');

    const lilyGardenBtn = document.getElementById('lilyGardenBtn');
    const lilyGarden = document.getElementById('lilyGarden');
    const cardGeneratorBtn = document.getElementById('cardGeneratorBtn');
    const cardModal = document.getElementById('cardModal');
    const closeCardBtn = cardModal.querySelector('.close-btn');
    const cardTextInput = document.getElementById('cardText');
    const cardPreviewMessage = document.querySelector('#cardPreview .card-message');
    const generateCardBtn = document.getElementById('generateCardBtn');
    const downloadCardBtn = document.getElementById('downloadCardBtn');
    const showMemoriesBtn = document.getElementById('showMemoriesBtn');
    const memoriesModal = document.getElementById('memoriesGallery');
    const closeMemoriesBtn = memoriesModal.querySelector('.close-memories');
    const memoriesDisplay = document.getElementById('memoriesDisplay');

    const dedicationWall = document.getElementById('dedicationWall');
    const creditsSection = document.getElementById('creditsSection');
    const editCreditsBtn = document.getElementById('editCreditsBtn');
    const favoriteMoments = document.getElementById('favoriteMoments');
    const addMomentBtn = document.getElementById('addMomentBtn');
    const futureMemories = document.getElementById('futureMemories');
    const addFutureBtn = document.getElementById('addFutureBtn');

    const anniversaryDateDisplay = document.getElementById('anniversaryDate');

    // State
    let messages = JSON.parse(localStorage.getItem('dawnbringerMessages') || '[]');
    let lilyGardenActive = false;
    let cards = JSON.parse(localStorage.getItem('dawnbringerCards') || '[]');
    let memories = JSON.parse(localStorage.getItem('dawnbringerMemories') || '[]');
    let dedications = JSON.parse(localStorage.getItem('dawnbringerDedications') || []);
    let credits = JSON.parse(localStorage.getItem('dawnbringerCredits') || ['CookieVerse Hermes', 'Cookie Runners Community']);
    let moments = JSON.parse(localStorage.getItem('dawnbringerMoments') || []);
    let futures = JSON.parse(localStorage.getItem('dawnbringerFutures') || []);

    // Initialize
    function init() {
        console.log('[Dawnbringer] init called');
        showScreen(welcomeScreen);
        renderSavedMessages();
        renderLilyGarden();
        renderCards();
        renderMemoriesGallery();
        renderDedications();
        renderCredits();
        renderMoments();
        renderFutures();
        updateAnniversaryDate();
        startPetalAnimation();
    }

    // Screen navigation
    function showScreen(screenToShow) {
        screens.forEach(screen => screen.classList.remove('active'));
        screenToShow.classList.add('active');
    }

    beginBtn.addEventListener('click', () => {
        console.log('[Dawnbringer] beginBtn clicked');
        showScreen(journeyScreen);
    });

    // Petal animation
    function startPetalAnimation() {
        // Clear existing petals
        petalContainer.innerHTML = '';
        // Create petals periodically
        setInterval(createPetal, 300);
    }

    function createPetal() {
        const petal = document.createElement('div');
        petal.className = 'petal';
        
        // Random start position across width
        const startX = Math.random() * 100;
        petal.style.left = `${startX}%`;
        
        // Random size
        const size = 10 + Math.random() * 20;
        petal.style.width = `${size}px`;
        petal.style.height = `${size}px`;
        
        // Animation duration variation
        const duration = 4 + Math.random() * 4;
        petal.style.animationDuration = `${duration}s`;
        
        // Set custom properties for keyframes
        petal.style.setProperty('--start-y', `${window.innerHeight}px`);
        petal.style.setProperty('--end-y', `-${size}px`);
        
        petalContainer.appendChild(petal);
        
        // Remove petal after animation ends
        setTimeout(() => {
            if (petal.parentNode) {
                petal.parentNode.removeChild(petal);
            }
        }, (duration + 1) * 1000);
    }

    // Message handling
    saveMessageBtn.addEventListener('click', () => {
        const messageText = visitorMessageInput.value.trim();
        if (messageText === '') {
            showStatus('Please write a message before saving.', 'error');
            return;
        }
        
        const messageObj = {
            id: Date.now(),
            text: messageText,
            timestamp: new Date().toISOString()
        };
        
        messages.push(messageObj);
        localStorage.setItem('dawnbringerMessages', JSON.stringify(messages));
        renderSavedMessages();
        visitorMessageInput.value = '';
        showStatus('Message saved successfully!', 'success');
    });

    function renderSavedMessages() {
        savedMessagesDiv.innerHTML = '<h3>Messages from Cookie Runners</h3>';
        if (messages.length === 0) {
            savedMessagesDiv.innerHTML += '<p>No messages yet. Be the first to share your thoughts!</p>';
            return;
        }
        
        messages.slice().reverse().forEach(msg => {
            const messageEl = document.createElement('div');
            messageEl.className = 'message-card';
            messageEl.innerHTML = `
                <p>${msg.text}</p>
                <div class="timestamp">${new Date(msg.timestamp).toLocaleString()}</div>
            `;
            savedMessagesDiv.appendChild(messageEl);
        });
    }

    function showStatus(msg, type) {
        messageStatus.textContent = msg;
        messageStatus.className = `status ${type}`;
        // Clear after 3 seconds
        setTimeout(() => {
            messageStatus.textContent = '';
            messageStatus.className = 'status';
        }, 3000);
    }

    // Lily Garden
    lilyGardenBtn.addEventListener('click', () => {
        lilyGardenActive = !lilyGardenActive;
        if (lilyGardenActive) {
            lilyGardenBtn.textContent = 'Collect Flowers';
            startLilyGarden();
        } else {
            lilyGardenBtn.textContent = 'Leave a Flower for Dawnbringer';
            stopLilyGarden();
        }
    });

    let gardenInterval = null;
    function startLilyGarden() {
        gardenInterval = setInterval(() => {
            createLily();
        }, 800);
    }

    function stopLilyGarden() {
        if (gardenInterval) {
            clearInterval(gardenInterval);
            gardenInterval = null;
        }
    }

    function createLily() {
        const lily = document.createElement('div');
        lily.className = 'lily';
        
        // Random position
        const x = Math.random() * (lilyGarden.clientWidth - 40);
        const y = Math.random() * (lilyGarden.clientHeight - 40);
        lily.style.left = `${x}px`;
        lily.style.top = `${y}px`;
        
        // Random rotation
        const rotation = Math.random() * 360;
        lily.style.setProperty('--rotation', `${rotation}deg`);
        
        // Lily SVG (simple white lily)
        lily.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white">
                <path d="M12 2L15 8H22l-3 5 1 6-6-3-6 3 1-6-3-5h7z"/>
            </svg>
        `;
        
        lilyGarden.appendChild(lily);
        
        // Remove lily after animation
        setTimeout(() => {
            if (lily.parentNode) {
                lily.parentNode.removeChild(lily);
            }
        }, 1500);
    }

    // Card Generator
    closeCardBtn.addEventListener('click', () => {
        cardModal.classList.add('hidden');
    });

    cardGeneratorBtn.addEventListener('click', () => {
        cardModal.classList.remove('hidden');
        cardTextInput.focus();
    });

    generateCardBtn.addEventListener('click', () => {
        const cardMessage = cardTextInput.value.trim();
        if (cardMessage === '') {
            alert('Please write a message for your card.');
            return;
        }
        
        cardPreviewMessage.textContent = cardMessage;
        downloadCardBtn.disabled = false;
    });

    downloadCardBtn.addEventListener('click', () => {
        // Create a canvas from the card preview for download
        // For simplicity, we'll just save the message as text for now
        // In a full implementation, we'd use html2canvas or similar
        const cardData = {
            message: cardTextInput.value,
            timestamp: new Date().toISOString()
        };
        
        cards.push(cardData);
        localStorage.setItem('dawnbringerCards', JSON.stringify(cards));
        
        // Show download notification
        alert('Card saved to your collection! (Feature: In a full implementation, this would download an image)');
        cardModal.classList.add('hidden');
        cardTextInput.value = '';
        cardPreviewMessage.textContent = '';
        downloadCardBtn.disabled = true;
    });

    // Memories Gallery
    closeMemoriesBtn.addEventListener('click', () => {
        memoriesModal.classList.add('hidden');
    });

    showMemoriesBtn.addEventListener('click', () => {
        memoriesModal.classList.remove('hidden');
    });

    function renderMemoriesGallery() {
        memoriesDisplay.innerHTML = '';
        if (memories.length === 0) {
            memoriesDisplay.innerHTML = '<p>No memories uploaded yet. Add some to see them here!</p>';
            return;
        }
        
        memories.forEach(memory => {
            const memoryEl = document.createElement('div');
            memoryEl.className = 'memory-item';
            memoryEl.innerHTML = `
                <img src="${memory.url}" alt="Anniversary memory">
                <p>${memory.caption || 'Memory'}</p>
            `;
            memoriesDisplay.appendChild(memoryEl);
        });
    }

    // For demonstration, we'll add a placeholder memory function
    // In reality, users would upload images via file input
    function addSampleMemory() {
        const sampleMemory = {
            url: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"%3E%3Crect width="200" height="200" fill="%23fff0f5"/%3E%3Ctext x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="%23999" font-size="16"%3EMemory Placeholder%3C/text%3E%3C/svg%3E',
            caption: 'Sample Anniversary Memory'
        };
        memories.push(sampleMemory);
        localStorage.setItem('dawnbringerMemories', JSON.stringify(memories));
        renderMemoriesGallery();
    }

    // Dedication Wall
    function renderDedications() {
        dedicationWall.innerHTML = '';
        if (dedications.length === 0) {
            dedicationWall.innerHTML = '<p>No dedications yet. Add yours to the wall!</p>';
            return;
        }
        
        dedications.forEach(dedication => {
            const dedicationEl = document.createElement('div');
            dedicationEl.className = 'dedication-item';
            dedicationEl.textContent = dedication;
            dedicationWall.appendChild(dedicationEl);
        });
    }

    // For demo, add a sample dedication
    function addSampleDedication() {
        dedications.push('Forever in our hearts, White Lily Cookie 🤍');
        localStorage.setItem('dawnbringerDedications', JSON.stringify(dedications));
        renderDedications();
    }

    // Credits Section
    function renderCredits() {
        creditsSection.innerHTML = '';
        if (credits.length === 0) {
            creditsSection.innerHTML = '<p>No credits to display.</p>';
            return;
        }
        
        credits.forEach(credit => {
            const creditEl = document.createElement('div');
            creditEl.className = 'credit-item';
            creditEl.textContent = credit;
            creditsSection.appendChild(creditEl);
        });
    }

    editCreditsBtn.addEventListener('click', () => {
        const newCredits = prompt('Enter credits (one per line):', credits.join('\n'));
        if (newCredits !== null) {
            const creditsArray = newCredits.split('\n').map(line => line.trim()).filter(line => line.length > 0);
            credits = creditsArray;
            localStorage.setItem('dawnbringerCredits', JSON.stringify(credits));
            renderCredits();
        }
    });

    // Favorite Moments
    function renderMoments() {
        favoriteMoments.innerHTML = '';
        if (moments.length === 0) {
            favoriteMoments.innerHTML = '<p>Share your favorite White Lily Cookie moments here.</p>';
            return;
        }
        
        moments.forEach(moment => {
            const momentEl = document.createElement('div');
            momentEl.className = 'moment-item';
            momentEl.textContent = moment;
            favoriteMoments.appendChild(momentEl);
        });
    }

    addMomentBtn.addEventListener('click', () => {
        const moment = prompt('Share a favorite White Lily Cookie moment:');
        if (moment !== null && moment.trim() !== '') {
            moments.push(moment.trim());
            localStorage.setItem('dawnbringerMoments', JSON.stringify(moments));
            renderMoments();
        }
    });

    // Future Anniversary Memories/Hopes
    function renderFutures() {
        futureMemories.innerHTML = '';
        if (futures.length === 0) {
            futureMemories.innerHTML = '<p>What hopes do you hold for future celebrations?</p>';
            return;
        }
        
        futures.forEach(future => {
            const futureEl = document.createElement('div');
            futureEl.className = 'future-item';
            futureEl.textContent = future;
            futureMemories.appendChild(futureEl);
        });
    }

    addFutureBtn.addEventListener('click', () => {
        const future = prompt('What hope or wish do you have for future White Lily Cookie anniversaries?');
        if (future !== null && future.trim() !== '') {
            futures.push(future.trim());
            localStorage.setItem('dawnbringerFutures', JSON.stringify(futures));
            renderFutures();
        }
    });

    // Anniversary Date Display
    function updateAnniversaryDate() {
        const anniversary = new Date('2026-10-22');
        const today = new Date();
        
        if (today.toDateString() === anniversary.toDateString()) {
            anniversaryDateDisplay.textContent = 'First Anniversary Celebration • Today!';
        } else if (today > anniversary) {
            const yearsDiff = today.getFullYear() - anniversary.getFullYear();
            anniversaryDateDisplay.textContent = `${yearsDiff}${yearsDiff === 1 ? 'st' : 'nd'} Anniversary Celebration • October 22, ${anniversary.getFullYear() + yearsDiff}`;
        } else {
            // Before anniversary (shouldn't happen on anniversary day, but just in case)
            const diffTime = anniversary - today;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            anniversaryDateDisplay.textContent = `${diffDays} days until anniversary`;
        }
    }

    // Initialize sample data for demo (optional - comment out for clean start)
    // Uncomment the lines below to add sample data
    /*
    addSampleMemory();
    addSampleDedication();
    */

    // Start the application
    init();
});

// Helper for touch events (for mobile)
document.addEventListener('touchstart', function(){}, {passive:true});