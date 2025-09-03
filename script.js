// Tangani pengiriman formulir reservasi
document.getElementById('reservation-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const checkin = document.getElementById('checkin').value;
    const checkout = document.getElementById('checkout').value;
    const room = document.getElementById('room').value;

    alert(`Terima kasih, ${name}! Reservasi Anda untuk ${room} dari ${checkin} hingga ${checkout} telah diterima. Kami akan menghubungi Anda segera. 💖`);
    this.reset();
});

// Inisialisasi peta
document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map-container').setView([-6.200000, 106.816666], 15); // Koordinat Jakarta
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
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
    setInterval(nextSlide, 5000); // Ganti slide setiap 5 detik
});

// Pop-up Promosi
document.addEventListener('DOMContentLoaded', function () {
    const popup = document.getElementById('promo-popup');
    const closePopup = document.getElementById('close-popup');

    // Tampilkan pop-up saat halaman dimuat
    popup.style.display = 'flex';

    // Tutup pop-up saat tombol close diklik
    closePopup.addEventListener('click', function () {
        popup.style.display = 'none';
    });

    // Tutup pop-up saat area di luar konten diklik
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

    // Tampilkan chatbot saat halaman dimuat
    chatbot.style.display = 'flex';

    // Respon otomatis sederhana
    const responses = {
        'halo': 'Halo! Selamat datang di Hotel Cinta. Bagaimana saya bisa membantu Anda? 💖',
        'kamar': 'Kami memiliki Deluxe Room, Honeymoon Suite, dan Premium Suite. Mau info lebih lanjut?',
        'harga': 'Harga mulai dari Rp1.000.000/malam untuk Deluxe Room. Silakan cek bagian reservasi!',
        'reservasi': 'Silakan isi formulir di bagian reservasi atau tanyakan detail di sini!'
    };

    chatbotInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && chatbotInput.value.trim()) {
            const userMessage = chatbotInput.value.trim().toLowerCase();
            chatbotMessages.innerHTML += `<p><b>Anda:</b> ${userMessage}</p>`;

            const botResponse = responses[userMessage] || 'Maaf, saya tidak mengerti. Coba tanya tentang kamar, harga, atau reservasi!';
            chatbotMessages.innerHTML += `<p><b>CintaBot:</b> ${botResponse}</p>`;
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
    const fadeElements = document.querySelectorAll('.features, .gallery, .testimonials, .reservation, .map, .contact');

    function checkVisibility() {
        fadeElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.8) {
                element.classList.add('fade-in', 'visible');
            }
        });
    }

    window.addEventListener('scroll', checkVisibility);
    checkVisibility(); // Cek saat halaman dimuat
});
