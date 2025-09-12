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

// Investment Form Submission
document.getElementById('investment-form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Pendaftaran investasi berhasil! Tim kami akan menghubungi Anda.');
    closeModal();
    e.target.reset();
});

// Fetch Investment Data (Mock API Example)
async function fetchInvestmentData() {
    try {
        // Ganti dengan API nyata jika tersedia
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

// Load Investment Data on Page Load
document.addEventListener('DOMContentLoaded', fetchInvestmentData);
