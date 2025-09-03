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
