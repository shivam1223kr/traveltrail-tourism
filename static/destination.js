document.querySelector('#detail-booking-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const response = await fetch('/api/bookings', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(Object.fromEntries(new FormData(event.target)))});
  const data = await response.json();
  document.querySelector('#detail-booking-message').textContent = data.error || `${data.message} Reference: ${data.booking_id}`;
  if (response.ok) event.target.reset();
});
