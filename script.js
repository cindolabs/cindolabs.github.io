// Initialize AOS
AOS.init();

// Welcome Popup Functionality
function showWelcomePopup() {
    const welcomePopup = document.getElementById('welcome-popup');
    const welcomeMessage = document.getElementById('welcome-message');
    const userName = sessionStorage.getItem('userName') || '';

    if (!sessionStorage.getItem('welcomePopupShown') && welcomePopup) {
        // Personalize message if user name is available
        if (userName) {
            welcomeMessage.textContent = `Halo ${userName}, nikmati pengalaman menginap yang luar biasa dan jelajahi peluang investasi strategis dengan kami!`;
        }
        welcomePopup.classList.add('active');
        sessionStorage.setItem('welcomePopupShown', 'true');

        // Auto-close after 10 seconds if no interaction
        setTimeout(() => {
            if (welcomePopup.classList.contains('active')) {
                closeWelcomePopup();
            }
        }, 10000);

        // Set focus on close button for accessibility
        const closeButton = welcomePopup.querySelector('.welcome-close');
        closeButton.focus();
    }
}

function closeWelcomePopup() {
    const welcomePopup = document.getElementById('welcome-popup');
    if (welcomePopup) {
        welcomePopup.classList.remove('active');
    }
}

// Show welcome popup on page load
document.addEventListener('DOMContentLoaded', () => {
    showWelcomePopup();
});

// Navbar Hamburger Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        const isExpanded = navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
        hamburger.setAttribute('aria-expanded', isExpanded);
    });

    // Close menu when a link is clicked
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        });
    });
} else {
    console.error('Hamburger atau nav-menu tidak ditemukan');
}

// Smooth Scroll
function scrollToSection(sectionId) {
    const section = document.querySelector(`#${sectionId}`);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Format Rupiah Function
function formatRupiah(number) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 2
    }).format(number);
}

// Display Asset and Investment Stats on Page Load
document.addEventListener('DOMContentLoaded', () => {
    // Asset Values
    const assetValueElement = document.getElementById('asset-value');
    const depositedBalanceElement = document.getElementById('deposited-balance');
    const withdrawnBalanceElement = document.getElementById('withdrawn-balance');

    const assetAmount = 100000;
    const depositedBalance = 500000;
    const withdrawnBalance = 10000;

    if (assetValueElement) assetValueElement.textContent = formatRupiah(assetAmount);
    if (depositedBalanceElement) depositedBalanceElement.textContent = formatRupiah(depositedBalance);
    if (withdrawnBalanceElement) withdrawnBalanceElement.textContent = formatRupiah(withdrawnBalance);

    // Investment Stats
    const investorCountElement = document.getElementById('investor-count');
    const managedFundsElement = document.getElementById('managed-funds');
    const fundsGrowthElement = document.getElementById('funds-growth');
    const profitShareElement = document.getElementById('profit-share');
    const managerCountElement = document.getElementById('manager-count');
    const instrumentCountElement = document.getElementById('instrument-count');

    const investorCount = 5;
    const managedFunds = 35834.68; // Sesuai dengan HTML
    const fundsGrowth = 936.44; // Sesuai dengan HTML
    const profitShare = 100;
    const managerCount = 2;
    const instrumentCount = 5;

    if (investorCountElement) investorCountElement.textContent = investorCount;
    if (managedFundsElement) managedFundsElement.textContent = formatRupiah(managedFunds);
    if (fundsGrowthElement) fundsGrowthElement.textContent = formatRupiah(fundsGrowth);
    if (profitShareElement) profitShareElement.textContent = formatRupiah(profitShare);
    if (managerCountElement) managerCountElement.textContent = managerCount;
    if (instrumentCountElement) instrumentCountElement.textContent = `${instrumentCount} Simbol`;

    // Investment Packages
    const investmentData = [
        { title: 'Basic Package', description: 'Investasi awal dengan ROI stabil.', price: 'Rp 500 Juta' },
        { title: 'Premium Package', description: 'Investasi dengan fasilitas eksklusif.', price: 'Rp 1 Miliar' },
        { title: 'Elite Package', description: 'Investasi premium dengan keuntungan maksimal.', price: 'Rp 2 Miliar' }
    ];

    const investmentGrid = document.getElementById('investment-data');
    if (investmentGrid) {
        investmentData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'service-card';
            card.setAttribute('data-aos', 'fade-up');
            card.innerHTML = `
                <h3>${item.title}</h3>
                <p>${item.description}</p>
                <p><strong>Harga: ${item.price}</strong></p>
                <button onclick="viewPackageDetails('${item.title}')">Lihat Detail</button>
            `;
            investmentGrid.appendChild(card);
        });
    } else {
        console.error('Element #investment-data tidak ditemukan');
    }
});

