// === FORM RESERVASI UPGRADE ===
document.getElementById('reservation-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const checkin = new Date(document.getElementById('checkin').value);
    const checkout = new Date(document.getElementById('checkout').value);
    const room = document.getElementById('room').value;

    // Validasi nama minimal 3 huruf
    if (name.length < 3) {
        Swal.fire('Oops 😅', 'Nama minimal 3 huruf!', 'error');
        return;
    }

    // Validasi tanggal
    if (checkout <= checkin) {
        Swal.fire('Tanggal Salah 📅', 'Tanggal checkout harus lebih besar dari checkin!', 'warning');
        return;
    }

    // Simpan data ke localStorage (riwayat reservasi)
    const reservation = { name, checkin, checkout, room };
    let history = JSON.parse(localStorage.getItem('reservations')) || [];
    history.push(reservation);
    localStorage.setItem('reservations', JSON.stringify(history));

    // SweetAlert2 popup
    Swal.fire({
        icon: 'success',
        title: `Terima kasih, ${name}! 💖`,
        html: `Reservasi Anda untuk <b>${room}</b><br>dari <b>${checkin.toDateString()}</b> hingga <b>${checkout.toDateString()}</b> telah diterima.<br>Kami akan segera menghubungi Anda.`,
        confirmButtonText: 'OK',
        confirmButtonColor: '#d63384'
    });

    this.reset();
});

// === PETA INTERAKTIF ===
document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map-container', { zoomControl: false }).setView([-6.200000, 106.816666], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const marker = L.marker([-6.200000, 106.816666], { bounceOnAdd: true }).addTo(map);
    marker.bindPopup('<b>Hotel Cinta 🏩</b><br>Jl. Cinta Abadi No. 123, Jakarta<br><a href="mailto:support@hotelcinta.com">Hubungi Kami</a>');

    // Tombol zoom custom
    L.control.zoom({ position: 'bottomright' }).addTo(map);
});

// === SLIDER TESTIMONI ===
document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.testimonial-item');
    const dotsContainer = document.getElementById('testimonial-dots');
    let currentSlide = 0;

    // Buat indikator bulat
    slides.forEach((_, i) => {
        const dot = document.createElement('span');
        dot.classList.add('dot');
        if (i === 0) dot.classList.add('active');
        dot.addEventListener('click', () => showSlide(i));
        dotsContainer.appendChild(dot);
    });
    const dots = dotsContainer.querySelectorAll('.dot');

    function showSlide(index) {
        slides.forEach((s, i) => s.classList.toggle('active', i === index));
        dots.forEach((d, i) => d.classList.toggle('active', i === index));
        currentSlide = index;
    }

    function nextSlide() {
        showSlide((currentSlide + 1) % slides.length);
    }

    // Auto play
    setInterval(nextSlide, 5000);

    // Init
    showSlide(currentSlide);
});

// === POPUP PROMOSI ===
document.addEventListener('DOMContentLoaded', function () {
    const popup = document.getElementById('promo-popup');
    const closePopup = document.getElementById('close-popup');

    // Hanya tampil sekali per sesi
    if (!sessionStorage.getItem('promoShown')) {
        popup.classList.add('show');
        sessionStorage.setItem('promoShown', 'true');
    }

    closePopup.addEventListener('click', () => popup.classList.remove('show'));
    popup.addEventListener('click', e => { if (e.target === popup) popup.classList.remove('show'); });
});

// === CHATBOT UPGRADE ===
document.addEventListener('DOMContentLoaded', function () {
    const chatbot = document.getElementById('chatbot');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const toggleChatbot = document.getElementById('toggle-chatbot');

    // Respon pintar (contains keyword)
    const responses = [
        { keywords: ['halo', 'hi'], reply: 'Halo! Selamat datang di Hotel Cinta. Bagaimana saya bisa membantu Anda? 💖' },
        { keywords: ['kamar'], reply: 'Kami memiliki Deluxe Room, Honeymoon Suite, dan Premium Suite.' },
        { keywords: ['harga', 'biaya'], reply: 'Harga mulai Rp1.000.000/malam untuk Deluxe Room.' },
        { keywords: ['reservasi', 'booking'], reply: 'Silakan isi formulir reservasi atau tanya detail di sini!' }
    ];

    function getResponse(msg) {
        for (let r of responses) {
            if (r.keywords.some(k => msg.includes(k))) return r.reply;
        }
        return 'Maaf, saya tidak mengerti. Coba tanya tentang kamar, harga, atau reservasi!';
    }

    function addMessage(sender, text) {
        chatbotMessages.innerHTML += `<p><b>${sender}:</b> ${text}</p>`;
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Load history dari localStorage
    const history = JSON.parse(localStorage.getItem('chatHistory')) || [];
    history.forEach(m => addMessage(m.sender, m.text));

    chatbotInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && chatbotInput.value.trim()) {
            const msg = chatbotInput.value.trim();
            addMessage('Anda', msg);

            const botReply = getResponse(msg.toLowerCase());
            addMessage('CintaBot', botReply);

            // Simpan history
            history.push({ sender: 'Anda', text: msg }, { sender: 'CintaBot', text: botReply });
            localStorage.setItem('chatHistory', JSON.stringify(history));

            chatbotInput.value = '';
        }
    });

    toggleChatbot.addEventListener('click', () => chatbot.classList.toggle('minimized'));
});

// === ANIMASI SCROLL (IntersectionObserver) ===
document.addEventListener('DOMContentLoaded', function () {
    const fadeElements = document.querySelectorAll('.features, .gallery, .testimonials, .reservation, .map, .contact');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('fade-in', 'visible');
        });
    }, { threshold: 0.2 });

    fadeElements.forEach(el => observer.observe(el));
});
