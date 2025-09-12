// Initialize AOS (Animate on Scroll)
AOS.init({
    duration: 1000,
    once: true
});

// Navbar Scroll Effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Hamburger Menu Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Smooth Scroll for Nav Links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        document.getElementById(targetId).scrollIntoView({ behavior: 'smooth' });
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Scroll to Section Function
function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}

// Modal Functions
function openModal() {
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

window.onclick = (event) => {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
};

// Contact Form Submission
document.getElementById('contact-form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Pesan Anda telah dikirim! Kami akan segera menghubungi Anda.');
    e.target.reset();
});

// Konfigurasi Telegram Bot
const TELEGRAM_BOT_TOKEN = '8320437529:AAHM9-j1kpXIdeV5JTf0SsdnUR_SYGeg-X0'; // Token bot hocindobot
const TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'; // Ganti dengan Chat ID Anda (misalnya, 123456789)

// Investment Form Submission
document.getElementById('investment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: e.target.querySelector('input[name="name"]').value,
        email: e.target.querySelector('input[name="email"]').value,
        phone: e.target.querySelector('input[name="phone"]').value,
        package: e.target.querySelector('select[name="package"]').value
    };

    // Format pesan untuk Telegram (menggunakan HTML untuk bold dan line break)
    const message = `
        <b>Pendaftaran Investasi Baru dari Hocindo!</b>
        <b>Nama Lengkap:</b> ${formData.name}<br>
        <b>Email:</b> ${formData.email}<br>
        <b>Nomor Telepon:</b> ${formData.phone}<br>
        <b>Paket Investasi:</b> ${formData.package}<br>
        <i>Tanggal: ${new Date().toLocaleString('id-ID')}</i>
    `;

    try {
        const response = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chat_id: TELEGRAM_CHAT_ID,
                text: message,
                parse_mode: 'HTML'
            })
        });

        const result = await response.json();

        if (result.ok) {
            alert('Pendaftaran investasi berhasil! Data telah dikirim ke Telegram tim kami.');
            closeModal();
            e.target.reset();
        } else {
            console.error('Telegram API Error:', result);
            alert(`Terjadi kesalahan: ${result.description}. Silakan coba lagi atau hubungi tim.`);
        }
    } catch (error) {
        console.error('Error mengirim ke Telegram:', error);
        alert('Terjadi kesalahan koneksi. Silakan coba lagi nanti.');
    }
});

// Fetch Investment Data (Mock API Example)
async function fetchInvestmentData() {
    try {
        const response = await fetch('https://api.mocki.io/v2/51597ef3/investments');
        const data = await response.json();
        const investmentGrid = document.getElementById('investment-data');
        
        data.forEach(item => {
            const card = document.createElement('div');
            card.classList.add('investment-card');
            card.innerHTML = `
                <h3>${item.title}</h3>
                <p>${item.description}</p>
                <p><strong>ROI: ${item.roi}%</strong></p>
            `;
            investmentGrid.appendChild(card);
        });
    } catch (error) {
        console.error('Error fetching investment data:', error);
        document.getElementById('investment-data').innerHTML = '<p>Maaf, data investasi tidak dapat dimuat.</p>';
    }
}

// Chatbot Functionality
function toggleChatbot() {
    const chatbot = document.getElementById('chatbot');
    chatbot.classList.toggle('active');
}

function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const messages = document.getElementById('chatbot-messages');
    const userMessage = input.value.trim();

    if (userMessage === '') return;

    const userDiv = document.createElement('div');
    userDiv.classList.add('user-message');
    userDiv.textContent = userMessage;
    messages.appendChild(userDiv);

    const botDiv = document.createElement('div');
    botDiv.classList.add('bot-message');
    botDiv.textContent = getBotResponse(userMessage.toLowerCase());
    messages.appendChild(botDiv);

    input.value = '';
    messages.scrollTop = messages.scrollHeight;
}

function getBotResponse(message) {
    if (message.includes('hotel')) {
        return 'Kami menawarkan resor bintang lima dengan fasilitas premium. Ingin tahu lebih lanjut tentang paket menginap?';
    } else if (message.includes('cinta') || message.includes('romantis')) {
        return 'Kami memiliki paket romantis seperti makan malam di tepi pantai dan pernikahan impian. Apa yang Anda cari?';
    } else if (message.includes('investasi')) {
        return 'Peluang investasi kami mencakup properti hotel dengan ROI hingga 15%. Ingin mendaftar untuk acara investasi?';
    } else if (message.includes('halo') || message.includes('hai')) {
        return 'Hai! Apa yang bisa HocindoBot bantu hari ini?';
    } else {
        return 'Maaf, saya belum paham. Coba tanyakan tentang hotel, acara romantis, atau investasi!';
    }
}

// Load Investment Data on Page Load
document.addEventListener('DOMContentLoaded', fetchInvestmentData);

// Enter key untuk mengirim pesan di chatbot
document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