// View Package Details
function viewPackageDetails(title) {
    alert(`Detail untuk ${title}: Segera hubungi tim kami untuk informasi lebih lanjut!`);
}

// Chatbot Functionality
function toggleChatbot() {
    const chatbot = document.getElementById('chatbot');
    if (chatbot) {
        chatbot.classList.toggle('active');
    }
}

function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const messages = document.getElementById('chatbot-messages');
    const message = input.value.trim();

    if (!message || !message.replace(/\s/g, '').length) {
        return;
    }

    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = message;
    messages.appendChild(userMessage);

    // Simulate bot response
    setTimeout(() => {
        const botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.textContent = getBotResponse(message);
        messages.appendChild(botMessage);
        messages.scrollTop = messages.scrollHeight;
    }, 500);

    input.value = '';
}

function getBotResponse(message) {
    message = message.toLowerCase();
    if (message.includes('hotel')) {
        return 'Hocindo menawarkan pengalaman menginap dengan daya tarik kemewahan dan romansa! Ingin tahu lebih banyak tentang fasilitas kami?';
    } else if (message.includes('cinta') || message.includes('romantis')) {
        return 'Dengan gravitasi cinta, kami punya paket romantis dan acara spesial untuk Anda. Tertarik untuk pernikahan impian?';
    } else if (message.includes('investasi') || message.includes('aset') || message.includes('dana') || message.includes('investor') || message.includes('manajer') || message.includes('instrumen') || message.includes('saldo')) {
        return 'Peluang investasi di Hocindo menawarkan ROI menarik! Saat ini: Aset Anda Rp 100.000, Saldo Disetor Rp 500.000, Saldo Ditarik Rp 10.000, 5 investor, 2 manajer investasi, 5 instrumen investasi, dana kelolaan Rp 35.834,68, pertumbuhan dana Rp 936,44, bagi hasil Rp 100. Klik "Daftar Investasi" untuk detail!';
    } else if (message.includes('apa itu') || message.includes('tentang')) {
        return 'Hocindo adalah hotel kreatif yang menggabungkan penginapan, bisnis, dan investasi strategis. Tanya saya lebih lanjut!';
    } else {
        return 'Saya HocindoBot, siap membantu Anda menjelajahi gravitasi cinta dan kemewahan! Apa yang ingin Anda tahu?';
    }
}

// Modal Functionality
function openModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.classList.add('active');
        modal.querySelector('input[name="name"]').focus();
    }
}

function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Form Submission (Contact)
document.getElementById('contact-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const nameInput = e.target.querySelector('input[name="name"]').value;
    const emailInput = e.target.querySelector('input[name="email"]');
    if (!emailInput.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        alert('Email tidak valid!');
        return;
    }
    sessionStorage.setItem('userName', nameInput); // Store name for personalization
    alert('Pesan Anda telah dikirim! Tim Hocindo akan segera menghubungi Anda.');
    e.target.reset();
});

// Form Submission (Investment)
document.getElementById('investment-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const nameInput = e.target.querySelector('input[name="name"]').value;
    const emailInput = e.target.querySelector('input[name="email"]');
    if (!emailInput.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        alert('Email tidak valid!');
        return;
    }
    sessionStorage.setItem('userName', nameInput); // Store name for personalization
    alert('Pendaftaran investasi berhasil! Tim Hocindo akan menghubungi Anda untuk langkah selanjutnya.');
    e.target.reset();
    closeModal();
});
