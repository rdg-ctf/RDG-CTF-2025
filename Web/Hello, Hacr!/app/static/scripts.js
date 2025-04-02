document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.createElement('canvas');
    document.body.prepend(canvas);
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const ctx = canvas.getContext('2d');
    const columns = Math.floor(canvas.width / 20);
    const drops = Array(columns).fill(0);

    function drawMatrixRain() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff00';
        ctx.font = '10px Tourney';

        for (let i = 0; i < drops.length; i++) {
            const text = String.fromCharCode(Math.random() * 128);
            const x = i * 20;
            const y = drops[i] * 20;

            ctx.fillText(text, x, y);

            if (y > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(drawMatrixRain, 50);

    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        const cursor = document.createElement('div');
        cursor.classList.add('cursor');
        input.parentElement.appendChild(cursor);

        input.addEventListener('focus', () => {
            cursor.style.display = 'block';
        });

        input.addEventListener('blur', () => {
            cursor.style.display = 'none';
        });
    });
});