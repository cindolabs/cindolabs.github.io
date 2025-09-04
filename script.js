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
  const map = L.map('map-container').setView([-6.200000, 106.816666], 15); // Jakarta
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
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
  setInterval(nextSlide, 5000); // setiap 5 detik
});

// Pop-up Promosi
document.addEventListener('DOMContentLoaded', function () {
  const popup = document.getElementById('promo-popup');
  const closePopup = document.getElementById('close-popup');

  popup.style.display = 'flex'; // tampilkan saat load

  closePopup.addEventListener('click', function () {
    popup.style.display = 'none';
  });

  popup.addEventListener('click', function (e) {
    if (e.target === popup) {
      popup.style.display = 'none';
    }
  });
});

// Animasi Scroll (fade-in)
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
  checkVisibility();
});
