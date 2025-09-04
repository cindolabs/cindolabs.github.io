// Tangani pengiriman formulir reservasi
document.getElementById('reservation-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const checkin = document.getElementById('checkin').value;
    const checkout = document.getElementById('checkout').value;
    const room = document.getElementById('room').value;

    // Validasi sederhana
    if (!name || !checkin || !checkout) {
        alert('Harap isi semua kolom yang diperlukan.');
        return;
    }

    // Validasi tanggal
    const today = new Date().toISOString().split('T')[0];
    if (checkin < today) {
        alert('Tanggal check-in tidak boleh sebelum hari ini.');
        return;
    }
    if (checkout <= checkin) {
        alert('Tanggal check-out harus setelah tanggal check-in.');
        return;
    }

    alert(`Terima kasih, ${name}! Reservasi Anda untuk ${room} dari ${checkin} hingga ${checkout} telah diterima. Kami akan menghubungi Anda segera. 💖`);
    this.reset();
});

// Inisialisasi peta
document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map-container').setView([-6.200000, 106.816666], 15); // Koordinat Jakarta
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 18
    }).addTo(map);

    L.marker([-6.200000, 106.816666])
        .addTo(map)
        .bindPopup('<b>Hotel Cinta 🏩</b><br>Jl. Cinta Abadi No. 123, Jakarta<br><a href="mailto:support@hotelcinta.com">Hubungi Kami</a>')
        .openPopup();
});

// Slider Testimoni
document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.testimonial-item');
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    showSlide(currentSlide);
    setInterval(nextSlide, 5000);
});

// Pop-up Promosi
document.addEventListener('DOMContentLoaded', function () {
    const popup = document.getElementById('promo-popup');
    const closePopup = document.getElementById('close-popup');

    // Tampilkan pop-up setelah 2 detik
    setTimeout(() => {
        popup.style.display = 'flex';
    }, 2000);

    closePopup.addEventListener('click', function () {
        popup.style.display = 'none';
    });

    popup.addEventListener('click', function (e) {
        if (e.target === popup) {
            popup.style.display = 'none';
        }
    });
});

// Chatbot Sederhana
document.addEventListener('DOMContentLoaded', function () {
    const chatbot = document.getElementById('chatbot');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const closeChatbot = document.getElementById('close-chatbot');

    chatbot.style.display = 'flex';

    const responses = {
        'halo': 'Halo! Selamat datang di Hotel Cinta. Bagaimana saya bisa membantu Anda? 💖',
        'kamar': 'Kami memiliki Deluxe Room, Honeymoon Suite, dan Premium Suite. Mau info lebih lanjut?',
        'harga': 'Harga mulai dari Rp1.000.000/malam untuk Deluxe Room. Silakan cek bagian reservasi!',
        'reservasi': 'Silakan isi formulir di bagian reservasi atau tanyakan detail di sini!'
    };

    chatbotInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && chatbotInput.value.trim()) {
            const userMessage = chatbotInput.value.trim().toLowerCase();
            const userMessageElement = document.createElement('p');
            userMessageElement.innerHTML = `<b>Anda:</b> ${userMessage}`;
            chatbotMessages.appendChild(userMessageElement);

            const botResponse = responses[userMessage] || 'Maaf, saya tidak mengerti. Coba tanya tentang kamar, harga, atau reservasi!';
            const botMessageElement = document.createElement('p');
            botMessageElement.innerHTML = `<b>CintaBot:</b> ${botResponse}`;
            chatbotMessages.appendChild(botMessageElement);

            chatbotInput.value = '';
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }
    });

    closeChatbot.addEventListener('click', function () {
        chatbot.style.display = 'none';
    });
});

// Animasi Scroll
document.addEventListener('DOMContentLoaded', function () {
    const fadeElements = document.querySelectorAll('.fade-in');

    function checkVisibility() {
        fadeElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.8 && rect.bottom > 0) {
                element.classList.add('visible');
            }
        });
    }

    window.addEventListener('scroll', checkVisibility);
    checkVisibility();
});
