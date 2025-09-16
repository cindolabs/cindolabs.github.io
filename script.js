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
        return 'Ghocin menawarkan pengalaman menginap dengan daya tarik kemewahan dan romansa! Ingin tahu lebih banyak tentang fasilitas kami?';
    } else if (message.includes('cinta') || message.includes('romantis')) {
        return 'Dengan gravitasi cinta, kami punya paket romantis dan acara spesial untuk Anda. Tertarik untuk pernikahan impian?';
    } else if (message.includes('investasi')) {
        return 'Peluang investasi di Ghocin menawarkan ROI menarik di properti mewah. Klik "Daftar Investasi" untuk detail!';
    } else {
        return 'Saya GhocinBot, siap membantu Anda menjelajahi gravitasi cinta dan kemewahan! Apa yang ingin Anda tahu?';
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
    alert('Pesan Anda telah dikirim! Tim Ghocin akan segera menghubungi Anda.');
    e.target.reset();
});

// Form Submission (Investment)
document.getElementById('investment-form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Pendaftaran investasi berhasil! Tim Ghocin akan menghubungi Anda untuk langkah selanjutnya.');
    e.target.reset();
    closeModal();
});

// Simulate API Data for Investment Section
document.addEventListener('DOMContentLoaded', () => {
    const investmentData = [
        { title: 'Basic Package', description: 'Investasi awal dengan ROI stabil.', price: 'Rp 500 Juta', '32.258,06 USD' },
        { title: 'Premium Package', description: 'Investasi dengan fasilitas eksklusif.', price: 'Rp 1 Miliar', '65.258,06 USD' },
        { title: 'Elite Package', description: 'Investasi premium dengan keuntungan maksimal.', price: 'Rp 2 Miliar', '113.258,06 USD' }
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
