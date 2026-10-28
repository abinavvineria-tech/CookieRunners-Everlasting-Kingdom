// ShadowVerse JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize
    const pages = document.querySelectorAll('.page');
    const navLinks = document.querySelectorAll('.nav-link');
    const loadingScreen = document.getElementById('loading-screen');
    
    // Hide loading screen after a short delay
    setTimeout(() => {
        loadingScreen.style.display = 'none';
    }, 1500);
    
    // Navigation
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            
            // Hide all pages
            pages.forEach(page => {
                page.classList.remove('active');
            });
            
            // Show target page
            document.getElementById(targetId).classList.add('active');
            
            // Update active nav link
            navLinks.forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
    
    // Enter the Masquerade button
    const enterBtn = document.getElementById('enter-btn');
    if (enterBtn) {
        enterBtn.addEventListener('click', function() {
            // Scroll to arena section or set active
            const arenaSection = document.getElementById('arena');
            if (arenaSection) {
                // Hide all pages
                pages.forEach(page => {
                    page.classList.remove('active');
                });
                // Show arena
                arenaSection.classList.add('active');
                
                // Update nav
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#arena') {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    // Character data for arena (sample data - clearly labeled as fan-made/fictional)
    const arenaCharacters = [
        {
            id: 1,
            name: "Shadow Milk Cookie",
            title: "The Masquerade Trickster",
            type: "Trickster",
            description: "A mysterious cookie who hides behind elegant smiles and masks. Known for illusion-based abilities.",
            image: "assets/images/shadow-milk-cookie.png",
            stats: {
                attack: 85,
                defense: 70,
                speed: 95,
                technique: 90
            }
        },
        {
            id: 2,
            name: "Moonlight Cookie",
            title: "The Night's Guardian",
            type: "Champion",
            description: "Protects the realm under the silver moon. Wields lunar energy with grace.",
            image: "assets/images/gallery-1.png",
            stats: {
                attack: 90,
                defense: 85,
                speed: 75,
                technique: 80
            }
        },
        {
            id: 3,
            name: "Pure Vanilla Cookie",
            title: "The Eternal Light",
            type: "Champion",
            description: "Bearer of hope and purity. Shines brightly even in the darkest masquerade.",
            image: "assets/images/gallery-1.png",
            stats: {
                attack: 75,
                defense: 90,
                speed: 70,
                technique: 85
            }
        },
        {
            id: 4,
            name: "Dark Choco Cookie",
            title: "The Shadow Knight",
            type: "Trickster",
            description: "Moves through shadows with deadly precision. Loyal to no one but his own code.",
            image: "assets/images/gallery-1.png",
            stats: {
                attack: 95,
                defense: 80,
                speed: 85,
                technique: 75
            }
        },
        {
            id: 5,
            name: "Strawberry Cookie",
            title: "The Sweet Ambusher",
            type: "Trickster",
            description: "Appears innocent but strikes with surprising ferocity. Lures opponents with sweetness.",
            image: "assets/images/gallery-1.png",
            stats: {
                attack: 80,
                defense: 65,
                speed: 90,
                technique: 85
            }
        }
    ];
    
    // Match history data (clearly labeled as sample/fictional)
    const matchHistory = [
        {
            id: 1,
            match: "Match #001",
            player: "Shadow Milk Cookie",
            opponent: "Moonlight Cookie",
            result: "Victory",
            score: "3-2"
        },
        {
            id: 2,
            match: "Match #002",
            player: "Pure Vanilla Cookie",
            opponent: "Dark Choco Cookie",
            result: "Defeat",
            score: "1-3"
        },
        {
            id: 3,
            match: "Match #003",
            player: "Strawberry Cookie",
            opponent: "Shadow Milk Cookie",
            result: "Victory",
            score: "2-1"
        },
        {
            id: 4,
            match: "Match #004",
            player: "Moonlight Cookie",
            opponent: "Pure Vanilla Cookie",
            result: "Draw",
            score: "2-2"
        }
    ];
    
    // Arena functionality
    const characterGrid = document.getElementById('character-grid');
    const matchTableBody = document.querySelector('#match-table tbody');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('search-arena');
    
    // Render character cards
    function renderCharacters(filterType = 'all', searchTerm = '') {
        characterGrid.innerHTML = '';
        
        const filteredChars = arenaCharacters.filter(char => {
            const typeMatch = filterType === 'all' || char.type.toLowerCase() === filterType;
            const searchMatch = searchTerm === '' || 
                               char.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                               char.title.toLowerCase().includes(searchTerm.toLowerCase());
            return typeMatch && searchMatch;
        });
        
        filteredChars.forEach(char => {
            const card = document.createElement('div');
            card.className = 'character-card';
            card.innerHTML = `
                <img src="${char.image}" alt="${char.name}">
                <div class="character-info">
                    <h3>${char.name}</h3>
                    <p>${char.title}</p>
                    <p>${char.type}</p>
                </div>
            `;
            
            // Add click event to show details (in a real app, this might open a modal)
            card.addEventListener('click', function() {
                alert(`Details for ${char.name}:\n\n${char.description}\n\nStats:\nAttack: ${char.stats.attack}\nDefense: ${char.stats.defense}\nSpeed: ${char.stats.speed}\nTechnique: ${char.stats.technique}`);
            });
            
            characterGrid.appendChild(card);
        });
    }
    
    // Render match history
    function renderMatchHistory() {
        matchTableBody.innerHTML = '';
        matchHistory.forEach(match => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${match.match}</td>
                <td>${match.player}</td>
                <td>${match.opponent}</td>
                <td>${match.result}</td>
                <td>${match.score}</td>
            `;
            matchTableBody.appendChild(row);
        });
    }
    
    // Filter buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const filterType = this.id.replace('filter-', '');
            const searchTerm = searchInput.value.trim();
            renderCharacters(filterType, searchTerm);
        });
    });
    
    // Search input
    searchInput.addEventListener('input', function() {
        const activeFilter = document.querySelector('.filter-btn.active');
        const filterType = activeFilter.id.replace('filter-', '');
        const searchTerm = this.value.trim();
        renderCharacters(filterType, searchTerm);
    });
    
    // Initialize arena
    renderCharacters('all', '');
    renderMatchHistory();
    
    // Anniversary Hall functionality
    const anniversaryTitleInput = document.getElementById('anniversary-title');
    const anniversaryDateInput = document.getElementById('anniversary-date');
    const beginCelebrationBtn = document.getElementById('begin-celebration');
    const skipCelebrationBtn = document.getElementById('skip-celebration');
    const replayCelebrationBtn = document.getElementById('replay-celebration');
    const celebrationDisplay = document.getElementById('celebration-display');
    const timelineDiv = document.getElementById('timeline');
    const particlesContainer = document.getElementById('particles-container');
    
    let celebrationActive = false;
    let celebrationInterval = null;
    
    // Sample timeline data
    const timelineEvents = [
        { year: "2020", event: "Project Conception: The idea for ShadowVerse was born." },
        { year: "2021", event: "First Designs: Initial concepts for Shadow Milk Cookie's masquerade form." },
        { year: "2022", event: "Community Feedback: Early fans shared their thoughts and ideas." },
        { year: "2023", event: "Development Begins: Core mechanics and aesthetics implemented." },
        { year: "2024", event: "Beta Testing: Closed trials with selected community members." },
        { year: "2025", event: "Public Demo: First playable version released to fans." },
        { year: "2026", event: "Official Launch: ShadowVerse - The Eternal Masquerade arrives." }
    ];
    
    // Create particle effect (simple floating diamonds)
    function createParticles() {
        // Clear existing particles
        particlesContainer.innerHTML = '';
        
        // Create 20 particle elements
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Random position
            const posX = Math.random() * 100;
            const posY = Math.random() * 100;
            
            // Random size and animation duration
            const size = Math.random() * 10 + 5;
            const duration = Math.random() * 3 + 2;
            
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${posX}%`;
            particle.style.top = `${posY}%`;
            particle.style.animationDuration = `${duration}s`;
            particle.style.animationDelay = `${Math.random() * 2}s`;
            
            particlesContainer.appendChild(particle);
        }
    }
    
    // Start celebration animation
    function startCelebration() {
        if (celebrationActive) return;
        
        celebrationActive = true;
        
        // Show timeline
        timelineDiv.innerHTML = '';
        timelineEvents.forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.innerHTML = `<strong>${event.year}:</strong> ${event.event}`;
            timelineDiv.appendChild(eventDiv);
        });
        
        // Create particles
        createParticles();
        
        // Simulate ongoing celebration (just for visual effect)
        celebrationInterval = setInterval(() => {
            // Occasionally recreate particles for variety
            if (Math.random() > 0.9) {
                createParticles();
            }
        }, 5000);
    }
    
    // Stop celebration
    function stopCelebration() {
        celebrationActive = false;
        if (celebrationInterval) {
            clearInterval(celebrationInterval);
            celebrationInterval = null;
        }
    }
    
    // Event listeners for anniversary controls
    beginCelebrationBtn.addEventListener('click', function() {
        startCelebration();
    });
    
    skipCelebrationBtn.addEventListener('click', function() {
        stopCelebration();
        // Still show timeline but without active animation
        timelineDiv.innerHTML = '';
        timelineEvents.forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.innerHTML = `<strong>${event.year}:</strong> ${event.event}`;
            timelineDiv.appendChild(eventDiv);
        });
        // Create static particles
        createParticles();
    });
    
    replayCelebrationBtn.addEventListener('click', function() {
        stopCelebration();
        setTimeout(() => {
            startCelebration();
        }, 300);
    });
    
    // Initialize anniversary section (show config by default)
    // No automatic start - user must click begin
    
    // Gallery functionality
    const galleryGrid = document.getElementById('gallery-grid');
    const gallerySearch = document.getElementById('search-gallery');
    const clearFilterBtn = document.getElementById('clear-filter');
    
    // Gallery items (sample data)
    const galleryItems = [
        {
            id: 1,
            title: "Shadow Milk Cookie - Masquerade Form",
            description: "The elegant trickster in her signature masquerade attire.",
            image: "assets/images/shadow-milk-cookie.png",
            character: "Shadow Milk Cookie"
        },
        {
            id: 2,
            title: "Moonlight Cookie - Lunar Guardian",
            description: "Protector of the night sky.",
            image: "assets/images/gallery-1.png",
            character: "Moonlight Cookie"
        },
        {
            id: 3,
            title: "Pure Vanilla Cookie - Radiant Light",
            description: "Bringing hope to the masquerade.",
            image: "assets/images/gallery-1.png",
            character: "Pure Vanilla Cookie"
        },
        {
            id: 4,
            title: "Dark Choco Cookie - Shadow Knight",
            description: "Warrior of the darkness.",
            image: "assets/images/gallery-1.png",
            character: "Dark Choco Cookie"
        },
        {
            id: 5,
            title: "Strawberry Cookie - Sweet Ambusher",
            description: "Deceptively sweet and dangerous.",
            image: "assets/images/gallery-1.png",
            character: "Strawberry Cookie"
        }
    ];
    
    // Render gallery items
    function renderGallery(filterTerm = '') {
        galleryGrid.innerHTML = '';
        
        const filteredItems = galleryItems.filter(item => {
            return filterTerm === '' || 
                   item.title.toLowerCase().includes(filterTerm.toLowerCase()) ||
                   item.description.toLowerCase().includes(filterTerm.toLowerCase()) ||
                   item.character.toLowerCase().includes(filterTerm.toLowerCase());
        });
        
        if (filteredItems.length === 0) {
            galleryGrid.innerHTML = '<p class="no-results">No gallery items match your search.</p>';
            return;
        }
        
        filteredItems.forEach(item => {
            const galleryItem = document.createElement('div');
            galleryItem.className = 'gallery-item';
            galleryItem.innerHTML = `
                <img src="${item.image}" alt="${item.title}" onerror="this.src='assets/images/gallery-1.png'; this.alt='Image not available';">
                <h3>${item.title}</h3>
                <p>${item.description}</p>
                <p><small>Featured: ${item.character}</small></p>
            `;
            galleryGrid.appendChild(galleryItem);
        });
    }
    
    // Gallery search and filter
    gallerySearch.addEventListener('input', function() {
        const searchTerm = this.value.trim();
        renderGallery(searchTerm);
    });
    
    clearFilterBtn.addEventListener('click', function() {
        gallerySearch.value = '';
        renderGallery('');
    });
    
    // Initialize gallery
    renderGallery('');
    
    // Journal functionality
    const journalInput = document.getElementById('journal-input');
    const saveJournalBtn = document.getElementById('save-journal');
    const clearJournalBtn = document.getElementById('clear-journal');
    const journalEntriesDiv = document.getElementById('journal-entries');
    
    // Load entries from localStorage
    function loadJournalEntries() {
        const entries = JSON.parse(localStorage.getItem('shadowverseJournal') || '[]');
        journalEntriesDiv.innerHTML = '';
        
        if (entries.length === 0) {
            journalEntriesDiv.innerHTML = '<p class="no-entries">No memories saved yet. Write your first entry!</p>';
            return;
        }
        
        entries.forEach((entry, index) => {
            const entryDiv = document.createElement('div');
            entryDiv.className = 'journal-entry-item';
            entryDiv.innerHTML = `
                <h4>Memory #${index + 1}</h4>
                <p>${entry.text.replace(/\n/g, '<br>')}</p>
                <small>${new Date(entry.timestamp).toLocaleString()}</small>
            `;
            journalEntriesDiv.appendChild(entryDiv);
        });
    }
    
    // Save journal entry
    saveJournalBtn.addEventListener('click', function() {
        const text = journalInput.value.trim();
        if (text === '') {
            alert('Please write something before saving.');
            return;
        }
        
        const entries = JSON.parse(localStorage.getItem('shadowverseJournal') || '[]');
        entries.push({
            text: text,
            timestamp: new Date().toISOString()
        });
        
        localStorage.setItem('shadowverseJournal', JSON.stringify(entries));
        journalInput.value = '';
        loadJournalEntries();
    });
    
    // Clear journal entries
    clearJournalBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete all journal entries? This cannot be undone.')) {
            localStorage.removeItem('shadowverseJournal');
            loadJournalEntries();
        }
    });
    
    // Initialize journal
    loadJournalEntries();
    
    // Add some initial sample quotes to journal (optional)
    // We'll add one sample entry if journal is empty
    const sampleEntries = JSON.parse(localStorage.getItem('shadowverseJournal') || '[]');
    if (sampleEntries.length === 0) {
        const sampleEntry = {
            text: "I attended the first ShadowVerse masquerade ball last night. The atmosphere was electric with mystery and excitement. Seeing Shadow Milk Cookie in person was truly enchanting - her smile hid depths I could only imagine.",
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('shadowverseJournal', JSON.stringify([sampleEntry]));
        loadJournalEntries();
    }
    
    // Keyboard accessibility: close alerts with ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            // Close any alert-like overlays (we don't have modals, but we can blur active elements)
            document.activeElement.blur();
        }
    });
    
    // Focus management for better accessibility
    document.querySelectorAll('button, input, textarea').forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid var(--cyan)';
        });
        element.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
});