// Initialize AOS
AOS.init();

// Navbar Hamburger Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Smooth Scroll
function scrollToSection(sectionId) {
    document.querySelector(`#${sectionId}`).scrollIntoView({ behavior: 'smooth' });
}

// Format Rupiah Function
function formatRupiah(number) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(number);
}

// Display Asset and Investment Stats on Page Load
document.addEventListener('DOMContentLoaded', () => {
    // Asset Values
    const assetValueElement = document.getElementById('asset-value');
    const depositedBalanceElement = document.getElementById('deposited-balance');
    const withdrawnBalanceElement = document.getElementById('withdrawn-balance');

    const assetAmount = 100000; // Rp100,000
    const depositedBalance = 500000; // Rp500,000
    const withdrawnBalance = 10000; // Rp10,000

    assetValueElement.textContent = formatRupiah(assetAmount);
    depositedBalanceElement.textContent = formatRupiah(depositedBalance);
    withdrawnBalanceElement.textContent = formatRupiah(withdrawnBalance);

    // Investment Stats
    const investorCountElement = document.getElementById('investor-count');
    const managedFundsElement = document.getElementById('managed-funds');
    const fundsGrowthElement = document.getElementById('funds-growth');
    const profitShareElement = document.getElementById('profit-share');
    const managerCountElement = document.getElementById('manager-count');
    const instrumentCountElement = document.getElementById('instrument-count');

    const investorCount = 5; // 5 Orang
    const managedFunds = 30000; // Rp30,000
    const fundsGrowth = 800; // Rp800
    const profitShare = 100; // Rp100
    const managerCount = 2; // 2 Orang
    const instrumentCount = 5; // 5 Instrumen

    investorCountElement.textContent = `${investorCount};
    managedFundsElement.textContent = formatRupiah(managedFunds);
    fundsGrowthElement.textContent = formatRupiah(fundsGrowth);
    profitShareElement.textContent = formatRupiah(profitShare);
    managerCountElement.textContent = `${managerCount} Orang`;
    instrumentCountElement.textContent = `${instrumentCount} Instrumen`;

    // Investment Packages
    const investmentData = [
        { title: 'Basic Package', description: 'Investasi awal dengan ROI stabil.', price: 'Rp 500 Juta' },
        { title: 'Premium Package', description: 'Investasi dengan fasilitas eksklusif.', price: 'Rp 1 Miliar' },
        { title: 'Elite Package', description: 'Investasi premium dengan keuntungan maksimal.', price: 'Rp 2 Miliar' }
    ];

    const investmentGrid = document.getElementById('investment-data');
    investmentData.forEach(item => {
        const card = document.createElement('div');
        card.className = 'service-card';
        card.setAttribute('data-aos', 'fade-up');
        card.innerHTML = `
            <h3>${item.title}</h3>
            <p>${item.description}</p>
            <p><strong>Harga: ${item.price}</strong></p>
        `;
        investmentGrid.appendChild(card);
    });
});

// Chatbot Functionality
function toggleChatbot() {
    const chatbot = document.getElementById('chatbot');
    chatbot.style.display = chatbot.style.display === 'block' ? 'none' : 'block';
}

function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const messages = document.getElementById('chatbot-messages');
    const message = input.value.trim();

    if (message) {
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
}

function getBotResponse(message) {
    message = message.toLowerCase();
    if (message.includes('hotel')) {
        return 'Hocindo menawarkan pengalaman menginap dengan daya tarik kemewahan dan romansa! Ingin tahu lebih banyak tentang fasilitas kami?';
    } else if (message.includes('cinta') || message.includes('romantis')) {
        return 'Dengan gravitasi cinta, kami punya paket romantis dan acara spesial untuk Anda. Tertarik untuk pernikahan impian?';
    } else if (message.includes('investasi') || message.includes('aset') || message.includes('dana') || message.includes('investor') || message.includes('manajer') || message.includes('instrumen') || message.includes('saldo')) {
        return 'Peluang investasi di Hocindo menawarkan ROI menarik! Saat ini: Aset Anda Rp 100.000, Saldo Disetor Rp 500.000, Saldo Ditarik Rp 10.000, 5 investor, 2 manajer investasi, 5 instrumen investasi, dana kelolaan Rp 30.000, pertumbuhan dana Rp 800, bagi hasil Rp 100. Klik "Daftar Investasi" untuk detail!';
    } else {
        return 'Saya HocindoBot, siap membantu Anda menjelajahi gravitasi cinta dan kemewahan! Apa yang ingin Anda tahu?';
    }
}

// Modal Functionality
function openModal() {
    document.getElementById('modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Form Submission (Contact)
document.getElementById('contact-form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Pesan Anda telah dikirim! Tim Hocindo akan segera menghubungi Anda.');
    e.target.reset();
});

// Form Submission (Investment)
document.getElementById('investment-form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Pendaftaran investasi berhasil! Tim Hocindo akan menghubungi Anda untuk langkah selanjutnya.');
    e.target.reset();
    closeModal();
});
